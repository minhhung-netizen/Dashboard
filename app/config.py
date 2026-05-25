from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Settings:
    database_path: Path
    webhook_secret: str | None = None
    price_refresh_minutes: int = 30
    market_sessions: str = "09:00-11:30,13:00-15:00"
    duplicate_window_minutes: int = 5


def _resolve_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return path


def get_settings() -> Settings:
    _load_env_file()
    database_path = _resolve_path(os.getenv("DATABASE_PATH", "data/signals.db"))
    secret = os.getenv("WEBHOOK_SECRET") or None
    refresh_minutes = int(os.getenv("PRICE_REFRESH_MINUTES", "30"))
    market_sessions = os.getenv("MARKET_SESSIONS", "09:00-11:30,13:00-15:00")
    duplicate_window_minutes = int(os.getenv("DUPLICATE_WINDOW_MINUTES", "5"))
    return Settings(
        database_path=database_path,
        webhook_secret=secret,
        price_refresh_minutes=max(1, refresh_minutes),
        market_sessions=market_sessions,
        duplicate_window_minutes=max(1, duplicate_window_minutes),
    )


def _load_env_file() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    load_dotenv(PROJECT_ROOT / ".env")
