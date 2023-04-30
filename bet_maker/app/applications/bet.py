import logging
import hashlib

from datetime import datetime as dt

from pydantic.error_wrappers import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event, EventState
from app.models.bet import Bet, BetState
from app.schemas.bet import (
    BetCreateScheme,
    BetReturnScheme,
)
from app.applications.event import EventController

class BetController:
    @classmethod
    def get_all(
        cls,
        session: AsyncSession,
    ) -> BetReturnScheme:
        pass

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        origin: BetCreateScheme
    ) -> BetReturnScheme:
        event = await EventController.get_by_id(
            session=session,
            id=origin.event_id,
        )

        if not event or event.state != EventState.NEW:
            return None

        bet_id_raw = f'{event.event_id}.{origin.amount}.{str(dt.now())}'
        bet_id = hashlib.sha256(bet_id_raw.encode('utf-8')).hexdigest()

        bet = Bet(
            bet_id=bet_id,
            event_id=event.event_id,
            amount=origin.amount,
            state=BetState.NEW,
        )

        session.add(bet)

        try:
            await session.commit()
        except IntegrityError:
            return None

        return BetReturnScheme.from_orm(bet)

    def close(
        self,
        session: AsyncSession,
        bet_id: int,
        bet_state: BetState,
    ) -> bool:
        return True