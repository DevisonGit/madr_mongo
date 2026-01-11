from bson import ObjectId
from pymongo import ReturnDocument
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.results import InsertOneResult


class AuthorRepository:
    def __init__(self, db: AsyncDatabase):
        self.collection = db['authors']

    async def create(self, author: dict) -> InsertOneResult:
        result = await self.collection.insert_one(author)
        return result.inserted_id

    async def delete(self, _id: ObjectId) -> bool:
        result = await self.collection.delete_one({'_id': _id})
        return result.deleted_count == 1

    async def update(self, _id: ObjectId, author: dict) -> dict:
        return await self.collection.find_one_and_update(
            {'_id': _id},
            {'$set': author},
            return_document=ReturnDocument.AFTER,
        )

    async def get_author_by_id(self, _id: ObjectId) -> dict:
        return await self.collection.find_one({'_id': _id})

    async def get_authors_filter(self, name: str, limit: int) -> list[dict]:
        cursor = self.collection.find({'name': {'$regex': name}})
        return await cursor.to_list(length=limit)
