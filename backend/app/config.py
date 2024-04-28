from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    auth_token_secret: str = Field("xxx", alias="TOKEN_SECRET")
    auth_token_alg: str = "HS256"
    db_file_path: str = "/pasynkov.db"

    model_config = SettingsConfigDict(env_file='.env', extra=None)


@lru_cache
def get_settings():
    return Settings()
