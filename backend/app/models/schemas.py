from datetime import datetime

from pydantic import BaseModel


class ApiStatusSchema(BaseModel):
    requests_remaining: int | None
    guard_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class OddsSchema(BaseModel):
    id: int
    bookmaker: str
    selection: str
    value: float
    fetched_at: datetime

    model_config = {"from_attributes": True}


class MarketSchema(BaseModel):
    id: int
    market_type: str
    odds: list[OddsSchema] = []

    model_config = {"from_attributes": True}


class EventSchema(BaseModel):
    id: int
    source_id: str
    source: str
    sport: str
    name: str
    start_time: datetime
    markets: list[MarketSchema] = []

    model_config = {"from_attributes": True}
