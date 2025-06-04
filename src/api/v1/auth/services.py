from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.auth import utils
from src.api.v1.users.repositories import UserRepository


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = UserRepository(session)

    async def authenticate_user(self, username: str, password: str):
        user = await self.repo.get_by_username(username)
        if not user or not utils.verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user
