from pydantic import Field

from ..filter import FilterPage


class AuthorFilter(FilterPage):
    name: str | None = Field(None, max_length=20)
