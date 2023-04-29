from typing import List

from pydantic import BaseModel

from app.models.event import EventState
from datetime import datetime as dt


class EventScheme(BaseModel):
    event_id: str
    coefficient: float
    deadline: dt
    state: EventState

    class Config:
        orm_mode = True


class ListEventScheme(BaseModel):
    events: List[EventScheme]

    class Config:
        orm_mode = True
