from typing import Annotated

from fastapi import Depends, Request

from app.repositories.authors import AuthorRepository
from app.repositories.books import BookRepository
from app.repositories.users import UserRepository
from app.services.auth import AuthService
from app.services.authors import AuthorService
from app.services.books import BookService
from app.services.users import UserService


def user_service(request: Request) -> UserService:
    repo = UserRepository(request.app.database)
    return UserService(repo)


def auth_service(request: Request) -> AuthService:
    repo = UserRepository(request.app.database)
    return AuthService(repo)


def author_service(request: Request) -> AuthorService:
    repo = AuthorRepository(request.app.database)
    return AuthorService(repo)


def book_service(request: Request) -> BookService:
    repo = BookRepository(request.app.database)
    author = author_service(request.app.database)
    return BookService(repo, author)


UserServiceDep = Annotated[UserService, Depends(user_service)]
AuthServiceDep = Annotated[AuthService, Depends(auth_service)]
AuthorServiceDep = Annotated[AuthorService, Depends(author_service)]
BookServiceDep = Annotated[BookService, Depends(book_service)]
