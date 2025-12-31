from http import HTTPStatus

from fastapi import APIRouter

from app.schemas.message import Message
from app.schemas.user.create import UserCreate
from app.schemas.user.public import UserPublic
from app.schemas.user.update import UserUpdate
from app.services.users import UserService

router = APIRouter()


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=UserPublic,
    response_model_by_alias=False,
)
async def create_user(user: UserCreate):
    return await UserService().create(user)


@router.delete('/{user_id}', response_model=Message)
async def delete_user(user_id: str):
    return await UserService().delete(user_id)


@router.put(
    '/{user_id}', response_model=UserPublic, response_model_by_alias=False
)
async def update_user(user_id: str, user: UserUpdate):
    return await UserService().update(user_id, user)
