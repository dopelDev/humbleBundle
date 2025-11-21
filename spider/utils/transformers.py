from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Iterable, Optional


BASE_URL = 'https://www.humblebundle.com'


def normalize_text(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None


def serialize_list(value: Any) -> Optional[str]:
    if value in (None, '', []):
        return None
    if isinstance(value, str):
        return value
    try:
        return json.dumps(value, ensure_ascii=False)
    except (TypeError, ValueError):
        return str(value)


def absolute_url(value: Optional[str], base: str = BASE_URL) -> Optional[str]:
    if not value:
        return None
    if value.startswith('http://') or value.startswith('https://'):
        return value
    return f'{base.rstrip("/")}/{value.lstrip("/")}'


def safe_float(value: Any) -> Optional[float]:
    if value in (None, '', []):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def compute_duration_days(start: Optional[datetime], end: Optional[datetime]) -> Optional[float]:
    if not start or not end:
        return None
    delta = end - start
    return round(delta.total_seconds() / 86400, 3)


def compute_is_active(start: Optional[datetime], end: Optional[datetime], now: Optional[datetime] = None) -> bool:
    now = now or datetime.now(timezone.utc)
    if not start or not end:
        return False
    return start <= now <= end


def normalize_columns(frame, columns: Iterable[str]):
    for column in columns:
        if column in frame.columns:
            frame[column] = frame[column].apply(normalize_text)

