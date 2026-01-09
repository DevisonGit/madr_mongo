from pydantic import BaseModel

from app.schemas.book.public import BookPublic


class BookList(BaseModel):
    books: list[BookPublic]
