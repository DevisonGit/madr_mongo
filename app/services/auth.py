from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import create_access_token, verify_password
from app.exceptions.auth import AuthCredentialsValidate, AuthUnauthorized
from app.repositories.users import UserRepository
from app.schemas.user.create import UserCreate
from app.schemas.user.public import UserPublic


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def read(self, form_data: OAuth2PasswordRequestForm):
        user = await self.repo.get_user_by_username(form_data.username)

        if not user:
            raise AuthUnauthorized()

        user = UserCreate.model_validate(user)

        if not verify_password(form_data.password, user.password):
            raise AuthUnauthorized()

        access_token = create_access_token(data={'sub': user.email})

        return {'access_token': access_token, 'token_type': 'bearer'}

    @staticmethod
    async def refresh_access_token(user: UserPublic):
        new_access_token = create_access_token(data={'sub': user.email})

        return {'access_token': new_access_token, 'token_type': 'bearer'}

    async def validate_current_user(self, email: str):
        user = await self.repo.get_user_by_username(email)
        if not user:
            raise AuthCredentialsValidate()
        user['id'] = str(user.pop('_id'))
        return UserPublic.model_validate(user)
