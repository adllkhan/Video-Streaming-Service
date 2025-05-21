from .repositories import UserRepository
from . import schemas
from .models import User


class UserServices:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def get_users(self) -> list[schemas.UsersOut]:
        users_in_db = await self.repository.get_users()
        users = [
            schemas.UsersOut(
                user_id=user.id,
                username=user.username
            ) for user in users_in_db
        ]
        return users

    async def get_user(self, user_id: int) -> schemas.UserOut:
        user_in_db = await self.repository.get_user(user_id)
        if not user_in_db:
            return None # TODO сделать исключение или пустой ответ
        user = schemas.UserOut(
            user_id=user_in_db.id,
            username=user_in_db.username,
            first_name=user_in_db.first_name,
            last_name=user_in_db.last_name
        )
        return user

    async def create_user(self, user: schemas.UserIn) -> schemas.UserOut:
        user_model = User(**user.model_dump())
        user_in_db = await self.repository.create_user(user=user_model)
        user = schemas.UserOut(
            user_id=user_in_db.id,
            username=user_in_db.username,   
            first_name=user_in_db.first_name,
            last_name=user_in_db.last_name
        )
        return user

    async def update_user(
        self, user_id: int, user: schemas.UserIn
    ) -> schemas.UserOut:
        user_in_db = await self.repository.get_user(user_id=user_id)
        if not user_in_db:
            return None # TODO сделать исключение или пустой ответ

        user_model = User(**user.model_dump(), id=user_id)
        user_in_db = await self.repository.update_user(user=user_model)
        user = schemas.UserOut(
            user_id=user_in_db.id,
            username=user_in_db.username,
            first_name=user_in_db.first_name,
            last_name=user_in_db.last_name
        )
        return user

    async def delete_user(self, user_id: int) -> schemas.UserOut:
        # TODO При удалении возвращается либо ничего либо сам юзер

        user_in_db = await self.repository.get_user(user_id=user_id)
        if not user_in_db:
            return None # TODO сделать исключение или пустой ответ

        user_in_db = await self.repository.delete_user(user_id=user_id)
        user = schemas.UserOut(
            user_id=user_in_db.id,
            username=user_in_db.username,
            first_name=user_in_db.first_name,
            last_name=user_in_db.last_name
        )
        return user
        