from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_get_book_id(client, book):
    response = await client.get(f'/api/v1/books/{book.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == book.model_dump()


@pytest.mark.asyncio
async def test_get_book_id_not_found(client, object_id):
    response = await client.get(f'/api/v1/books/{object_id}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'error': 'book not found'}


@pytest.mark.asyncio
async def test_get_book_id_invalid(
    client,
):
    response = await client.get('/api/v1/books/1')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'error': 'book not found'}


@pytest.mark.asyncio
async def test_get_books_filters(client, book):
    response = await client.get(
        f'/api/v1/books/?title={book.title}&year={book.year}'
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'books': [book.model_dump()]}


@pytest.mark.asyncio
async def test_get_books_filter_title(client, book):
    response = await client.get(f'/api/v1/books/?title={book.title}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'books': [book.model_dump()]}


@pytest.mark.asyncio
async def test_get_books_filter_year(client, book):
    response = await client.get(f'/api/v1/books/?year={book.year}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'books': [book.model_dump()]}


@pytest.mark.asyncio
async def test_get_books_filter_empty(client):
    response = await client.get('/api/v1/books/?')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'books': []}
