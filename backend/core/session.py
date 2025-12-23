# core/deps.py (optional place)
from fastapi import Cookie, HTTPException, Depends
from core.deps import get_db, get_redis
from models.user import User

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
