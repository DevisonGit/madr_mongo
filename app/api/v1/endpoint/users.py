from http import HTTPStatus

from fastapi import APIRouter

from app.api.deps.aliases import CurrentUser
from app.api.deps.sevice import UserServiceDep
from app.schemas.message import Message
from app.schemas.user.create import UserCreate
from app.schemas.user.public import UserPublic
from app.schemas.user.update import UserUpdate

router = APIRouter()


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=UserPublic,
    response_model_by_alias=False,
)
async def create_user(user: UserCreate, service: UserServiceDep):
    return await service.create(user)


@router.delete('/{user_id}', response_model=Message)
async def delete_user(
        user_id: str, service: UserServiceDep, current_user: CurrentUser):
    return await service.delete(user_id)


@router.put(
    '/{user_id}', response_model=UserPublic, response_model_by_alias=False
)
async def update_user(user_id: str, user: UserUpdate, service: UserServiceDep):
    return await service.update(user_id, user)
