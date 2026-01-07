from app.repositories.authors import AuthorRepository
from app.schemas.author.create import AuthorCreate
from app.schemas.author.filter import AuthorFilter
from app.schemas.author.update import AuthorUpdate
from app.utils.sanitize import sanitize_string


class AuthorService:
    def __init__(self, repo: AuthorRepository):
        self.repo = repo

    async def create(self, author: AuthorCreate):
        author.name = sanitize_string(author.name)
        return await self.repo.create(author)

    async def delete(self, author_id: str):
        await self.repo.delete(author_id)
        return {'message': 'author deleted'}

    async def update(self, author_id: str, author: AuthorUpdate):
        if author.name:
            author.name = sanitize_string(author.name)
        return await self.repo.update(author_id, author)

    async def get_author_by_id(self, author_id: str):
        return await self.repo.get_author_by_id(author_id)

    async def get_authors_filter(self, author_filter: AuthorFilter):
        authors = await self.repo.get_authors_filter(author_filter)
        return {'authors': authors}
