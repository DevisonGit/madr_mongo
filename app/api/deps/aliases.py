from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps.users import get_current_user
from app.schemas.user.public import UserPublic

# dependency


# user
CurrentUser = Annotated[UserPublic, Depends(get_current_user)]


OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
