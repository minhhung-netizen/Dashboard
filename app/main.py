from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Any

from fastapi import BackgroundTasks, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field

from app.config import PROJECT_ROOT, get_settings
from app.database import SignalStore, utc_now_iso
from app.services.enrichment import (
    VnstockEnricher,
    coerce_float,
    normalize_action,
    normalize_ticker,
)
from app.services.market_hours import is_market_open
from app.services.manual_portfolio import build_manual_portfolio
from app.services.performance import build_performance


settings = get_settings()
store = SignalStore(settings.database_path)
enricher = VnstockEnricher()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(price_refresh_loop())
    try:
        yield
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass


app = FastAPI(title="TradingView VN Dashboard", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=PROJECT_ROOT / "app" / "static"), name="static")


class WebhookPayload(BaseModel):
    model_config = ConfigDict(extra="allow")

    ticker: str = Field(..., examples=["HOSE:VPB"])
    action: str = Field(..., examples=["buy"])
    price: str | float | int | None = None
    timeframe: str | None = None
    strategy: str | None = None
    note: str | None = None
    time: str | None = None
    secret: str | None = None


class ManualPositionPayload(BaseModel):
    ticker: str = Field(..., examples=["VPB"])
    weight_pct: float = Field(..., gt=0, examples=[10])
    entry_price: float = Field(..., gt=0, examples=[19.5])
    current_price: float | None = Field(default=None, gt=0, examples=[20.2])
    quantity: float | None = Field(default=None, gt=0, examples=[1000])
    entry_date: str | None = None
    note: str | None = None


class ManualPositionUpdatePayload(BaseModel):
    ticker: str | None = None
    weight_pct: float | None = Field(default=None, gt=0)
    entry_price: float | None = Field(default=None, gt=0)
    current_price: float | None = Field(default=None, gt=0)
    quantity: float | None = Field(default=None, gt=0)
    entry_date: str | None = None
    note: str | None = None


class ManualClosePayload(BaseModel):
    exit_price: float = Field(..., gt=0)
    closed_at: str | None = None


@app.get("/")
def dashboard() -> FileResponse:
    return FileResponse(PROJECT_ROOT / "app" / "static" / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/webhook")
def receive_webhook(
    payload: WebhookPayload,
    background_tasks: BackgroundTasks,
    secret: str | None = Query(default=None),
) -> dict[str, Any]:
    if settings.webhook_secret and settings.webhook_secret not in {secret, payload.secret}:
        raise HTTPException(status_code=401, detail="Invalid webhook secret")

    try:
        ticker, exchange = normalize_ticker(payload.ticker)
        action = normalize_action(payload.action)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    duplicate = store.find_duplicate_signal(
        ticker=ticker,
        action=action,
        timeframe=payload.timeframe,
        strategy=payload.strategy,
        source_time=payload.time,
        window_minutes=settings.duplicate_window_minutes,
    )
    if duplicate:
        store.record_invalid_signal(
            ticker=ticker,
            action=action,
            timeframe=payload.timeframe,
            strategy=payload.strategy,
            reason="duplicate_webhook",
            source_time=payload.time,
            payload=payload.model_dump(),
        )
        return {"status": "duplicate", "signal": duplicate}

    signal = store.insert_signal(
        ticker=ticker,
        exchange=exchange,
        action=action,
        price=coerce_float(payload.price),
        timeframe=payload.timeframe,
        strategy=payload.strategy,
        note=payload.note,
        source_time=payload.time,
        payload=payload.model_dump(),
        enrichment={"status": "pending", "ticker": ticker, "history": [], "metrics": {}},
    )
    background_tasks.add_task(enrich_signal, signal["id"], ticker)
    return {"status": "accepted", "signal": signal}


@app.get("/api/signals")
def list_signals(ticker: str | None = None, limit: int = 100) -> dict[str, Any]:
    normalized_ticker = normalize_ticker(ticker)[0] if ticker else None
    return {"signals": store.list_signals(ticker=normalized_ticker, limit=limit)}


@app.delete("/api/signals/{signal_id}")
def delete_signal(signal_id: int) -> dict[str, Any]:
    if not store.delete_signal(signal_id):
        raise HTTPException(status_code=404, detail="Signal not found")
    return {"status": "deleted", "signal_id": signal_id}


@app.get("/api/summary")
def summary() -> dict[str, Any]:
    return store.summary()


@app.get("/api/performance")
def performance(ticker: str | None = None, strategy: str | None = None) -> dict[str, Any]:
    normalized_ticker = normalize_ticker(ticker)[0] if ticker else None
    signals = store.list_all_signals(ticker=normalized_ticker)
    if strategy:
        strategy_filter = strategy.strip().lower()
        signals = [
            signal
            for signal in signals
            if strategy_filter in (signal.get("strategy") or "").strip().lower()
        ]
    return build_performance(signals)


@app.get("/api/invalid-signals")
def invalid_signals(limit: int = 100) -> dict[str, Any]:
    return {"invalid_signals": store.list_invalid_signals(limit=limit)}


@app.get("/api/manual-portfolio")
def manual_portfolio() -> dict[str, Any]:
    return build_manual_portfolio(store.list_manual_positions())


@app.post("/api/manual-portfolio")
def create_manual_position(
    payload: ManualPositionPayload, background_tasks: BackgroundTasks
) -> dict[str, Any]:
    ticker, _ = normalize_ticker(payload.ticker)
    position = store.insert_manual_position(
        ticker=ticker,
        weight_pct=payload.weight_pct,
        entry_price=payload.entry_price,
        current_price=payload.current_price,
        quantity=payload.quantity,
        entry_date=payload.entry_date,
        note=payload.note,
    )
    background_tasks.add_task(refresh_manual_ticker_price, ticker)
    return {"status": "created", "position": position}


@app.patch("/api/manual-portfolio/{position_id}")
def update_manual_position(
    position_id: int, payload: ManualPositionUpdatePayload
) -> dict[str, Any]:
    updates = payload.model_dump(exclude_unset=True)
    if "ticker" in updates and updates["ticker"]:
        updates["ticker"] = normalize_ticker(updates["ticker"])[0]
    try:
        position = store.update_manual_position(position_id, updates)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Manual position not found") from exc
    return {"status": "updated", "position": position}


@app.post("/api/manual-portfolio/refresh-prices")
async def refresh_manual_portfolio_prices_endpoint() -> dict[str, Any]:
    updated = await refresh_manual_portfolio_prices()
    return {"status": "refreshed", "updated_positions": updated}


@app.post("/api/manual-portfolio/{position_id}/close")
def close_manual_position(position_id: int, payload: ManualClosePayload) -> dict[str, Any]:
    try:
        position = store.close_manual_position(
            position_id, exit_price=payload.exit_price, closed_at=payload.closed_at
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Manual position not found") from exc
    return {"status": "closed", "position": position}


@app.delete("/api/manual-portfolio/{position_id}")
def delete_manual_position(position_id: int) -> dict[str, Any]:
    if not store.delete_manual_position(position_id):
        raise HTTPException(status_code=404, detail="Manual position not found")
    return {"status": "deleted", "position_id": position_id}


@app.get("/api/chart/{ticker}")
def chart(ticker: str) -> dict[str, Any]:
    normalized_ticker, _ = normalize_ticker(ticker)
    ticker_signals = store.list_all_signals(ticker=normalized_ticker)
    history = []
    for signal in reversed(ticker_signals):
        if signal["enrichment"].get("history"):
            history = signal["enrichment"]["history"]
            break
    markers = [
        {
            "id": signal["id"],
            "action": signal["action"],
            "price": signal["price"],
            "strategy": signal["strategy"],
            "source_time": signal["source_time"],
            "received_at": signal["received_at"],
        }
        for signal in ticker_signals
        if (signal["action"] or "").lower() in {"buy", "sell"}
    ]
    return {"ticker": normalized_ticker, "history": history, "markers": markers}


def enrich_signal(signal_id: int, ticker: str) -> None:
    enrichment = enricher.enrich(ticker)
    enrichment["refreshed_at"] = utc_now_iso()
    store.update_signal_enrichment(signal_id, enrichment)


async def price_refresh_loop() -> None:
    interval_seconds = settings.price_refresh_minutes * 60
    while True:
        try:
            if is_market_open(sessions=settings.market_sessions):
                await refresh_open_position_prices()
        except asyncio.CancelledError:
            raise
        except BaseException:
            logger.exception("Scheduled price refresh failed")
        await asyncio.sleep(interval_seconds)


async def refresh_open_position_prices() -> None:
    performance_data = build_performance(store.list_all_signals())
    open_trades = performance_data["open_trades"]
    signal_ids_by_ticker: dict[str, list[int]] = {}
    for trade in open_trades:
        signal_ids_by_ticker.setdefault(trade["ticker"], []).append(trade["entry_signal_id"])

    manual_tickers = set(store.list_open_manual_tickers())
    refresh_tickers = sorted(set(signal_ids_by_ticker) | manual_tickers)

    for ticker in refresh_tickers:
        try:
            enrichment = await asyncio.to_thread(enricher.enrich, ticker)
        except asyncio.CancelledError:
            raise
        except BaseException:
            logger.exception("Skipping scheduled price refresh for %s", ticker)
            continue
        enrichment["refreshed_by"] = "scheduled_price_refresh"
        enrichment["refreshed_at"] = utc_now_iso()
        for signal_id in signal_ids_by_ticker.get(ticker, []):
            store.update_signal_enrichment(signal_id, enrichment)
        if ticker in manual_tickers:
            price = latest_history_close(enrichment)
            if price is not None and price > 0:
                store.update_manual_market_price(
                    ticker=ticker,
                    price=price,
                    recorded_at=enrichment["refreshed_at"],
                )


async def refresh_manual_portfolio_prices() -> int:
    updated = 0
    for ticker in store.list_open_manual_tickers():
        updated += await asyncio.to_thread(refresh_manual_ticker_price, ticker)
    return updated


def refresh_manual_ticker_price(ticker: str) -> int:
    enrichment = enricher.enrich(ticker)
    price = latest_history_close(enrichment)
    if price is None or price <= 0:
        return 0
    return store.update_manual_market_price(
        ticker=ticker,
        price=price,
        recorded_at=utc_now_iso(),
    )


def latest_history_close(enrichment: dict[str, Any]) -> float | None:
    history = enrichment.get("history") or []
    if not history:
        return None
    latest_row = history[-1]
    value = (
        latest_row.get("close")
        or latest_row.get("Close")
        or latest_row.get("closePrice")
        or latest_row.get("c")
    )
    return coerce_float(value)
