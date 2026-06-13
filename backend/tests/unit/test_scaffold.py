"""Smoke tests verifying the FastAPI scaffold is wired correctly."""

from fastapi.testclient import TestClient


def test_health_no_auth(client: TestClient) -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_openapi_docs_loads(client: TestClient) -> None:
    resp = client.get("/docs")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]


def test_openapi_schema_loads(client: TestClient) -> None:
    resp = client.get("/openapi.json")
    assert resp.status_code == 200
    schema = resp.json()
    assert schema["info"]["title"] == "OddToBelieve"


def test_odds_events_requires_auth(client: TestClient) -> None:
    resp = client.get("/odds/events")
    assert resp.status_code == 401


def test_odds_events_with_valid_token(client: TestClient, auth_headers: dict) -> None:
    resp = client.get("/odds/events", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_odds_event_not_found(client: TestClient, auth_headers: dict) -> None:
    resp = client.get("/odds/events/9999", headers=auth_headers)
    assert resp.status_code == 404


def test_odds_markets_not_found(client: TestClient, auth_headers: dict) -> None:
    resp = client.get("/odds/events/9999/markets", headers=auth_headers)
    assert resp.status_code == 404


def test_auth_token_wrong_password(client: TestClient) -> None:
    resp = client.post("/auth/token", data={"username": "admin", "password": "wrong"})
    assert resp.status_code == 401


def test_auth_token_valid(client: TestClient) -> None:
    resp = client.post(
        "/auth/token", data={"username": "admin", "password": "changeme"}
    )
    assert resp.status_code == 200
    body = resp.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"
