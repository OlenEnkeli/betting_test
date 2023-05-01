from enum import Enum
from datetime import datetime as dt

from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Float,
    DateTime,
    Enum as saEnum,
)

from app.core.db import Base


class BetState(str, Enum):
    NEW = 'new'
    WIN = 'win'
    LOSE = 'lose'


class Bet(Base):
    __tablename__ = 'bet'

    bet_id = Column(String, primary_key=True, index=True)
    event_id = Column(String, ForeignKey("event.event_id"), index=True)
    amount = Column(Float)
    created_at = Column(DateTime, default=dt.utcnow)
    closed_at = Column(DateTime, nullable=True)
    state = Column(saEnum(BetState), default=BetState.NEW)
