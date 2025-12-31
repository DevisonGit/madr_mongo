import logging

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from pymongo import AsyncMongoClient
from testcontainers.mongodb import MongoDbContainer

from app.main import app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest_asyncio.fixture(scope='session')
async def mongo_container():
    with MongoDbContainer('mongo:latest') as mongo:
        yield mongo


@pytest_asyncio.fixture
async def client(mongo_container):
    mongo_url = mongo_container.get_connection_url()
    client = AsyncMongoClient(mongo_url)

    app.database = client['test_db']

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as ac:
        yield ac

    await client.close()
