from typing import Annotated

from pydantic import BeforeValidator, Field

from .base import AuthorBase

PyObjectId = Annotated[str, BeforeValidator(str)]


class AuthorPublic(AuthorBase):
    id: str
