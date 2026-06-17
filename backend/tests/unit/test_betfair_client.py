"""Unit tests for BetfairClient — STORY-2.

All Betfair HTTP calls are mocked; no real network requests are made.
Betfair credentials are never referenced directly in assertions or log output.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.betfair import BetfairClient


def _mock_login_response(token: str = "test-session-token") -> MagicMock:
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    resp.json.return_value = {"status": "SUCCESS", "token": token}
    return resp


def _mock_http_client(post_side_effect) -> tuple[MagicMock, MagicMock]:
    """Return (mock_cls, mock_instance) where mock_cls patches httpx.AsyncClient."""
    mock_instance = AsyncMock()
    mock_instance.post = AsyncMock(side_effect=post_side_effect)

    mock_cls = MagicMock()
    mock_cls.return_value.__aenter__ = AsyncMock(return_value=mock_instance)
    mock_cls.return_value.__aexit__ = AsyncMock(return_value=False)
    return mock_cls, mock_instance


# ── AC1: successful _login stores token and returns it ───────────────────────


async def test_login_success_stores_and_returns_session_token() -> None:
    """_login() with a SUCCESS response stores the token in memory and returns it."""
    client = BetfairClient()
    assert client._session_token is None

    mock_cls, _ = _mock_http_client(lambda *a, **kw: _mock_login_response("abc-123"))

    with patch("app.services.betfair.httpx.AsyncClient", mock_cls):
        token = await client._login()

    assert token == "abc-123"
    assert client._session_token == "abc-123"


# ── AC3: non-SUCCESS login status raises RuntimeError ────────────────────────


async def test_login_fail_status_raises_runtime_error() -> None:
    """_login() raises RuntimeError when Betfair returns status != SUCCESS."""
    client = BetfairClient()

    fail_resp = MagicMock()
    fail_resp.raise_for_status = MagicMock()
    fail_resp.json.return_value = {
        "status": "FAIL",
        "error": "INVALID_USERNAME_OR_PASSWORD",
    }

    mock_cls, _ = _mock_http_client(lambda *a, **kw: fail_resp)

    with patch("app.services.betfair.httpx.AsyncClient", mock_cls):
        with pytest.raises(RuntimeError, match="Betfair login failed"):
            await client._login()


async def test_login_error_field_included_in_runtime_error() -> None:
    """RuntimeError message includes the Betfair error field."""
    client = BetfairClient()

    fail_resp = MagicMock()
    fail_resp.raise_for_status = MagicMock()
    fail_resp.json.return_value = {"status": "FAIL", "error": "ACCOUNT_LOCKED"}

    mock_cls, _ = _mock_http_client(lambda *a, **kw: fail_resp)

    with patch("app.services.betfair.httpx.AsyncClient", mock_cls):
        with pytest.raises(RuntimeError, match="ACCOUNT_LOCKED"):
            await client._login()


# ── AC2: 403 response triggers re-auth and exactly one retry ─────────────────


async def test_post_403_reauthenticates_and_retries_exactly_once() -> None:
    """_post() re-auths on first 403 and retries; no further retry on second 403."""
    client = BetfairClient()
    client._session_token = "stale-token"

    ok_payload = {"result": "success"}
    call_iter = iter(
        [
            # call 1: initial API request → 403
            MagicMock(status_code=403, raise_for_status=MagicMock()),
            # call 2: _login re-auth → SUCCESS
            _mock_login_response("fresh-token"),
            # call 3: retry API request → 200
            MagicMock(
                status_code=200,
                raise_for_status=MagicMock(),
                json=MagicMock(return_value=ok_payload),
            ),
        ]
    )

    mock_cls, mock_instance = _mock_http_client(lambda *a, **kw: next(call_iter))

    with patch("app.services.betfair.httpx.AsyncClient", mock_cls):
        result = await client._post("listEvents/", {})

    assert result == ok_payload
    assert client._session_token == "fresh-token"
    # Exactly three HTTP POST calls: initial, re-auth login, retry
    assert mock_instance.post.call_count == 3


async def test_post_auto_logs_in_when_no_session_token() -> None:
    """_post() calls _login automatically if no session token is set."""
    client = BetfairClient()
    assert client._session_token is None

    payload = [
        {
            "event": {"id": "42", "name": "Test", "openDate": None},
            "eventType": {"id": "1"},
        }
    ]
    call_iter = iter(
        [
            # call 1: _login (session_token is None triggers login first)
            _mock_login_response("auto-token"),
            # call 2: actual API request → 200
            MagicMock(
                status_code=200,
                raise_for_status=MagicMock(),
                json=MagicMock(return_value=payload),
            ),
        ]
    )

    mock_cls, _ = _mock_http_client(lambda *a, **kw: next(call_iter))

    with patch("app.services.betfair.httpx.AsyncClient", mock_cls):
        result = await client._post("listEvents/", {})

    assert result == payload
    assert client._session_token == "auto-token"


# ── AC4: list_events returns dicts with id, name, sport, start_time ──────────


async def test_list_events_returns_correct_keys_and_values() -> None:
    """list_events() maps Betfair response to dicts with id/name/sport/start_time."""
    client = BetfairClient()
    client._session_token = "valid-token"

    betfair_response = [
        {
            "event": {
                "id": "123",
                "name": "Arsenal v Chelsea",
                "openDate": "2026-06-20T15:00:00Z",
            },
            "eventType": {"id": "1"},
        },
        {
            "event": {
                "id": "456",
                "name": "Grand National",
                "openDate": "2026-06-21T14:00:00Z",
            },
            "eventType": {"id": "7"},
        },
    ]

    api_resp = MagicMock()
    api_resp.status_code = 200
    api_resp.raise_for_status = MagicMock()
    api_resp.json.return_value = betfair_response

    mock_cls, _ = _mock_http_client(lambda *a, **kw: api_resp)

    with patch("app.services.betfair.httpx.AsyncClient", mock_cls):
        events = await client.list_events(sport_ids=["1", "7"])

    assert len(events) == 2

    soccer = events[0]
    assert soccer["id"] == "123"
    assert soccer["name"] == "Arsenal v Chelsea"
    assert soccer["sport"] == "1"
    assert soccer["start_time"] == "2026-06-20T15:00:00Z"

    racing = events[1]
    assert racing["id"] == "456"
    assert racing["name"] == "Grand National"
    assert racing["sport"] == "7"
    assert racing["start_time"] == "2026-06-21T14:00:00Z"


async def test_list_events_empty_response_returns_empty_list() -> None:
    """list_events() with an empty Betfair response returns an empty list."""
    client = BetfairClient()
    client._session_token = "valid-token"

    api_resp = MagicMock()
    api_resp.status_code = 200
    api_resp.raise_for_status = MagicMock()
    api_resp.json.return_value = []

    mock_cls, _ = _mock_http_client(lambda *a, **kw: api_resp)

    with patch("app.services.betfair.httpx.AsyncClient", mock_cls):
        events = await client.list_events(sport_ids=["1"])

    assert events == []


async def test_list_events_missing_event_fields_handled_gracefully() -> None:
    """list_events() uses .get() so partially populated events don't crash."""
    client = BetfairClient()
    client._session_token = "valid-token"

    betfair_response = [{"event": {}, "eventType": {}}]

    api_resp = MagicMock()
    api_resp.status_code = 200
    api_resp.raise_for_status = MagicMock()
    api_resp.json.return_value = betfair_response

    mock_cls, _ = _mock_http_client(lambda *a, **kw: api_resp)

    with patch("app.services.betfair.httpx.AsyncClient", mock_cls):
        events = await client.list_events(sport_ids=["1"])

    assert len(events) == 1
    assert events[0]["id"] is None
    assert events[0]["name"] is None
    assert events[0]["sport"] is None
    assert events[0]["start_time"] is None


# ── AC5: sentinel — no real HTTP calls escape the mock boundary ───────────────


async def test_no_real_http_calls_reach_betfair_identity_sso() -> None:
    """All _login() calls are intercepted; httpx never dials identitysso.betfair.com."""
    client = BetfairClient()

    mock_cls, mock_instance = _mock_http_client(
        lambda *a, **kw: _mock_login_response("sentinel-token")
    )

    with patch("app.services.betfair.httpx.AsyncClient", mock_cls):
        await client._login()

    # The mock was called, so the real httpx.AsyncClient was never used
    assert mock_instance.post.called
    # Confirm the URL passed was the Betfair identity SSO URL (not a real call)
    call_url = mock_instance.post.call_args[0][0]
    assert "identitysso.betfair.com" in call_url
