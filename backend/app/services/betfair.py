import logging
from typing import Any

import httpx

from app.config import settings

logger = logging.getLogger(__name__)

_BETFAIR_LOGIN_URL = "https://identitysso.betfair.com/api/login"
_BETFAIR_API_BASE = "https://api.betfair.com/exchange/betting/rest/v1.0"


class BetfairClient:
    def __init__(self) -> None:
        self._session_token: str | None = None

    async def _login(self) -> str:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                _BETFAIR_LOGIN_URL,
                data={
                    "username": settings.betfair_username,
                    "password": settings.betfair_password,
                },
                headers={
                    "X-Application": settings.betfair_app_key,
                    "Accept": "application/json",
                },
            )
        resp.raise_for_status()
        body = resp.json()
        if body.get("status") != "SUCCESS":
            raise RuntimeError(f"Betfair login failed: {body.get('error')}")
        self._session_token = body["token"]
        return self._session_token

    async def _post(self, endpoint: str, payload: dict[str, Any]) -> Any:
        if self._session_token is None:
            await self._login()

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{_BETFAIR_API_BASE}/{endpoint}",
                json=payload,
                headers={
                    "X-Authentication": self._session_token or "",
                    "X-Application": settings.betfair_app_key,
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
            )

        if resp.status_code == 403:
            logger.warning("Betfair 403 — re-authenticating")
            await self._login()
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{_BETFAIR_API_BASE}/{endpoint}",
                    json=payload,
                    headers={
                        "X-Authentication": self._session_token or "",
                        "X-Application": settings.betfair_app_key,
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                )

        resp.raise_for_status()
        return resp.json()

    async def list_events(self, sport_ids: list[str]) -> list[dict[str, Any]]:
        payload = {
            "filter": {"eventTypeIds": sport_ids},
        }
        data = await self._post("listEvents/", payload)
        results = []
        for item in data:
            event = item.get("event", {})
            results.append(
                {
                    "id": event.get("id"),
                    "name": event.get("name"),
                    "sport": item.get("eventType", {}).get("id"),
                    "start_time": event.get("openDate"),
                }
            )
        return results
