from typing import Annotated

from pydantic import BeforeValidator, Field

from .base import UserBase

PyObjectId = Annotated[str, BeforeValidator(str)]


class UserPublic(UserBase):
    id: PyObjectId = Field(alias='_id')
