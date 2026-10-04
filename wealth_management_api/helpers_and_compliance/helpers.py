"""Small shared list operations. Nothing in here knows about FastAPI."""

from datetime import date, datetime
from typing import Any
from zoneinfo import ZoneInfo

import config


def find_one(records: list[dict[str, Any]], key: str, value: Any) -> dict | None:
    return next((r for r in records if r[key] == value), None)


def next_id(records: list[dict[str, Any]], key: str) -> int:
    return max((r[key] for r in records), default=0) + 1


def remove_where(records: list[dict[str, Any]], key: str, value: Any) -> None:
    """Remove matching rows in place, so every module importing this list sees the change."""
    records[:] = [r for r in records if r[key] != value]
    
def today() -> date:
    """Today's date in the firm's timezone, so 'stale' means the same thing on any server."""
    return datetime.now(tz=ZoneInfo(config.BUSINESS_TIMEZONE)).date()