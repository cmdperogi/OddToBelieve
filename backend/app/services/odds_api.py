import logging
from typing import Any

import httpx

from app.config import settings

logger = logging.getLogger(__name__)

_ODDS_API_BASE = "https://api.the-odds-api.com/v4"
_QUOTA_GUARD_THRESHOLD = 50


class OddsApiService:
    def __init__(self) -> None:
        self._requests_remaining: int | None = None

    @property
    def requests_remaining(self) -> int | None:
        return self._requests_remaining

    @property
    def guard_active(self) -> bool:
        return (
            self._requests_remaining is not None
            and self._requests_remaining < _QUOTA_GUARD_THRESHOLD
        )

    async def fetch(
        self, sport: str, regions: str = "uk", markets: str = "h2h"
    ) -> list[dict[str, Any]]:
        if self.guard_active:
            logger.warning(
                "Odds API quota guard active — requests remaining: %s",
                self._requests_remaining,
            )
            return []

        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{_ODDS_API_BASE}/sports/{sport}/odds",
                params={
                    "apiKey": settings.the_odds_api_key,
                    "regions": regions,
                    "markets": markets,
                },
            )
        resp.raise_for_status()

        remaining = resp.headers.get("x-requests-remaining")
        if remaining is not None:
            self._requests_remaining = int(remaining)

        return resp.json()


# Singleton shared between the scheduler and the API router so that
# request-quota state persists across poll cycles and is visible via
# GET /odds/api-status without a live API call.
odds_api_service = OddsApiService()
