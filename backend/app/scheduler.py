import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.config import settings

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def _poll_feeds() -> None:
    logger.info("Scheduler: poll cycle starting")
    from app.services.betfair import BetfairClient
    from app.services.odds_api import odds_api_service

    betfair = BetfairClient()
    odds_api = odds_api_service

    try:
        events = await betfair.list_events(sport_ids=["1", "7"])
        logger.info("Betfair: fetched %d events", len(events))
    except Exception as exc:
        logger.error("Betfair poll failed: %s", exc)

    try:
        soccer_odds = await odds_api.fetch("soccer_epl")
        logger.info("Odds API: fetched %d soccer events", len(soccer_odds))
    except Exception as exc:
        logger.error("Odds API poll failed: %s", exc)


def start_scheduler() -> None:
    scheduler.add_job(
        _poll_feeds,
        "interval",
        minutes=settings.odds_poll_interval_minutes,
        id="poll_feeds",
        replace_existing=True,
    )
    scheduler.start()
    logger.info(
        "Scheduler started — interval: %d min", settings.odds_poll_interval_minutes
    )
