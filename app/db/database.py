from fastapi import Depends
from pymongo import MongoClient

from app.core.settings import settings


def connect_to_mongo() -> MongoClient:
    return MongoClient(settings.mongodb_url)


def get_collection(collection_name: str):
    def _get_collection(
        client: MongoClient = Depends(connect_to_mongo),
    ):
        db = client['madr']
        return db[collection_name]

    return _get_collection
