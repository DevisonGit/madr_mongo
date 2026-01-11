from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_create_author(client, token):
    response = await client.post(
        '/api/v1/authors/',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Machado 98'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['name'] == 'machado 98'


@pytest.mark.asyncio
async def test_create_author_name_exists(client, token, author):
    response = await client.post(
        '/api/v1/authors/',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': author.name},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'error': 'author already exists'}


@pytest.mark.asyncio
async def test_create_author_not_authenticated(client, author):
    response = await client.post(
        '/api/v1/authors/',
        headers={'Authorization': 'Bearer invalid'},
        json={'name': author.name},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'error': 'could not validate credentials'}
