from __future__ import annotations

import json
import os
import sys
import threading
import time
import base64
import hashlib
import hmac
from copy import deepcopy
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from datetime import date, datetime, timedelta, timezone
from importlib import import_module
from io import StringIO
from typing import Any
from urllib import error as urllib_error
from urllib import parse as urllib_parse
from urllib import request as urllib_request
from uuid import uuid4

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


def normalize_stock_price(value: Any) -> float | None:
    price = coerce_float(value)
    if price is None:
        return None
    return price / 1000 if abs(price) >= 1000 else price


def normalize_action(raw_action: str | None) -> str:
    if not raw_action:
        raise ValueError("action is required")
    action = raw_action.strip().lower()
    compact_action = "".join(ch for ch in action if ch.isalnum())
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
        "confirmationbuy": "confirm_buy",
        "confimbuy": "confirm_buy",
        "confibuy": "confirm_buy",
        "confirmsell": "confirm_sell",
        "confirm-sell": "confirm_sell",
        "confirmation_sell": "confirm_sell",
        "confirmationsell": "confirm_sell",
        "confimsell": "confirm_sell",
        "confisell": "confirm_sell",
    }
    return aliases.get(action, aliases.get(compact_action, action))


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

    def enrich(self, ticker: str, *, force: bool = False) -> dict[str, Any]:
        if not force:
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


class DnseEnricher:
    """DNSE REST market-data adapter using DNSE's documented HMAC signing."""

    def __init__(
        self,
        *,
        api_key: str,
        api_secret: str,
        base_url: str = "https://openapi.dnse.com.vn",
        api_version: str = "2026-05-07",
        lookback_days: int = 90,
        cache_ttl_seconds: int = 240 * 60,
        min_request_interval_seconds: float = 1.0,
        client: Any = None,
    ) -> None:
        self.lookback_days = lookback_days
        self.cache_ttl_seconds = cache_ttl_seconds
        self.min_request_interval_seconds = min_request_interval_seconds
        self._cache: dict[str, tuple[float, dict[str, Any]]] = {}
        self._lock = threading.Lock()
        self._last_request_at = 0.0
        self.client = client or DnseRestClient(
            api_key=api_key,
            api_secret=api_secret,
            base_url=base_url,
            api_version=api_version,
        )

    def enrich(self, ticker: str, *, force: bool = False) -> dict[str, Any]:
        if not force:
            cached = self._get_cached(ticker)
            if cached is not None:
                return cached
        try:
            enrichment = self._enrich_with_dnse(ticker)
        except BaseException as exc:
            enrichment = {
                "status": "unavailable",
                "source": "dnse",
                "message": str(exc),
                "ticker": ticker,
                "history": [],
                "metrics": {},
            }
        self._set_cached(ticker, enrichment)
        return deepcopy(enrichment)

    def _enrich_with_dnse(self, ticker: str) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        start = now - timedelta(days=self.lookback_days)
        self._wait_for_rate_limit()
        ohlc_status, ohlc_body = self.client.get_ohlc(
            bar_type="STOCK",
            query={
                "symbol": ticker.upper(),
                "resolution": "1D",
                "from": int(start.timestamp()),
                "to": int(now.timestamp()),
            },
            dry_run=False,
        )
        history = _normalize_dnse_stock_history(
            _dnse_ohlc_records(_dnse_response(ohlc_status, ohlc_body))
        )

        self._wait_for_rate_limit()
        trade_status, trade_body = self.client.get_latest_trade(
            symbol=ticker.upper(),
            dry_run=False,
        )
        latest_trade = _dnse_response(trade_status, trade_body)
        latest_price = _find_number(
            latest_trade,
            ("price", "matchPrice", "lastPrice", "close", "last"),
        )
        latest_price = normalize_stock_price(latest_price)
        if latest_price is not None and latest_price > 0:
            if history:
                history[-1]["close"] = latest_price
            else:
                history = [{"time": now.isoformat(), "close": latest_price}]

        if not history:
            raise RuntimeError("DNSE returned no market price history")
        return {
            "status": "ok",
            "source": "dnse",
            "ticker": ticker,
            "history": history[-80:],
            "metrics": {},
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


class MarketDataEnricher:
    """Use DNSE first and transparently fall back to VNStock."""

    def __init__(
        self,
        *,
        dnse: DnseEnricher | None,
        vnstock: VnstockEnricher,
    ) -> None:
        self.dnse = dnse
        self.vnstock = vnstock

    def enrich(self, ticker: str, *, force: bool = False) -> dict[str, Any]:
        if self.dnse is not None:
            primary = self.dnse.enrich(ticker, force=force)
            if primary.get("status") == "ok" and primary.get("history"):
                return primary
            fallback = self.vnstock.enrich(ticker, force=force)
            fallback["fallback_from"] = "dnse"
            fallback["dnse_message"] = primary.get("message")
            fallback.setdefault("source", "vnstock")
            return fallback
        result = self.vnstock.enrich(ticker, force=force)
        result.setdefault("source", "vnstock")
        return result


class DnseRestClient:
    def __init__(
        self,
        *,
        api_key: str,
        api_secret: str,
        base_url: str,
        api_version: str,
        timeout_seconds: float = 20,
    ) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url.rstrip("/")
        self.api_version = api_version
        self.timeout_seconds = timeout_seconds

    def get_ohlc(self, *, bar_type: str, query: dict[str, Any], dry_run: bool = False):
        request_query = dict(query)
        request_query["type"] = bar_type
        return self._request("GET", "/price/ohlc", query=request_query, dry_run=dry_run)

    def get_latest_trade(self, *, symbol: str, dry_run: bool = False):
        return self._request("GET", f"/price/{symbol}/trades/latest", dry_run=dry_run)

    def _request(
        self,
        method: str,
        path: str,
        *,
        query: dict[str, Any] | None = None,
        dry_run: bool = False,
    ) -> tuple[int | None, str | None]:
        url = f"{self.base_url}{path}"
        if query:
            url += f"?{urllib_parse.urlencode(query)}"
        headers = self._signed_headers(method, path)
        if dry_run:
            return None, None
        req = urllib_request.Request(url, method=method, headers=headers)
        try:
            with urllib_request.urlopen(req, timeout=self.timeout_seconds) as response:
                return response.status, response.read().decode("utf-8")
        except urllib_error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
            return exc.code, body

    def _signed_headers(self, method: str, path: str) -> dict[str, str]:
        date_value = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S %z")
        nonce = uuid4().hex
        signing_string = (
            f"(request-target): {method.lower()} {path}\n"
            f"date: {date_value}\n"
            f"nonce: {nonce}"
        )
        digest = hmac.new(
            self.api_secret.encode("utf-8"),
            signing_string.encode("utf-8"),
            hashlib.sha256,
        ).digest()
        signature = urllib_parse.quote(base64.b64encode(digest).decode("utf-8"), safe="")
        signature_header = (
            f'Signature keyId="{self.api_key}",algorithm="hmac-sha256",'
            f'headers="(request-target) date",signature="{signature}",nonce="{nonce}"'
        )
        return {
            "Date": date_value,
            "X-Signature": signature_header,
            "x-api-key": self.api_key,
            "version": self.api_version,
        }


def _dnse_response(status: Any, body: Any) -> Any:
    try:
        status_code = int(status)
    except (TypeError, ValueError):
        status_code = 0
    if not 200 <= status_code < 300:
        raise RuntimeError(f"DNSE request failed with status {status}: {body}")
    if isinstance(body, (dict, list)):
        return body
    if not body:
        return {}
    try:
        return json.loads(body)
    except (TypeError, json.JSONDecodeError) as exc:
        raise RuntimeError("DNSE returned invalid JSON") from exc


def _dnse_ohlc_records(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict) and isinstance(payload.get("data"), (dict, list)):
        payload = payload["data"]
    if isinstance(payload, list):
        records = [_normalize_dnse_ohlc_row(row) for row in payload if isinstance(row, dict)]
        return [row for row in records if row.get("close") is not None]
    if not isinstance(payload, dict):
        return []

    times = payload.get("t") or payload.get("time") or payload.get("times") or []
    opens = payload.get("o") or payload.get("open") or []
    highs = payload.get("h") or payload.get("high") or []
    lows = payload.get("l") or payload.get("low") or []
    closes = payload.get("c") or payload.get("close") or []
    volumes = payload.get("v") or payload.get("volume") or []
    if not isinstance(closes, list):
        return [_normalize_dnse_ohlc_row(payload)]
    records = []
    for index, close in enumerate(closes):
        records.append(
            {
                "time": _sequence_value(times, index),
                "open": _sequence_value(opens, index),
                "high": _sequence_value(highs, index),
                "low": _sequence_value(lows, index),
                "close": close,
                "volume": _sequence_value(volumes, index),
            }
        )
    return records


def _normalize_dnse_stock_history(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized = []
    for row in records:
        cleaned = dict(row)
        cleaned["time"] = _normalize_dnse_time(cleaned.get("time"))
        for field in ("open", "high", "low", "close"):
            cleaned[field] = normalize_stock_price(cleaned.get(field))
        normalized.append(cleaned)
    return normalized


def _normalize_dnse_time(value: Any) -> Any:
    numeric = coerce_float(value)
    if numeric is None:
        return value
    timestamp = numeric / 1000 if numeric >= 1_000_000_000_000 else numeric
    try:
        return datetime.fromtimestamp(timestamp, timezone.utc).isoformat()
    except (OSError, OverflowError, ValueError):
        return value


def _normalize_dnse_ohlc_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "time": row.get("time") or row.get("t") or row.get("timestamp"),
        "open": row.get("open") if row.get("open") is not None else row.get("o"),
        "high": row.get("high") if row.get("high") is not None else row.get("h"),
        "low": row.get("low") if row.get("low") is not None else row.get("l"),
        "close": row.get("close") if row.get("close") is not None else row.get("c"),
        "volume": row.get("volume") if row.get("volume") is not None else row.get("v"),
    }


def _sequence_value(value: Any, index: int) -> Any:
    return value[index] if isinstance(value, list) and index < len(value) else None


def _find_number(payload: Any, keys: tuple[str, ...]) -> float | None:
    if isinstance(payload, dict):
        for key in keys:
            value = coerce_float(payload.get(key))
            if value is not None:
                return value
        for value in payload.values():
            found = _find_number(value, keys)
            if found is not None:
                return found
    elif isinstance(payload, list):
        for value in payload:
            found = _find_number(value, keys)
            if found is not None:
                return found
    return None


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
