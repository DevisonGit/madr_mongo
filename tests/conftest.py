import logging

import pytest
import pytest_asyncio
from bson import ObjectId
from httpx import ASGITransport, AsyncClient
from pymongo import AsyncMongoClient
from testcontainers.mongodb import MongoDbContainer

from app.core.security import get_password_hash
from app.db.indexes import create_indexes
from app.main import app
from app.schemas.author.public import AuthorPublic
from app.schemas.book.public import BookPublic
from app.schemas.user.public import UserPublic

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
PASSWORD = 'testtest'


@pytest_asyncio.fixture(scope='session')
async def mongo_container():
    with MongoDbContainer('mongo:latest') as mongo:
        yield mongo


@pytest_asyncio.fixture
async def client(mongo_container):
    mongo_url = mongo_container.get_connection_url()
    client = AsyncMongoClient(mongo_url)

    app.database = client['test_db']
    await create_indexes(app.database)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as ac:
        yield ac

    await client.close()


@pytest_asyncio.fixture
async def user():
    user = {
        'username': 'test',
        'email': 'test@test.com',
        'password': get_password_hash(PASSWORD),
    }
    result = await app.database.users.insert_one(user)
    user['id'] = result.inserted_id
    return UserPublic.model_validate(user)


@pytest_asyncio.fixture(autouse=True)
async def clear_database(client):
    yield
    for collection in await app.database.list_collection_names():
        await app.database[collection].delete_many({})


@pytest_asyncio.fixture
async def token(client, user):
    response = await client.post(
        '/api/v1/auth/token',
        data={'username': user.email, 'password': PASSWORD},
    )
    return response.json()['access_token']


@pytest.fixture
def object_id():
    return ObjectId()


@pytest_asyncio.fixture
async def author():
    author = {'name': 'machado 98'}
    result = await app.database.authors.insert_one(author)
    author['id'] = str(result.inserted_id)
    return AuthorPublic.model_validate(author)


@pytest_asyncio.fixture
async def other_author():
    author = {'name': 'paulo urso'}
    result = await app.database.authors.insert_one(author)
    author['id'] = str(result.inserted_id)
    return AuthorPublic.model_validate(author)


@pytest_asyncio.fixture
async def book(author):
    book = {'title': 'test', 'year': 1998, 'author_id': author.id}
    result = await app.database.books.insert_one(book)
    book['id'] = str(result.inserted_id)
    return BookPublic.model_validate(book)
