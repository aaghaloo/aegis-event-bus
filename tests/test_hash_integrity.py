# tests/test_hash_integrity.py
# Purpose: verify the Postgres trigger fills sha256. Skips on SQLite (CI default).

import hashlib
import os
import uuid
from pathlib import Path

import pytest
from sqlalchemy import text
from sqlmodel import create_engine


def _get_pg_dsn() -> str:
    # 1) env, 2) .env.local fallback, else sqlite://
    dsn = os.getenv("DATABASE_URL", "")
    if not dsn and Path(".env.local").exists():
        for line in Path(".env.local").read_text().splitlines():
            if line.startswith("DATABASE_URL="):
                dsn = line.split("=", 1)[1].strip().strip('"')
                break
    return dsn or "sqlite://"


@pytest.mark.integration
def test_audit_log_hash_trigger_direct():
    """Insert into audit_log and confirm sha256 is filled by trigger."""
    dsn = _get_pg_dsn()
    if not dsn.startswith("postgresql"):
        pytest.skip("CI uses SQLite; skipping trigger test.")

    engine = create_engine(dsn)

    job_id = f"UT-{uuid.uuid4()}"
    action = "unit.test"

    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO audit_log (job_id, action) VALUES (:job_id, :action)"),
            {"job_id": job_id, "action": action},
        )
        row = conn.execute(
            text(
                "SELECT job_id, sha256 FROM audit_log "
                "WHERE job_id = :job_id ORDER BY id DESC LIMIT 1"
            ),
            {"job_id": job_id},
        ).one()

    expected = hashlib.sha256(job_id.encode()).hexdigest()
    assert row.sha256 == expected
    assert len(row.sha256) == 64
