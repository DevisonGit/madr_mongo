from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import create_access_token, verify_password
from app.exceptions.auth import AuthUnauthorized
from app.repositories.users import UserRepository
from app.schemas.user.public import UserPublic


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def read(self, form_data: OAuth2PasswordRequestForm):
        user = await self.repo.read_username(form_data.username)

        if not user:
            raise AuthUnauthorized()

        if not verify_password(form_data.password, user.password):
            raise AuthUnauthorized()

        access_token = create_access_token(data={'sub': user.email})

        return {'access_token': access_token, 'token_type': 'bearer'}

    @staticmethod
    async def refresh_access_token(user: UserPublic):
        new_access_token = create_access_token(data={'sub': user.email})

        return {'access_token': new_access_token, 'token_type': 'bearer'}

    async def validate_current_user(self, email: str):
        return await self.repo.read_username(email)
