from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    openrouter_api_key: str = ""
    openrouter_model: str = "google/gemini-2.0-flash-001"
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
