from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.exceptions import HTTPAlreadyExists, HTTPFieldAlreadyTaken
from models import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_users(self) -> list[User]:
        stmt = select(User)
        result = await self.session.scalars(stmt)
        return result.all()

    async def get_user(self, user_id: int) -> User:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.scalars(stmt)
        return result.first()

    async def get_user_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result = await self.session.scalars(stmt)
        return result.first()

    async def create_user(self, user: User) -> User:
        self.session.add(user)
        try:
            await self.session.commit()
        except IntegrityError:
            raise HTTPAlreadyExists(model=User, request={"username": user.username})
        await self.session.refresh(user)
        return user

    async def update_user(self, user: User) -> User:
        check = await self.get_user_by_username(user.username)
        if check and check.id != user.id:
            raise HTTPFieldAlreadyTaken(field="username", value=user.username)
        merged = await self.session.merge(user)
        await self.session.commit()
        await self.session.refresh(merged)
        return user

    async def delete_user(self, user: User) -> User:
        await self.session.delete(user)
        await self.session.commit()
        return user
