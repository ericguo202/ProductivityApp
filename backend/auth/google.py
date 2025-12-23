# auth/google.py
import secrets
from datetime import timedelta
from urllib.parse import urlencode

import requests
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from redis import Redis
from models.user import User
from core.config import settings
from core.deps import get_db, get_redis
from crud.user import get_or_create_google_user
from core.session import get_current_user

router = APIRouter(prefix="/auth/google", tags=["auth"])

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"

SESSION_TTL_SECONDS = 60 * 60 * 24 * 7  # 7 days


# --------------------- Helpers ---------------------


def exchange_code_for_tokens(code: str) -> dict:
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    resp = requests.post(GOOGLE_TOKEN_URL, data=data, timeout=10)
    if not resp.ok:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to exchange code: {resp.text}",
        )
    return resp.json()


def fetch_google_userinfo(access_token: str) -> dict:
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(GOOGLE_USERINFO_URL, headers=headers, timeout=10)
    if not resp.ok:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to fetch userinfo: {resp.text}",
        )
    return resp.json()


def create_session(redis: Redis, user_id: int) -> str:
    session_id = secrets.token_urlsafe(32)
    key = f"session:{session_id}"
    redis.setex(key, SESSION_TTL_SECONDS, str(user_id))
    return session_id


# --------------------- Routes ---------------------


@router.get("/login")
def google_login(redis: Redis = Depends(get_redis)):
    """
    Step 1: generate Google OAuth URL + state.
    Frontend hits this and then redirects the user to `auth_url`.
    """
    state = secrets.token_urlsafe(32)

    # Save state for CSRF protection
    redis.setex(f"oauth_state:{state}", 600, "google")

    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "include_granted_scopes": "true",
        "state": state,
        "prompt": "consent",
    }

    url = GOOGLE_AUTH_URL + "?" + urlencode(params)
    return {"auth_url": url}


@router.get("/callback")
async def google_callback(
    code: str,
    state: str,
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    """
    Step 2: Google redirects here with `code` and `state`.
    We validate state, exchange code for tokens, fetch userinfo,
    upsert user, create session, and redirect to frontend.
    """
    # 1. Validate state
    state_key = f"oauth_state:{state}"
    stored = redis.get(state_key)
    if stored != "google":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired state",
        )
    redis.delete(state_key)

    # 2. Exchange code -> tokens
    token_data = exchange_code_for_tokens(code)
    access_token = token_data.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No access_token returned from Google",
        )

    # 3. Get userinfo from Google
    userinfo = fetch_google_userinfo(access_token)
    # userinfo typically has: sub, email, name, picture, etc.
    google_sub = userinfo["sub"]
    email = userinfo.get("email")
    name = userinfo.get("name")
    picture = userinfo.get("picture")

    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google did not return an email",
        )

    # 4. Upsert user in Postgres
    user = get_or_create_google_user(
        db,
        google_sub=google_sub,
        email=email,
        name=name,
        picture=picture,
    )

    # 5. Create session in Redis
    session_id = create_session(redis, user.id)

    # 6. Redirect to frontend with session cookie
    redirect_url = f"{settings.FRONTEND_URL}"
    response = RedirectResponse(url=redirect_url, status_code=302)
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=False,  # set True in production with HTTPS
        samesite="lax",
        max_age=SESSION_TTL_SECONDS,
    )
    return response

@router.get("/me")
def get_me(user: User = Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "picture": user.picture,
    }
