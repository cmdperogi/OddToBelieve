import logging
from datetime import datetime
from typing import Any

import httpx
from sqlalchemy.orm import Session

from app.config import settings

logger = logging.getLogger(__name__)

_ODDS_API_BASE = "https://api.the-odds-api.com/v4"
_QUOTA_GUARD_THRESHOLD = 50


class OddsApiService:
    def __init__(self) -> None:
        self._requests_remaining: int | None = None

    async def fetch(
        self,
        sport: str,
        regions: str = "uk",
        markets: str = "h2h",
        db: Session | None = None,
    ) -> list[dict[str, Any]]:
        if (
            self._requests_remaining is not None
            and self._requests_remaining < _QUOTA_GUARD_THRESHOLD
        ):
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

        data: list[dict[str, Any]] = resp.json()

        if db is not None:
            self._persist(data, db)

        return data

    def _persist(self, events: list[dict[str, Any]], db: Session) -> None:
        from app.db.models import Event, Market, Odds

        for event_data in events:
            home = event_data.get("home_team", "")
            away = event_data.get("away_team", "")
            start_time = datetime.fromisoformat(
                event_data["commence_time"].replace("Z", "+00:00")
            ).replace(tzinfo=None)
            event = Event(
                source_id=event_data["id"],
                source="odds_api",
                sport=event_data.get("sport_key", ""),
                name=f"{home} vs {away}",
                start_time=start_time,
            )
            db.add(event)
            db.flush()

            market_by_type: dict[str, Market] = {}
            for bookmaker in event_data.get("bookmakers", []):
                for market_data in bookmaker.get("markets", []):
                    mtype = market_data["key"]
                    if mtype not in market_by_type:
                        market = Market(event_id=event.id, market_type=mtype)
                        db.add(market)
                        db.flush()
                        market_by_type[mtype] = market

                    market = market_by_type[mtype]
                    for outcome in market_data.get("outcomes", []):
                        db.add(
                            Odds(
                                market_id=market.id,
                                bookmaker=bookmaker["key"],
                                selection=outcome["name"],
                                value=outcome["price"],
                            )
                        )

        db.commit()
