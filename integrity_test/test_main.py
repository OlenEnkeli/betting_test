import asyncio

from datetime import datetime as dt
from datetime import timedelta as td

import httpx
import pytest

from config import config


@pytest.mark.asyncio
async def test_main():
    """ Тест предусматривает работу с поднятым Docker окружением"""

    assert config.LINE_PROVER_API_URL is not None
    assert config.BET_MAKER_API_URL is not None

    test_event_id = 'test_event'
    test_event_coefficient = 12.0

    async with httpx.AsyncClient() as client:

        # Удаляем событие с id 'test_event', если оно есть
        resp = await client.delete(
            f'{config.LINE_PROVER_API_URL}/events/{test_event_id}'
        )
        assert resp.status_code in (200, 404)

        # Создаем событие с id 'test_event'
        resp = await client.post(
            f'{config.LINE_PROVER_API_URL}/events/',
            json={
                'event_id': test_event_id,
                'coefficient': test_event_coefficient,
                'deadline': str(dt.now() + td(seconds=5)),
                'state': 'new',
            }
        )

        json = resp.json()
        assert resp.status_code == 200
        assert json['event_id'] == test_event_id
        assert json['state'] == 'new'

        # Делаем ставку
        await asyncio.sleep(2)
        resp = await client.post(
            f'{config.BET_MAKER_API_URL}/bets/',
            json={
                'event_id': test_event_id,
                'amount': 10000,
            }
        )

        json = resp.json()
        assert resp.status_code == 200
        bet_id = json['bet_id']


        # Ждем, пока событие завершится и его проверяем статус
        await asyncio.sleep(3)
        resp = await client.get(
            f'{config.LINE_PROVER_API_URL}/events/{test_event_id}'
        )

        json = resp.json()
        assert resp.status_code == 200
        assert json['state'] != 'new'
        line_state = json['state']

        # Проверяем статус ставки
        resp = await client.get(
            f'{config.BET_MAKER_API_URL}/bets/{bet_id}',
        )

        json = resp.json()
        assert resp.status_code == 200
        assert json['bet_id'] == bet_id
        if line_state == 'finished_win':
            assert json['state'] == 'win'
        else:
            assert json['state'] == 'lose'
