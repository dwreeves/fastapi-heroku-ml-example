import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=DeprecationWarning)
    from celery import Celery

from redis import Redis

from app.config import settings

celery_app = Celery(
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

redis = Redis.from_url(settings.REDIS_URL)
