from __future__ import annotations

import asyncio
import csv
import hmac
import io
import logging
import os
from contextlib import asynccontextmanager
from datetime import date
from pathlib import Path
from typing import Any, Literal

import pandas as pd
from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field

from app.config import PROJECT_ROOT, get_settings
from app.database import BacktestStore
from app.services.auth import (
    SESSION_COOKIE,
    hash_password,
    hash_session_token,
    new_session,
    verify_password,
)
from app.services.backtesting import (
    BacktestConfig,
    download_vnstock_ohlcv,
    normalise_ohlcv,
    parse_symbols,
    run_backtest,
    strategy_catalog,
)


logger = logging.getLogger(__name__)
settings = get_settings()
store = BacktestStore(settings.database_path)
configured_admin = store.get_user_credentials(settings.admin_username)
if configured_admin is None:
    store.ensure_admin_user(
        username=settings.admin_username,
        password_hash=hash_password(settings.admin_password),
    )
elif settings.admin_password_managed and not verify_password(
    settings.admin_password, configured_admin["password_hash"]
):
    store.update_admin_password(configured_admin["id"], hash_password(settings.admin_password))


def database_is_persistent() -> bool:
    if not os.getenv("RAILWAY_ENVIRONMENT"):
        return True
    try:
        return settings.database_path.resolve().is_relative_to(Path("/data").resolve())
    except (OSError, ValueError):
        return False


@asynccontextmanager
async def lifespan(app: FastAPI):
    store.mark_interrupted_backtests()
    if settings.require_webhook_secret and not settings.webhook_secret:
        raise RuntimeError("WEBHOOK_SECRET is required in production")
    if os.getenv("RAILWAY_ENVIRONMENT") and not database_is_persistent():
        logger.warning(
            "SQLite is not under /data. Attach a Railway Volume at /data and set DATABASE_PATH=/data/backtests.db."
        )
    yield


app = FastAPI(title="VN Equity Backtest", version="1.0.0", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=PROJECT_ROOT / "app" / "static"), name="static")

_CSP = (
    "default-src 'self'; "
    "script-src 'self'; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src https://fonts.gstatic.com; "
    "img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("Referrer-Policy", "same-origin")
    response.headers.setdefault("Content-Security-Policy", _CSP)
    response.headers.setdefault("Strict-Transport-Security", "max-age=31536000")
    return response


@app.middleware("http")
async def require_login(request: Request, call_next):
    path = request.url.path
    public = {
        "/",
        "/health",
        "/api/auth/login",
        "/api/auth/me",
        "/api/auth/logout",
        "/webhook",
        "/api/backtests/import",
    }
    if path in public or path.startswith("/static/") or not path.startswith("/api/"):
        return await call_next(request)
    token = request.cookies.get(SESSION_COOKIE)
    user = store.get_session_user(hash_session_token(token)) if token else None
    if user is None:
        return JSONResponse({"detail": "Authentication required"}, status_code=401)
    request.state.user = user
    return await call_next(request)


class LoginPayload(BaseModel):
    username: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=1, max_length=256)


class BacktestRunPayload(BaseModel):
    symbols: str | list[str] = Field(..., examples=["FPT, VCB, TCB"])
    start_date: date = Field(..., examples=["2020-01-01"])
    end_date: date = Field(..., examples=["2025-12-31"])
    strategy: str = Field(default="ma_crossover", max_length=60)
    initial_cash: float = Field(default=1_000_000_000, gt=0)
    fast_window: int = Field(default=20, ge=1, le=500)
    slow_window: int = Field(default=100, ge=2, le=1000)
    rsi_window: int = Field(default=14, ge=2, le=200)
    rsi_entry: float = Field(default=30, gt=0, lt=100)
    rsi_exit: float = Field(default=55, gt=0, lt=100)
    breakout_window: int = Field(default=55, ge=2, le=1000)
    breakout_exit_window: int = Field(default=20, ge=2, le=1000)
    commission_rate: float = Field(default=0.0015, ge=0, le=0.1)
    sell_tax_rate: float = Field(default=0.001, ge=0, le=0.1)
    slippage_bps: float = Field(default=10, ge=0, le=1000)
    lot_size: int = Field(default=100, ge=1, le=100_000)
    max_participation_rate: float = Field(default=0.05, gt=0, le=1)
    rebalance_interval_days: int = Field(default=20, ge=1, le=252)


class SignalFilterPayload(BaseModel):
    allowed_tickers: str | list[str] = ""
    allowed_strategies: str | list[str] = ""
    allow_buy: bool = True
    allow_sell: bool = True


class SignalClassificationPayload(BaseModel):
    status: Literal["pending", "accepted", "excluded"]
    category: str = Field(default="watch", min_length=1, max_length=40)
    classification_note: str | None = Field(default=None, max_length=500)


class WebhookPayload(BaseModel):
    model_config = ConfigDict(extra="allow")

    ticker: str | dict[str, Any] | None = None
    action: str
    price: float | str | None = None
    timeframe: str | None = None
    strategy: str | None = None
    note: str | None = None
    time: str | None = None
    secret: str | None = None


class BacktestImportPayload(BaseModel):
    symbols: str | list[str]
    strategy: str = Field(min_length=1, max_length=80)
    start_date: date
    end_date: date
    config: dict[str, Any] = Field(default_factory=dict)
    metrics: dict[str, Any]
    equity_points: list[dict[str, Any]] = Field(default_factory=list)
    trades: list[dict[str, Any]] = Field(default_factory=list)
    set_standard: bool = False


@app.get("/", include_in_schema=False)
def dashboard() -> FileResponse:
    return FileResponse(PROJECT_ROOT / "app" / "static" / "index.html")


@app.get("/health")
def health() -> dict[str, Any]:
    status = store.database_status()
    return {
        "status": "ok",
        "database": "ok",
        "journal_mode": status["journal_mode"],
        "persistent_storage": database_is_persistent(),
    }


@app.get("/api/auth/me")
def auth_me(request: Request) -> dict[str, Any]:
    token = request.cookies.get(SESSION_COOKIE)
    user = store.get_session_user(hash_session_token(token)) if token else None
    return {"user": {"username": user["username"], "role": "admin"} if user else None}


@app.post("/api/auth/login")
def login(payload: LoginPayload) -> JSONResponse:
    user = store.get_user_credentials(payload.username)
    if user is None or not user["active"] or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token, token_hash, expires_at = new_session(settings.session_days)
    store.create_session(token_hash=token_hash, user_id=user["id"], expires_at=expires_at)
    response = JSONResponse({"user": {"username": user["username"], "role": "admin"}})
    response.set_cookie(
        SESSION_COOKIE,
        token,
        httponly=True,
        secure=bool(os.getenv("RAILWAY_ENVIRONMENT")),
        samesite="lax",
        max_age=settings.session_days * 86_400,
    )
    return response


@app.post("/api/auth/logout")
def logout(request: Request) -> JSONResponse:
    token = request.cookies.get(SESSION_COOKIE)
    if token:
        store.delete_session(hash_session_token(token))
    response = JSONResponse({"status": "logged_out"})
    response.delete_cookie(SESSION_COOKIE)
    return response


def _csv_values(value: str | list[str], *, upper: bool = False) -> list[str]:
    values = value.split(",") if isinstance(value, str) else value
    cleaned = [str(item).strip() for item in values if str(item).strip()]
    if upper:
        cleaned = [item.upper() for item in cleaned]
    return list(dict.fromkeys(cleaned))


def _normalise_webhook_ticker(value: str | dict[str, Any] | None) -> tuple[str, str | None]:
    if isinstance(value, dict):
        value = value.get("ticker") or value.get("symbol") or value.get("value")
    raw = str(value or "").strip().upper()
    if not raw:
        raise ValueError("ticker is required")
    exchange, separator, ticker = raw.partition(":")
    if not separator:
        ticker, exchange = exchange, None
    ticker = ticker.strip()
    if not ticker or len(ticker) > 20 or not ticker.replace("_", "").isalnum():
        raise ValueError("ticker is invalid")
    return ticker, exchange


def _normalise_action(value: str) -> str:
    action = "".join(char for char in value.lower() if char.isalnum())
    if action in {"buy", "long", "longstart", "entry", "enter"}:
        return "buy"
    if action in {"sell", "exit", "close", "closelong"}:
        return "sell"
    return "other"


def _automatic_signal_classification(
    *, ticker: str, action: str, strategy: str | None,
) -> tuple[str, str, str | None]:
    filters = store.get_signal_filter_settings()
    reasons: list[str] = []
    if action == "other":
        reasons.append("Only long-only BUY and SELL signals are accepted")
    if action == "buy" and not filters["allow_buy"]:
        reasons.append("BUY signals are disabled by the dashboard filter")
    if action == "sell" and not filters["allow_sell"]:
        reasons.append("SELL signals are disabled by the dashboard filter")
    if filters["allowed_tickers"] and ticker not in set(filters["allowed_tickers"]):
        reasons.append("Ticker is outside the dashboard allow list")
    normalized_strategy = (strategy or "").strip().lower()
    allowed_strategies = {item.lower() for item in filters["allowed_strategies"]}
    if allowed_strategies and normalized_strategy not in allowed_strategies:
        reasons.append("Strategy is outside the dashboard allow list")
    return ("excluded", "excluded", "; ".join(reasons)) if reasons else ("pending", "watch", None)


@app.post("/webhook")
def tradingview_webhook(payload: WebhookPayload, request: Request) -> dict[str, Any]:
    supplied_secret = (
        payload.secret
        or request.query_params.get("secret")
        or request.headers.get("X-Webhook-Secret")
    )
    if settings.webhook_secret:
        if not supplied_secret or not hmac.compare_digest(supplied_secret, settings.webhook_secret):
            raise HTTPException(status_code=401, detail="Invalid webhook secret")
    elif settings.require_webhook_secret:
        raise HTTPException(status_code=503, detail="Webhook secret is not configured")
    try:
        ticker, exchange = _normalise_webhook_ticker(payload.ticker)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    action = _normalise_action(payload.action)
    strategy = payload.strategy.strip() if payload.strategy else None
    status, category, reason = _automatic_signal_classification(
        ticker=ticker, action=action, strategy=strategy
    )
    raw_payload = payload.model_dump(mode="json")
    raw_payload.pop("secret", None)
    signal = store.create_signal(
        ticker=ticker,
        exchange=exchange,
        action=action,
        timeframe=payload.timeframe.strip() if payload.timeframe else None,
        strategy=strategy,
        note=payload.note.strip() if payload.note else None,
        source_time=payload.time,
        status=status,
        category=category,
        classification_note=None,
        rejection_reason=reason,
        payload=raw_payload,
    )
    return {"status": "stored", "signal": signal}


@app.get("/api/signal-filters")
def get_signal_filters() -> dict[str, Any]:
    return {"filters": store.get_signal_filter_settings()}


@app.put("/api/signal-filters")
def update_signal_filters(payload: SignalFilterPayload) -> dict[str, Any]:
    filters = store.update_signal_filter_settings(
        allowed_tickers=_csv_values(payload.allowed_tickers, upper=True),
        allowed_strategies=_csv_values(payload.allowed_strategies),
        allow_buy=payload.allow_buy,
        allow_sell=payload.allow_sell,
    )
    return {"filters": filters}


@app.get("/api/signals")
def list_signals(status: str | None = None, ticker: str | None = None) -> dict[str, Any]:
    if status and status not in {"pending", "accepted", "excluded"}:
        raise HTTPException(status_code=422, detail="Invalid signal status")
    standards = {item["strategy"]: item for item in store.list_backtest_standards()}
    signals = store.list_signals(status=status, ticker=ticker)
    for signal in signals:
        standard = standards.get(signal.get("strategy") or "")
        if standard:
            signal["backtest_standard"] = {
                "id": standard["id"],
                "total_return": (standard.get("metrics") or {}).get("total_return"),
                "max_drawdown": (standard.get("metrics") or {}).get("max_drawdown"),
            }
    return {"signals": signals, "summary": store.signal_summary()}


@app.patch("/api/signals/{signal_id}")
def classify_signal(signal_id: int, payload: SignalClassificationPayload) -> dict[str, Any]:
    try:
        signal = store.classify_signal(
            signal_id, status=payload.status, category=payload.category,
            classification_note=payload.classification_note,
        )
    except KeyError as error:
        raise HTTPException(status_code=404, detail="Signal not found") from error
    return {"signal": signal}


@app.delete("/api/signals/{signal_id}")
def delete_signal(signal_id: int) -> dict[str, Any]:
    if not store.delete_signal(signal_id):
        raise HTTPException(status_code=404, detail="Signal not found")
    return {"status": "deleted", "signal_id": signal_id}


def _build_backtest_config(payload: BacktestRunPayload) -> BacktestConfig:
    if payload.strategy not in {item["key"] for item in strategy_catalog()}:
        raise ValueError("Unknown long-only strategy")
    values = payload.model_dump(exclude={"symbols", "start_date", "end_date", "strategy"})
    return BacktestConfig(strategy_name=payload.strategy, **values)


def _backtest_cache_covers(bars: list[dict[str, Any]], start_date: str, end_date: str) -> bool:
    if len(bars) < 10:
        return False
    first = pd.Timestamp(str(bars[0]["date"])[:10])
    last = pd.Timestamp(str(bars[-1]["date"])[:10])
    return first <= pd.Timestamp(start_date) + pd.Timedelta(days=7) and last >= pd.Timestamp(end_date) - pd.Timedelta(days=7)


def _load_backtest_history(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    cached = store.list_backtest_price_bars(ticker=symbol, start_date=start_date, end_date=end_date)
    if _backtest_cache_covers(cached, start_date, end_date):
        return normalise_ohlcv(pd.DataFrame(cached), symbol)
    downloaded = download_vnstock_ohlcv(symbol, start_date, end_date)
    store.upsert_backtest_price_bars(ticker=symbol, bars=downloaded.to_dict("records"), provider="vnstock")
    return downloaded


def execute_backtest_run(run_id: int) -> None:
    try:
        store.mark_backtest_running(run_id)
        run = store.get_backtest_run(run_id)
        config = BacktestConfig(**run["config"])
        frames = {
            symbol: _load_backtest_history(symbol, run["start_date"], run["end_date"])
            for symbol in run["symbols"]
        }
        result = run_backtest(frames, config)
        store.complete_backtest_run(
            run_id,
            metrics=result.metrics,
            equity_points=result.equity_curve.to_dict("records"),
            trades=result.trades.to_dict("records"),
        )
    except BaseException as error:
        logger.exception("Backtest %s failed", run_id)
        store.fail_backtest_run(run_id, str(error) or type(error).__name__)


@app.get("/api/backtests/strategies")
def backtest_strategies() -> dict[str, Any]:
    return {
        "strategies": strategy_catalog(),
        "execution": "Close T signal, next open fill; BUY and SELL-to-close only.",
    }


@app.get("/api/backtests")
def list_backtests() -> dict[str, Any]:
    return {"backtests": store.list_backtest_runs()}


@app.get("/api/backtests/standards")
def list_backtest_standards() -> dict[str, Any]:
    return {"standards": store.list_backtest_standards()}


def _valid_upload_token(request: Request) -> bool:
    if not settings.backtest_upload_token:
        return False
    authorization = request.headers.get("Authorization", "")
    token = authorization.removeprefix("Bearer ").strip()
    return bool(token) and hmac.compare_digest(token, settings.backtest_upload_token)


@app.post("/api/backtests/import", status_code=201)
def import_local_backtest(payload: BacktestImportPayload, request: Request) -> dict[str, Any]:
    if not _valid_upload_token(request):
        raise HTTPException(status_code=401, detail="Invalid local backtest upload token")
    if payload.end_date <= payload.start_date:
        raise HTTPException(status_code=422, detail="End date must be after start date")
    try:
        symbols = parse_symbols(payload.symbols)
        run = store.create_backtest_run(
            created_by_user_id=None,
            symbols=symbols,
            strategy=payload.strategy.strip(),
            config=payload.config,
            start_date=payload.start_date.isoformat(),
            end_date=payload.end_date.isoformat(),
            data_source="local_import",
        )
        store.complete_backtest_run(
            run["id"], metrics=payload.metrics,
            equity_points=payload.equity_points, trades=payload.trades,
        )
        if payload.set_standard:
            store.set_backtest_standard(run["id"])
        saved = store.get_backtest_run(run["id"])
    except (KeyError, TypeError, ValueError) as error:
        raise HTTPException(status_code=422, detail=f"Invalid imported backtest: {error}") from error
    return {"status": "imported", "backtest": saved}


@app.post("/api/backtests", status_code=202)
def create_backtest(payload: BacktestRunPayload, request: Request, background_tasks: BackgroundTasks) -> dict[str, Any]:
    if payload.end_date <= payload.start_date:
        raise HTTPException(status_code=422, detail="End date must be after start date")
    try:
        symbols = parse_symbols(payload.symbols)
        config = _build_backtest_config(payload)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    run = store.create_backtest_run(
        created_by_user_id=request.state.user["id"],
        symbols=symbols,
        strategy=config.strategy_name,
        config=config.serialisable(),
        start_date=payload.start_date.isoformat(),
        end_date=payload.end_date.isoformat(),
    )
    background_tasks.add_task(execute_backtest_run, run["id"])
    return {"status": "queued", "backtest": run}


@app.post("/api/backtests/{run_id}/standard")
def set_backtest_standard(run_id: int) -> dict[str, Any]:
    try:
        run = store.set_backtest_standard(run_id)
    except KeyError as error:
        raise HTTPException(status_code=404, detail="Backtest not found") from error
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    return {"backtest": run}


@app.get("/api/backtests/{run_id}")
def get_backtest(run_id: int) -> dict[str, Any]:
    try:
        run = store.get_backtest_run(run_id)
    except KeyError as error:
        raise HTTPException(status_code=404, detail="Backtest not found") from error
    return {
        "backtest": run,
        "equity_curve": store.list_backtest_equity_points(run_id),
        "trades": store.list_backtest_trades(run_id),
    }


@app.get("/api/backtests/{run_id}/trades.csv")
def export_backtest_trades(run_id: int) -> Response:
    try:
        store.get_backtest_run(run_id)
    except KeyError as error:
        raise HTTPException(status_code=404, detail="Backtest not found") from error
    output = io.StringIO()
    rows = store.list_backtest_trades(run_id)
    writer = csv.DictWriter(output, fieldnames=["date", "symbol", "side", "quantity", "fill_price", "notional", "costs"])
    writer.writeheader()
    writer.writerows(rows)
    return Response(
        output.getvalue(), media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=backtest-{run_id}-trades.csv"},
    )


@app.delete("/api/backtests/{run_id}")
def delete_backtest(run_id: int) -> dict[str, Any]:
    if not store.delete_backtest_run(run_id):
        raise HTTPException(status_code=404, detail="Backtest not found")
    return {"status": "deleted", "backtest_id": run_id}
