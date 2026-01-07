from typing import Annotated

from fastapi import Query

from app.schemas.author.filter import AuthorFilter

AuthorFilterDep = Annotated[AuthorFilter, Query()]
