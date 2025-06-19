from core.exceptions import HTTPNotFound
from models import User
from repositories import UserRepository
from schemas.users import UserInSchema, UserOutSchema, UserUpdateSchema
from utils.auth import hash_password


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def get_users(self) -> list[UserOutSchema]:
        users = await self.repository.get_users()
        users = [UserOutSchema.model_validate(obj=user) for user in users]
        return users

    async def get_user(self, user_id: int) -> UserOutSchema:
        user = await self.repository.get_user(user_id)
        if not user:
            raise HTTPNotFound(model=User, request={"user_id": user_id})
        return UserOutSchema.model_validate(obj=user)

    async def create_user(self, user: UserInSchema) -> UserOutSchema:
        user.password = hash_password(user.password)
        user = User(**user.model_dump())
        user = await self.repository.create_user(user=user)
        return UserOutSchema.model_validate(obj=user)

    async def update_user(self, update: UserUpdateSchema, user: User) -> UserOutSchema:
        user.first_name = update.first_name or user.first_name
        user.last_name = update.last_name or user.last_name
        user.username = update.username or user.username
        user.password = (
            hash_password(update.password) if update.password else user.password
        )
        user = await self.repository.update_user(user=user)
        return UserOutSchema.model_validate(obj=user)

    async def delete_user(self, user: User) -> UserOutSchema:
        user = await self.repository.delete_user(user=user)
        return UserOutSchema.model_validate(obj=user)
