from http import HTTPStatus

from fastapi import APIRouter

from app.api.deps.aliases import CurrentUser
from app.api.deps.sevice import BookServiceDep
from app.schemas.book.create import BookCreate
from app.schemas.book.public import BookPublic

router = APIRouter()


@router.post('/', status_code=HTTPStatus.CREATED, response_model=BookPublic)
async def create_book(
    book: BookCreate, current_user: CurrentUser, service: BookServiceDep
):
    return await service.create(book)
