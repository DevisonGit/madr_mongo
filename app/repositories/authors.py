from bson import ObjectId
from bson.errors import InvalidId
from pymongo import ReturnDocument
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.errors import DuplicateKeyError

from app.exceptions.author import AuthorAlreadyExists, AuthorNotFound
from app.schemas.author.base import AuthorBase
from app.schemas.author.public import AuthorPublic
from app.schemas.author.update import AuthorUpdate


class AuthorRepository:
    def __init__(self, db: AsyncDatabase):
        self.collection = db['authors']

    async def create(self, author: AuthorBase):
        try:
            author_dict = author.model_dump(by_alias=True)
            result = await self.collection.insert_one(author_dict)
            author_dict['id'] = str(result.inserted_id)
            return AuthorPublic.model_validate(author_dict)
        except DuplicateKeyError:
            raise AuthorAlreadyExists()

    async def delete(self, author_id: str):
        try:
            result = await self.collection.delete_one(
                {'_id': ObjectId(author_id)})
            if result.deleted_count == 1:
                return True
            raise AuthorNotFound()
        except InvalidId:
            raise AuthorNotFound()

    async def update(self, author_id: str, author: AuthorUpdate):
        try:
            _id = ObjectId(author_id)
        except InvalidId:
            raise AuthorNotFound()
        author = {
            k: v
            for k, v in author.model_dump(by_alias=True).items()
            if v is not None
        }
        if not author:
            result = await self.collection.find_one({'_id': _id})
            if result is None:
                raise AuthorNotFound()
        else:
            result = await self.collection.find_one_and_update(
                {'_id': ObjectId(author_id)},
                {'$set': author},
                return_document=ReturnDocument.AFTER,
            )
            if result is None:
               raise AuthorNotFound()
        result['id'] = str(result.pop('_id'))
        return AuthorPublic.model_validate(result)
