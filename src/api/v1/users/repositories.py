from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.exceptions import (
    HTTPAlreadyExists,
    HTTPNotFound,
    HTTPValidationError,
    HTTPBadRequest
    )

from .models import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_users(self) -> list[User]:
        stmt = select(User)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_user(self, user_id: int) -> User:
        if user_id <= 0:
            raise HTTPBadRequest(errors={"user_id": "id must be a positive!"})
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalars().first()
        if not user:
            raise HTTPNotFound(model=User, search={"id": user_id})
        return user

    async def create_user(self, user: User) -> User:
        if len(user.username)<3:
            raise HTTPValidationError(errors={"username": "Username must be at least 3 characters long"})
        if not user.first_name or not user.last_name:
            raise HTTPValidationError(errors={"first_name / last_name": "Name fields cannot be empty"})
        self.session.add(user)
        try:
            await self.session.commit()
        except IntegrityError:
            raise HTTPAlreadyExists(model=User, request={"username": user.username})
        await self.session.refresh(user)
        return user

    async def update_user(self, user: User) -> User:
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete_user(self, user_id: int) -> User:
        user = await self.get_user(user_id=user_id)
        if user:
            await self.session.delete(user)
            await self.session.commit()
        return user
