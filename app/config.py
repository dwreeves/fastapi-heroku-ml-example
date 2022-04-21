import os.path as op
from enum import Enum
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv
from pydantic import BaseSettings
from pydantic import DirectoryPath
from pydantic import PostgresDsn
from pydantic import RedisDsn
from pydantic import validator


APP_ROOT = op.dirname(__file__)

load_dotenv()


class Environment(str, Enum):
    DEVELOPMENT = "DEVELOPMENT"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"


class Settings(BaseSettings):
    ENV: Environment = Environment.DEVELOPMENT
    APP_NAME: str = "Airport Distance Lookup"
    FAVICON_EMOJI: str = "✈️"

    SECRET_KEY: str = str(uuid4())

    DATABASE_URL: PostgresDsn = "postgresql://postgres@postgres:5432/postgres"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return str(self.DATABASE_URL) \
            .replace("postgresql://", "postgresql+asyncpg://", 1)

    @validator("DATABASE_URL", pre=True)
    def validate_database_url(cls, v: str) -> str:
        # Heroku database URL schemes are postgres://, not postgresql://.
        return v.replace("postgres://", "postgresql://")

    REDIS_URL: RedisDsn = "redis://redis:6379/"

    DEFAULT_STATIC_DATA_DIR: DirectoryPath = op.join(APP_ROOT, "db", "data")
    DEFAULT_AIRPORTS_CSV: str = "airports_v1.csv"

    @property
    def DEFAULT_AIRPORTS_CSV_FULL_PATH(self) -> Path:
        return self.DEFAULT_STATIC_DATA_DIR / self.DEFAULT_AIRPORTS_CSV


settings = Settings()
