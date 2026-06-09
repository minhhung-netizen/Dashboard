from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterator


SCHEMA = """
CREATE TABLE IF NOT EXISTS signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    exchange TEXT,
    action TEXT NOT NULL,
    price REAL,
    timeframe TEXT,
    strategy TEXT,
    note TEXT,
    source_time TEXT,
    received_at TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    enrichment_json TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_signals_ticker_received_at
ON signals (ticker, received_at DESC);

CREATE INDEX IF NOT EXISTS idx_signals_action_received_at
ON signals (action, received_at DESC);

CREATE INDEX IF NOT EXISTS idx_signals_duplicate_lookup
ON signals (ticker, action, timeframe, strategy, source_time, received_at DESC);

CREATE TABLE IF NOT EXISTS invalid_signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT,
    action TEXT,
    timeframe TEXT,
    strategy TEXT,
    reason TEXT NOT NULL,
    source_time TEXT,
    received_at TEXT NOT NULL,
    payload_json TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_invalid_signals_received_at
ON invalid_signals (received_at DESC);

CREATE TABLE IF NOT EXISTS derivative_signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    exchange TEXT,
    action TEXT NOT NULL,
    price REAL NOT NULL,
    quantity REAL NOT NULL,
    contract_multiplier REAL NOT NULL,
    timeframe TEXT,
    strategy TEXT,
    reason TEXT,
    source_time TEXT,
    received_at TEXT NOT NULL,
    payload_json TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_derivative_signals_symbol_received_at
ON derivative_signals (symbol, received_at DESC);

CREATE INDEX IF NOT EXISTS idx_derivative_signals_duplicate_lookup
ON derivative_signals (
    symbol, action, timeframe, strategy, source_time, received_at DESC
);

CREATE TABLE IF NOT EXISTS app_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS manual_positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    weight_pct REAL NOT NULL,
    entry_price REAL NOT NULL,
    current_price REAL NOT NULL,
    quantity REAL,
    entry_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'open',
    exit_price REAL,
    closed_at TEXT,
    note TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_manual_positions_status_ticker
ON manual_positions (status, ticker);

CREATE TABLE IF NOT EXISTS manual_price_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    position_id INTEGER NOT NULL,
    price REAL NOT NULL,
    recorded_at TEXT NOT NULL,
    FOREIGN KEY (position_id) REFERENCES manual_positions(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_manual_price_snapshots_position_time
ON manual_price_snapshots (position_id, recorded_at);

CREATE TABLE IF NOT EXISTS manual_daily_performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trade_date TEXT NOT NULL UNIQUE,
    portfolio_return_pct REAL,
    equity_value REAL NOT NULL,
    total_weight_pct REAL NOT NULL,
    open_count INTEGER NOT NULL,
    closed_count INTEGER NOT NULL,
    cost_value REAL,
    market_value REAL,
    pnl_value REAL,
    recorded_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_manual_daily_performance_date
ON manual_daily_performance (trade_date ASC);

CREATE TABLE IF NOT EXISTS dividend_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    ex_date TEXT NOT NULL,
    cash_amount REAL,
    stock_ratio_pct REAL,
    issue_ratio_pct REAL,
    issue_price REAL,
    note TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_dividend_events_ticker_date
ON dividend_events (ticker, ex_date ASC);
"""


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class SignalStore:
    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def init_db(self) -> None:
        with self.connect() as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            conn.executescript(SCHEMA)
            self._ensure_dividend_event_columns(conn)
            conn.execute("UPDATE signals SET price = price / 1000 WHERE price >= 1000")
            self._normalize_signal_actions(conn)

    def _ensure_dividend_event_columns(self, conn: sqlite3.Connection) -> None:
        columns = {
            row["name"]
            for row in conn.execute("PRAGMA table_info(dividend_events)").fetchall()
        }
        if "issue_ratio_pct" not in columns:
            conn.execute("ALTER TABLE dividend_events ADD COLUMN issue_ratio_pct REAL")
        if "issue_price" not in columns:
            conn.execute("ALTER TABLE dividend_events ADD COLUMN issue_price REAL")

    def _normalize_signal_actions(self, conn: sqlite3.Connection) -> None:
        action_expr = """
            lower(
                replace(
                    replace(
                        replace(
                            replace(
                                replace(action, ' ', ''),
                                char(9),
                                ''
                            ),
                            char(10),
                            ''
                        ),
                        '-',
                        ''
                    ),
                    '_',
                    ''
                )
            )
        """
        conn.execute(
            f"""
            UPDATE signals
            SET action = 'confirm_buy'
            WHERE {action_expr} IN (
                'confirmbuy',
                'confirmationbuy',
                'confimbuy',
                'confibuy'
            )
            """
        )
        conn.execute(
            f"""
            UPDATE signals
            SET action = 'confirm_sell'
            WHERE {action_expr} IN (
                'confirmsell',
                'confirmationsell',
                'confimsell',
                'confisell'
            )
            """
        )

    def insert_signal(
        self,
        *,
        ticker: str,
        exchange: str | None,
        action: str,
        price: float | None,
        timeframe: str | None,
        strategy: str | None,
        note: str | None,
        source_time: str | None,
        payload: dict[str, Any],
        enrichment: dict[str, Any],
    ) -> dict[str, Any]:
        received_at = utc_now_iso()
        with self.connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO signals (
                    ticker, exchange, action, price, timeframe, strategy, note,
                    source_time, received_at, payload_json, enrichment_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    ticker,
                    exchange,
                    action,
                    price,
                    timeframe,
                    strategy,
                    note,
                    source_time,
                    received_at,
                    json.dumps(payload, ensure_ascii=True),
                    json.dumps(enrichment, ensure_ascii=True),
                ),
            )
            signal_id = cursor.lastrowid
        return self.get_signal(signal_id)

    def get_signal(self, signal_id: int) -> dict[str, Any]:
        with self.connect() as conn:
            row = conn.execute("SELECT * FROM signals WHERE id = ?", (signal_id,)).fetchone()
        if row is None:
            raise KeyError(f"Signal {signal_id} was not found")
        return row_to_signal(row)

    def update_signal_enrichment(self, signal_id: int, enrichment: dict[str, Any]) -> None:
        with self.connect() as conn:
            conn.execute(
                "UPDATE signals SET enrichment_json = ? WHERE id = ?",
                (json.dumps(enrichment, ensure_ascii=True), signal_id),
            )

    def delete_signal(self, signal_id: int) -> bool:
        with self.connect() as conn:
            cursor = conn.execute("DELETE FROM signals WHERE id = ?", (signal_id,))
            return cursor.rowcount > 0

    def insert_derivative_signal(
        self,
        *,
        symbol: str,
        exchange: str | None,
        action: str,
        price: float,
        quantity: float,
        contract_multiplier: float,
        timeframe: str | None,
        strategy: str | None,
        reason: str | None,
        source_time: str | None,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        received_at = utc_now_iso()
        with self.connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO derivative_signals (
                    symbol, exchange, action, price, quantity,
                    contract_multiplier, timeframe, strategy, reason,
                    source_time, received_at, payload_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    symbol.upper(),
                    exchange,
                    action,
                    price,
                    quantity,
                    contract_multiplier,
                    timeframe,
                    strategy,
                    reason,
                    source_time,
                    received_at,
                    json.dumps(payload, ensure_ascii=True),
                ),
            )
            signal_id = cursor.lastrowid
        return self.get_derivative_signal(signal_id)

    def get_derivative_signal(self, signal_id: int) -> dict[str, Any]:
        with self.connect() as conn:
            row = conn.execute(
                "SELECT * FROM derivative_signals WHERE id = ?",
                (signal_id,),
            ).fetchone()
        if row is None:
            raise KeyError(f"Derivative signal {signal_id} was not found")
        return row_to_derivative_signal(row)

    def list_all_derivative_signals(self) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT *
                FROM derivative_signals
                ORDER BY received_at ASC, id ASC
                """
            ).fetchall()
        return [row_to_derivative_signal(row) for row in rows]

    def delete_derivative_signal(self, signal_id: int) -> bool:
        with self.connect() as conn:
            cursor = conn.execute(
                "DELETE FROM derivative_signals WHERE id = ?",
                (signal_id,),
            )
            return cursor.rowcount > 0

    def find_duplicate_derivative_signal(
        self,
        *,
        symbol: str,
        action: str,
        timeframe: str | None,
        strategy: str | None,
        source_time: str | None,
        window_minutes: int,
    ) -> dict[str, Any] | None:
        params: list[Any] = [symbol.upper(), action, timeframe or "", strategy or ""]
        if source_time:
            source_clause = "AND source_time = ?"
            params.append(source_time)
        else:
            cutoff = datetime.now(timezone.utc) - timedelta(minutes=window_minutes)
            source_clause = "AND source_time IS NULL AND received_at >= ?"
            params.append(cutoff.isoformat())
        with self.connect() as conn:
            row = conn.execute(
                f"""
                SELECT *
                FROM derivative_signals
                WHERE symbol = ?
                  AND action = ?
                  AND COALESCE(timeframe, '') = ?
                  AND COALESCE(strategy, '') = ?
                  {source_clause}
                ORDER BY received_at DESC
                LIMIT 1
                """,
                params,
            ).fetchone()
        return row_to_derivative_signal(row) if row else None

    def get_app_setting(self, key: str, default: str | None = None) -> str | None:
        with self.connect() as conn:
            row = conn.execute(
                "SELECT value FROM app_settings WHERE key = ?",
                (key,),
            ).fetchone()
        return row["value"] if row else default

    def set_app_setting(self, key: str, value: str) -> str:
        now = utc_now_iso()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO app_settings (key, value, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(key) DO UPDATE SET
                    value = excluded.value,
                    updated_at = excluded.updated_at
                """,
                (key, value, now),
            )
        return value

    def insert_manual_position(
        self,
        *,
        ticker: str,
        weight_pct: float,
        entry_price: float,
        current_price: float | None,
        quantity: float | None,
        entry_date: str | None,
        note: str | None,
    ) -> dict[str, Any]:
        now = utc_now_iso()
        mark_price = current_price if current_price is not None else entry_price
        with self.connect() as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.execute(
                """
                INSERT INTO manual_positions (
                    ticker, weight_pct, entry_price, current_price, quantity,
                    entry_date, status, note, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, 'open', ?, ?, ?)
                """,
                (
                    ticker.upper(),
                    weight_pct,
                    entry_price,
                    mark_price,
                    quantity,
                    entry_date or now,
                    note,
                    now,
                    now,
                ),
            )
            position_id = cursor.lastrowid
            self._insert_manual_snapshot(conn, position_id, entry_price, entry_date or now)
            if mark_price != entry_price:
                self._insert_manual_snapshot(conn, position_id, mark_price, now)
        return self.get_manual_position(position_id)

    def get_manual_position(self, position_id: int) -> dict[str, Any]:
        with self.connect() as conn:
            row = conn.execute(
                "SELECT * FROM manual_positions WHERE id = ?", (position_id,)
            ).fetchone()
            snapshots = conn.execute(
                """
                SELECT price, recorded_at
                FROM manual_price_snapshots
                WHERE position_id = ?
                ORDER BY recorded_at ASC, id ASC
                """,
                (position_id,),
            ).fetchall()
        if row is None:
            raise KeyError(f"Manual position {position_id} was not found")
        return row_to_manual_position(row, snapshots)

    def list_manual_positions(self) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT * FROM manual_positions
                ORDER BY CASE status WHEN 'open' THEN 0 ELSE 1 END, ticker ASC, entry_date ASC, id ASC
                """
            ).fetchall()
            snapshots_by_position: dict[int, list[sqlite3.Row]] = {}
            if rows:
                position_ids = [row["id"] for row in rows]
                placeholders = ",".join("?" for _ in position_ids)
                snapshot_rows = conn.execute(
                    f"""
                    SELECT position_id, price, recorded_at
                    FROM manual_price_snapshots
                    WHERE position_id IN ({placeholders})
                    ORDER BY recorded_at ASC, id ASC
                    """,
                    position_ids,
                ).fetchall()
                for snapshot in snapshot_rows:
                    snapshots_by_position.setdefault(snapshot["position_id"], []).append(snapshot)
        return [
            row_to_manual_position(row, snapshots_by_position.get(row["id"], []))
            for row in rows
        ]

    def list_open_manual_tickers(self) -> list[str]:
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT DISTINCT ticker
                FROM manual_positions
                WHERE status = 'open'
                ORDER BY ticker ASC
                """
            ).fetchall()
        return [row["ticker"] for row in rows]

    def update_manual_market_price(
        self, *, ticker: str, price: float, recorded_at: str
    ) -> int:
        ticker = ticker.upper()
        with self.connect() as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            rows = conn.execute(
                """
                SELECT id
                FROM manual_positions
                WHERE ticker = ? AND status = 'open'
                """,
                (ticker,),
            ).fetchall()
            if not rows:
                return 0
            conn.execute(
                """
                UPDATE manual_positions
                SET current_price = ?, updated_at = ?
                WHERE ticker = ? AND status = 'open'
                """,
                (price, recorded_at, ticker),
            )
            for row in rows:
                self._insert_manual_snapshot(conn, row["id"], price, recorded_at)
        return len(rows)

    def update_manual_position(
        self, position_id: int, updates: dict[str, Any]
    ) -> dict[str, Any]:
        allowed = {
            "ticker",
            "weight_pct",
            "entry_price",
            "current_price",
            "quantity",
            "entry_date",
            "note",
        }
        fields = {key: value for key, value in updates.items() if key in allowed}
        if not fields:
            return self.get_manual_position(position_id)

        if "ticker" in fields and fields["ticker"] is not None:
            fields["ticker"] = str(fields["ticker"]).upper()
        now = utc_now_iso()
        fields["updated_at"] = now
        assignments = ", ".join(f"{key} = ?" for key in fields)
        params = [*fields.values(), position_id]

        with self.connect() as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.execute(
                f"UPDATE manual_positions SET {assignments} WHERE id = ?",
                params,
            )
            if cursor.rowcount == 0:
                raise KeyError(f"Manual position {position_id} was not found")
            if "entry_price" in updates and updates["entry_price"] is not None:
                position = conn.execute(
                    "SELECT entry_date FROM manual_positions WHERE id = ?",
                    (position_id,),
                ).fetchone()
                self._insert_manual_snapshot(
                    conn, position_id, float(updates["entry_price"]), position["entry_date"]
                )
            if "current_price" in updates and updates["current_price"] is not None:
                self._insert_manual_snapshot(
                    conn, position_id, float(updates["current_price"]), now
                )
        return self.get_manual_position(position_id)

    def close_manual_position(
        self, position_id: int, *, exit_price: float, closed_at: str | None
    ) -> dict[str, Any]:
        now = utc_now_iso()
        close_time = closed_at or now
        with self.connect() as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.execute(
                """
                UPDATE manual_positions
                SET status = 'closed',
                    exit_price = ?,
                    current_price = ?,
                    closed_at = ?,
                    updated_at = ?
                WHERE id = ?
                """,
                (exit_price, exit_price, close_time, now, position_id),
            )
            if cursor.rowcount == 0:
                raise KeyError(f"Manual position {position_id} was not found")
            self._insert_manual_snapshot(conn, position_id, exit_price, close_time)
        return self.get_manual_position(position_id)

    def delete_manual_position(self, position_id: int) -> bool:
        with self.connect() as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.execute("DELETE FROM manual_positions WHERE id = ?", (position_id,))
            return cursor.rowcount > 0

    def upsert_manual_daily_performance(
        self,
        *,
        trade_date: str,
        portfolio_return_pct: float | None,
        equity_value: float,
        total_weight_pct: float,
        open_count: int,
        closed_count: int,
        cost_value: float | None,
        market_value: float | None,
        pnl_value: float | None,
        recorded_at: str,
    ) -> dict[str, Any]:
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO manual_daily_performance (
                    trade_date, portfolio_return_pct, equity_value,
                    total_weight_pct, open_count, closed_count,
                    cost_value, market_value, pnl_value, recorded_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(trade_date) DO UPDATE SET
                    portfolio_return_pct = excluded.portfolio_return_pct,
                    equity_value = excluded.equity_value,
                    total_weight_pct = excluded.total_weight_pct,
                    open_count = excluded.open_count,
                    closed_count = excluded.closed_count,
                    cost_value = excluded.cost_value,
                    market_value = excluded.market_value,
                    pnl_value = excluded.pnl_value,
                    recorded_at = excluded.recorded_at
                """,
                (
                    trade_date,
                    portfolio_return_pct,
                    equity_value,
                    total_weight_pct,
                    open_count,
                    closed_count,
                    cost_value,
                    market_value,
                    pnl_value,
                    recorded_at,
                ),
            )
        return self.get_manual_daily_performance(trade_date)

    def get_manual_daily_performance(self, trade_date: str) -> dict[str, Any]:
        with self.connect() as conn:
            row = conn.execute(
                "SELECT * FROM manual_daily_performance WHERE trade_date = ?",
                (trade_date,),
            ).fetchone()
        if row is None:
            raise KeyError(f"Manual daily performance {trade_date} was not found")
        return dict(row)

    def list_manual_daily_performance(self) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT *
                FROM manual_daily_performance
                ORDER BY trade_date ASC
                """
            ).fetchall()
        return [dict(row) for row in rows]

    def delete_manual_daily_performance(self, trade_date: str) -> bool:
        with self.connect() as conn:
            cursor = conn.execute(
                "DELETE FROM manual_daily_performance WHERE trade_date = ?",
                (trade_date,),
            )
            return cursor.rowcount > 0

    def insert_dividend_event(
        self,
        *,
        ticker: str,
        ex_date: str,
        cash_amount: float | None,
        stock_ratio_pct: float | None,
        issue_ratio_pct: float | None = None,
        issue_price: float | None = None,
        note: str | None = None,
    ) -> dict[str, Any]:
        now = utc_now_iso()
        with self.connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO dividend_events (
                    ticker, ex_date, cash_amount, stock_ratio_pct,
                    issue_ratio_pct, issue_price, note,
                    created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    ticker.upper(),
                    ex_date,
                    cash_amount,
                    stock_ratio_pct,
                    issue_ratio_pct,
                    issue_price,
                    note,
                    now,
                    now,
                ),
            )
            event_id = cursor.lastrowid
        return self.get_dividend_event(event_id)

    def get_dividend_event(self, event_id: int) -> dict[str, Any]:
        with self.connect() as conn:
            row = conn.execute(
                "SELECT * FROM dividend_events WHERE id = ?",
                (event_id,),
            ).fetchone()
        if row is None:
            raise KeyError(f"Dividend event {event_id} was not found")
        return dict(row)

    def list_dividend_events(self, ticker: str | None = None) -> list[dict[str, Any]]:
        params: list[Any] = []
        where = ""
        if ticker:
            where = "WHERE ticker = ?"
            params.append(ticker.upper())
        with self.connect() as conn:
            rows = conn.execute(
                f"""
                SELECT *
                FROM dividend_events
                {where}
                ORDER BY ex_date ASC, ticker ASC, id ASC
                """,
                params,
            ).fetchall()
        return [dict(row) for row in rows]

    def delete_dividend_event(self, event_id: int) -> bool:
        with self.connect() as conn:
            cursor = conn.execute("DELETE FROM dividend_events WHERE id = ?", (event_id,))
            return cursor.rowcount > 0

    def _insert_manual_snapshot(
        self,
        conn: sqlite3.Connection,
        position_id: int,
        price: float,
        recorded_at: str,
    ) -> None:
        conn.execute(
            """
            INSERT INTO manual_price_snapshots (position_id, price, recorded_at)
            VALUES (?, ?, ?)
            """,
            (position_id, price, recorded_at),
        )

    def find_duplicate_signal(
        self,
        *,
        ticker: str,
        action: str,
        timeframe: str | None,
        strategy: str | None,
        source_time: str | None,
        window_minutes: int,
    ) -> dict[str, Any] | None:
        params: list[Any] = [ticker, action, timeframe or "", strategy or ""]
        source_clause = ""
        if source_time:
            source_clause = "AND source_time = ?"
            params.append(source_time)
        else:
            cutoff = datetime.now(timezone.utc) - timedelta(minutes=window_minutes)
            source_clause = "AND source_time IS NULL AND received_at >= ?"
            params.append(cutoff.isoformat())

        with self.connect() as conn:
            row = conn.execute(
                f"""
                SELECT * FROM signals
                WHERE ticker = ?
                  AND action = ?
                  AND COALESCE(timeframe, '') = ?
                  AND COALESCE(strategy, '') = ?
                  {source_clause}
                ORDER BY received_at DESC
                LIMIT 1
                """,
                params,
            ).fetchone()
        return row_to_signal(row) if row else None

    def record_invalid_signal(
        self,
        *,
        ticker: str | None,
        action: str | None,
        timeframe: str | None,
        strategy: str | None,
        reason: str,
        source_time: str | None,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        received_at = utc_now_iso()
        with self.connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO invalid_signals (
                    ticker, action, timeframe, strategy, reason,
                    source_time, received_at, payload_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    ticker,
                    action,
                    timeframe,
                    strategy,
                    reason,
                    source_time,
                    received_at,
                    json.dumps(payload, ensure_ascii=True),
                ),
            )
            invalid_id = cursor.lastrowid
        return self.get_invalid_signal(invalid_id)

    def get_invalid_signal(self, invalid_id: int) -> dict[str, Any]:
        with self.connect() as conn:
            row = conn.execute(
                "SELECT * FROM invalid_signals WHERE id = ?", (invalid_id,)
            ).fetchone()
        if row is None:
            raise KeyError(f"Invalid signal {invalid_id} was not found")
        return row_to_invalid_signal(row)

    def list_invalid_signals(self, *, limit: int = 100) -> list[dict[str, Any]]:
        limit = max(1, min(limit, 500))
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT * FROM invalid_signals
                ORDER BY received_at DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [row_to_invalid_signal(row) for row in rows]

    def list_signals(
        self, *, ticker: str | None = None, limit: int = 100
    ) -> list[dict[str, Any]]:
        limit = max(1, min(limit, 500))
        params: list[Any] = []
        where = ""
        if ticker:
            where = "WHERE ticker = ?"
            params.append(ticker.upper())
        params.append(limit)
        with self.connect() as conn:
            rows = conn.execute(
                f"""
                SELECT * FROM signals
                {where}
                ORDER BY received_at DESC
                LIMIT ?
                """,
                params,
            ).fetchall()
        return [row_to_signal(row) for row in rows]

    def list_all_signals(self, *, ticker: str | None = None) -> list[dict[str, Any]]:
        params: list[Any] = []
        where = ""
        if ticker:
            where = "WHERE ticker = ?"
            params.append(ticker.upper())
        with self.connect() as conn:
            rows = conn.execute(
                f"""
                SELECT * FROM signals
                {where}
                ORDER BY received_at ASC, id ASC
                """,
                params,
            ).fetchall()
        return [row_to_signal(row) for row in rows]

    def summary(self) -> dict[str, Any]:
        with self.connect() as conn:
            totals = conn.execute(
                """
                SELECT
                    COUNT(*) AS total,
                    SUM(CASE WHEN lower(action) = 'buy' THEN 1 ELSE 0 END) AS buy_count,
                    SUM(CASE WHEN lower(action) = 'sell' THEN 1 ELSE 0 END) AS sell_count,
                    COUNT(DISTINCT ticker) AS tickers
                FROM signals
                """
            ).fetchone()
            latest = conn.execute(
                """
                SELECT received_at
                FROM signals
                ORDER BY received_at DESC
                LIMIT 1
                """
            ).fetchone()
        return {
            "total": totals["total"] or 0,
            "buy_count": totals["buy_count"] or 0,
            "sell_count": totals["sell_count"] or 0,
            "tickers": totals["tickers"] or 0,
            "latest_received_at": latest["received_at"] if latest else None,
        }


def row_to_signal(row: sqlite3.Row) -> dict[str, Any]:
    data = dict(row)
    data["payload"] = json.loads(data.pop("payload_json") or "{}")
    data["enrichment"] = json.loads(data.pop("enrichment_json") or "{}")
    return data


def row_to_invalid_signal(row: sqlite3.Row) -> dict[str, Any]:
    data = dict(row)
    data["payload"] = json.loads(data.pop("payload_json") or "{}")
    return data


def row_to_derivative_signal(row: sqlite3.Row) -> dict[str, Any]:
    data = dict(row)
    data["payload"] = json.loads(data.pop("payload_json") or "{}")
    return data


def row_to_manual_position(
    row: sqlite3.Row, snapshots: list[sqlite3.Row]
) -> dict[str, Any]:
    data = dict(row)
    data["snapshots"] = [
        {"price": snapshot["price"], "recorded_at": snapshot["recorded_at"]}
        for snapshot in snapshots
    ]
    return data
