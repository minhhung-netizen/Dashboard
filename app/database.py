from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE COLLATE NOCASE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'admin' CHECK (role = 'admin'),
    active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sessions (
    token_hash TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    expires_at TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_sessions_expires_at ON sessions (expires_at);

CREATE TABLE IF NOT EXISTS signal_filter_settings (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    allowed_tickers_json TEXT NOT NULL DEFAULT '[]',
    allowed_strategies_json TEXT NOT NULL DEFAULT '[]',
    allow_buy INTEGER NOT NULL DEFAULT 1,
    allow_sell INTEGER NOT NULL DEFAULT 1,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    exchange TEXT,
    action TEXT NOT NULL CHECK (action IN ('buy', 'sell', 'other')),
    timeframe TEXT,
    strategy TEXT,
    note TEXT,
    source_time TEXT,
    received_at TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'excluded')),
    category TEXT NOT NULL DEFAULT 'watch',
    classification_note TEXT,
    rejection_reason TEXT,
    payload_json TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_signals_received_at ON signals (received_at DESC);
CREATE INDEX IF NOT EXISTS idx_signals_status_received_at ON signals (status, received_at DESC);
CREATE INDEX IF NOT EXISTS idx_signals_ticker_received_at ON signals (ticker, received_at DESC);

CREATE TABLE IF NOT EXISTS backtest_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_by_user_id INTEGER,
    symbols_json TEXT NOT NULL,
    strategy TEXT NOT NULL,
    config_json TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    data_source TEXT NOT NULL DEFAULT 'vnstock',
    is_standard INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'queued'
        CHECK (status IN ('queued', 'running', 'completed', 'failed')),
    error_text TEXT,
    metrics_json TEXT,
    created_at TEXT NOT NULL,
    started_at TEXT,
    finished_at TEXT,
    FOREIGN KEY (created_by_user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_backtest_runs_created_at
ON backtest_runs (created_at DESC);

CREATE TABLE IF NOT EXISTS backtest_price_bars (
    ticker TEXT NOT NULL,
    trade_date TEXT NOT NULL,
    open REAL NOT NULL,
    high REAL NOT NULL,
    low REAL NOT NULL,
    close REAL NOT NULL,
    volume REAL NOT NULL,
    provider TEXT NOT NULL,
    retrieved_at TEXT NOT NULL,
    PRIMARY KEY (ticker, trade_date)
);

CREATE INDEX IF NOT EXISTS idx_backtest_price_bars_lookup
ON backtest_price_bars (ticker, trade_date ASC);

CREATE TABLE IF NOT EXISTS backtest_equity_points (
    run_id INTEGER NOT NULL,
    trade_date TEXT NOT NULL,
    equity REAL NOT NULL,
    cash REAL NOT NULL,
    invested_symbols INTEGER NOT NULL,
    PRIMARY KEY (run_id, trade_date),
    FOREIGN KEY (run_id) REFERENCES backtest_runs(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS backtest_trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL,
    trade_date TEXT NOT NULL,
    ticker TEXT NOT NULL,
    side TEXT NOT NULL CHECK (side IN ('BUY', 'SELL')),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    fill_price REAL NOT NULL,
    notional REAL NOT NULL,
    costs REAL NOT NULL,
    FOREIGN KEY (run_id) REFERENCES backtest_runs(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_backtest_trades_run_date
ON backtest_trades (run_id, trade_date ASC);
"""


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class BacktestStore:
    """SQLite persistence for the single-purpose backtest dashboard."""

    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.database_path, timeout=10)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA busy_timeout = 10000")
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def init_db(self) -> None:
        with self.connect() as conn:
            conn.execute("PRAGMA journal_mode = WAL")
            conn.execute("PRAGMA synchronous = NORMAL")
            conn.executescript(SCHEMA)
            self._ensure_backtest_run_columns(conn)
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_backtest_runs_strategy_standard
                ON backtest_runs (strategy, is_standard) WHERE is_standard = 1
                """
            )
            conn.execute("PRAGMA optimize")

    @staticmethod
    def _ensure_backtest_run_columns(conn: sqlite3.Connection) -> None:
        columns = {
            row["name"] for row in conn.execute("PRAGMA table_info(backtest_runs)").fetchall()
        }
        if "is_standard" not in columns:
            conn.execute("ALTER TABLE backtest_runs ADD COLUMN is_standard INTEGER NOT NULL DEFAULT 0")

    def database_status(self) -> dict[str, Any]:
        with self.connect() as conn:
            journal_mode = conn.execute("PRAGMA journal_mode").fetchone()[0]
        return {
            "path": str(self.database_path),
            "journal_mode": journal_mode,
            "size_bytes": self.database_path.stat().st_size
            if self.database_path.exists() else 0,
        }

    def get_user_credentials(self, username: str) -> dict[str, Any] | None:
        with self.connect() as conn:
            row = conn.execute(
                "SELECT * FROM users WHERE username = ?", (username.strip(),)
            ).fetchone()
        return dict(row) if row else None

    def ensure_admin_user(self, *, username: str, password_hash: str) -> None:
        now = utc_now_iso()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO users (username, password_hash, role, active, created_at, updated_at)
                VALUES (?, ?, 'admin', 1, ?, ?)
                ON CONFLICT(username) DO NOTHING
                """,
                (username.strip(), password_hash, now, now),
            )

    def update_admin_password(self, user_id: int, password_hash: str) -> None:
        with self.connect() as conn:
            conn.execute(
                "UPDATE users SET password_hash = ?, updated_at = ? WHERE id = ?",
                (password_hash, utc_now_iso(), user_id),
            )

    def create_session(self, *, token_hash: str, user_id: int, expires_at: str) -> None:
        with self.connect() as conn:
            conn.execute(
                "INSERT INTO sessions (token_hash, user_id, expires_at, created_at) VALUES (?, ?, ?, ?)",
                (token_hash, user_id, expires_at, utc_now_iso()),
            )

    def get_session_user(self, token_hash: str) -> dict[str, Any] | None:
        now = utc_now_iso()
        with self.connect() as conn:
            conn.execute("DELETE FROM sessions WHERE expires_at <= ?", (now,))
            row = conn.execute(
                """
                SELECT users.* FROM sessions
                JOIN users ON users.id = sessions.user_id
                WHERE sessions.token_hash = ? AND sessions.expires_at > ? AND users.active = 1
                """,
                (token_hash, now),
            ).fetchone()
        return dict(row) if row else None

    def delete_session(self, token_hash: str) -> None:
        with self.connect() as conn:
            conn.execute("DELETE FROM sessions WHERE token_hash = ?", (token_hash,))

    def get_signal_filter_settings(self) -> dict[str, Any]:
        now = utc_now_iso()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO signal_filter_settings
                (id, allowed_tickers_json, allowed_strategies_json, allow_buy, allow_sell, updated_at)
                VALUES (1, '[]', '[]', 1, 1, ?)
                """,
                (now,),
            )
            row = conn.execute("SELECT * FROM signal_filter_settings WHERE id = 1").fetchone()
        result = dict(row)
        result["allowed_tickers"] = json.loads(result.pop("allowed_tickers_json"))
        result["allowed_strategies"] = json.loads(result.pop("allowed_strategies_json"))
        result["allow_buy"] = bool(result["allow_buy"])
        result["allow_sell"] = bool(result["allow_sell"])
        return result

    def update_signal_filter_settings(
        self, *, allowed_tickers: list[str], allowed_strategies: list[str],
        allow_buy: bool, allow_sell: bool,
    ) -> dict[str, Any]:
        now = utc_now_iso()
        with self.connect() as conn:
            conn.execute(
                """
                INSERT INTO signal_filter_settings
                (id, allowed_tickers_json, allowed_strategies_json, allow_buy, allow_sell, updated_at)
                VALUES (1, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                allowed_tickers_json = excluded.allowed_tickers_json,
                allowed_strategies_json = excluded.allowed_strategies_json,
                allow_buy = excluded.allow_buy, allow_sell = excluded.allow_sell,
                updated_at = excluded.updated_at
                """,
                (json.dumps(allowed_tickers), json.dumps(allowed_strategies), int(allow_buy), int(allow_sell), now),
            )
        return self.get_signal_filter_settings()

    def create_signal(
        self, *, ticker: str, exchange: str | None, action: str, timeframe: str | None,
        strategy: str | None, note: str | None, source_time: str | None,
        status: str, category: str, classification_note: str | None,
        rejection_reason: str | None, payload: dict[str, Any],
    ) -> dict[str, Any]:
        with self.connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO signals
                (ticker, exchange, action, timeframe, strategy, note, source_time, received_at,
                 status, category, classification_note, rejection_reason, payload_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (ticker, exchange, action, timeframe, strategy, note, source_time, utc_now_iso(), status,
                 category, classification_note, rejection_reason, json.dumps(payload)),
            )
            signal_id = int(cursor.lastrowid)
            row = conn.execute("SELECT * FROM signals WHERE id = ?", (signal_id,)).fetchone()
        return self._decode_signal(row)

    @staticmethod
    def _decode_signal(row: sqlite3.Row) -> dict[str, Any]:
        result = dict(row)
        try:
            result["payload"] = json.loads(result.pop("payload_json"))
        except (TypeError, json.JSONDecodeError):
            result["payload"] = {}
        return result

    def list_signals(
        self, *, status: str | None = None, ticker: str | None = None, limit: int = 100,
    ) -> list[dict[str, Any]]:
        clauses: list[str] = []
        parameters: list[Any] = []
        if status:
            clauses.append("status = ?")
            parameters.append(status)
        if ticker:
            clauses.append("ticker = ?")
            parameters.append(ticker.strip().upper())
        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        parameters.append(max(1, min(limit, 500)))
        with self.connect() as conn:
            rows = conn.execute(
                f"SELECT * FROM signals {where} ORDER BY id DESC LIMIT ?", parameters
            ).fetchall()
        return [self._decode_signal(row) for row in rows]

    def signal_summary(self) -> dict[str, int]:
        with self.connect() as conn:
            rows = conn.execute(
                "SELECT status, COUNT(*) AS total FROM signals GROUP BY status"
            ).fetchall()
        totals = {row["status"]: int(row["total"]) for row in rows}
        return {
            "total": sum(totals.values()), "pending": totals.get("pending", 0),
            "accepted": totals.get("accepted", 0), "excluded": totals.get("excluded", 0),
        }

    def classify_signal(
        self, signal_id: int, *, status: str, category: str, classification_note: str | None,
    ) -> dict[str, Any]:
        with self.connect() as conn:
            cursor = conn.execute(
                """
                UPDATE signals SET status = ?, category = ?, classification_note = ?,
                rejection_reason = CASE WHEN ? = 'excluded' THEN COALESCE(?, rejection_reason, 'Excluded from dashboard') ELSE NULL END
                WHERE id = ?
                """,
                (status, category, classification_note, status, classification_note, signal_id),
            )
            if not cursor.rowcount:
                raise KeyError("Signal was not found")
            row = conn.execute("SELECT * FROM signals WHERE id = ?", (signal_id,)).fetchone()
        return self._decode_signal(row)

    def delete_signal(self, signal_id: int) -> bool:
        with self.connect() as conn:
            return conn.execute("DELETE FROM signals WHERE id = ?", (signal_id,)).rowcount > 0

    def create_backtest_run(
        self, *, created_by_user_id: int | None, symbols: list[str], strategy: str,
        config: dict[str, Any], start_date: str, end_date: str, data_source: str = "vnstock",
    ) -> dict[str, Any]:
        now = utc_now_iso()
        with self.connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO backtest_runs
                (created_by_user_id, symbols_json, strategy, config_json, start_date, end_date, data_source, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (created_by_user_id, json.dumps(symbols), strategy, json.dumps(config), start_date, end_date, data_source, now),
            )
            run_id = int(cursor.lastrowid)
        return self.get_backtest_run(run_id)

    @staticmethod
    def _decode_run(row: sqlite3.Row) -> dict[str, Any]:
        result = dict(row)
        for source, target, fallback in (
            ("symbols_json", "symbols", []),
            ("config_json", "config", {}),
            ("metrics_json", "metrics", None),
        ):
            try:
                result[target] = json.loads(result[source]) if result[source] else fallback
            except (TypeError, json.JSONDecodeError):
                result[target] = fallback
            result.pop(source, None)
        return result

    def get_backtest_run(self, run_id: int) -> dict[str, Any]:
        with self.connect() as conn:
            row = conn.execute("SELECT * FROM backtest_runs WHERE id = ?", (run_id,)).fetchone()
        if not row:
            raise KeyError("Backtest run was not found")
        return self._decode_run(row)

    def list_backtest_runs(self, *, limit: int = 40) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute(
                "SELECT * FROM backtest_runs ORDER BY id DESC LIMIT ?",
                (max(1, min(limit, 200)),),
            ).fetchall()
        return [self._decode_run(row) for row in rows]

    def mark_backtest_running(self, run_id: int) -> None:
        with self.connect() as conn:
            conn.execute(
                "UPDATE backtest_runs SET status = 'running', started_at = ?, error_text = NULL WHERE id = ?",
                (utc_now_iso(), run_id),
            )

    def mark_interrupted_backtests(self) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                UPDATE backtest_runs SET status = 'failed', finished_at = ?,
                error_text = 'The Railway service restarted before this run completed.'
                WHERE status IN ('queued', 'running')
                """,
                (utc_now_iso(),),
            )

    def complete_backtest_run(
        self, run_id: int, *, metrics: dict[str, Any], equity_points: list[dict[str, Any]],
        trades: list[dict[str, Any]],
    ) -> None:
        with self.connect() as conn:
            conn.execute("DELETE FROM backtest_equity_points WHERE run_id = ?", (run_id,))
            conn.execute("DELETE FROM backtest_trades WHERE run_id = ?", (run_id,))
            conn.executemany(
                """
                INSERT INTO backtest_equity_points (run_id, trade_date, equity, cash, invested_symbols)
                VALUES (?, ?, ?, ?, ?)
                """,
                [(run_id, str(row["date"])[:10], float(row["equity"]), float(row["cash"]), int(row["invested_symbols"])) for row in equity_points],
            )
            conn.executemany(
                """
                INSERT INTO backtest_trades (run_id, trade_date, ticker, side, quantity, fill_price, notional, costs)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [(run_id, str(row["date"])[:10], str(row["symbol"]).upper(), str(row["side"]).upper(), int(row["quantity"]), float(row["fill_price"]), float(row["notional"]), float(row["costs"])) for row in trades],
            )
            conn.execute(
                "UPDATE backtest_runs SET status = 'completed', metrics_json = ?, finished_at = ?, error_text = NULL WHERE id = ?",
                (json.dumps(metrics), utc_now_iso(), run_id),
            )

    def fail_backtest_run(self, run_id: int, error: str) -> None:
        with self.connect() as conn:
            conn.execute(
                "UPDATE backtest_runs SET status = 'failed', error_text = ?, finished_at = ? WHERE id = ?",
                (error[:1_000], utc_now_iso(), run_id),
            )

    def set_backtest_standard(self, run_id: int) -> dict[str, Any]:
        run = self.get_backtest_run(run_id)
        if run["status"] != "completed":
            raise ValueError("Only a completed backtest can be a standard")
        with self.connect() as conn:
            conn.execute("UPDATE backtest_runs SET is_standard = 0 WHERE strategy = ?", (run["strategy"],))
            conn.execute("UPDATE backtest_runs SET is_standard = 1 WHERE id = ?", (run_id,))
        return self.get_backtest_run(run_id)

    def list_backtest_standards(self) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute(
                "SELECT * FROM backtest_runs WHERE is_standard = 1 ORDER BY strategy ASC"
            ).fetchall()
        return [self._decode_run(row) for row in rows]

    def delete_backtest_run(self, run_id: int) -> bool:
        with self.connect() as conn:
            return conn.execute("DELETE FROM backtest_runs WHERE id = ?", (run_id,)).rowcount > 0

    def list_backtest_equity_points(self, run_id: int) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute(
                "SELECT trade_date AS date, equity, cash, invested_symbols FROM backtest_equity_points WHERE run_id = ? ORDER BY trade_date ASC",
                (run_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def list_backtest_trades(self, run_id: int) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute(
                "SELECT trade_date AS date, ticker AS symbol, side, quantity, fill_price, notional, costs FROM backtest_trades WHERE run_id = ? ORDER BY trade_date ASC, id ASC",
                (run_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def list_backtest_price_bars(self, *, ticker: str, start_date: str, end_date: str) -> list[dict[str, Any]]:
        with self.connect() as conn:
            rows = conn.execute(
                """
                SELECT trade_date AS date, open, high, low, close, volume, provider
                FROM backtest_price_bars WHERE ticker = ? AND trade_date >= ? AND trade_date <= ?
                ORDER BY trade_date ASC
                """,
                (ticker.strip().upper(), start_date, end_date),
            ).fetchall()
        return [dict(row) for row in rows]

    def upsert_backtest_price_bars(self, *, ticker: str, bars: list[dict[str, Any]], provider: str) -> None:
        now = utc_now_iso()
        with self.connect() as conn:
            conn.executemany(
                """
                INSERT INTO backtest_price_bars
                (ticker, trade_date, open, high, low, close, volume, provider, retrieved_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(ticker, trade_date) DO UPDATE SET
                open = excluded.open, high = excluded.high, low = excluded.low, close = excluded.close,
                volume = excluded.volume, provider = excluded.provider, retrieved_at = excluded.retrieved_at
                """,
                [(ticker.strip().upper(), str(row["date"])[:10], float(row["open"]), float(row["high"]), float(row["low"]), float(row["close"]), float(row["volume"]), provider, now) for row in bars],
            )
