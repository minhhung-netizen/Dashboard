from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Settings:
    database_path: Path
    webhook_secret: str | None = None
    price_refresh_minutes: int = 120
    market_sessions: str = "09:00-11:30,13:00-15:00"
    duplicate_window_minutes: int = 5
    vnstock_cache_ttl_minutes: int = 240
    vnstock_min_request_interval_seconds: float = 4.0
    vnstock_lookback_days: int = 90
    vnstock_include_metrics: bool = False
    default_signal_weight_pct: float = 5.0


def _resolve_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path


def get_settings() -> Settings:
    _load_env_file()
    database_path = _resolve_path(os.getenv("DATABASE_PATH", "data/signals.db"))
    secret = os.getenv("WEBHOOK_SECRET") or None
    refresh_minutes = int(os.getenv("PRICE_REFRESH_MINUTES", "120"))
    market_sessions = os.getenv("MARKET_SESSIONS", "09:00-11:30,13:00-15:00")
    duplicate_window_minutes = int(os.getenv("DUPLICATE_WINDOW_MINUTES", "5"))
    vnstock_cache_ttl_minutes = int(os.getenv("VNSTOCK_CACHE_TTL_MINUTES", "240"))
    vnstock_min_request_interval_seconds = float(
        os.getenv("VNSTOCK_MIN_REQUEST_INTERVAL_SECONDS", "4")
    )
    vnstock_lookback_days = int(os.getenv("VNSTOCK_LOOKBACK_DAYS", "90"))
    vnstock_include_metrics = _env_bool("VNSTOCK_INCLUDE_METRICS", default=False)
    default_signal_weight_pct = float(os.getenv("DEFAULT_SIGNAL_WEIGHT_PCT", "5"))
    return Settings(
        database_path=database_path,
        webhook_secret=secret,
        price_refresh_minutes=max(1, refresh_minutes),
        market_sessions=market_sessions,
        duplicate_window_minutes=max(1, duplicate_window_minutes),
        vnstock_cache_ttl_minutes=max(1, vnstock_cache_ttl_minutes),
        vnstock_min_request_interval_seconds=max(0.0, vnstock_min_request_interval_seconds),
        vnstock_lookback_days=max(30, vnstock_lookback_days),
        vnstock_include_metrics=vnstock_include_metrics,
        default_signal_weight_pct=max(0.01, default_signal_weight_pct),
    )


def _load_env_file() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    load_dotenv(PROJECT_ROOT / ".env")


def _env_bool(name: str, *, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}
