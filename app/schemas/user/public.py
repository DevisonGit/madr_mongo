from typing import Annotated

from pydantic import BeforeValidator

from .base import UserBase

PyObjectId = Annotated[str, BeforeValidator(str)]


class UserPublic(UserBase):
    id: str
