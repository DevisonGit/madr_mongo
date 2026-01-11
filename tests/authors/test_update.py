from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_update_author(client, token, author):
    response = await client.put(
        f'/api/v1/authors/{author.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Machado 98 update'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': author.id, 'name': 'machado 98 update'}


@pytest.mark.asyncio
async def test_update_author_empty_not_found(client, token, object_id):
    response = await client.put(
        f'/api/v1/authors/{object_id}',
        headers={'Authorization': f'Bearer {token}'},
        json={},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'error': 'author not found'}


@pytest.mark.asyncio
async def test_update_author_not_found(client, token, object_id):
    response = await client.put(
        f'/api/v1/authors/{object_id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'test'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'error': 'author not found'}


@pytest.mark.asyncio
async def test_update_author_object_invalid(client, token, object_id):
    response = await client.put(
        '/api/v1/authors/1',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'test'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'error': 'id of author invalid'}
