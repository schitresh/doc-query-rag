from os import getenv

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env: str = getenv("BACKEND_ENV", "development")
    host: str = getenv("BACKEND_HOST", "localhost")
    port: int = getenv("BACKEND_PORT", 8000)
    url: str = getenv("BACKEND_URL", "http://localhost:8000")

    postgres_url: str = getenv("POSTGRES_URL") or getenv("DB_URL", "")


class LlmSettings(BaseSettings):
    gemini_api_key: str
    gemini_model: str
    gemini_embedding_model: str = getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001")


settings = Settings()
llm_settings = LlmSettings()
