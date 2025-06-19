from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from core.config import config

async_engine = create_async_engine(url=config.DATABASE_URL, echo=True)

async_session = async_sessionmaker(
    bind=async_engine, expire_on_commit=False, autoflush=False
)

Base = declarative_base()
