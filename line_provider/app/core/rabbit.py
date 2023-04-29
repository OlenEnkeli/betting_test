import aiorabbit

from aiorabbit.client import Client

from app.core.config import config


async def get_rabbit_client() -> Client:
    async with aiorabbit.connect(config.RABBIT_URL) as client:
        await client.confirm_select()
        yield client
