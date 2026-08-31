from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Settings:
    database_path: Path
    admin_username: str
    admin_password: str
    admin_password_managed: bool
    session_days: int
    webhook_secret: str | None
    require_webhook_secret: bool
    backtest_upload_token: str | None


def _resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else PROJECT_ROOT / path


def get_settings() -> Settings:
    _load_env_file()
    production = bool(os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("ENVIRONMENT", "").lower() == "production")
    return Settings(
        database_path=_resolve_path(os.getenv("DATABASE_PATH", "data/backtests.db")),
        admin_username=os.getenv("ADMIN_USERNAME", "admin").strip() or "admin",
        admin_password=os.getenv("ADMIN_PASSWORD", "change-me"),
        admin_password_managed="ADMIN_PASSWORD" in os.environ,
        session_days=max(1, int(os.getenv("SESSION_DAYS", "30"))),
        webhook_secret=os.getenv("WEBHOOK_SECRET") or None,
        require_webhook_secret=_env_bool("REQUIRE_WEBHOOK_SECRET", default=production),
        backtest_upload_token=os.getenv("BACKTEST_UPLOAD_TOKEN") or None,
    )


def _load_env_file() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    load_dotenv(PROJECT_ROOT / ".env")


def _env_bool(name: str, *, default: bool) -> bool:
    value = os.getenv(name)
    return default if value is None else value.strip().lower() in {"1", "true", "yes", "on"}
