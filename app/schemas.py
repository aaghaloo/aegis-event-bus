# app/schemas.py
from typing import List, Optional

from pydantic import BaseModel

from .models import AuditLog


class Job(BaseModel):
    job_id: str


class Token(BaseModel):
    access_token: str
    token_type: str


class JobsPage(BaseModel):
    items: List[AuditLog]
    next_cursor: Optional[int] = None
