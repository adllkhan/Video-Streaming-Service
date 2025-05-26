from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.exceptions import (
    HTTPAlreadyExists,
    HTTPNotFound,
    HTTPDatabaseError,
)
from .models import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_users(self) -> list[User]:
        try:
            stmt = select(User)
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise HTTPDatabaseError(error=str(e))

    async def get_user(self, user_id: int) -> User:
        try:
            stmt = select(User).where(User.id == user_id)
            result = await self.session.execute(stmt)
            user = result.scalars().first()
            if not user:
                raise HTTPNotFound(model="User", search={"id": user_id})
            return user
        except SQLAlchemyError as e:
            raise HTTPDatabaseError(error=str(e))

    async def create_user(self, user: User) -> User:
        self.session.add(user)
        try:
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except IntegrityError:
            raise HTTPAlreadyExists(model="User", request={"username": user.username})
        except SQLAlchemyError as e:
            raise HTTPDatabaseError(error=str(e))

    async def update_user(self, user: User) -> User:
        try:
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except SQLAlchemyError as e:
            raise HTTPDatabaseError(error=str(e))

    async def delete_user(self, user_id: int) -> User:
        try:
            user = await self.get_user(user_id=user_id)
            await self.session.delete(user)
            await self.session.commit()
            return user
        except HTTPNotFound:
            raise
        except SQLAlchemyError as e:
            raise HTTPDatabaseError(error=str(e))
