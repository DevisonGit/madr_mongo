from ..filter import FilterPage


class BookFilter(FilterPage):
    title: str | None = None
    year: int | None = None
