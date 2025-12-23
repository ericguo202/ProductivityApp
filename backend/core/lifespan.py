# core/lifespan.py
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis

from core.config import settings
from models.user import Base  # import Base so we can create tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- Postgres engine + sessionmaker (sync) ----
    engine = create_engine(
        str(settings.DATABASE_URL),
        pool_pre_ping=True,
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create tables (dev only; in prod you’d run migrations)
    Base.metadata.create_all(bind=engine)

    # ---- Redis client (sync) ----
    redis_client = redis.from_url(str(settings.REDIS_URL), decode_responses=True)

    # Put them on app.state so deps can access
    app.state.db_engine = engine
    app.state.db_sessionmaker = SessionLocal
    app.state.redis = redis_client

    try:
        yield
    finally:
        engine.dispose()
        try:
            redis_client.close()
        except Exception:
            redis_client.connection_pool.disconnect()
