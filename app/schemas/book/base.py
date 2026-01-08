from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    title: str
    year: int
    author_id: str
    model_config = ConfigDict(
        populate_by_name=True, arbitrary_types_allowed=True
    )
