from pymongo import AsyncMongoClient

from app.core.settings import settings


def connect_to_mongo():
    return AsyncMongoClient(settings.mongodb_url)


def get_collection(collection):
    client = connect_to_mongo()
    db = client.get_database('madr')
    return db.get_collection(collection)
