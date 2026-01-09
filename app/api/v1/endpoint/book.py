from http import HTTPStatus

from fastapi import APIRouter

from app.api.deps.aliases import CurrentUser
from app.api.deps.book import BookFilterDep
from app.api.deps.sevice import BookServiceDep
from app.schemas.book.create import BookCreate
from app.schemas.book.list import BookList
from app.schemas.book.public import BookPublic
from app.schemas.book.update import BookUpdate
from app.schemas.message import Message

router = APIRouter()


@router.post('/', status_code=HTTPStatus.CREATED, response_model=BookPublic)
async def create_book(
    book: BookCreate, current_user: CurrentUser, service: BookServiceDep
):
    return await service.create(book)


@router.delete('/{book_id}', response_model=Message)
async def delete_book(
    book_id: str, current_user: CurrentUser, service: BookServiceDep
):
    return await service.delete(book_id)


@router.put('/{book_id}', response_model=BookPublic)
async def update_book(
    book_id: str,
    current_user: CurrentUser,
    service: BookServiceDep,
    book: BookUpdate,
):
    return await service.update(book_id, book)


@router.get('/{book_id}', response_model=BookPublic)
async def get_book_by_id(book_id: str, service: BookServiceDep):
    return await service.get_book_by_id(book_id)


@router.get('/', response_model=BookList)
async def get_book_filter(service: BookServiceDep, book_filter: BookFilterDep):
    return await service.get_book_filter(book_filter)
