"""Unit tests for GET /health (STORY-10)."""

from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError


def test_health_returns_200(client: TestClient) -> None:
    resp = client.get("/health")
    assert resp.status_code == 200


def test_health_content_type_json(client: TestClient) -> None:
    resp = client.get("/health")
    assert "application/json" in resp.headers["content-type"]


def test_health_no_auth_required(client: TestClient) -> None:
    """Endpoint must not require JWT auth — no Authorization header sent."""
    resp = client.get("/health")
    assert resp.status_code == 200


def test_health_status_ok_when_db_up(client: TestClient) -> None:
    resp = client.get("/health")
    body = resp.json()
    assert body["status"] == "ok"
    assert body["db"] == "ok"


def test_health_db_error_still_returns_200(client: TestClient) -> None:
    """DB error must not change HTTP status — always 200."""
    from app.dependencies import get_db
    from app.main import app

    def broken_db():
        db = MagicMock()
        db.execute.side_effect = OperationalError("SELECT 1", {}, Exception("gone"))
        yield db

    app.dependency_overrides[get_db] = broken_db
    try:
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok", "db": "error"}
    finally:
        # Restore the test DB override from conftest
        from tests.conftest import _override_get_db

        app.dependency_overrides[get_db] = _override_get_db
