from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.exceptions import HTTPAlreadyExists, HTTPNotFound

from .models import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_users(self) -> list[User]:
        stmt = select(User)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_user(self, user_id: int) -> User:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalars().first()
        if not user:
            raise HTTPNotFound(model=User, request={"user_id": user_id})
        return user

    async def create_user(self, user: User) -> User:
        self.session.add(user)
        try:
            await self.session.commit()
        except IntegrityError:
            raise HTTPAlreadyExists(model=User, request={"username": user.username})
        await self.session.refresh(user)
        return user

    async def update_user(self, user: User) -> User:
        await self.get_user(user_id=user.id)
        merged = await self.session.merge(user)
        await self.session.commit()
        await self.session.refresh(merged)
        return user

    async def delete_user(self, user_id: int) -> User:
        user = await self.get_user(user_id=user_id)
        await self.session.delete(user)
        await self.session.commit()
        return user
