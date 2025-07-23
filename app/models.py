# app/models.py

import datetime as dt
from typing import Optional

from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel


class AuditLog(SQLModel, table=True):
    """
    Core immutable event log for A0.

    sha256 is a tamper‑evident hash (computed in DB trigger) of job_id.
    """

    __tablename__ = "audit_log"

    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: str = Field(index=True)
    action: str
    # Keep timezone‑aware timestamps (your existing style)
    timestamp: dt.datetime = Field(
        default_factory=lambda: dt.datetime.now(dt.UTC),
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    # NEW integrity column (filled ONLY by DB trigger)
    sha256: Optional[str] = Field(
        default=None, description="Integrity hash of job_id (sha256)"
    )
