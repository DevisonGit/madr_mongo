from http import HTTPStatus

from fastapi import APIRouter

from app.api.deps.aliases import CurrentUser
from app.api.deps.sevice import AuthorServiceDep
from app.schemas.author.create import AuthorCreate
from app.schemas.author.public import AuthorPublic
from app.schemas.author.update import AuthorUpdate
from app.schemas.message import Message

router = APIRouter()


@router.post('/', status_code=HTTPStatus.CREATED, response_model=AuthorPublic)
async def create_author(
    author: AuthorCreate, current_user: CurrentUser, service: AuthorServiceDep
):
    return await service.create(author)


@router.delete('/{author_id}', response_model=Message)
async def delete_author(
    author_id: str, current_user: CurrentUser, service: AuthorServiceDep
):
    return await service.delete(author_id)


@router.put('/{author_id}', response_model=AuthorPublic)
async def update_author(
    author_id: str,
    author: AuthorUpdate,
    current_user: CurrentUser,
    service: AuthorServiceDep,
):
    return await service.update(author_id, author)
