from app.repositories.users import UserRepository
from app.schemas.user.create import UserCreate
from app.schemas.user.public import UserPublic
from app.schemas.user.update import UserUpdate


class UserService:
    def __init__(self):
        self.repo = UserRepository()

    async def create(self, user: UserCreate) -> UserPublic:
        new_user = user.model_dump(by_alias=True)
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
            return await self.repo.update(user_id, user)
