import json

import aiorabbit

from app.core.config import config
from app.schemas.event import EventScheme


async def rabbit_publish(
    client: aiorabbit.client.Client,
    rk: str,
    message: dict,
) -> bool:
    if not await client.publish(
        config.RABBIT_EXCHANGE,
        rk,
        json.dumps(message).encode('utf-8'),
    ):
        return False

    return True


async def rabbit_new_event(
    client: aiorabbit.client.Client,
    event: EventScheme,
) -> bool:
    return await rabbit_publish(
        client=client,
        rk=config.NEW_EVENT_RK,
        message=event.dict(),
    )


async def rabbit_update_event(
    client: aiorabbit.client.Client,
    event: EventScheme,
) -> bool:
    return await rabbit_publish(
        client=client,
        rk=config.UPDATE_EVENT_RK,
        message=event.dict(),
    )


async def rabbit_remove_event(
    client: aiorabbit.client.Client,
    event_id: str,
) -> bool:
    return await rabbit_publish(
        client=client,
        rk=config.UPDATE_EVENT_RK,
        message={'event_id': event_id},
    )
