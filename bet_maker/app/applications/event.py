import logging

from pydantic.error_wrappers import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.event import (
    EventScheme,
    ListEventScheme,
)
from app.models.event import Event, EventState
from app.applications.bet import BetController


class EventController:

    @classmethod
    async def get_all(
        cls,
        session: AsyncSession,
    ) -> ListEventScheme:
        query = (
            select(Event)
            .filter(Event.state == EventState.NEW)
            .order_by(Event.event_id)
        )
        result = await session.scalars(query)
        return ListEventScheme.parse_obj({
            'events': result.all()
        })

    @classmethod
    async def _get_by_id(
        cls,
        session: AsyncSession,
        id: str,
    ) -> Event | None:
        query = (
            select(Event)
            .filter(Event.event_id == id)
        )

        fetch = await session.execute(query)
        result = fetch.scalar_one_or_none()

        return result

    @classmethod
    async def get_by_id(
        cls,
        session: AsyncSession,
        id: str,
    ) -> EventScheme | None:
        result = await cls._get_by_id(
            session=session,
            id=id,
        )

        if not result:
            return None

        return EventScheme.from_orm(result)

    @staticmethod
    def _parse_event(
        origin: dict,
    ) -> EventScheme:
        try:
            parsed = EventScheme.parse_obj(origin)
        except ValidationError as e:
            logging.error(f'Can`t parse event object - {e}. Skipping.')
            return None

        return parsed

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        origin: dict,
    ) -> Event | None:
        parsed = cls._parse_event(origin=origin)

        event = Event(**parsed.dict())
        session.add(event)

        try:
            await session.commit()
        except IntegrityError:
            return None

        return event

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        origin: dict,
    ) -> Event | None:
        event = await cls._get_by_id(session=session, id=origin['event_id'])
        if not event:
            return None

        parsed = cls._parse_event(origin=origin)

        updated_event = Event(**parsed.dict())
        await session.merge(updated_event)
        await session.commit()

        if updated_event.state != EventState.NEW:
            bets = await BetController.get_all_bets_for_events(
                session=session,
                event=updated_event,
            )

            for bet in bets:
                await BetController.close(
                    session=session,
                    bet_id=bet.bet_id,
                    bet_state=bet.state,
                )

        return updated_event

    @classmethod
    async def remove(
        cls,
        session: AsyncSession,
        id: str,
    ) -> bool:
        event = await cls._get_by_id(session=session, id=id)
        if not event:
            return None

        await session.delete(event)
        await session.commit()

        return True
