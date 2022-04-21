import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession as _AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.api import depends
from app.config import settings
from app.main import app


@pytest.fixture
def client(db) -> TestClient:
    return TestClient(app)


@pytest.fixture
def db(monkeypatch):
    # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#using-multiple-asyncio-event-loops
    async_engine = create_async_engine(
        settings.SQLALCHEMY_DATABASE_URI,
        poolclass=NullPool
    )
    AsyncSession = sessionmaker(
        bind=async_engine,
        class_=_AsyncSession
    )
    monkeypatch.setattr(
        depends,
        "AsyncSession",
        AsyncSession
    )
