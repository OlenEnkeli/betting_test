import hashlib
from datetime import datetime as dt
from typing import List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.bet import Bet, BetState
from app.models.event import Event
from app.schemas.bet import (
    BetCreateScheme,
    BetReturnScheme,
    BetsListScheme,
)


class BetController:
    @classmethod
    async def get_all(
        cls,
        session: AsyncSession,
    ) -> BetsListScheme:
        query = (
            select(Bet)
            .order_by(Bet.event_id)
        )
        result = await session.scalars(query)
        return BetsListScheme.parse_obj({
            'bets': result.all(),
        })

    @classmethod
    async def get_all_bets_for_events(
        cls,
        session: AsyncSession,
        event: Event,
    ) -> List[Bet]:
        query = (
            select(Bet)
            .filter(Bet.event_id == event.event_id)
            .order_by(Bet.created_at)
        )
        return await session.scalars(query)

    @classmethod
    async def _get_by_id(
        cls,
        session: AsyncSession,
        id: str,
    ) -> Bet | None:
        query = (
            select(Bet)
            .filter(Bet.bet_id == id)
        )

        fetch = await session.execute(query)
        result = fetch.scalar_one_or_none()

        return result

    @classmethod
    async def get_by_id(
        cls,
        session: AsyncSession,
        id: str,
    ) -> BetReturnScheme | None:
        result = await cls._get_by_id(
            session=session,
            id=id,
        )

        if not result:
            return None

        return BetReturnScheme.from_orm(result)

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        event: Event,
        origin: BetCreateScheme,
    ) -> BetReturnScheme:

        bet_id_raw = f'{event.event_id}.{origin.amount}.{dt.utcnow()!s}'
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

    @classmethod
    async def close(
        cls,
        session: AsyncSession,
        bet_id: str,
        bet_state: BetState,
    ) -> bool | None:
        bet = await cls._get_by_id(
            session=session,
            id=bet_id,
        )

        if not bet or bet.state != BetState.NEW:
            return None

        bet.state = bet_state

        await session.merge(bet)
        await session.commit()
