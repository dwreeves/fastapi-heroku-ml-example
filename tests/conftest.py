import os.path as op
import typing as t

import nest_asyncio
import orjson
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession as _AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.config import settings
from app.db import core as db_core
from app.main import app


# The test client runs an event loop separate of the Pytest event loop.
# Use `nest_asyncio.apply()` to avoid any weird bugs.
nest_asyncio.apply()


TEST_DIR = op.abspath(op.dirname(__file__))
REQUESTS_DIR = op.join(TEST_DIR, "resources", "requests")
RESPONSES_DIR = op.join(TEST_DIR, "resources", "responses")


@pytest.fixture
def client(db) -> TestClient:
    return TestClient(app)


@pytest.fixture
def request_response(request) -> t.Tuple[dict, dict]:
    with open(op.join(REQUESTS_DIR, f"{request.param}.json"), "r") as f:
        req = orjson.loads(f.read())
    with open(op.join(RESPONSES_DIR, f"{request.param}.json"), "r") as f:
        res = orjson.loads(f.read())
    return req, res


@pytest.fixture
async def db(monkeypatch):
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
        db_core,
        "async_engine",
        async_engine
    )
    monkeypatch.setattr(
        db_core,
        "AsyncSession",
        AsyncSession
    )
