import typing as t

import httpx
from asgi_correlation_id.context import correlation_id

from app.db.core import AsyncSession


async def get_db() -> t.Generator[AsyncSession, None, None]:
    async with AsyncSession() as db:
        yield db


async def get_http_client() -> t.Generator[httpx.AsyncClient, None, None]:
    headers = {}
    if cid := correlation_id.get():
        headers["X-Request-ID"] = cid
    async with httpx.AsyncClient(headers=headers) as client:
        yield client
