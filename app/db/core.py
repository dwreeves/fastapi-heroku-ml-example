import typing as t

from sqlalchemy.ext.asyncio import AsyncSession as _AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

Base = declarative_base()


engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
)


__sm = sessionmaker(
    bind=engine,
    class_=_AsyncSession,
    autocommit=False,
    autoflush=False
)


def AsyncSession() -> _AsyncSession:  # noqa
    return __sm()


# Use with fastapi.Depends
async def get_db() -> t.Generator[_AsyncSession, None, None]:
    with AsyncSession() as session:
        session: _AsyncSession
        yield session
