from __future__ import annotations

import json
import os
import sys
import threading
import time
from copy import deepcopy
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from datetime import date, timedelta
from importlib import import_module
from io import StringIO
from typing import Any

from app.config import PROJECT_ROOT


EXCHANGE_PREFIXES = {"HOSE", "HNX", "UPCOM", "VNINDEX", "INDEX"}


def normalize_ticker(raw_ticker: Any) -> tuple[str, str | None]:
    if not raw_ticker:
        raise ValueError("ticker is required")

    value = _ticker_value(raw_ticker).strip().upper()
    exchange: str | None = None

    if ":" in value:
        prefix, symbol = value.split(":", 1)
        if prefix in EXCHANGE_PREFIXES and symbol:
            exchange = prefix
            value = symbol

    value = value.replace(" ", "")
    if not value:
        raise ValueError("ticker is required")
    return value, exchange


def _ticker_value(raw_ticker: Any) -> str:
    if isinstance(raw_ticker, dict):
        for key in ("symbol", "ticker", "tickerid"):
            value = raw_ticker.get(key)
            if value:
                return str(value)
        raise ValueError("ticker is required")

    value = str(raw_ticker).strip()
    if value.startswith("="):
        value = value[1:].strip()
    if value.startswith("{"):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return value
        if isinstance(parsed, dict):
            return _ticker_value(parsed)
    return value


def coerce_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(str(value).replace(",", ""))
    except ValueError:
        return None


def normalize_action(raw_action: str | None) -> str:
    if not raw_action:
        raise ValueError("action is required")
    action = raw_action.strip().lower()
    aliases = {
        "long": "buy",
        "entry": "buy",
        "open": "buy",
        "short": "sell",
        "exit": "sell",
        "close": "sell",
        "confirmbuy": "confirm_buy",
        "confirm-buy": "confirm_buy",
        "confirmation_buy": "confirm_buy",
        "confirmsell": "confirm_sell",
        "confirm-sell": "confirm_sell",
        "confirmation_sell": "confirm_sell",
    }
    return aliases.get(action, action)


class VnstockEnricher:
    """Small adapter around vnstock with graceful fallback when APIs differ."""

    def __init__(
        self,
        lookback_days: int = 90,
        *,
        cache_ttl_seconds: int = 240 * 60,
        min_request_interval_seconds: float = 4.0,
        include_metrics: bool = False,
    ) -> None:
        self.lookback_days = lookback_days
        self.cache_ttl_seconds = cache_ttl_seconds
        self.min_request_interval_seconds = min_request_interval_seconds
        self.include_metrics = include_metrics
        self._cache: dict[str, tuple[float, dict[str, Any]]] = {}
        self._lock = threading.Lock()
        self._last_request_at = 0.0

    def enrich(self, ticker: str) -> dict[str, Any]:
        cached = self._get_cached(ticker)
        if cached is not None:
            return cached
        try:
            enrichment = self._enrich_with_vnstock(ticker)
        except BaseException as exc:  # vnstock may raise non-Exception exits internally.
            enrichment = {
                "status": "unavailable",
                "message": str(exc),
                "ticker": ticker,
                "history": [],
                "metrics": {},
            }
        self._set_cached(ticker, enrichment)
        return deepcopy(enrichment)

    def _enrich_with_vnstock(self, ticker: str) -> dict[str, Any]:
        vnstock_home = PROJECT_ROOT / "data" / "vnstock-home"
        vnstock_home.mkdir(parents=True, exist_ok=True)
        os.environ["HOME"] = str(vnstock_home)
        os.environ["USERPROFILE"] = str(vnstock_home)
        for stream in (sys.stdout, sys.stderr):
            if hasattr(stream, "reconfigure"):
                stream.reconfigure(encoding="utf-8", errors="replace")

        with quiet_output():
            module = __import__("vnstock")
            end = date.today()
            start = end - timedelta(days=self.lookback_days)
            self._wait_for_rate_limit()
            history = self._get_history(module, ticker, start.isoformat(), end.isoformat())
            metrics = {}
            if self.include_metrics:
                self._wait_for_rate_limit()
                metrics = self._get_metrics(module, ticker)

        return {
            "status": "ok",
            "ticker": ticker,
            "history": history[-80:],
            "metrics": metrics,
        }

    def _get_cached(self, ticker: str) -> dict[str, Any] | None:
        now = time.monotonic()
        with self._lock:
            cached = self._cache.get(ticker)
            if not cached:
                return None
            cached_at, enrichment = cached
            if now - cached_at > self.cache_ttl_seconds:
                self._cache.pop(ticker, None)
                return None
            return deepcopy(enrichment)

    def _set_cached(self, ticker: str, enrichment: dict[str, Any]) -> None:
        with self._lock:
            self._cache[ticker] = (time.monotonic(), deepcopy(enrichment))

    def _wait_for_rate_limit(self) -> None:
        if self.min_request_interval_seconds <= 0:
            return
        with self._lock:
            now = time.monotonic()
            wait_seconds = self.min_request_interval_seconds - (now - self._last_request_at)
            if wait_seconds > 0:
                time.sleep(wait_seconds)
                now = time.monotonic()
            self._last_request_at = now

    def _get_history(
        self, module: Any, ticker: str, start: str, end: str
    ) -> list[dict[str, Any]]:
        try:
            quote_module = import_module("vnstock.api.quote")
            quote_class = getattr(quote_module, "Quote")
            for source in ("VCI", "KBS"):
                try:
                    quote = quote_class(symbol=ticker, source=source, show_log=False)
                    data = quote.history(start=start, end=end, interval="1D")
                    records = _records_from_dataframe_like(data)
                    if records:
                        return records
                except Exception:
                    continue
        except Exception:
            pass

        if hasattr(module, "stock_historical_data"):
            data = module.stock_historical_data(
                symbol=ticker,
                start_date=start,
                end_date=end,
                resolution="1D",
                type="stock",
            )
            return _records_from_dataframe_like(data)

        if hasattr(module, "Vnstock"):
            stock = module.Vnstock().stock(symbol=ticker, source="VCI")
            data = stock.quote.history(start=start, end=end, interval="1D")
            return _records_from_dataframe_like(data)

        raise RuntimeError("No supported vnstock history API was found")

    def _get_metrics(self, module: Any, ticker: str) -> dict[str, Any]:
        try:
            finance_module = import_module("vnstock.api.financial")
            finance_class = getattr(finance_module, "Finance")
            finance = finance_class(symbol=ticker, source="VCI", period="year", show_log=False)
            ratio = finance.ratio(period="year", lang="en", dropna=True)
            records = _records_from_dataframe_like(ratio)
            return records[-1] if records else {}
        except BaseException:
            pass

        try:
            if hasattr(module, "stock_intraday_data"):
                return {}
            if hasattr(module, "Vnstock"):
                stock = module.Vnstock().stock(symbol=ticker, source="VCI")
                ratio = stock.finance.ratio(period="year", lang="en", dropna=True)
                records = _records_from_dataframe_like(ratio)
                return records[-1] if records else {}
        except BaseException:
            return {}
        return {}


@contextmanager
def quiet_output() -> Any:
    sink = StringIO()
    with redirect_stdout(sink), redirect_stderr(sink):
        yield


def _records_from_dataframe_like(value: Any) -> list[dict[str, Any]]:
    if value is None:
        return []
    if hasattr(value, "to_dict"):
        records = value.to_dict(orient="records")
    elif isinstance(value, list):
        records = value
    else:
        return []
    return [_json_ready(row) for row in records]


def _json_ready(row: dict[str, Any]) -> dict[str, Any]:
    cleaned: dict[str, Any] = {}
    for key, value in row.items():
        if hasattr(value, "isoformat"):
            cleaned[str(key)] = value.isoformat()
        elif value != value:
            cleaned[str(key)] = None
        else:
            cleaned[str(key)] = value
    return cleaned
