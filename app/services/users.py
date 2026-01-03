from app.core.security import get_password_hash
from app.repositories.users import UserRepository
from app.schemas.user.create import UserCreate
from app.schemas.user.public import UserPublic
from app.schemas.user.update import UserUpdate
from app.utils.sanitize import sanitize_string


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create(self, user: UserCreate) -> UserPublic:
        new_user = user.model_dump(by_alias=True)
        new_user['username'] = sanitize_string(new_user['username'])
        new_user['password'] = get_password_hash(new_user['password'])
        return await self.repo.create(new_user)

    async def delete(self, user_id: str):
        await self.repo.delete(user_id)
        return {'message': 'user deleted'}

    async def update(self, user_id: str, user: UserUpdate):
        user = {
            k: v
            for k, v in user.model_dump(by_alias=True).items()
            if v is not None
        }
        if len(user) >= 1:
            if user.get('username'):
                user['username'] = sanitize_string(user['username'])
            if user.get('password'):
                user['password'] = get_password_hash(user['password'])
            return await self.repo.update(user_id, user)
        else:
            return await self.repo.read(user_id)
