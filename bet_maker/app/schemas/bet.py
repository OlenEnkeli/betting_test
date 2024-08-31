from datetime import datetime as dt
from typing import List

from pydantic import BaseModel

from app.models.bet import BetState


class BetCreateSchema(BaseModel):
    event_id: str
    amount: float

    class Config:
        orm_mode = True


class BetReturnSchema(BetCreateSchema):
    bet_id: str
    created_at: dt
    state: BetState
    closed_at: dt | None

    class Config:
        orm_mode = True


class BetsListSchema(BaseModel):
    bets: List[BetReturnSchema]

    class Config:
        orm_mode = True
