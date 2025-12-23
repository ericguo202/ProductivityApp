# core/config.py
from pydantic import AnyUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: AnyUrl = "postgresql+psycopg://postgres:postgres@localhost:5431/colab"
    REDIS_URL: AnyUrl = "redis://localhost:6379/0"

    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str = "http://localhost:9000/auth/google/callback"

    # where to send user after successful login
    FRONTEND_URL: str = "http://localhost:5173"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
