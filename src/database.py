from collections.abc import AsyncGenerator

from config import Config
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

async_engine = create_async_engine(url=Config().DATABASE_URL, echo=True)

async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)

Base = declarative_base()


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session
