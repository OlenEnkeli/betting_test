import asyncio

from random import randint
from datetime import datetime as dt

import logging
import aiorabbit
import logging.config
import coloredlogs

from sqlalchemy import select

from app.core.config import LOG_CONFIG, config
from app.schemas.event import EventScheme
from app.services.rabbit import rabbit_update_event
from app.models.event import Event, EventState
from app.core.db import async_session


async def line_finisher() -> None:

    async with async_session() as session:
        async with aiorabbit.connect(config.RABBIT_URL) as rabbit_client:
            await rabbit_client.confirm_select()

            logging.info('Starting line finisher proccessing..')

            while True:
                query = (
                    select(Event)
                    .filter(Event.state == EventState.NEW)
                    .filter(Event.deadline < dt.now())
                    .order_by(Event.deadline)
                )
                fetch = await session.scalars(query)
                events = fetch.all()

                for event in events:
                    if randint(0,1) == 0:
                        event.state = EventState.FINISHED_WIN
                    else:
                        event.state = EventState.FINISHED_LOSE

                    await session.merge(event)
                    await session.commit()
                    logging.info(f'Event {event.event_id}: set {event.state} state')

                    await rabbit_update_event(
                        client=rabbit_client,
                        event=EventScheme.from_orm(event),
                    )

                await asyncio.sleep(1)


if __name__ == '__main__':
    coloredlogs.install()
    logging.config.dictConfig(LOG_CONFIG)
    asyncio.run(line_finisher())
