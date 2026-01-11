from app.repositories.books import BookRepository
from app.schemas.book.create import BookCreate
from app.schemas.book.filter import BookFilter
from app.schemas.book.update import BookUpdate
from app.services.authors import AuthorService
from app.utils.sanitize import sanitize_string


class BookService:
    def __init__(self, repo: BookRepository, author_service: AuthorService):
        self.repo = repo
        self.author_service = author_service

    async def create(self, book: BookCreate):
        await self.author_service.get_author_by_id(book.author_id)
        book.title = sanitize_string(book.title)
        return await self.repo.create(book)

    async def delete(self, book_id: str):
        await self.repo.delete(book_id)
        return {'message': 'book deleted'}

    async def update(self, book_id: str, book: BookUpdate):
        if book.author_id:
            await self.author_service.get_author_by_id(book.author_id)
        if book.title:
            book.title = sanitize_string(book.title)
        return await self.repo.update(book_id, book)

    async def get_book_by_id(self, book_id: str):
        return await self.repo.get_book_by_id(book_id)

    async def get_book_filter(self, book_filter: BookFilter):
        books = await self.repo.get_books_filter(book_filter)
        return {'books': books}
