from typing import Optional

from pydantic import BaseModel


class BookUpdate(BaseModel):
    title: Optional[str] = None
    year: Optional[int] = None
    author_id: Optional[str] = None
