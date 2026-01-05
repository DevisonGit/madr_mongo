from typing import Optional

from pydantic import BaseModel


class AuthorUpdate(BaseModel):
    name: Optional[str] = None
