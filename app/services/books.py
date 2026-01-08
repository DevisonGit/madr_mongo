from app.repositories.authors import AuthorRepository
from app.repositories.books import BookRepository
from app.schemas.book.create import BookCreate
from app.utils.sanitize import sanitize_string


class BookService:
    def __init__(self, repo: BookRepository, author_repo: AuthorRepository):
        self.repo = repo
        self.author_repo = author_repo

    async def create(self, book: BookCreate):
        await self.author_repo.get_author_by_id(book.author_id)
        book.title = sanitize_string(book.title)
        return await self.repo.create(book)
