from typing import Annotated

from fastapi import Depends, Request

from app.repositories.users import UserRepository
from app.services.auth import AuthService
from app.services.users import UserService


def user_service(request: Request) -> UserService:
    repo = UserRepository(request.app.database)
    return UserService(repo)


def auth_service(request: Request) -> AuthService:
    repo = UserRepository(request.app.database)
    return AuthService(repo)


UserServiceDep = Annotated[UserService, Depends(user_service)]
AuthServiceDep = Annotated[AuthService, Depends(auth_service)]
