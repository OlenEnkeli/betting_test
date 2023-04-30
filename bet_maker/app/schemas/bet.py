from datetime import datetime as dt
from typing import List

from pydantic import BaseModel

from app.models.bet import BetState


class BetCreateScheme(BaseModel):
    event_id: str
    amount: float

    class Config:
        orm_mode = True


class BetReturnScheme(BetCreateScheme):
    bet_id: str
    created_at: dt
    state: BetState
    closed_at: dt | None

    class Config:
        orm_mode = True


class BetsListScheme(BaseModel):
    bets: List[BetReturnScheme]

    class Config:
        orm_mode = True
