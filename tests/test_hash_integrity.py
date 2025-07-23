# tests/test_hash_integrity.py
# Purpose: Prove the Postgres trigger sets sha256. Only skip if we truly have no PG DSN.

import hashlib
import os
import uuid

import pytest
from sqlalchemy import text
from sqlmodel import create_engine


def _pick_dsn() -> str:
    """
    Prefer PG_TRIGGER_TEST_DSN (so CI can override),
    else DATABASE_URL. Return '' if nothing.
    """
    return (os.getenv("PG_TRIGGER_TEST_DSN") or os.getenv("DATABASE_URL") or "").strip()


@pytest.mark.integration
def test_audit_log_hash_trigger_direct():
    dsn = _pick_dsn()

    # Skip ONLY if we genuinely don't have a Postgres DSN
    if not dsn or dsn.startswith("sqlite"):
        pytest.skip("No Postgres DSN available; skipping trigger test.")

    engine = create_engine(dsn)

    job_id = f"UT-{uuid.uuid4()}"
    action = "unit.test"

    with engine.begin() as conn:
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
