from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_update_user(client, user, token):
    response = await client.put(
        f'/api/v1/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'test_update',
            'email': 'test_update@test.com',
            'password': 'test_update',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': 'test_update',
        'email': 'test_update@test.com',
    }


@pytest.mark.asyncio
async def test_update_user_not_found(client, user, token, object_id):
    response = await client.put(
        f'/api/v1/users/{object_id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'test_update',
            'email': 'test_update@test.com',
            'password': 'test_update',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'error': 'user not found'}
