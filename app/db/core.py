import typing as t

from sqlalchemy.ext.asyncio import AsyncSession as _AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings


Base = declarative_base()


async_engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    pool_size=5,
    pool_recycle=10,
    max_overflow=10
)

AsyncSession: t.Type[_AsyncSession] = sessionmaker(
    bind=async_engine,
    class_=_AsyncSession,
)
