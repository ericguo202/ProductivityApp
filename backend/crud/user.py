# crud/user.py
from sqlalchemy.orm import Session

from models.user import User


def get_or_create_google_user(
    db: Session,
    *,
    google_sub: str,
    email: str,
    name: str | None,
    picture: str | None,
) -> User:
    user = db.query(User).filter(User.google_sub == google_sub).first()
    if user:
        # update basic info in case it changed
        user.email = email
        user.name = name
        user.picture = picture
    else:
        user = User(
            google_sub=google_sub,
            email=email,
            name=name,
            picture=picture,
        )
        db.add(user)
    db.commit()
    db.refresh(user)
    return user
