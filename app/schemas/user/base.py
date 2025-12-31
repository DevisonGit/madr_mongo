from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    model_config = ConfigDict(
        populate_by_name=True, arbitrary_types_allowed=True
    )
