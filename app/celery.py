from celery import Celery
from app.config import settings

from redis import Redis

celery_app = Celery(
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

redis = Redis.from_url(settings.REDIS_URL)
