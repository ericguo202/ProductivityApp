# core/deps.py
from typing import Generator

from fastapi import Request, Depends, Cookie, HTTPException
from sqlalchemy.orm import Session
from redis import Redis


def get_db(request: Request) -> Generator[Session, None, None]:
    SessionLocal = request.app.state.db_sessionmaker
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_redis(request: Request) -> Redis:
    return request.app.state.redis
def get_current_user(
    session_id: str | None = Cookie(default=None),
    db = Depends(get_db),
    redis = Depends(get_redis),
):
    if not session_id:
        raise HTTPException(401, "Not authenticated")

    user_id = redis.get(f"session:{session_id}")
    if not user_id:
        raise HTTPException(401, "Session expired or invalid")

    user = db.query(User).get(int(user_id))
    if not user:
        raise HTTPException(401, "User not found")

    return user