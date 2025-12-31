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
