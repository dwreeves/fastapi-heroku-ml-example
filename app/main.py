from fastapi import Depends
from fastapi import FastAPI
from fastapi import Response
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.routes import app as app_v1
from app.db.core import get_db

app = FastAPI(docs_url=None, redoc_url=None)
app.mount(app=app_v1, path="/api/v1")


@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse("/api/v1/docs")


@app.get("/healthz")
@app.get("/livez")
@app.get("/readyz")
async def health(db: AsyncSession = Depends(get_db)):
    """Health check"""
    await db.execute("select 1;")
    return Response(status_code=200)
