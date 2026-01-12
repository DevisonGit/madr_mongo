from bson import ObjectId
from bson.errors import InvalidId
from pymongo.errors import DuplicateKeyError

from app.core.security import get_password_hash
from app.exceptions.user import UserAlreadyExists, UserInvalidId, UserNotFound
from app.repositories.users import UserRepository
from app.schemas.message import Message
from app.schemas.user.create import UserCreate
from app.schemas.user.public import UserPublic
from app.schemas.user.update import UserUpdate
from app.utils.sanitize import sanitize_string


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create(self, user: UserCreate) -> UserPublic:
        user.username = sanitize_string(user.username)
        user.password = get_password_hash(user.password)
        new_user = user.model_dump(by_alias=True)

        try:
            user_id = await self.repo.create(new_user)
        except DuplicateKeyError:
            raise UserAlreadyExists()
        new_user['_id'] = user_id

        return self._to_public(new_user)

    async def delete(self, user_id: str) -> Message:
        _id = self.parse_object_id(user_id)
        deleted = await self.repo.delete(_id)
        if not deleted:
            raise UserNotFound()
        return Message(message='user deleted')

    async def update(self, user_id: str, user: UserUpdate) -> UserPublic:
        _id = self.parse_object_id(user_id)
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
            result = await self.repo.update(_id, user)
        else:
            result = await self.repo.get_user_by_id(_id)
        if not result:
            raise UserNotFound()
        return self._to_public(result)

    @staticmethod
    def _to_public(user: dict) -> UserPublic:
        user['id'] = str(user.pop('_id'))
        return UserPublic.model_validate(user)

    @staticmethod
    def parse_object_id(author_id: str) -> ObjectId:
        try:
            return ObjectId(author_id)
        except InvalidId:
            raise UserInvalidId()
