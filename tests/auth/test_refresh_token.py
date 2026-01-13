from http import HTTPStatus

import pytest
from freezegun import freeze_time

from tests.conftest import PASSWORD

TIME_INITIAL = '2025-01-01 12:00:00'
TIME_FINAL = '2025-01-01 13:00:01'


@pytest.mark.asyncio
async def test_refresh_token(client, token):
    response = await client.post(
        '/api/v1/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token


@pytest.mark.asyncio
async def test_refresh_token_expired_after_time(client, user):
    with freeze_time(TIME_INITIAL):
        response = await client.post(
            '/api/v1/auth/token',
            data={'username': user.email, 'password': PASSWORD},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']
    with freeze_time(TIME_FINAL):
        response = await client.post(
            '/api/v1/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'error': 'could not validate credentials'}
