from fastapi import APIRouter, Depends, HTTPException

from app.core.db import get_session
from app.core.rabbit import get_rabbit_client
from app.schemas.event import (
    EventScheme,
    ListEventScheme,
)
from app.applications.event import EventController


router = APIRouter(
    prefix='/events',
    tags=['События'],
)


@router.get(
    '/',
    response_model=ListEventScheme,
)
async def get_events(
    session=Depends(get_session),
):
    return await EventController.get_all(session=session)


@router.get(
    '/{event_id}',
    response_model=EventScheme,
)
async def get_event_by_id(
    event_id: str,
    session=Depends(get_session),
):
    event = await EventController.get_by_id(
        session=session,
        id=event_id,
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail='Event not found',
        )

    return event


@router.post(
    '/',
    response_model=EventScheme,
)
async def create_event(
    origin: EventScheme,
    session=Depends(get_session),
    rabbit_client=Depends(get_rabbit_client),
):
    event = await EventController.create(
        session=session,
        rabbit_client=rabbit_client,
        origin=origin,
    )

    if not event:
        raise HTTPException(
            status_code=422,
            detail='Duplicate event_id'
        )

    return event


@router.patch(
    '/',
    response_model=EventScheme,
)
async def update_event(
    origin: EventScheme,
    session=Depends(get_session),
    rabbit_client=Depends(get_rabbit_client),
):
    event = await EventController.update(
        session=session,
        rabbit_client=rabbit_client,
        origin=origin,
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail='Event not found'
        )

    return event


@router.delete('/{event_id}')
async def remove_event(
    event_id: str,
    session=Depends(get_session),
    rabbit_client=Depends(get_rabbit_client),
):
    removed = await EventController.remove(
        session=session,
        rabbit_client=rabbit_client,
        id=event_id,
    )

    if not removed:
        raise HTTPException(
            status_code=404,
            detail='Event not found'
        )

    return {'success': 'ok'}