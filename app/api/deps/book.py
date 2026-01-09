from typing import Annotated

from fastapi import Query

from app.schemas.book.filter import BookFilter

BookFilterDep = Annotated[BookFilter, Query()]
