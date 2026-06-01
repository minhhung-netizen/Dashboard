from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from math import prod
from typing import Any
from zoneinfo import ZoneInfo

from app.services.dividends import dividend_adjustment


DEFAULT_STRATEGY = "Unspecified"
MARKET_TZ = ZoneInfo("Asia/Ho_Chi_Minh")


@dataclass
class OpenPosition:
    ticker: str
    strategy: str
    entry_price: float
    entry_time: str
    entry_signal_id: int
    confirmations: list[dict[str, Any]] = field(default_factory=list)


def build_performance(
    signals: list[dict[str, Any]],
    dividend_events: list[dict[str, Any]] | None = None,
    as_of_date: date | None = None,
) -> dict[str, Any]:
    ordered = sorted(signals, key=lambda item: (_signal_sort_time(item), item["id"]))
    latest_prices = _latest_prices_by_ticker(ordered)
    open_positions: dict[tuple[str, str], OpenPosition] = {}
    trades: list[dict[str, Any]] = []
    ignored_signals: list[dict[str, Any]] = []

    for signal in ordered:
        ticker = signal["ticker"]
        strategy = _strategy_name(signal.get("strategy"))
        action = (signal.get("action") or "").lower()
        price = _safe_float(signal.get("price"))
        key = (ticker, strategy)

        if action == "buy":
            if price is None or price <= 0:
                ignored_signals.append(_ignored(signal, "missing_buy_price"))
                continue
            if key in open_positions:
                ignored_signals.append(_ignored(signal, "position_already_open"))
                continue
            open_positions[key] = OpenPosition(
                ticker=ticker,
                strategy=strategy,
                entry_price=price,
                entry_time=_signal_time(signal),
                entry_signal_id=signal["id"],
            )
            continue

        if action == "sell":
            position = open_positions.pop(key, None)
            if position is None:
                ignored_signals.append(_ignored(signal, "sell_without_open_buy"))
                continue
            if price is None or price <= 0:
                ignored_signals.append(_ignored(signal, "missing_sell_price"))
                open_positions[key] = position
                continue
            trades.append(
                _trade_record(
                    position=position,
                    exit_price=price,
                    exit_time=_signal_time(signal),
                    exit_signal_id=signal["id"],
                    status="closed",
                    dividend_events=dividend_events,
                    as_of_date=as_of_date,
                )
            )

        if action == "confirm_buy":
            base_strategy = _base_strategy_name(signal)
            if not base_strategy:
                continue
            position_key = _find_open_position_key(open_positions, ticker, base_strategy)
            if position_key is None:
                continue
            open_positions[position_key].confirmations.append(_confirmation_record(signal))
            continue

    open_trades = []
    for position in open_positions.values():
        current_price = latest_prices.get(position.ticker, position.entry_price)
        open_trades.append(
            _trade_record(
                position=position,
                exit_price=current_price,
                exit_time=None,
                exit_signal_id=None,
                status="open",
                dividend_events=dividend_events,
                as_of_date=as_of_date,
            )
        )

    strategy_rows = _strategy_summary(trades, open_trades)
    return {
        "strategies": strategy_rows,
        "closed_trades": trades,
        "open_trades": open_trades,
        "confirmation_stats": _confirmation_stats(trades),
        "ignored_signals": ignored_signals,
    }


def _strategy_summary(
    closed_trades: list[dict[str, Any]], open_trades: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], dict[str, Any]] = {}

    for trade in closed_trades:
        key = (trade["ticker"], trade["strategy"])
        row = grouped.setdefault(key, _empty_strategy(trade["ticker"], trade["strategy"]))
        row["closed_trades"] += 1
        row["wins"] += 1 if trade["return_pct"] > 0 else 0
        row["realized_return_factor"] *= 1 + trade["return_pct"] / 100
        row["realized_return_sum_pct"] += trade["return_pct"]

    for trade in open_trades:
        key = (trade["ticker"], trade["strategy"])
        row = grouped.setdefault(key, _empty_strategy(trade["ticker"], trade["strategy"]))
        row["open_trades"] += 1
        row["open_return_sum_pct"] += trade["return_pct"]

    for row in grouped.values():
        closed = row["closed_trades"]
        open_count = row["open_trades"]
        row["win_rate_pct"] = (row["wins"] / closed * 100) if closed else None
        row["avg_closed_return_pct"] = (
            row["realized_return_sum_pct"] / closed if closed else None
        )
        row["realized_return_pct"] = (row.pop("realized_return_factor") - 1) * 100
        row["open_return_avg_pct"] = (
            row["open_return_sum_pct"] / open_count if open_count else None
        )
        row["current_return_pct"] = _combined_return(row)
        del row["realized_return_sum_pct"]
        del row["open_return_sum_pct"]

    return sorted(
        grouped.values(),
        key=lambda item: (
            item["current_return_pct"] if item["current_return_pct"] is not None else -10**9
        ),
        reverse=True,
    )


def _combined_return(row: dict[str, Any]) -> float | None:
    factors = []
    if row["closed_trades"]:
        factors.append(1 + row["realized_return_pct"] / 100)
    if row["open_trades"] and row["open_return_avg_pct"] is not None:
        factors.append(1 + row["open_return_avg_pct"] / 100)
    if not factors:
        return None
    return (prod(factors) - 1) * 100


def _empty_strategy(ticker: str, strategy: str) -> dict[str, Any]:
    return {
        "ticker": ticker,
        "strategy": strategy,
        "closed_trades": 0,
        "open_trades": 0,
        "wins": 0,
        "win_rate_pct": None,
        "avg_closed_return_pct": None,
        "realized_return_factor": 1.0,
        "realized_return_sum_pct": 0.0,
        "open_return_sum_pct": 0.0,
        "open_return_avg_pct": None,
        "current_return_pct": None,
    }


def _confirmation_stats(closed_trades: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups = {
        "confirmed": {
            "status": "confirmed",
            "label": "With confirm",
            "closed_trades": 0,
            "wins": 0,
            "return_sum_pct": 0.0,
            "return_factor": 1.0,
        },
        "unconfirmed": {
            "status": "unconfirmed",
            "label": "Without confirm",
            "closed_trades": 0,
            "wins": 0,
            "return_sum_pct": 0.0,
            "return_factor": 1.0,
        },
    }
    for trade in closed_trades:
        key = "confirmed" if trade.get("has_confirm_buy") else "unconfirmed"
        row = groups[key]
        return_pct = _safe_float(trade.get("return_pct")) or 0
        row["closed_trades"] += 1
        row["wins"] += 1 if return_pct > 0 else 0
        row["return_sum_pct"] += return_pct
        row["return_factor"] *= 1 + return_pct / 100

    stats = []
    for key in ("confirmed", "unconfirmed"):
        row = groups[key]
        closed = row["closed_trades"]
        stats.append(
            {
                "status": row["status"],
                "label": row["label"],
                "closed_trades": closed,
                "win_rate_pct": (row["wins"] / closed * 100) if closed else None,
                "avg_return_pct": (row["return_sum_pct"] / closed) if closed else None,
                "total_return_pct": (row["return_factor"] - 1) * 100 if closed else None,
            }
        )
    return stats


def _trade_record(
    *,
    position: OpenPosition,
    exit_price: float,
    exit_time: str | None,
    exit_signal_id: int | None,
    status: str,
    dividend_events: list[dict[str, Any]] | None = None,
    as_of_date: date | None = None,
) -> dict[str, Any]:
    adjustment = dividend_adjustment(
        ticker=position.ticker,
        entry_price=position.entry_price,
        entry_time=position.entry_time,
        valuation_time=exit_time,
        dividend_events=dividend_events,
        as_of_date=as_of_date,
        include_upcoming=status == "open",
    )
    entry_price = adjustment["entry_price_adjusted"]
    return_pct = (exit_price - entry_price) / entry_price * 100
    holding_seconds = _holding_seconds(position.entry_time, exit_time)
    return {
        "ticker": position.ticker,
        "strategy": position.strategy,
        "status": status,
        "entry_price": entry_price,
        "entry_price_original": adjustment["entry_price_original"],
        "entry_time": position.entry_time,
        "entry_signal_id": position.entry_signal_id,
        "exit_price": exit_price,
        "exit_time": exit_time,
        "exit_signal_id": exit_signal_id,
        "holding_seconds": holding_seconds,
        "return_pct": return_pct,
        "dividend_adjusted": adjustment["dividend_adjusted"],
        "dividend_notes": adjustment["dividend_notes"],
        "confirmations": list(position.confirmations),
        "has_confirm_buy": any(
            confirmation.get("action") == "confirm_buy"
            for confirmation in position.confirmations
        ),
    }


def _latest_prices_by_ticker(signals: list[dict[str, Any]]) -> dict[str, float]:
    latest_signal_prices: dict[str, float] = {}
    latest_history_prices: dict[str, tuple[str, float]] = {}
    for signal in signals:
        price = _safe_float(signal.get("price"))
        enrichment = signal.get("enrichment") or {}
        history_price = _latest_history_close(enrichment)
        if price is not None and price > 0:
            latest_signal_prices[signal["ticker"]] = price
        if history_price is not None and history_price > 0:
            marker = enrichment.get("refreshed_at") or signal["received_at"]
            existing = latest_history_prices.get(signal["ticker"])
            if existing is None or marker > existing[0]:
                latest_history_prices[signal["ticker"]] = (marker, history_price)

    latest = dict(latest_signal_prices)
    for ticker, (_, history_price) in latest_history_prices.items():
        latest[ticker] = history_price
    return latest


def _latest_history_close(enrichment: dict[str, Any]) -> float | None:
    history = enrichment.get("history") or []
    if not history:
        return None
    latest_row = history[-1]
    return _safe_float(
        latest_row.get("close")
        or latest_row.get("Close")
        or latest_row.get("closePrice")
        or latest_row.get("c")
    )


def _strategy_name(value: str | None) -> str:
    return (value or DEFAULT_STRATEGY).strip() or DEFAULT_STRATEGY


def _base_strategy_name(signal: dict[str, Any]) -> str | None:
    payload = signal.get("payload") or {}
    for key in ("base_strategy", "confirm_for", "requires_open_strategy"):
        value = payload.get(key)
        if value and str(value).strip():
            return str(value).strip()
    return None


def _find_open_position_key(
    open_positions: dict[tuple[str, str], OpenPosition],
    ticker: str,
    strategy: str,
) -> tuple[str, str] | None:
    target_strategy = strategy.strip().lower()
    for key, position in open_positions.items():
        if position.ticker == ticker and position.strategy.strip().lower() == target_strategy:
            return key
    return None


def _confirmation_record(signal: dict[str, Any]) -> dict[str, Any]:
    return {
        "signal_id": signal["id"],
        "action": signal.get("action"),
        "strategy": _strategy_name(signal.get("strategy")),
        "price": _safe_float(signal.get("price")),
        "time": _signal_time(signal),
        "note": signal.get("note"),
    }


def _safe_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _holding_seconds(entry_time: str, exit_time: str | None) -> int | None:
    if not exit_time:
        return None
    entry = _parse_datetime(entry_time)
    exit_ = _parse_datetime(exit_time)
    if entry is None or exit_ is None:
        return None
    return max(0, int((exit_ - entry).total_seconds()))


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    value = value.strip()
    try:
        return _market_datetime(datetime.fromisoformat(value.replace("Z", "+00:00")))
    except ValueError:
        pass
    try:
        return _market_datetime(datetime.strptime(value, "%Y-%m-%d %H:%M:%S"))
    except ValueError:
        pass
    for fmt in ("%m/%d/%Y, %I:%M:%S %p", "%d/%m/%Y, %I:%M:%S %p"):
        try:
            return _market_datetime(datetime.strptime(value, fmt))
        except ValueError:
            continue
    return None


def _market_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=MARKET_TZ)
    return value.astimezone(MARKET_TZ)


def _signal_time(signal: dict[str, Any]) -> str:
    return signal.get("source_time") or signal["received_at"]


def _signal_sort_time(signal: dict[str, Any]) -> str:
    signal_time = _signal_time(signal)
    parsed = _parse_datetime(signal_time)
    return parsed.isoformat() if parsed else signal_time


def _ignored(signal: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "signal_id": signal["id"],
        "ticker": signal["ticker"],
        "strategy": _strategy_name(signal.get("strategy")),
        "action": signal.get("action"),
        "reason": reason,
    }
