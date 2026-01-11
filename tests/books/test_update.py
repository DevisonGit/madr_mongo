from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_update_book(client, book, token):
    response = await client.put(
        f'/api/v1/books/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'test_update',
            'year': 2005,
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': book.id,
        'author_id': book.author_id,
        'title': 'test_update',
        'year': 2005,
    }


@pytest.mark.asyncio
async def test_update_book_not_found(client, object_id, token):
    response = await client.put(
        f'/api/v1/books/{object_id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'test_update',
            'year': 2005,
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'error': 'book not found'}


@pytest.mark.asyncio
async def test_update_book_not_found_empty(client, object_id, token):
    response = await client.put(
        f'/api/v1/books/{object_id}',
        headers={'Authorization': f'Bearer {token}'},
        json={},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'error': 'book not found'}


@pytest.mark.asyncio
async def test_update_book_empty(client, book, token):
    response = await client.put(
        f'/api/v1/books/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == book.model_dump()


@pytest.mark.asyncio
async def test_update_book_not_authenticated(client, book):
    response = await client.put(
        f'/api/v1/books/{book.id}',
        headers={'Authorization': 'Bearer invalid'},
        json={},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'error': 'could not validate credentials'}


@pytest.mark.asyncio
async def test_update_book_author(client, book, other_author, token):
    response = await client.put(
        f'/api/v1/books/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'author_id': other_author.id},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': book.id,
        'author_id': other_author.id,
        'title': book.title,
        'year': book.year,
    }
