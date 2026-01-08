from pymongo.asynchronous.database import AsyncDatabase
from pymongo.errors import DuplicateKeyError

from app.exceptions.book import BookAlreadyExists
from app.schemas.book.create import BookCreate
from app.schemas.book.public import BookPublic


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

    @staticmethod
    def _to_public(book: dict) -> BookPublic:
        book['id'] = str(book.pop('_id'))
        return BookPublic.model_validate(book)
