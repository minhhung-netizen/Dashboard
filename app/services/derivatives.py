from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo


MARKET_TZ = ZoneInfo("Asia/Ho_Chi_Minh")
DERIVATIVE_ACTIONS = {
    "long_start",
    "short_start",
    "dca_long",
    "dca_short",
    "close_long",
    "close_short",
    "mark",
}


@dataclass
class DerivativePosition:
    symbol: str
    strategy: str
    side: str
    quantity: float
    total_cost: float
    entry_time: str
    entry_signal_id: int
    contract_multiplier: float
    layers: list[dict[str, Any]] = field(default_factory=list)
    latest_payload: dict[str, Any] = field(default_factory=dict)

    @property
    def average_price(self) -> float:
        return self.total_cost / self.quantity if self.quantity > 0 else 0


def normalize_derivative_action(raw_action: str | None) -> str:
    if not raw_action:
        raise ValueError("action is required")
    action = raw_action.strip().lower()
    compact = "".join(ch for ch in action if ch.isalnum())
    aliases = {
        "long": "long_start",
        "buylong": "long_start",
        "longstart": "long_start",
        "short": "short_start",
        "sellshort": "short_start",
        "shortstart": "short_start",
        "dcalong": "dca_long",
        "longdca": "dca_long",
        "dcashort": "dca_short",
        "shortdca": "dca_short",
        "closelong": "close_long",
        "exitlong": "close_long",
        "longexit": "close_long",
        "closeshort": "close_short",
        "exitshort": "close_short",
        "shortexit": "close_short",
        "mark": "mark",
        "positionupdate": "mark",
        "priceupdate": "mark",
    }
    normalized = aliases.get(action, aliases.get(compact, action))
    if normalized not in DERIVATIVE_ACTIONS:
        raise ValueError(f"unsupported derivative action: {raw_action}")
    return normalized


def build_derivative_performance(
    events: list[dict[str, Any]],
    initial_capital: float = 0,
) -> dict[str, Any]:
    ordered = sorted(events, key=lambda item: (_event_sort_time(item), item["id"]))
    visible_events = [event for event in ordered if event["action"] != "mark"]
    positions: dict[tuple[str, str], DerivativePosition] = {}
    latest_prices: dict[str, float] = {}
    closed_trades: list[dict[str, Any]] = []
    ignored_events: list[dict[str, Any]] = []

    for event in ordered:
        symbol = event["symbol"]
        strategy = (event.get("strategy") or "Unspecified").strip() or "Unspecified"
        key = (symbol, strategy)
        action = event["action"]
        price = _safe_float(event.get("price"))
        quantity = _safe_float(event.get("quantity")) or 0
        multiplier = _safe_float(event.get("contract_multiplier")) or 100000
        if price is not None and price > 0:
            latest_prices[symbol] = price

        if action in {"long_start", "short_start"}:
            if key in positions:
                ignored_events.append(_ignored(event, "position_already_open"))
                continue
            if price is None or price <= 0 or quantity <= 0:
                ignored_events.append(_ignored(event, "invalid_entry"))
                continue
            side = "long" if action == "long_start" else "short"
            positions[key] = DerivativePosition(
                symbol=symbol,
                strategy=strategy,
                side=side,
                quantity=quantity,
                total_cost=price * quantity,
                entry_time=_event_time(event),
                entry_signal_id=event["id"],
                contract_multiplier=multiplier,
                layers=[_layer_record(event, price, quantity)],
                latest_payload=event.get("payload") or {},
            )
            continue

        if action in {"dca_long", "dca_short"}:
            position = positions.get(key)
            expected_side = "long" if action == "dca_long" else "short"
            if position is None or position.side != expected_side:
                ignored_events.append(_ignored(event, "dca_without_matching_position"))
                continue
            if price is None or price <= 0 or quantity <= 0:
                ignored_events.append(_ignored(event, "invalid_dca"))
                continue
            position.total_cost += price * quantity
            position.quantity += quantity
            position.layers.append(_layer_record(event, price, quantity))
            position.latest_payload = event.get("payload") or {}
            continue

        if action in {"close_long", "close_short"}:
            position = positions.get(key)
            expected_side = "long" if action == "close_long" else "short"
            if position is None or position.side != expected_side:
                ignored_events.append(_ignored(event, "close_without_matching_position"))
                continue
            if price is None or price <= 0:
                ignored_events.append(_ignored(event, "invalid_close"))
                continue
            closed_trades.append(_trade_record(position, price, event, status="closed"))
            positions.pop(key, None)
            continue

        if action == "mark":
            position = positions.get(key)
            if position is None:
                ignored_events.append(_ignored(event, "mark_without_open_position"))
                continue
            position.latest_payload = event.get("payload") or position.latest_payload

    open_positions = [
        _trade_record(
            position,
            latest_prices.get(position.symbol, position.average_price),
            None,
            status="open",
        )
        for position in positions.values()
    ]
    return {
        "summary": _summary(open_positions, closed_trades, initial_capital),
        "open_positions": sorted(open_positions, key=lambda row: (row["symbol"], row["strategy"])),
        "closed_trades": sorted(
            closed_trades,
            key=lambda row: (_parse_timestamp(row.get("exit_time")), row["exit_signal_id"]),
            reverse=True,
        ),
        "events": sorted(visible_events, key=lambda row: row["id"], reverse=True),
        "ignored_events": ignored_events,
    }


def _trade_record(
    position: DerivativePosition,
    mark_price: float,
    exit_event: dict[str, Any] | None,
    *,
    status: str,
) -> dict[str, Any]:
    direction = 1 if position.side == "long" else -1
    points_per_contract = (mark_price - position.average_price) * direction
    pnl_points = points_per_contract * position.quantity
    pnl_vnd = pnl_points * position.contract_multiplier
    payload = exit_event.get("payload") if exit_event else position.latest_payload
    return {
        "symbol": position.symbol,
        "strategy": position.strategy,
        "side": position.side,
        "status": status,
        "average_price": position.average_price,
        "current_price": mark_price,
        "exit_price": mark_price if status == "closed" else None,
        "quantity": position.quantity,
        "layer_count": len(position.layers),
        "layers": list(position.layers),
        "entry_time": position.entry_time,
        "exit_time": _event_time(exit_event) if exit_event else None,
        "entry_signal_id": position.entry_signal_id,
        "exit_signal_id": exit_event["id"] if exit_event else None,
        "exit_reason": (exit_event or {}).get("reason"),
        "points_per_contract": points_per_contract,
        "pnl_points": pnl_points,
        "pnl_vnd": pnl_vnd,
        "contract_multiplier": position.contract_multiplier,
        "take_profit": _safe_float((payload or {}).get("take_profit")),
        "stop_loss": _safe_float((payload or {}).get("stop_loss")),
    }


def _summary(
    open_positions: list[dict[str, Any]],
    closed_trades: list[dict[str, Any]],
    initial_capital: float,
) -> dict[str, Any]:
    wins = sum(1 for trade in closed_trades if trade["pnl_points"] > 0)
    realized_pnl_vnd = sum(row["pnl_vnd"] for row in closed_trades)
    open_pnl_vnd = sum(row["pnl_vnd"] for row in open_positions)
    equity = initial_capital
    peak_equity = initial_capital
    max_drawdown_vnd = 0.0
    max_drawdown_pct = 0.0
    for trade in closed_trades:
        equity += trade["pnl_vnd"]
        peak_equity = max(peak_equity, equity)
        drawdown_vnd = max(0.0, peak_equity - equity)
        drawdown_pct = drawdown_vnd / peak_equity * 100 if peak_equity > 0 else 0.0
        if drawdown_vnd > max_drawdown_vnd:
            max_drawdown_vnd = drawdown_vnd
        if drawdown_pct > max_drawdown_pct:
            max_drawdown_pct = drawdown_pct
    return {
        "open_count": len(open_positions),
        "closed_count": len(closed_trades),
        "wins": wins,
        "win_rate_pct": wins / len(closed_trades) * 100 if closed_trades else None,
        "open_pnl_points": sum(row["pnl_points"] for row in open_positions),
        "open_pnl_vnd": open_pnl_vnd,
        "realized_pnl_points": sum(row["pnl_points"] for row in closed_trades),
        "realized_pnl_vnd": realized_pnl_vnd,
        "initial_capital": initial_capital,
        "realized_equity": initial_capital + realized_pnl_vnd,
        "current_equity": initial_capital + realized_pnl_vnd + open_pnl_vnd,
        "max_drawdown_vnd": max_drawdown_vnd,
        "max_drawdown_pct": max_drawdown_pct if initial_capital > 0 else None,
    }


def _layer_record(event: dict[str, Any], price: float, quantity: float) -> dict[str, Any]:
    return {
        "signal_id": event["id"],
        "price": price,
        "quantity": quantity,
        "time": _event_time(event),
    }


def _ignored(event: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "id": event["id"],
        "symbol": event["symbol"],
        "strategy": event.get("strategy"),
        "action": event["action"],
        "reason": reason,
        "time": _event_time(event),
    }


def _event_time(event: dict[str, Any] | None) -> str | None:
    if not event:
        return None
    return event.get("source_time") or event.get("received_at")


def _event_sort_time(event: dict[str, Any]) -> float:
    return _parse_timestamp(_event_time(event))


def _parse_timestamp(value: str | None) -> float:
    if not value:
        return 0
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=MARKET_TZ)
        return parsed.timestamp()
    except (TypeError, ValueError):
        return 0


def _safe_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
