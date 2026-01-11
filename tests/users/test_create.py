from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post(
        '/api/v1/users/',
        json={
            'username': 'test',
            'email': 'test@test.com',
            'password': 'testtest',
        },
    )

    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.asyncio
async def test_create_user_username_exists(client, user):
    response = await client.post(
        '/api/v1/users/',
        json={
            'username': user.username,
            'email': 'test_another@test.com',
            'password': 'testtest',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'error': 'user already exists'}


@pytest.mark.asyncio
async def test_create_user_email_exists(client, user):
    response = await client.post(
        '/api/v1/users/',
        json={
            'username': 'test_another',
            'email': user.email,
            'password': 'testtest',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'error': 'user already exists'}
