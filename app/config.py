import typing as t
from enum import Enum

from pydantic import BaseSettings
from pydantic import PostgresDsn
from pydantic import RedisDsn
from pydantic import validator
from pydantic import Field
from pydantic import PrivateAttr
from pydantic import root_validator
from dotenv import load_dotenv


load_dotenv()


class Environment(str, Enum):
    DEVELOPMENT = "DEVELOPMENT"
    INTEGRATION = "INTEGRATION"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"


class Settings(BaseSettings):
    ENV: Environment = Environment.DEVELOPMENT
    DATABASE_URL: PostgresDsn = "postgresql://postgres@postgres:5432/postgres"
    REDIS_URL: RedisDsn = "redis://redis:6379/"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return str(self.DATABASE_URL).replace("postgresql", "postgresql+asyncpg", 1)


settings = Settings()
