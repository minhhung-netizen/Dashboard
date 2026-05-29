from __future__ import annotations

from datetime import date, datetime, time
from typing import Any
from zoneinfo import ZoneInfo

from app.services.dividends import dividend_adjustment


MARKET_TZ = ZoneInfo("Asia/Ho_Chi_Minh")
EQUITY_CURVE_DAILY_CUTOFF = time(18, 0)


def build_manual_portfolio(
    positions: list[dict[str, Any]],
    daily_performance: list[dict[str, Any]] | None = None,
    dividend_events: list[dict[str, Any]] | None = None,
    as_of_date: date | None = None,
) -> dict[str, Any]:
    rows = [
        _position_row(position, dividend_events=dividend_events, as_of_date=as_of_date)
        for position in positions
    ]
    open_positions = [row for row in rows if row["status"] == "open"]
    closed_positions = [row for row in rows if row["status"] == "closed"]
    return {
        "summary": _summary(rows, open_positions, closed_positions),
        "positions": rows,
        "open_positions": open_positions,
        "closed_positions": closed_positions,
        "daily_performance": daily_performance or [],
        "equity_curve": _stored_equity_curve(daily_performance)
        if daily_performance
        else _equity_curve(positions),
    }


def build_daily_performance_record(
    positions: list[dict[str, Any]],
    recorded_at: str | None = None,
    dividend_events: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    recorded_at = recorded_at or datetime.now(MARKET_TZ).isoformat()
    recorded_dt = _parse_market_datetime(recorded_at)
    if recorded_dt is None:
        recorded_dt = datetime.now(MARKET_TZ)
        recorded_at = recorded_dt.isoformat()

    rows = [
        _position_row(
            position,
            dividend_events=dividend_events,
            as_of_date=recorded_dt.date(),
        )
        for position in positions
    ]
    open_positions = [row for row in rows if row["status"] == "open"]
    closed_positions = [row for row in rows if row["status"] == "closed"]
    summary = _summary(rows, open_positions, closed_positions)
    portfolio_return = summary["portfolio_return_pct"]
    equity_value = 100 + (portfolio_return or 0)
    return {
        "trade_date": recorded_dt.date().isoformat(),
        "portfolio_return_pct": portfolio_return,
        "equity_value": equity_value,
        "total_weight_pct": summary["total_weight_pct"],
        "open_count": summary["open_count"],
        "closed_count": summary["closed_count"],
        "cost_value": summary["cost_value"],
        "market_value": summary["market_value"],
        "pnl_value": summary["pnl_value"],
        "recorded_at": recorded_at,
    }


def is_after_daily_cutoff(recorded_at: str | None = None) -> bool:
    recorded_dt = _parse_market_datetime(recorded_at)
    if recorded_dt is None:
        recorded_dt = datetime.now(MARKET_TZ)
    return recorded_dt.time() >= EQUITY_CURVE_DAILY_CUTOFF


def _position_row(
    position: dict[str, Any],
    dividend_events: list[dict[str, Any]] | None = None,
    as_of_date: date | None = None,
) -> dict[str, Any]:
    original_entry_price = _safe_float(position.get("entry_price")) or 0
    current_price = _safe_float(position.get("current_price")) or original_entry_price
    exit_price = _safe_float(position.get("exit_price"))
    status = position.get("status") or "open"
    mark_price = exit_price if status == "closed" and exit_price is not None else current_price
    adjustment = dividend_adjustment(
        ticker=position.get("ticker"),
        entry_price=original_entry_price,
        entry_time=position.get("entry_date") or position.get("created_at"),
        valuation_time=position.get("closed_at") if status == "closed" else None,
        dividend_events=dividend_events,
        as_of_date=as_of_date,
        include_upcoming=status == "open",
    )
    entry_price = adjustment["entry_price_adjusted"]
    quantity = _safe_float(position.get("quantity"))
    weight_pct = _safe_float(position.get("weight_pct")) or 0
    return_pct = ((mark_price - entry_price) / entry_price * 100) if entry_price > 0 else None
    cost_value = entry_price * quantity if quantity is not None else None
    market_value = mark_price * quantity if quantity is not None else None
    pnl_value = market_value - cost_value if market_value is not None and cost_value is not None else None
    row = dict(position)
    row.update(
        {
            "weight_pct": weight_pct,
            "entry_price": entry_price,
            "entry_price_original": adjustment["entry_price_original"],
            "current_price": current_price,
            "mark_price": mark_price,
            "quantity": quantity,
            "return_pct": return_pct,
            "dividend_adjusted": adjustment["dividend_adjusted"],
            "dividend_notes": adjustment["dividend_notes"],
            "cost_value": cost_value,
            "market_value": market_value,
            "pnl_value": pnl_value,
        }
    )
    return row


def _summary(
    rows: list[dict[str, Any]],
    open_positions: list[dict[str, Any]],
    closed_positions: list[dict[str, Any]],
) -> dict[str, Any]:
    total_weight = sum(row["weight_pct"] for row in open_positions)
    weighted_return = _weighted_return(open_positions)
    cost_value = sum(row["cost_value"] or 0 for row in open_positions)
    market_value = sum(row["market_value"] or 0 for row in open_positions)
    return {
        "total_positions": len(rows),
        "open_count": len(open_positions),
        "closed_count": len(closed_positions),
        "total_weight_pct": total_weight,
        "portfolio_return_pct": weighted_return,
        "cost_value": cost_value or None,
        "market_value": market_value or None,
        "pnl_value": market_value - cost_value if cost_value or market_value else None,
        "winners": sum(1 for row in open_positions if (row["return_pct"] or 0) > 0),
        "losers": sum(1 for row in open_positions if (row["return_pct"] or 0) < 0),
    }


def _weighted_return(rows: list[dict[str, Any]]) -> float | None:
    weighted = [
        (row["weight_pct"], row["return_pct"])
        for row in rows
        if row["weight_pct"] > 0 and row["return_pct"] is not None
    ]
    total_weight = sum(weight for weight, _ in weighted)
    if total_weight <= 0:
        return None
    return sum(weight * return_pct for weight, return_pct in weighted) / total_weight


def _equity_curve(positions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    positions_by_id = {position["id"]: position for position in positions}
    for position in positions:
        entry_date = position.get("entry_date") or position.get("created_at")
        if entry_date:
            events.append(
                {
                    "position_id": position["id"],
                    "price": _safe_float(position.get("entry_price")) or 0,
                    "time": entry_date,
                    "sort_time": _sort_timestamp(entry_date),
                }
            )
        events.extend(_daily_equity_snapshot_events(position, entry_date))

    events = sorted(
        [event for event in events if event["time"] and event["price"] > 0],
        key=lambda event: (event["sort_time"], event["position_id"]),
    )
    if not events:
        return []

    marks: dict[int, float] = {}
    curve: list[dict[str, Any]] = []
    last_time = ""
    for event in events:
        marks[event["position_id"]] = event["price"]
        time = event["time"]
        if time == last_time and curve:
            curve.pop()
        eligible_rows = []
        for position_id, mark_price in marks.items():
            position = positions_by_id[position_id]
            row = dict(position)
            row["current_price"] = mark_price
            closed_at = position.get("closed_at") or ""
            if position.get("status") == "closed" and closed_at and closed_at <= time:
                row["exit_price"] = mark_price
            else:
                row["exit_price"] = None
                row["status"] = "open"
            eligible_rows.append(_position_row(row))
        weighted_return = _weighted_return(eligible_rows) or 0
        curve.append(
            {
                "time": time,
                "value": 100 + weighted_return,
                "return_pct": weighted_return,
            }
        )
        last_time = time
    return curve


def _stored_equity_curve(daily_performance: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    curve = []
    for row in daily_performance or []:
        trade_date = row.get("trade_date")
        if not trade_date:
            continue
        portfolio_return = _safe_float(row.get("portfolio_return_pct"))
        equity_value = _safe_float(row.get("equity_value"))
        if equity_value is None:
            equity_value = 100 + (portfolio_return or 0)
        curve.append(
            {
                "time": row.get("recorded_at") or trade_date,
                "trade_date": trade_date,
                "value": equity_value,
                "return_pct": portfolio_return or 0,
            }
        )
    return curve


def _daily_equity_snapshot_events(
    position: dict[str, Any], entry_date: str | None
) -> list[dict[str, Any]]:
    snapshots_by_day: dict[str, dict[str, Any]] = {}
    for snapshot in position.get("snapshots") or []:
        price = _safe_float(snapshot.get("price")) or 0
        recorded_at = snapshot.get("recorded_at") or entry_date
        recorded_dt = _parse_market_datetime(recorded_at)
        if price <= 0 or recorded_dt is None:
            continue
        if recorded_dt.time() < EQUITY_CURVE_DAILY_CUTOFF:
            continue

        market_day = recorded_dt.date().isoformat()
        event = {
            "position_id": position["id"],
            "price": price,
            "time": recorded_at,
            "sort_time": recorded_dt.timestamp(),
        }
        existing = snapshots_by_day.get(market_day)
        if existing is None or event["sort_time"] > existing["sort_time"]:
            snapshots_by_day[market_day] = event
    return list(snapshots_by_day.values())


def _parse_market_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=MARKET_TZ)
    return parsed.astimezone(MARKET_TZ)


def _sort_timestamp(value: str | None) -> float:
    parsed = _parse_market_datetime(value)
    return parsed.timestamp() if parsed else 0


def _safe_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
