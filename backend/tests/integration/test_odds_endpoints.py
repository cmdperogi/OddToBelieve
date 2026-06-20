"""Integration tests for /odds/* endpoints (STORY-4)."""

from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from app.db import models as db_models


@pytest.fixture
def seeded_event(db_session):
    event = db_models.Event(
        source_id="betfair-001",
        source="betfair",
        sport="soccer",
        name="Arsenal vs Chelsea",
        start_time=datetime(2026, 7, 1, 15, 0, 0),
    )
    db_session.add(event)
    db_session.flush()

    market = db_models.Market(event_id=event.id, market_type="match_winner")
    db_session.add(market)
    db_session.flush()

    odds = db_models.Odds(
        market_id=market.id,
        bookmaker="betfair",
        selection="Arsenal",
        value=2.5,
        fetched_at=datetime(2026, 7, 1, 12, 0, 0),
    )
    db_session.add(odds)
    db_session.commit()
    db_session.refresh(event)
    return event


# ---------------------------------------------------------------------------
# GET /odds/events — happy path + 401
# ---------------------------------------------------------------------------


def test_list_events_requires_auth(client: TestClient) -> None:
    resp = client.get("/odds/events")
    assert resp.status_code == 401


def test_list_events_returns_empty_list(client: TestClient, auth_headers: dict) -> None:
    resp = client.get("/odds/events", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_events_returns_seeded_event(
    client: TestClient, auth_headers: dict, seeded_event: db_models.Event
) -> None:
    resp = client.get("/odds/events", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["id"] == seeded_event.id
    assert data[0]["name"] == "Arsenal vs Chelsea"
    assert data[0]["sport"] == "soccer"
    assert data[0]["source"] == "betfair"


# ---------------------------------------------------------------------------
# GET /odds/events/{event_id} — happy path + 401 + 404
# ---------------------------------------------------------------------------


def test_get_event_requires_auth(client: TestClient) -> None:
    resp = client.get("/odds/events/1")
    assert resp.status_code == 401


def test_get_event_not_found(client: TestClient, auth_headers: dict) -> None:
    resp = client.get("/odds/events/9999", headers=auth_headers)
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Event not found"


def test_get_event_returns_event(
    client: TestClient, auth_headers: dict, seeded_event: db_models.Event
) -> None:
    resp = client.get(f"/odds/events/{seeded_event.id}", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == seeded_event.id
    assert data["name"] == "Arsenal vs Chelsea"
    assert len(data["markets"]) == 1
    assert data["markets"][0]["market_type"] == "match_winner"


def test_get_event_markets_nested(
    client: TestClient, auth_headers: dict, seeded_event: db_models.Event
) -> None:
    resp = client.get(f"/odds/events/{seeded_event.id}", headers=auth_headers)
    assert resp.status_code == 200
    market = resp.json()["markets"][0]
    assert len(market["odds"]) == 1
    assert market["odds"][0]["bookmaker"] == "betfair"
    assert market["odds"][0]["selection"] == "Arsenal"
    assert market["odds"][0]["value"] == pytest.approx(2.5)


# ---------------------------------------------------------------------------
# GET /odds/events/{event_id}/markets — happy path + 401 + 404
# ---------------------------------------------------------------------------


def test_list_markets_requires_auth(client: TestClient) -> None:
    resp = client.get("/odds/events/1/markets")
    assert resp.status_code == 401


def test_list_markets_event_not_found(client: TestClient, auth_headers: dict) -> None:
    resp = client.get("/odds/events/9999/markets", headers=auth_headers)
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Event not found"


def test_list_markets_returns_markets(
    client: TestClient, auth_headers: dict, seeded_event: db_models.Event
) -> None:
    resp = client.get(f"/odds/events/{seeded_event.id}/markets", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["market_type"] == "match_winner"


def test_list_markets_empty_when_no_markets(
    client: TestClient, auth_headers: dict, db_session
) -> None:
    event = db_models.Event(
        source_id="betfair-002",
        source="betfair",
        sport="tennis",
        name="Wimbledon Final",
        start_time=datetime(2026, 7, 6, 14, 0, 0),
    )
    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)

    resp = client.get(f"/odds/events/{event.id}/markets", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json() == []
