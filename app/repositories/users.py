from bson import ObjectId
from pymongo import ReturnDocument
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.errors import DuplicateKeyError

from app.exceptions.user import UserAlreadyExists, UserNotFound
from app.schemas.user.create import UserCreate


class UserRepository:
    def __init__(self, db: AsyncDatabase):
        self.collection = db['users']

    async def create(self, new_user: dict):
        try:
            result = await self.collection.insert_one(new_user)
            new_user['_id'] = result.inserted_id
            return new_user
        except DuplicateKeyError:
            raise UserAlreadyExists()

    async def delete(self, user_id: str):
        result = await self.collection.delete_one({'_id': ObjectId(user_id)})
        if result.deleted_count == 1:
            return True
        raise UserNotFound()

    async def update(self, user_id: str, user: dict):
        result = await self.collection.find_one_and_update(
            {'_id': ObjectId(user_id)},
            {'$set': user},
            return_document=ReturnDocument.AFTER,
        )
        if result is not None:
            return result
        raise UserNotFound()

    async def read(self, user_id: str):
        result = await self.collection.find_one({'_id': ObjectId(user_id)})
        if result is not None:
            return result
        raise UserNotFound()

    async def read_username(self, username: str) -> UserCreate:
        result = await self.collection.find_one({'email': username})
        if result is not None:
            return UserCreate.model_validate(result)
        raise UserNotFound()
