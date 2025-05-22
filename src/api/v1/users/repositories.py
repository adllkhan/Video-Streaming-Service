from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
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
        return result.scalars().first()

    async def create_user(self, user: User) -> User:
        self.session.add(user)
        # existing_user = await self.repository.get_user(user=user)
        try:
            await self.session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=f"Username {user.username} is busy!"
            )
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
