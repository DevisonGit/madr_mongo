import re

from bson import ObjectId
from bson.errors import InvalidId
from pymongo.errors import DuplicateKeyError

from app.exceptions.book import BookAlreadyExists, BookNotFound
from app.repositories.books import BookRepository
from app.schemas.book.create import BookCreate
from app.schemas.book.filter import BookFilter
from app.schemas.book.list import BookList
from app.schemas.book.public import BookPublic
from app.schemas.book.update import BookUpdate
from app.schemas.message import Message
from app.services.authors import AuthorService
from app.utils.sanitize import sanitize_string


class BookService:
    def __init__(self, repo: BookRepository, author_service: AuthorService):
        self.repo = repo
        self.author_service = author_service

    async def create(self, book: BookCreate):
        await self.author_service.get_author_by_id(book.author_id)
        book.title = sanitize_string(book.title)
        book_dict = book.model_dump(by_alias=True)
        try:
            result = await self.repo.create(book_dict)
        except DuplicateKeyError:
            raise BookAlreadyExists()
        book_dict['_id'] = result
        return self._to_public(book_dict)

    async def delete(self, book_id: str) -> Message:
        _id = self._parse_object_id(book_id)
        deleted = await self.repo.delete(_id)
        if not deleted:
            raise BookNotFound()
        return Message(message='book deleted')

    async def update(self, book_id: str, book: BookUpdate) -> BookPublic:
        _id = self._parse_object_id(book_id)
        if book.author_id:
            await self.author_service.get_author_by_id(book.author_id)
        if book.title:
            book.title = sanitize_string(book.title)
        book = {
            k: v
            for k, v in book.model_dump(by_alias=True).items()
            if v is not None
        }
        if not book:
            result = await self.repo.get_book_by_id(_id)
        else:
            result = await self.repo.update(_id, book)
        if result is None:
            raise BookNotFound()
        return self._to_public(result)

    async def get_book_by_id(self, book_id: str) -> BookPublic:
        _id = self._parse_object_id(book_id)
        book = await self.repo.get_book_by_id(_id)
        if not book:
            raise BookNotFound()
        return self._to_public(book)

    async def get_book_filter(self, book_filter: BookFilter) -> BookList:
        query = {}
        if book_filter.title:
            escaped = re.escape(book_filter.title.lower())
            query['title'] = {'$regex': escaped}
        if book_filter.year:
            query['year'] = book_filter.year

        books = await self.repo.get_books_filter(query, book_filter.limit)
        return BookList(books=[self._to_public(book) for book in books])

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
