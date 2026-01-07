from pydantic import BaseModel

from .public import AuthorPublic


class AuthorList(BaseModel):
    authors: list[AuthorPublic]
