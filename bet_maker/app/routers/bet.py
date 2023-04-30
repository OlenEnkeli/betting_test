from fastapi import APIRouter, Depends, HTTPException

from app.core.db import get_session
from app.schemas.bet import (
    BetCreateScheme,
    BetReturnScheme,
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
