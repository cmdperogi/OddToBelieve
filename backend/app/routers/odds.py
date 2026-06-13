from fastapi import APIRouter, HTTPException

from app.db import models as db_models
from app.dependencies import DbDep, UserDep
from app.models.schemas import EventSchema, MarketSchema

router = APIRouter(prefix="/odds", tags=["odds"])


@router.get("/events", response_model=list[EventSchema])
async def list_events(_user: UserDep, db: DbDep) -> list[db_models.Event]:
    return db.query(db_models.Event).all()


@router.get("/events/{event_id}", response_model=EventSchema)
async def get_event(event_id: int, _user: UserDep, db: DbDep) -> db_models.Event:
    event = db.get(db_models.Event, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.get("/events/{event_id}/markets", response_model=list[MarketSchema])
async def list_markets(
    event_id: int, _user: UserDep, db: DbDep
) -> list[db_models.Market]:
    event = db.get(db_models.Event, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event.markets
