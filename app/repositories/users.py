from bson import ObjectId
from pymongo import ReturnDocument
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.results import InsertOneResult


class UserRepository:
    def __init__(self, db: AsyncDatabase):
        self.collection = db['users']

    async def create(self, new_user: dict) -> InsertOneResult:
        result = await self.collection.insert_one(new_user)
        return result.inserted_id

    async def delete(self, _id: ObjectId) -> bool:
        result = await self.collection.delete_one({'_id': _id})
        return result.deleted_count == 1

    async def update(self, _id: ObjectId, user: dict) -> dict:
        return await self.collection.find_one_and_update(
            {'_id': _id},
            {'$set': user},
            return_document=ReturnDocument.AFTER,
        )

    async def get_user_by_id(self, _id: ObjectId) -> dict:
        return await self.collection.find_one({'_id': _id})

    async def get_user_by_username(self, username: str) -> dict:
        return await self.collection.find_one({'email': username})
