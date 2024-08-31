from datetime import datetime as dt
from typing import List

from pydantic import BaseModel

from app.models.event import EventState


class EventSchema(BaseModel):
    event_id: str
    coefficient: float
    deadline: dt
    state: EventState

    class Config:
        orm_mode = True


class ListEventSchema(BaseModel):
    events: List[EventSchema]

    class Config:
        orm_mode = True
