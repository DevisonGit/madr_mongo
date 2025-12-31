from bson import ObjectId
from pymongo import ReturnDocument

from app.db.database import get_collection
from app.schemas.user.create import UserCreate


class UserRepository:
    def __init__(self):
        self.collection = get_collection('users')

    async def create(self, new_user: UserCreate):
        result = await self.collection.insert_one(new_user)
        new_user['_id'] = result.inserted_id
        return new_user

    async def delete(self, user_id: str):
        result = await self.collection.delete_one({'_id': ObjectId(user_id)})
        if result.deleted_count == 1:
            return True
        return False

    async def update(self, user_id: str, user: dict):
        result = await self.collection.find_one_and_update(
            {'_id': ObjectId(user_id)},
            {'$set': user},
            return_document=ReturnDocument.AFTER,
        )
        if result is not None:
            return result
        return False
