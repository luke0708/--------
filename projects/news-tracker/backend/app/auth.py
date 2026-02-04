from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext
from sqlmodel import Session, select

from .config import settings
from .models import User

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
ALGORITHM = "HS256"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(session: Session, username: str, password: str) -> Optional[User]:
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)


def ensure_admin_seed(session: Session) -> None:
    existing_admin = None
    if settings.admin_username:
        existing_admin = session.exec(
            select(User).where(User.username == settings.admin_username)
        ).first()
    if existing_admin:
        return

    any_user = session.exec(select(User)).first()
    if any_user:
        return

    username = settings.admin_username or "admin"
    password = settings.admin_password or "change_me"
    user = User(
        username=username,
        password_hash=get_password_hash(password),
        role="admin",
    )
    session.add(user)
    session.commit()
