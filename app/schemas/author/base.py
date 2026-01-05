from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: str
    model_config = ConfigDict(
        populate_by_name=True, arbitrary_types_allowed=True
    )
