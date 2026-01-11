from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_delete_book(client, book, token):
    response = await client.delete(
        f'/api/v1/books/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'book deleted'}


@pytest.mark.asyncio
async def test_delete_book_not_found(client, author, object_id, token):
    response = await client.delete(
        f'/api/v1/books/{object_id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'error': 'book not found'}


@pytest.mark.asyncio
async def test_delete_book_invalid_id(client, token):
    response = await client.delete(
        '/api/v1/books/1',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'error': 'book not found'}


@pytest.mark.asyncio
async def test_delete_book_not_authenticated(client, author, book):
    response = await client.delete(
        f'/api/v1/books/{book.id}',
        headers={'Authorization': 'Bearer invalid'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'error': 'could not validate credentials'}
