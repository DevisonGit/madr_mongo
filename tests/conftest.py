import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient
from testcontainers.mongodb import MongoDbContainer

from app.db.database import get_collection
from app.main import app


@pytest.fixture(scope='session')
def mongo_container():
    with MongoDbContainer('mongo:7.0') as container:
        yield container


@pytest.fixture(scope='session')
def db_client(mongo_container):
    connection_url = mongo_container.get_connection_url()
    client = MongoClient(connection_url)
    yield client
    client.close()


@pytest.fixture
def client(db_client):

    def override_get_collection():
        yield db_client.test_db

    app.dependency_overrides[get_collection] = override_get_collection

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def clean_db(db_client):
    db_client.drop_database('test_db')
