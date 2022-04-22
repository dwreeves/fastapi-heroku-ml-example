import time
import typing as t

from asgi_correlation_id import CorrelationIdMiddleware
from asgi_correlation_id.context import correlation_id
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from fastapi.exception_handlers import http_exception_handler
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse
from fastapi.responses import ORJSONResponse
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.depends import get_db
from app.api.v1.routes import router as router_v1
from app.config import settings


app = FastAPI(
    title=settings.APP_NAME,
    docs_url=None,
    default_response_class=ORJSONResponse
)

app.include_router(router_v1)

app.add_middleware(CorrelationIdMiddleware)


@app.middleware("http")
async def time_it(
        request: Request,
        call_next: t.Callable[[Request], t.Awaitable[Response]]
) -> Response:
    start = time.time()
    res = await call_next(request)
    res.headers["X-Process-Time"] = str(time.time() - start)
    return res


@app.exception_handler(Exception)
async def internal_server_error_handler(
        request: Request,
        exc: Exception
) -> JSONResponse:
    return await http_exception_handler(
        request,
        HTTPException(
            500,
            "Internal server error",
            headers={
                "X-Request-ID": correlation_id.get() or "",
                "Access-Control-Expose-Headers": "X-Request-ID"
            }
        ))


@app.get("/docs", include_in_schema=False)
async def docs():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=settings.APP_NAME,
        swagger_favicon_url="/favicon.ico"
    )


@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse("/docs")


@app.get("/healthz")
@app.get("/livez", include_in_schema=False)
@app.get("/readyz", include_in_schema=False)
async def health(db: AsyncSession = Depends(get_db)):
    """Health check"""
    await db.execute("select 1;")
    return Response(status_code=200)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
        f'<text y=".9em" font-size="90">{settings.FAVICON_EMOJI}</text>'
        '</svg>',
        media_type="image/svg+xml"
    )
