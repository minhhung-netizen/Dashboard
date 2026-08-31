from __future__ import annotations

from datetime import datetime, time
from zoneinfo import ZoneInfo


MARKET_TZ = ZoneInfo("Asia/Ho_Chi_Minh")


def is_market_open(
    now: datetime | None = None,
    sessions: str = "09:00-11:30,13:00-15:00",
) -> bool:
    current = now or datetime.now(MARKET_TZ)
    if current.tzinfo is None:
        current = current.replace(tzinfo=MARKET_TZ)
    else:
        current = current.astimezone(MARKET_TZ)

    if current.weekday() >= 5:
        return False

    current_time = current.time()
    return any(
        start <= current_time <= end for start, end in parse_market_sessions(sessions)
    )


def parse_market_sessions(sessions: str) -> list[tuple[time, time]]:
    parsed = []
    for raw_session in sessions.split(","):
        raw_session = raw_session.strip()
        if not raw_session:
            continue
        start_raw, end_raw = raw_session.split("-", 1)
        parsed.append((_parse_time(start_raw), _parse_time(end_raw)))
    return parsed


def _parse_time(value: str) -> time:
    hour, minute = value.strip().split(":", 1)
    return time(hour=int(hour), minute=int(minute))
