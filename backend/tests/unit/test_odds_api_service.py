"""Unit tests for OddsApiService — STORY-3.

All Odds API HTTP calls are mocked; no real network requests are made.
The Odds API key is never referenced directly in assertions or log output.
The Odds API has a hard limit of 500 req/month — tests must never call
api.the-odds-api.com.
"""

import logging
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base
from app.db.models import Event, Market, Odds
from app.services.odds_api import OddsApiService


@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()
    Base.metadata.drop_all(bind=engine)


def _mock_get_response(
    payload: list,
    remaining: str | None = "200",
    status_code: int = 200,
) -> MagicMock:
    """Return a mock httpx Response for a GET call."""
    resp = MagicMock()
    resp.status_code = status_code
    resp.raise_for_status = MagicMock()
    resp.json.return_value = payload
    resp.headers = {"x-requests-remaining": remaining} if remaining is not None else {}
    return resp


def _mock_http_client(get_side_effect) -> tuple[MagicMock, MagicMock]:
    """Return (mock_cls, mock_instance) where mock_cls patches httpx.AsyncClient."""
    mock_instance = AsyncMock()
    mock_instance.get = AsyncMock(side_effect=get_side_effect)

    mock_cls = MagicMock()
    mock_cls.return_value.__aenter__ = AsyncMock(return_value=mock_instance)
    mock_cls.return_value.__aexit__ = AsyncMock(return_value=False)
    return mock_cls, mock_instance


# ── AC1: quota guard blocks request when x-requests-remaining < 50 ───────────


async def test_quota_guard_blocks_request_when_remaining_below_threshold(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """fetch() does NOT make an HTTP request when _requests_remaining < 50."""
    svc = OddsApiService()
    svc._requests_remaining = 49

    mock_cls, mock_instance = _mock_http_client(lambda *a, **kw: _mock_get_response([]))

    with caplog.at_level(logging.WARNING, logger="app.services.odds_api"):
        with patch("app.services.odds_api.httpx.AsyncClient", mock_cls):
            result = await svc.fetch("soccer_epl")

    assert result == []
    mock_instance.get.assert_not_called()


async def test_quota_guard_logs_warning_with_remaining_count(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """fetch() logs a WARNING containing the remaining request count."""
    svc = OddsApiService()
    svc._requests_remaining = 10

    mock_cls, _ = _mock_http_client(lambda *a, **kw: _mock_get_response([]))

    with caplog.at_level(logging.WARNING, logger="app.services.odds_api"):
        with patch("app.services.odds_api.httpx.AsyncClient", mock_cls):
            await svc.fetch("soccer_epl")

    assert any("10" in record.message for record in caplog.records)
    assert any(record.levelno == logging.WARNING for record in caplog.records)


async def test_quota_guard_blocks_at_exactly_49() -> None:
    """Guard triggers at 49 — one below the threshold of 50."""
    svc = OddsApiService()
    svc._requests_remaining = 49

    mock_cls, mock_instance = _mock_http_client(lambda *a, **kw: _mock_get_response([]))

    with patch("app.services.odds_api.httpx.AsyncClient", mock_cls):
        result = await svc.fetch("soccer_epl")

    assert result == []
    mock_instance.get.assert_not_called()


async def test_quota_guard_blocks_at_zero() -> None:
    """Guard triggers at 0 remaining requests."""
    svc = OddsApiService()
    svc._requests_remaining = 0

    mock_cls, mock_instance = _mock_http_client(lambda *a, **kw: _mock_get_response([]))

    with patch("app.services.odds_api.httpx.AsyncClient", mock_cls):
        result = await svc.fetch("soccer_epl")

    assert result == []
    mock_instance.get.assert_not_called()


# ── AC2: fetch proceeds normally when x-requests-remaining >= 50 ─────────────


async def test_fetch_proceeds_when_remaining_at_threshold() -> None:
    """fetch() makes the HTTP request when _requests_remaining == 50."""
    svc = OddsApiService()
    svc._requests_remaining = 50

    payload = [{"id": "evt-1", "sport_key": "soccer_epl"}]
    mock_cls, mock_instance = _mock_http_client(
        lambda *a, **kw: _mock_get_response(payload, remaining="50")
    )

    with patch("app.services.odds_api.httpx.AsyncClient", mock_cls):
        result = await svc.fetch("soccer_epl")

    assert result == payload
    mock_instance.get.assert_called_once()


async def test_fetch_proceeds_when_remaining_is_none() -> None:
    """fetch() makes the request when _requests_remaining has never been set."""
    svc = OddsApiService()
    assert svc._requests_remaining is None

    payload = [{"id": "evt-2", "sport_key": "americanfootball_nfl"}]
    mock_cls, mock_instance = _mock_http_client(
        lambda *a, **kw: _mock_get_response(payload, remaining="300")
    )

    with patch("app.services.odds_api.httpx.AsyncClient", mock_cls):
        result = await svc.fetch("americanfootball_nfl")

    assert result == payload
    mock_instance.get.assert_called_once()


async def test_fetch_proceeds_when_remaining_well_above_threshold() -> None:
    """fetch() makes the request when remaining is comfortably above 50."""
    svc = OddsApiService()
    svc._requests_remaining = 400

    payload = [{"id": "evt-3"}]
    mock_cls, mock_instance = _mock_http_client(
        lambda *a, **kw: _mock_get_response(payload, remaining="399")
    )

    with patch("app.services.odds_api.httpx.AsyncClient", mock_cls):
        result = await svc.fetch("soccer_epl")

    assert result == payload
    mock_instance.get.assert_called_once()


async def test_fetch_updates_remaining_from_response_header() -> None:
    """fetch() stores the x-requests-remaining header value after a successful call."""
    svc = OddsApiService()
    assert svc._requests_remaining is None

    mock_cls, _ = _mock_http_client(
        lambda *a, **kw: _mock_get_response([], remaining="123")
    )

    with patch("app.services.odds_api.httpx.AsyncClient", mock_cls):
        await svc.fetch("soccer_epl")

    assert svc._requests_remaining == 123


async def test_fetch_no_remaining_header_leaves_state_unchanged() -> None:
    """fetch() does not mutate _requests_remaining when header is absent."""
    svc = OddsApiService()
    svc._requests_remaining = 200

    mock_cls, _ = _mock_http_client(
        lambda *a, **kw: _mock_get_response([], remaining=None)
    )

    with patch("app.services.odds_api.httpx.AsyncClient", mock_cls):
        await svc.fetch("soccer_epl")

    assert svc._requests_remaining == 200


# ── AC3: valid response payload is parsed and returned correctly ──────────────


async def test_fetch_returns_parsed_odds_payload() -> None:
    """fetch() returns the full parsed list from the Odds API JSON body."""
    svc = OddsApiService()

    odds_payload = [
        {
            "id": "event-abc",
            "sport_key": "soccer_epl",
            "sport_title": "EPL",
            "commence_time": "2026-06-20T15:00:00Z",
            "home_team": "Arsenal",
            "away_team": "Chelsea",
            "bookmakers": [
                {
                    "key": "bet365",
                    "title": "Bet365",
                    "markets": [
                        {
                            "key": "h2h",
                            "outcomes": [
                                {"name": "Arsenal", "price": 2.10},
                                {"name": "Chelsea", "price": 3.50},
                                {"name": "Draw", "price": 3.20},
                            ],
                        }
                    ],
                }
            ],
        }
    ]

    mock_cls, _ = _mock_http_client(
        lambda *a, **kw: _mock_get_response(odds_payload, remaining="150")
    )

    with patch("app.services.odds_api.httpx.AsyncClient", mock_cls):
        result = await svc.fetch("soccer_epl")

    assert len(result) == 1
    event = result[0]
    assert event["id"] == "event-abc"
    assert event["sport_key"] == "soccer_epl"
    assert event["home_team"] == "Arsenal"
    assert event["away_team"] == "Chelsea"

    bookmaker = event["bookmakers"][0]
    assert bookmaker["key"] == "bet365"
    market = bookmaker["markets"][0]
    assert market["key"] == "h2h"
    outcomes = market["outcomes"]
    assert outcomes[0]["name"] == "Arsenal"
    assert outcomes[0]["price"] == 2.10


async def test_fetch_empty_payload_returns_empty_list() -> None:
    """fetch() with an empty Odds API response returns an empty list."""
    svc = OddsApiService()

    mock_cls, _ = _mock_http_client(
        lambda *a, **kw: _mock_get_response([], remaining="200")
    )

    with patch("app.services.odds_api.httpx.AsyncClient", mock_cls):
        result = await svc.fetch("soccer_epl")

    assert result == []


async def test_fetch_multiple_events_returned() -> None:
    """fetch() correctly returns multiple events from the payload."""
    svc = OddsApiService()

    payload = [
        {"id": "evt-1", "home_team": "Arsenal", "away_team": "Chelsea"},
        {"id": "evt-2", "home_team": "Man City", "away_team": "Liverpool"},
    ]

    mock_cls, _ = _mock_http_client(
        lambda *a, **kw: _mock_get_response(payload, remaining="198")
    )

    with patch("app.services.odds_api.httpx.AsyncClient", mock_cls):
        result = await svc.fetch("soccer_epl")

    assert len(result) == 2
    assert result[0]["id"] == "evt-1"
    assert result[1]["id"] == "evt-2"


async def test_fetch_passes_sport_in_url() -> None:
    """fetch() includes the sport key in the request URL path."""
    svc = OddsApiService()

    mock_cls, mock_instance = _mock_http_client(
        lambda *a, **kw: _mock_get_response([], remaining="200")
    )

    with patch("app.services.odds_api.httpx.AsyncClient", mock_cls):
        await svc.fetch("soccer_epl")

    call_url = mock_instance.get.call_args[0][0]
    assert "soccer_epl" in call_url


async def test_fetch_passes_regions_and_markets_params() -> None:
    """fetch() forwards regions and markets as query parameters."""
    svc = OddsApiService()

    mock_cls, mock_instance = _mock_http_client(
        lambda *a, **kw: _mock_get_response([], remaining="200")
    )

    with patch("app.services.odds_api.httpx.AsyncClient", mock_cls):
        await svc.fetch("soccer_epl", regions="us", markets="spreads")

    call_kwargs = mock_instance.get.call_args[1]
    params = call_kwargs.get("params", {})
    assert params["regions"] == "us"
    assert params["markets"] == "spreads"


# ── AC4: sentinel — no real HTTP calls reach api.the-odds-api.com ────────────


async def test_no_real_http_calls_reach_odds_api() -> None:
    """All fetch() calls are intercepted; httpx never dials api.the-odds-api.com."""
    svc = OddsApiService()

    mock_cls, mock_instance = _mock_http_client(
        lambda *a, **kw: _mock_get_response([], remaining="200")
    )

    with patch("app.services.odds_api.httpx.AsyncClient", mock_cls):
        await svc.fetch("soccer_epl")

    assert mock_instance.get.called
    call_url = mock_instance.get.call_args[0][0]
    assert "the-odds-api.com" in call_url


async def test_quota_guard_prevents_any_http_call_when_low() -> None:
    """When quota guard is active, not a single HTTP call is initiated."""
    svc = OddsApiService()
    svc._requests_remaining = 1

    mock_cls, mock_instance = _mock_http_client(lambda *a, **kw: _mock_get_response([]))

    with patch("app.services.odds_api.httpx.AsyncClient", mock_cls):
        await svc.fetch("soccer_epl")

    mock_instance.get.assert_not_called()
    mock_cls.assert_not_called()


# ── AC3 (persistence): Event, Market, and Odds records are written to DB ──────

_FULL_ODDS_PAYLOAD = [
    {
        "id": "event-abc",
        "sport_key": "soccer_epl",
        "sport_title": "EPL",
        "commence_time": "2026-06-20T15:00:00Z",
        "home_team": "Arsenal",
        "away_team": "Chelsea",
        "bookmakers": [
            {
                "key": "bet365",
                "title": "Bet365",
                "markets": [
                    {
                        "key": "h2h",
                        "outcomes": [
                            {"name": "Arsenal", "price": 2.10},
                            {"name": "Chelsea", "price": 3.50},
                            {"name": "Draw", "price": 3.20},
                        ],
                    }
                ],
            }
        ],
    }
]


async def test_persist_creates_event_record(db_session) -> None:
    """fetch() with db writes one Event record per API event."""
    svc = OddsApiService()
    mock_cls, _ = _mock_http_client(
        lambda *a, **kw: _mock_get_response(_FULL_ODDS_PAYLOAD, remaining="150")
    )

    with patch("app.services.odds_api.httpx.AsyncClient", mock_cls):
        await svc.fetch("soccer_epl", db=db_session)

    events = db_session.query(Event).all()
    assert len(events) == 1
    ev = events[0]
    assert ev.source_id == "event-abc"
    assert ev.source == "odds_api"
    assert ev.sport == "soccer_epl"
    assert ev.name == "Arsenal vs Chelsea"
    assert ev.start_time == datetime(2026, 6, 20, 15, 0, 0)


async def test_persist_creates_market_record(db_session) -> None:
    """fetch() with db writes one Market record per market type per event."""
    svc = OddsApiService()
    mock_cls, _ = _mock_http_client(
        lambda *a, **kw: _mock_get_response(_FULL_ODDS_PAYLOAD, remaining="150")
    )

    with patch("app.services.odds_api.httpx.AsyncClient", mock_cls):
        await svc.fetch("soccer_epl", db=db_session)

    markets = db_session.query(Market).all()
    assert len(markets) == 1
    assert markets[0].market_type == "h2h"
    assert markets[0].event_id == db_session.query(Event).first().id


async def test_persist_creates_odds_records(db_session) -> None:
    """fetch() with db writes one Odds record per bookmaker outcome."""
    svc = OddsApiService()
    mock_cls, _ = _mock_http_client(
        lambda *a, **kw: _mock_get_response(_FULL_ODDS_PAYLOAD, remaining="150")
    )

    with patch("app.services.odds_api.httpx.AsyncClient", mock_cls):
        await svc.fetch("soccer_epl", db=db_session)

    odds_rows = db_session.query(Odds).all()
    assert len(odds_rows) == 3
    by_selection = {o.selection: o for o in odds_rows}
    assert by_selection["Arsenal"].value == pytest.approx(2.10)
    assert by_selection["Arsenal"].bookmaker == "bet365"
    assert by_selection["Chelsea"].value == pytest.approx(3.50)
    assert by_selection["Draw"].value == pytest.approx(3.20)


async def test_persist_deduplicates_market_types_across_bookmakers(db_session) -> None:
    """When two bookmakers share the same market key, only one Market row is written."""
    payload = [
        {
            "id": "event-dup",
            "sport_key": "soccer_epl",
            "commence_time": "2026-06-21T12:00:00Z",
            "home_team": "Man City",
            "away_team": "Liverpool",
            "bookmakers": [
                {
                    "key": "betfair",
                    "markets": [
                        {
                            "key": "h2h",
                            "outcomes": [
                                {"name": "Man City", "price": 1.90},
                                {"name": "Liverpool", "price": 4.00},
                            ],
                        }
                    ],
                },
                {
                    "key": "paddypower",
                    "markets": [
                        {
                            "key": "h2h",
                            "outcomes": [
                                {"name": "Man City", "price": 1.95},
                                {"name": "Liverpool", "price": 3.90},
                            ],
                        }
                    ],
                },
            ],
        }
    ]
    svc = OddsApiService()
    mock_cls, _ = _mock_http_client(
        lambda *a, **kw: _mock_get_response(payload, remaining="150")
    )

    with patch("app.services.odds_api.httpx.AsyncClient", mock_cls):
        await svc.fetch("soccer_epl", db=db_session)

    assert db_session.query(Market).count() == 1
    assert db_session.query(Odds).count() == 4


async def test_persist_multiple_events(db_session) -> None:
    """fetch() persists all events in a multi-event payload."""
    payload = [
        {
            "id": "evt-1",
            "sport_key": "soccer_epl",
            "commence_time": "2026-06-20T15:00:00Z",
            "home_team": "Arsenal",
            "away_team": "Chelsea",
            "bookmakers": [],
        },
        {
            "id": "evt-2",
            "sport_key": "soccer_epl",
            "commence_time": "2026-06-20T17:30:00Z",
            "home_team": "Man City",
            "away_team": "Tottenham",
            "bookmakers": [],
        },
    ]
    svc = OddsApiService()
    mock_cls, _ = _mock_http_client(
        lambda *a, **kw: _mock_get_response(payload, remaining="148")
    )

    with patch("app.services.odds_api.httpx.AsyncClient", mock_cls):
        await svc.fetch("soccer_epl", db=db_session)

    events = db_session.query(Event).all()
    assert len(events) == 2
    source_ids = {e.source_id for e in events}
    assert source_ids == {"evt-1", "evt-2"}


async def test_persist_skipped_when_no_db(db_session) -> None:
    """fetch() without a db argument does not write any records."""
    svc = OddsApiService()
    mock_cls, _ = _mock_http_client(
        lambda *a, **kw: _mock_get_response(_FULL_ODDS_PAYLOAD, remaining="150")
    )

    with patch("app.services.odds_api.httpx.AsyncClient", mock_cls):
        await svc.fetch("soccer_epl")

    assert db_session.query(Event).count() == 0
