import re
from typing import Annotated
from urllib.parse import unquote

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


def _validate_safe_string(v: str) -> str:
    """Validate string to prevent SQL injection and path traversal."""
    # Decode URL encoding to catch encoded attacks
    decoded = unquote(v)

    # Check for SQL injection patterns
    sql_patterns = [
        r"(\b(union|select|insert|update|delete|drop|create|alter|exec|execute)\b)",
        r"(--|#|/\*|\*/)",
        r"(\b(and|or)\b\s+\d+\s*[=<>])",
        r"(\bxp_|sp_)",
        r"(\bwaitfor\b)",
        r"(\b(union|select|insert|update|delete|drop|create|alter)\b\s+\w+)",
        r"(\b(and|or)\b\s+\w+\s*[=<>])",
        r"(\b(and|or)\b\s+\d+)",
        r"(\b(and|or)\b\s*[=<>])",
        r"(\bxp_cmdshell\b)",
        r"(\bsp_executesql\b)",
        r"(\b(union|select|insert|update|delete|drop|create|alter)\b\s*[;])",
        r"(\b(union|select|insert|update|delete|drop|create|alter)\b\s*[;]\s*\w+)",
        r"(\b(union|select|insert|update|delete|drop|create|alter)\b\s*[;]\s*\w+\s*[;])",
        r"(\bxp_\w+\b)",
        r"(\bsp_\w+\b)",
    ]

    for pattern in sql_patterns:
        if re.search(pattern, decoded, re.IGNORECASE):
            raise ValueError("potentially unsafe input detected")

    # Check for path traversal
    traversal_patterns = [
        r"\.\./",
        r"\.\.\\",
        r"\.\.%2f",
        r"\.\.%5c",
        r"\.\.%2e",
        r"\.\.%5e",
    ]

    for pattern in traversal_patterns:
        if re.search(pattern, decoded, re.IGNORECASE):
            raise ValueError("path traversal attempt detected")

    # Check for script injection
    script_patterns = [
        r"<script",
        r"javascript:",
        r"vbscript:",
        r"on\w+\s*=",
    ]

    for pattern in script_patterns:
        if re.search(pattern, decoded, re.IGNORECASE):
            raise ValueError("script injection attempt detected")

    return v


def _validate_agent_id(v: str) -> str:
    """Validate agent_id format and prevent injection."""
    if not re.fullmatch(r"[a-zA-Z0-9_-]{1,50}", v):
        raise ValueError("invalid agent_id format")
    return _validate_safe_string(v)


def _validate_task_id(v: str) -> str:
    """Validate task_id format and prevent injection."""
    if not re.fullmatch(r"[a-zA-Z0-9_-]{1,50}", v):
        raise ValueError("invalid task_id format")
    return _validate_safe_string(v)


def _validate_username(v: str) -> str:
    """Validate username format and prevent injection."""
    if not re.fullmatch(r"[a-zA-Z0-9_-]{3,30}", v):
        raise ValueError("invalid username format")
    return _validate_safe_string(v)


def _validate_json_payload(v: dict) -> dict:
    """Validate JSON payload size and content."""
    import json

    # Check payload size (max 1MB)
    payload_size = len(json.dumps(v))
    if payload_size > 1024 * 1024:
        raise ValueError("payload too large (max 1MB)")

    # Check for nested depth (max 10 levels)
    def check_depth(obj, depth=0):
        if depth > 10:
            raise ValueError("payload too deeply nested")
        if isinstance(obj, dict):
            for value in obj.values():
                check_depth(value, depth + 1)
        elif isinstance(obj, list):
            for item in obj:
                check_depth(item, depth + 1)

    check_depth(v)
    return v


# Type aliases for use in FastAPI
JobID = Annotated[str, AfterValidator(_validate_job_id)]
Cursor = Annotated[int | None, AfterValidator(_validate_cursor)]
Limit = Annotated[int, Field(default=20, ge=1, le=100)]
SafeString = Annotated[str, AfterValidator(_validate_safe_string)]
AgentID = Annotated[str, AfterValidator(_validate_agent_id)]
TaskID = Annotated[str, AfterValidator(_validate_task_id)]
Username = Annotated[str, AfterValidator(_validate_username)]
JSONPayload = Annotated[dict, AfterValidator(_validate_json_payload)]
