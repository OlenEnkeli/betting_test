from enum import Enum

from sqlalchemy import (
    Column,
    String,
    Float,
    Enum as saEnum,
    DateTime,
)
from sqlalchemy.orm import relationship

from app.core.db import Base


class EventState(str, Enum):
    NEW = 'new'
    FINISHED_WIN = 'finished_new'
    FINISHED_LOSE = 'finished_lose'


class Event(Base):
    __tablename__ = 'event'

    event_id = Column(String, primary_key=True, index=True)
    coefficient = Column(Float)
    deadline = Column(DateTime)
    state = Column(saEnum(EventState), default=EventState.NEW)
    bets = relationship("Bet")
