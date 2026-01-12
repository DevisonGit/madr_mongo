import re

from bson import ObjectId
from bson.errors import InvalidId
from pymongo.errors import DuplicateKeyError

from app.exceptions.author import (
    AuthorAlreadyExists,
    AuthorInvalidId,
    AuthorNotFound,
)
from app.repositories.authors import AuthorRepository
from app.schemas.author.create import AuthorCreate
from app.schemas.author.filter import AuthorFilter
from app.schemas.author.list import AuthorList
from app.schemas.author.public import AuthorPublic
from app.schemas.author.update import AuthorUpdate
from app.schemas.message import Message
from app.utils.sanitize import sanitize_string


class AuthorService:
    def __init__(self, repo: AuthorRepository):
        self.repo = repo

    async def create(self, author: AuthorCreate) -> AuthorPublic:
        author.name = sanitize_string(author.name)
        author_dict = author.model_dump(by_alias=True)

        try:
            author_id = await self.repo.create(author_dict)
        except DuplicateKeyError:
            raise AuthorAlreadyExists()

        author_dict['id'] = str(author_id)
        return AuthorPublic.model_validate(author_dict)

    async def delete(self, author_id: str) -> Message:
        _id = self.parse_object_id(author_id)
        deleted = await self.repo.delete(_id)
        if deleted:
            return Message(message='author deleted')
        raise AuthorNotFound()

    async def update(
        self, author_id: str, author: AuthorUpdate
    ) -> AuthorPublic:
        _id = self.parse_object_id(author_id)
        if author.name:
            author.name = sanitize_string(author.name)
        author = {
            k: v
            for k, v in author.model_dump(by_alias=True).items()
            if v is not None
        }
        if not author:
            return await self.get_author_by_id(author_id)
        updated = await self.repo.update(_id, author)
        if not updated:
            raise AuthorNotFound()
        return self._to_public(updated)

    async def get_author_by_id(self, author_id: str) -> AuthorPublic:
        _id = self.parse_object_id(author_id)
        author = await self.repo.get_author_by_id(_id)
        if not author:
            raise AuthorNotFound()
        return self._to_public(author)

    async def get_authors_filter(
        self, author_filter: AuthorFilter
    ) -> AuthorList:
        authors = []
        if author_filter.name:
            name = re.escape(author_filter.name.lower())
            authors = await self.repo.get_authors_filter(
                name, author_filter.limit
            )
        return AuthorList(
            authors=[self._to_public(author) for author in authors]
        )

    @staticmethod
    def parse_object_id(author_id: str) -> ObjectId:
        try:
            return ObjectId(author_id)
        except InvalidId:
            raise AuthorInvalidId()

    @staticmethod
    def _to_public(author: dict) -> AuthorPublic:
        author['id'] = str(author.pop('_id'))
        return AuthorPublic.model_validate(author)
