from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_delete_user(client, user, token):
    response = await client.delete(
        f'/api/v1/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'user deleted'}


@pytest.mark.asyncio
async def test_delete_user_not_found(client, token, object_id):
    response = await client.delete(
        f'/api/v1/users/{object_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'error': 'user not found'}
