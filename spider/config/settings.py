from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    pguser: str = 'postgres'
    pgpassword: str = 'postgres'
    pgdatabase: str = 'test'
    pghost: str = 'localhost'
    pgport: int = 5432
    sql_echo: bool = False

    model_config = SettingsConfigDict(
        env_prefix='DB_',
        env_file='.env',
        env_file_encoding='utf-8',
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()

