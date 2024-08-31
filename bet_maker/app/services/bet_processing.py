import asyncio
import json
import logging
import logging.config
from typing import Callable

import aiorabbit.client
import coloredlogs
from aiorabbit import client, exceptions

from app.applications.event import EventController
from app.core.config import LOG_CONFIG, config
from app.core.db import async_session


class RabbitEventConsmer:

    def __init__(self) -> None:
        self.client = client.Client(config.RABBIT_URL)
        self.shutdown = asyncio.Event()

    async def new_event_callback(self, msg: bytes) -> None:
        origin = json.loads(msg.body) # type:ignore[attr-defined]

        async with async_session() as session:
            await EventController.create(
                session=session,
                origin=origin,
            )

        logging.info(f'Event {origin["event_id"]} was created.')

    async def update_event_callback(self, msg: bytes) -> None:
        origin = json.loads(msg.body) # type:ignore[attr-defined]

        async with async_session() as session:
            await EventController.update(
                session=session,
                origin=origin,
            )

        logging.info(f'Event {origin["event_id"]} was updated.')

    async def remove_event_callback(self, msg: bytes) -> None:
        origin = json.loads(msg.body)  # type:ignore[attr-defined]

        async with async_session() as session:
            await EventController.remove(
                session=session,
                id=origin['event_id'],
            )

        logging.info(f'Event {origin["event_id"]} was removed.')

    async def _consume_queue(
        self,
        client: aiorabbit.client.Client,
        queue: str,
        callback: Callable,
    ) -> None:
        async for msg in client.consume(queue):
            await callback(msg)
            await client.basic_ack(msg.delivery_tag)

    async def consume(self) -> None:
        try:
            await self.client.connect()
        except exceptions.AccessRefused as e:
            logging.exception(f'Failed to connect to RabbitMQ: {e}')
            return
        await self.client.queue_declare(
            config.NEW_EVENT_QUEUE,
            durable=True,
        )
        await self.client.queue_declare(
            config.UPDATE_EVENT_QUEUE,
            durable=True,
        )
        await self.client.queue_declare(
            config.REMOVE_EVENT_QUEUE,
            durable=True,
        )

        logging.info('Start consuming RabbitMQ queues..')

        await asyncio.gather(
            self._consume_queue(
                client=self.client,
                queue=config.NEW_EVENT_QUEUE,
                callback=self.new_event_callback,
            ),
            self._consume_queue(
                client=self.client,
                queue=config.UPDATE_EVENT_QUEUE,
                callback=self.update_event_callback,
            ),
            self._consume_queue(
                client=self.client,
                queue=config.REMOVE_EVENT_QUEUE,
                callback=self.remove_event_callback,
            ),
        )

        await self.shutdown.wait()


async def run_consume() -> None:
    await RabbitEventConsmer().consume()


if __name__ == '__main__':
    coloredlogs.install()
    logging.config.dictConfig(LOG_CONFIG)
    asyncio.run(run_consume())
