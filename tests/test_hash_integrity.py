# tests/test_hash_integrity.py
# Purpose: verify Postgres trigger fills sha256.
# Runs ONLY if we can connect to a real Postgres DSN.
# Falls back to skip when connection fails or DSN is sqlite.

import hashlib
import os
import uuid

import pytest
from sqlalchemy import text
from sqlmodel import create_engine


def _pick_dsn() -> str:
    """
    Prefer a dedicated var set in CI (PG_TRIGGER_TEST_DSN). Otherwise use DATABASE_URL.
    """
    return (os.getenv("PG_TRIGGER_TEST_DSN") or os.getenv("DATABASE_URL", "")).strip()


@pytest.mark.integration
def test_audit_log_hash_trigger_direct():
    dsn = _pick_dsn()

    # If still empty or sqlite -> skip
    if not dsn or dsn.startswith("sqlite"):
        pytest.skip(f"Skipping: DSN looks non-PG ({dsn or '<empty>'}).")

    # Try to connect; if fails, skip instead of erroring CI
    try:
        engine = create_engine(dsn)
        with engine.begin() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as exc:  # pragma: no cover
        pytest.skip(f"Cannot connect to Postgres DSN ({dsn}): {exc}")

    # Insert and verify trigger
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
