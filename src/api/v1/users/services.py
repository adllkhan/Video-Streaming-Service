from . import schemas
from .models import User
from .repositories import UserRepository
from .utils import hash_password


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def get_users(self) -> list[schemas.UsersOut]:
        users_in_db = await self.repository.get_users()
        users = [
            schemas.UsersOut(user_id=user.id, username=user.username)
            for user in users_in_db
        ]
        return users

    async def get_user(self, user_id: int) -> schemas.UserOut:
        user_in_db = await self.repository.get_user(user_id)
        user = schemas.UserOut(
            user_id=user_in_db.id,
            username=user_in_db.username,
            first_name=user_in_db.first_name,
            last_name=user_in_db.last_name,
        )
        return user

    async def create_user(self, user: schemas.UserIn) -> schemas.UserOut:
        user.password = hash_password(user.password)
        user_model = User(**user.model_dump())
        user_in_db = await self.repository.create_user(user=user_model)
        user = schemas.UserOut(
            user_id=user_in_db.id,
            username=user_in_db.username,
            first_name=user_in_db.first_name,
            last_name=user_in_db.last_name,
        )
        return user

    async def update_user(
        self, update: schemas.UserUpdate, user: User
    ) -> schemas.UserOut:
        user.first_name = update.first_name or user.first_name
        user.last_name = update.last_name or user.last_name
        user.username = update.username or user.username
        user_in_db = await self.repository.update_user(user=user)
        user = schemas.UserOut(
            user_id=user_in_db.id,
            username=user_in_db.username,
            first_name=user_in_db.first_name,
            last_name=user_in_db.last_name,
        )
        return user

    async def delete_user(self, user: User) -> schemas.UserOut:
        user_in_db = await self.repository.delete_user(user=user)
        user = schemas.UserOut(
            user_id=user_in_db.id,
            username=user_in_db.username,
            first_name=user_in_db.first_name,
            last_name=user_in_db.last_name,
        )
        return user
