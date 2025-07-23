# tests/test_hash_integrity.py
# Purpose: Directly hit Postgres and make sure the trigger fills sha256.
# Skips ONLY if DATABASE_URL is missing or points to sqlite.

import hashlib
import os
import uuid

import pytest
from sqlalchemy import text
from sqlmodel import create_engine


def _get_pg_dsn() -> str:
    return os.getenv("DATABASE_URL", "").strip()


@pytest.mark.integration
def test_audit_log_hash_trigger_direct():
    dsn = _get_pg_dsn()
    if not dsn or dsn.startswith("sqlite"):
        pytest.skip("Not running against Postgres (DATABASE_URL is sqlite or empty).")

    engine = create_engine(dsn)

    job_id = f"UT-{uuid.uuid4()}"
    action = "unit.test"

    with engine.begin() as conn:
        # insert row (trigger should set sha256)
        conn.execute(
            text("INSERT INTO audit_log (job_id, action) VALUES (:jid, :act)"),
            {"jid": job_id, "act": action},
        )
        sha = conn.execute(
            text("SELECT sha256 FROM audit_log WHERE job_id = :jid"),
            {"jid": job_id},
        ).scalar_one()

    expected = hashlib.sha256(job_id.encode()).hexdigest()
    assert sha == expected
    assert len(sha) == 64
