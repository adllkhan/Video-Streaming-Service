from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    async def get_users(self) -> list[User]:
        stmt = select(User)
        async with self.session() as session:
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_user(self, user_id: int) -> User:
        stmt = select(User).where(User.id == user_id)
        async with self.session() as session:
            result = await session.execute(stmt)
            return result.scalars().first()

    async def create_user(self, user: User) -> User:
        async with self.session() as session:
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def update_user(self, user: User) -> User:
        async with self.session() as session:
            await session.merge(user)
            await session.commit()
            await session.refresh(user)
            return user
    
    async def delete_user(self, user_id: int) -> User:
        async with self.session() as session:
            user = await self.get_user(user_id)
            if user:
                await session.delete(user)
                await session.commit()
            return user