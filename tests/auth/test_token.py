from http import HTTPStatus

import pytest

from app.core.security import create_access_token
from tests.conftest import PASSWORD


@pytest.mark.asyncio
async def test_get_token(client, user):
    response = await client.post(
        '/api/v1/auth/token',
        data={'username': user.email, 'password': PASSWORD},
    )
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


@pytest.mark.asyncio
async def test_get_token_invalid_password(client, user):
    response = await client.post(
        '/api/v1/auth/token',
        data={'username': user.email, 'password': 'invalid'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'error': 'incorrect email or password'}


@pytest.mark.asyncio
async def test_get_token_not_user(client, user):
    response = await client.post(
        '/api/v1/auth/token',
        data={'username': 'invalid', 'password': 'invalid'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'error': 'incorrect email or password'}


@pytest.mark.asyncio
async def test_token_not_subject_email(client, user):
    data = {'test': 'test'}
    token = create_access_token(data)
    response = await client.delete(
        f'/api/v1/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'error': 'could not validate credentials'}


@pytest.mark.asyncio
async def test_token_not_user(client, user):
    data = {'sub': 'test'}
    token = create_access_token(data)
    response = await client.delete(
        f'/api/v1/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'error': 'could not validate credentials'}
