import re
from typing import Annotated

from pydantic import AfterValidator, Field


def _validate_job_id(v: str) -> str:
    """Validate job_id format and prevent path traversal."""
    if not re.fullmatch(r"FC-[0-9a-f-]{36}", v):
        raise ValueError("invalid job_id format")
    if ".." in v or "/" in v or "\\" in v:
        raise ValueError("path traversal chars in job_id")
    return v


def _validate_cursor(v: int | None) -> int | None:
    """Validate pagination cursor."""
    if v is not None and (v < 0 or v > 2**31):
        raise ValueError("invalid cursor value")
    return v


# Type aliases for use in FastAPI
JobID = Annotated[str, AfterValidator(_validate_job_id)]
Cursor = Annotated[int | None, AfterValidator(_validate_cursor)]
Limit = Annotated[int, Field(default=20, ge=1, le=100)]
