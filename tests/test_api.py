# tests/test_api.py
"""
API integration tests (synchronous) for the Event Bus service.

Key policy:
-----------
All external side‑effects (MQTT publish) are mocked so the test
suite never opens network connections on CI (important for
GitHub Actions ToS compliance and speed).

We rely on fixtures from tests/conftest.py:
- client  : FastAPI TestClient
- session : SQLModel Session bound to the test DB
"""

import paho.mqtt.publish as mqtt_publish
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models import AuditLog


# ────────────────────────── GLOBAL MQTT MOCK ──────────────────────────
@pytest.fixture(autouse=True)
def _mock_mqtt(monkeypatch):
    """
    Auto‑applied fixture that replaces paho.mqtt.publish.single with a no‑op.

    This guarantees **zero network traffic** for every test, even if a
    future test forgets to monkeypatch explicitly.
    """
    monkeypatch.setattr(mqtt_publish, "single", lambda *a, **k: None)


# ───────────────────────────── TESTS ──────────────────────────────────
def test_read_root_endpoint(client: TestClient):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"status": "Aegis Event Bus is online"}


def test_unauthenticated_routes(client: TestClient):
    # POST /job without token
    assert client.post("/job").status_code == 401
    # GET /jobs without token
    assert client.get("/jobs").status_code == 401


def test_auth_and_workflow(client: TestClient, session: Session):
    # 1. Obtain JWT
    token = client.post(
        "/token", data={"username": "testuser", "password": "testpassword"}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create a job (MQTT publish is silently mocked)
    job_id = client.post("/job", headers=headers).json()["job_id"]

    # 3. Verify DB row
    db_row = session.exec(select(AuditLog).where(AuditLog.job_id == job_id)).one()
    assert db_row.action == "job.created"

    # 4. List jobs & confirm first returned matches
    jobs_page = client.get("/jobs", headers=headers).json()
    assert jobs_page["items"][0]["job_id"] == job_id
