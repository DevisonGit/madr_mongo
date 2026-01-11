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
async def test_delete_user_not_found(client, token):
    response = await client.delete(
        '/api/v1/users/111111111111111111111111',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'error': 'user not found'}


# @pytest.mark.asyncio
# async def test_delete_user_not_authenticated(client, user):
#     response = await client.delete(f'/api/v1/users/{user.id}')
#
#     assert response.status_code == HTTPStatus.UNAUTHORIZED
#     assert response.json() == {'error': 'could not validate credentials'}
