from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from app.applications.event import EventController
from app.core.db import get_session
from app.schemas.event import EventSchema, ListEventSchema

router = APIRouter(
    prefix='/events',
    tags=['События'],
)


@router.get(
    '/',
    response_model=ListEventSchema,
)
async def get_events(
    session=Depends(get_session),
):
    return await EventController.get_all(session=session)


@router.get(
    '/{event_id}',
    response_model=EventSchema,
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
    response_model=EventSchema,
)
async def create_event(
    origin: EventSchema,
    session=Depends(get_session),
):
    event = await EventController.create(
        session=session,
        origin=origin,  # type:ignore[arg-type]
    )

    if not event:
        raise HTTPException(
            status_code=422,
            detail='Duplicate event_id',
        )

    return event


@router.patch(
    '/',
    response_model=EventSchema,
)
async def update_event(
    origin: EventSchema,
    session=Depends(get_session),
):
    event = await EventController.update(
        session=session,
        origin=origin,
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail='Event not found',
        )

    return event


@router.delete('/{event_id}')
async def remove_event(
    event_id: str,
    session=Depends(get_session),
):
    removed = await EventController.remove(
        session=session,
        id=event_id,
    )

    if not removed:
        raise HTTPException(
            status_code=404,
            detail='Event not found',
        )

    return {'success': 'ok'}
