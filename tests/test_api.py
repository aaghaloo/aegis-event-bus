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

import os

import paho.mqtt.publish as mqtt_publish
import pytest
from fastapi.testclient import TestClient


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


def test_auth_and_workflow(client: TestClient):
    """Test authentication and basic workflow."""
    # Login
    response = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": os.getenv("TEST_USER_PASSWORD", "TestPass123!"),
        },
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Test authenticated endpoint
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/jobs", headers=headers)
    assert response.status_code == 200
