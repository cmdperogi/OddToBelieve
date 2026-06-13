from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    source_id: Mapped[str] = mapped_column(String, index=True)
    source: Mapped[str] = mapped_column(String)  # "betfair" | "odds_api"
    sport: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    start_time: Mapped[datetime] = mapped_column(DateTime)

    markets: Mapped[list["Market"]] = relationship(
        "Market", back_populates="event", cascade="all, delete-orphan"
    )


class Market(Base):
    __tablename__ = "markets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey("events.id"))
    market_type: Mapped[str] = mapped_column(
        String
    )  # "match_winner" | "over_under" | "win"

    event: Mapped["Event"] = relationship("Event", back_populates="markets")
    odds: Mapped[list["Odds"]] = relationship(
        "Odds", back_populates="market", cascade="all, delete-orphan"
    )


class Odds(Base):
    __tablename__ = "odds"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    market_id: Mapped[int] = mapped_column(Integer, ForeignKey("markets.id"))
    bookmaker: Mapped[str] = mapped_column(String)
    selection: Mapped[str] = mapped_column(String)
    value: Mapped[float] = mapped_column(Float)
    fetched_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    market: Mapped["Market"] = relationship("Market", back_populates="odds")
