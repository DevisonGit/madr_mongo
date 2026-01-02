from fastapi import APIRouter

from app.api.deps.aliases import CurrentUser, OAuth2Form
from app.api.deps.sevice import AuthServiceDep
from app.schemas.auth import Token

router = APIRouter()


@router.post('/token', response_model=Token, response_model_by_alias=False)
async def login_for_access_token(
    form_data: OAuth2Form, service: AuthServiceDep
):
    return await service.read(form_data)


@router.post(
    '/refresh_token', response_model=Token, response_model_by_alias=False
)
async def refresh_token(user: CurrentUser, service: AuthServiceDep):
    return await service.refresh_access_token(user)
