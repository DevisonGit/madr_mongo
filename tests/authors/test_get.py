from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_get_author_id(client, author):
    response = await client.get(f'/api/v1/authors/{author.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': author.id, 'name': author.name}


@pytest.mark.asyncio
async def test_get_author_id_not_found(client, object_id):
    response = await client.get(f'/api/v1/authors/{object_id}')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'error': 'author not found'}


@pytest.mark.asyncio
async def test_get_author_id_invalid(client, object_id):
    response = await client.get('/api/v1/authors/1')

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'error': 'id of author invalid'}


@pytest.mark.asyncio
async def test_get_author_filter(client):
    response = await client.get('/api/v1/authors/?name=')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'authors': []}


@pytest.mark.asyncio
async def test_get_author_filter_with_author(client, author):
    response = await client.get('/api/v1/authors/?name=mach')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'authors': [{'name': author.name, 'id': author.id}]
    }
