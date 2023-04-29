import asyncio
import json
import logging

from aiorabbit import client, exceptions, message

from app.core.config import config
from app.core.db import async_session
from app.applications.event import EventController


class RabbitEventConsmer:

    def __init__(self):
        self.client = client.Client(config.RABBIT_URL)
        self.shutdown = asyncio.Event()

    async def new_event_callback(self, msg: bytes):
        print('new')
        origin = json.loads(msg.body)

        async with async_session() as session:
            await EventController.create(
                session=session,
                origin=origin,
            )

        await self.client.basic_ack(msg.delivery_tag)

    async def update_event_callback(self, msg: bytes):
        print('update')
        origin = json.loads(msg.body)

        async with async_session() as session:
            await EventController.update(
                session=session,
                origin=origin,
            )

        await self.client.basic_ack(msg.delivery_tag)

    async def remove_event_callback(self, msg: bytes):
        origin = json.loads(msg.body)

        async with async_session() as session:
            await EventController.remove(
                session=session,
                id=origin['event_id'],
            )

        await self.client.basic_ack(msg.delivery_tag)

    async def consume(self):
        try:
            await self.client.connect()
        except exceptions.AccessRefused as e:
            logging.error(f'Failed to connect to RabbitMQ: {e}')
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
            self.client.basic_consume(
                config.NEW_EVENT_QUEUE,
                callback=self.new_event_callback,
            ),
            self.client.basic_consume(
                config.UPDATE_EVENT_QUEUE,
                callback=self.update_event_callback,
            ),
            self.client.basic_consume(
                config.REMOVE_EVENT_QUEUE,
                callback=self.remove_event_callback,
            ),
        )

        await self.shutdown.wait()



async def run_consume():
    await RabbitEventConsmer().consume()


if __name__ == '__main__':
    asyncio.run(run_consume())
