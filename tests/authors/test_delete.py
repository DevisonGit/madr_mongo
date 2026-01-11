from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_delete_author(client, token, author):
    response = await client.delete(
        f'/api/v1/authors/{author.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'author deleted'}


@pytest.mark.asyncio
async def test_delete_author_not_found(client, token, object_id):
    response = await client.delete(
        f'/api/v1/authors/{object_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'error': 'author not found'}


@pytest.mark.asyncio
async def test_delete_author_invalid_id(client, token):
    response = await client.delete(
        '/api/v1/authors/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'error': 'author not found'}
