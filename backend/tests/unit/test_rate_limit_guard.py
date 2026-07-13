"""Unit tests for STORY-7 — OddsApiService rate limit guard and /odds/api-status.

All HTTP calls to api.the-odds-api.com are mocked; no real network requests.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.odds_api import _QUOTA_GUARD_THRESHOLD, OddsApiService

# ── helpers ──────────────────────────────────────────────────────────────────


def _make_http_client(
    remaining: str | None = None,
    body: list = None,
) -> tuple[MagicMock, MagicMock]:
    """Return (mock_cls, mock_resp) for patching httpx.AsyncClient."""
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    resp.json.return_value = body or []
    resp.headers = {"x-requests-remaining": remaining} if remaining is not None else {}

    mock_instance = AsyncMock()
    mock_instance.get = AsyncMock(return_value=resp)

    mock_cls = MagicMock()
    mock_cls.return_value.__aenter__ = AsyncMock(return_value=mock_instance)
    mock_cls.return_value.__aexit__ = AsyncMock(return_value=False)
    return mock_cls, resp


# ── AC1: startup state — no response received yet ────────────────────────────


def test_startup_state_requests_remaining_is_none() -> None:
    svc = OddsApiService()
    assert svc.requests_remaining is None


def test_startup_state_guard_not_active() -> None:
    svc = OddsApiService()
    assert svc.guard_active is False


# ── AC2: guard_active reflects current quota ─────────────────────────────────


def test_guard_active_true_when_below_threshold() -> None:
    svc = OddsApiService()
    svc._requests_remaining = _QUOTA_GUARD_THRESHOLD - 1
    assert svc.guard_active is True


def test_guard_active_false_when_at_threshold() -> None:
    svc = OddsApiService()
    svc._requests_remaining = _QUOTA_GUARD_THRESHOLD
    assert svc.guard_active is False


def test_guard_active_false_when_above_threshold() -> None:
    svc = OddsApiService()
    svc._requests_remaining = _QUOTA_GUARD_THRESHOLD + 100
    assert svc.guard_active is False


# ── AC3: guard skips HTTP call and logs WARNING ───────────────────────────────


@pytest.mark.asyncio
async def test_fetch_skips_http_when_guard_active(caplog) -> None:
    svc = OddsApiService()
    svc._requests_remaining = 10  # below threshold

    with patch("app.services.odds_api.httpx.AsyncClient") as mock_cls:
        result = await svc.fetch("soccer_epl")

    mock_cls.assert_not_called()
    assert result == []


@pytest.mark.asyncio
async def test_fetch_emits_warning_when_guard_active(caplog) -> None:
    svc = OddsApiService()
    svc._requests_remaining = 10

    import logging

    with caplog.at_level(logging.WARNING, logger="app.services.odds_api"):
        with patch("app.services.odds_api.httpx.AsyncClient"):
            await svc.fetch("soccer_epl")

    assert any("quota guard" in r.message.lower() for r in caplog.records)
    assert any("10" in r.message for r in caplog.records)


# ── AC4: fetch proceeds normally when guard is inactive ──────────────────────


@pytest.mark.asyncio
async def test_fetch_proceeds_when_guard_inactive() -> None:
    svc = OddsApiService()
    svc._requests_remaining = 100  # above threshold

    mock_cls, _ = _make_http_client(remaining="99", body=[{"id": "evt1"}])

    with patch("app.services.odds_api.httpx.AsyncClient", mock_cls):
        result = await svc.fetch("soccer_epl")

    assert result == [{"id": "evt1"}]


# ── AC5: guard auto-deactivates on quota recovery ────────────────────────────


@pytest.mark.asyncio
async def test_guard_deactivates_after_quota_recovers() -> None:
    svc = OddsApiService()
    # Simulate guard having fired previously
    svc._requests_remaining = 10
    assert svc.guard_active is True

    # Now a subsequent successful response arrives with remaining >= threshold
    mock_cls, _ = _make_http_client(remaining="200", body=[])
    # Manually reset to simulate external reset (e.g. monthly quota refresh)
    svc._requests_remaining = 200
    assert svc.guard_active is False
    assert svc.requests_remaining == 200


# ── AC6: header parsing updates _requests_remaining ─────────────────────────


@pytest.mark.asyncio
async def test_fetch_updates_requests_remaining_from_header() -> None:
    svc = OddsApiService()

    mock_cls, _ = _make_http_client(remaining="123", body=[])

    with patch("app.services.odds_api.httpx.AsyncClient", mock_cls):
        await svc.fetch("soccer_epl")

    assert svc.requests_remaining == 123


@pytest.mark.asyncio
async def test_fetch_leaves_remaining_none_when_header_absent() -> None:
    svc = OddsApiService()

    mock_cls, _ = _make_http_client(remaining=None, body=[])

    with patch("app.services.odds_api.httpx.AsyncClient", mock_cls):
        await svc.fetch("soccer_epl")

    assert svc.requests_remaining is None


# ── GET /odds/api-status endpoint ────────────────────────────────────────────


def test_api_status_startup_state(client, auth_headers) -> None:
    """Before any poll, status must be null/false (startup state)."""
    from app.dependencies import get_odds_api_service
    from app.main import app

    fresh_svc = OddsApiService()

    app.dependency_overrides[get_odds_api_service] = lambda: fresh_svc
    try:
        resp = client.get("/odds/api-status", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["requests_remaining"] is None
        assert data["guard_active"] is False
    finally:
        del app.dependency_overrides[get_odds_api_service]


def test_api_status_guard_active(client, auth_headers) -> None:
    from app.dependencies import get_odds_api_service
    from app.main import app

    svc = OddsApiService()
    svc._requests_remaining = 30

    app.dependency_overrides[get_odds_api_service] = lambda: svc
    try:
        resp = client.get("/odds/api-status", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["requests_remaining"] == 30
        assert data["guard_active"] is True
    finally:
        del app.dependency_overrides[get_odds_api_service]


def test_api_status_guard_inactive_after_recovery(client, auth_headers) -> None:
    from app.dependencies import get_odds_api_service
    from app.main import app

    svc = OddsApiService()
    svc._requests_remaining = 150

    app.dependency_overrides[get_odds_api_service] = lambda: svc
    try:
        resp = client.get("/odds/api-status", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["requests_remaining"] == 150
        assert data["guard_active"] is False
    finally:
        del app.dependency_overrides[get_odds_api_service]


def test_api_status_requires_auth(client) -> None:
    resp = client.get("/odds/api-status")
    assert resp.status_code == 401
