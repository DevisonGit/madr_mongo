from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_create_book(client, author, token):
    response = await client.post(
        '/api/v1/books/',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'test', 'year': 1998, 'author_id': author.id},
    )

    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.asyncio
async def test_create_book_already_exists(client, author, token, book):
    response = await client.post(
        '/api/v1/books/',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': book.title, 'year': 1988, 'author_id': author.id},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'error': 'book already exists'}


@pytest.mark.asyncio
async def test_create_book_not_authenticated(
    client,
    author,
    token,
):
    response = await client.post(
        '/api/v1/books/',
        headers={'Authorization': 'Bearer invalid'},
        json={'title': 'test', 'year': 1988, 'author_id': author.id},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'error': 'could not validate credentials'}


@pytest.mark.asyncio
async def test_create_book_author_not_found(client, token, object_id):
    response = await client.post(
        '/api/v1/books/',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'test', 'year': 1988, 'author_id': str(object_id)},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'error': 'author not found'}
