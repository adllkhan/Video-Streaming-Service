from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from config import Config


url = (
    f"{Config().DATABASE_PROTO}+{Config().DATABASE_DRIVER}"
    f"://{Config().DATABASE_USER}:{Config().DATABASE_PASSWORD}"
    f"@{Config().DATABASE_HOST}:{Config().DATABASE_PORT}/{Config().DATABASE_NAME}"
)
async_engine = create_async_engine(url=url, echo=True)

async_session = async_sessionmaker(
    bind=async_engine, expire_on_commit=False
)

Base = declarative_base()


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session
