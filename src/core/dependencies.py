from collections.abc import AsyncGenerator

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from repositories import UserRepository
from utils.auth import decode_access_token

from .config import security
from .database import async_session
from .exceptions import HTTPInvalidToken


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session


async def get_current_user(
    token: HTTPAuthorizationCredentials | None = Depends(security),
    session: AsyncSession = Depends(get_session),
) -> User:
    if not token or not token.credentials:
        raise HTTPInvalidToken()
    username = decode_access_token(token.credentials)
    if not username:
        raise HTTPInvalidToken()
    repo = UserRepository(session=session)
    user = await repo.get_user_by_username(username=username)
    if not user:
        raise HTTPInvalidToken()
    return user
