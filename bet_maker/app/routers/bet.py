from fastapi import APIRouter, Depends, HTTPException

from app.core.db import get_session
from app.schemas.bet import (
    BetCreateScheme,
    BetReturnScheme,
    BetsListScheme,
)
from app.applications.bet import BetController


router = APIRouter(
    prefix='/bets',
    tags=['Ставки'],
)


@router.post(
    '/',
    response_model=BetReturnScheme,
)
async def create_bet(
    origin: BetCreateScheme,
    session=Depends(get_session),
):
    bet = await BetController.create(
        session=session,
        origin=origin,
    )

    if not bet:
        raise HTTPException(
            status_code=422,
            detail='Can`t create bet for this event.'
        )

    return bet


@router.get(
    '/{bet_id}',
    response_model=BetReturnScheme,
)
async def get_bet_by_id(
    bet_id: str,
    session=Depends(get_session),
):
    event = await BetController.get_by_id(
        session=session,
        id=bet_id,
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail='Event not found',
        )

    return event


@router.get(
    '/',
    response_model=BetsListScheme,
)
async def get_events(
    session=Depends(get_session),
):
    return await BetController.get_all(session=session)
