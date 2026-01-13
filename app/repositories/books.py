from bson import ObjectId
from pymongo import ReturnDocument
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.results import InsertOneResult


class BookRepository:
    def __init__(self, db: AsyncDatabase):
        self.collection = db['books']

    async def create(self, book: dict) -> InsertOneResult:
        result = await self.collection.insert_one(book)
        return result.inserted_id

    async def delete(self, _id: ObjectId) -> bool:
        result = await self.collection.delete_one({'_id': _id})
        return result.deleted_count == 1

    async def update(self, _id: ObjectId, book: dict) -> dict:
        return await self.collection.find_one_and_update(
            {'_id': _id},
            {'$set': book},
            return_document=ReturnDocument.AFTER,
        )

    async def get_book_by_id(self, _id: ObjectId):
        return await self.collection.find_one({'_id': _id})

    async def get_books_filter(self, query: dict, limit: int) -> list[dict]:
        cursor = self.collection.find(query)
        return await cursor.to_list(length=limit)
