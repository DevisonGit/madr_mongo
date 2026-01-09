from bson import ObjectId
from bson.errors import InvalidId
from pymongo import ReturnDocument
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.errors import DuplicateKeyError

from app.exceptions.book import BookAlreadyExists, BookNotFound
from app.schemas.book.create import BookCreate
from app.schemas.book.public import BookPublic
from app.schemas.book.update import BookUpdate


class BookRepository:
    def __init__(self, db: AsyncDatabase):
        self.collection = db['books']

    async def create(self, book: BookCreate):
        try:
            book_dict = book.model_dump(by_alias=True)
            result = await self.collection.insert_one(book_dict)
            book_dict['_id'] = result.inserted_id
            return self._to_public(book_dict)
        except DuplicateKeyError:
            raise BookAlreadyExists()

    async def delete(self, book_id: str):
        _id = self._parse_object_id(book_id)
        result = await self.collection.delete_one({'_id': _id})
        if result.deleted_count == 1:
            return True
        raise BookNotFound()

    async def update(self, book_id: str, book: BookUpdate):
        _id = self._parse_object_id(book_id)
        book = {
            k: v
            for k, v in book.model_dump(by_alias=True).items()
            if v is not None
        }
        if not book:
            result = await self.collection.find_one({'_id': _id})
            if result is None:
                raise BookNotFound()
        else:
            result = await self.collection.find_one_and_update(
                {'_id': _id},
                {'$set': book},
                return_document=ReturnDocument.AFTER,
            )
            if result is None:
                raise BookNotFound()
        return self._to_public(result)

    @staticmethod
    def _parse_object_id(book_id: str) -> ObjectId:
        try:
            return ObjectId(book_id)
        except InvalidId:
            raise BookNotFound()

    @staticmethod
    def _to_public(book: dict) -> BookPublic:
        book['id'] = str(book.pop('_id'))
        return BookPublic.model_validate(book)
