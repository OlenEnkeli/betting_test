from typing import List

import aiorabbit

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.rabbit import (
    rabbit_new_event,
    rabbit_update_event,
    rabbit_remove_event,
)
from app.schemas.event import (
    EventScheme,
    ListEventScheme,
)
from app.models.event import Event


class EventController:

    @classmethod
    async def get_all(
        cls,
        session: AsyncSession,
    ) -> ListEventScheme:
        query = select(Event).order_by(Event.event_id)
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
        result = cls._get_by_id(
            session=session,
            id=id,
        )

        if not result:
            return None

        return EventScheme.from_orm(result)

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        rabbit_client: aiorabbit.client.Client,
        origin: EventScheme,
    ) -> EventScheme | None:
        new_event = Event(**origin.dict())
        session.add(new_event)

        try:
            await session.commit()
        except IntegrityError:
            return None

        event = EventScheme.from_orm(new_event)

        await rabbit_new_event(
            client=rabbit_client,
            event=event,
        )

        return event

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        origin: EventScheme,
        rabbit_client: aiorabbit.client.Client,
    ) -> EventScheme | None:
        event = await cls._get_by_id(session=session, id=origin.event_id)
        if not event:
            return None

        updated_event = Event(**origin.dict())
        await session.merge(updated_event)
        await session.commit()

        event = EventScheme.from_orm(updated_event)

        await rabbit_update_event(
            client=rabbit_client,
            event=event,
        )

        return event

    @classmethod
    async def remove(
        cls,
        session: AsyncSession,
        rabbit_client: aiorabbit.client.Client,
        id: str,
    ) -> bool:
        event = await cls._get_by_id(session=session, id=id)
        if not event:
            return None

        await session.delete(event)
        await session.commit()

        await rabbit_remove_event(
            client=rabbit_client,
            event_id=id,
        )

        return True
