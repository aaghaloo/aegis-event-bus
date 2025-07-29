# app/schemas.py
from typing import List, Optional

from pydantic import BaseModel, field_validator

from .models import AuditLog
from .validators import _validate_job_id


class Job(BaseModel):
    job_id: str

    @field_validator("job_id")
    @classmethod
    def validate_job_id(cls, v: str) -> str:
        return _validate_job_id(v)


class Token(BaseModel):
    access_token: str
    token_type: str


class JobsPage(BaseModel):
    items: List[AuditLog]
    next_cursor: Optional[int] = None
