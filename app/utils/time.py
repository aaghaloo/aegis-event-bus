# app/utils/time.py
# Purpose: single place to get a timezone-aware UTC "now" for the whole project.

from datetime import datetime, timezone


def utcnow() -> datetime:
    """Return timezone-aware UTC datetime (no deprecation warnings)."""
    return datetime.now(timezone.utc)
