from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ..auth import authenticate_user, create_access_token
from ..database import get_session
from ..deps import get_current_user
from ..models import User
from ..schemas import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, session: Session = Depends(get_session)) -> TokenResponse:
    user = authenticate_user(session, data.username, data.password)
    if not user:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    token = create_access_token({"sub": user.username})
    return TokenResponse(access_token=token)


@router.post("/refresh", response_model=TokenResponse)
def refresh(user: User = Depends(get_current_user)) -> TokenResponse:
    token = create_access_token({"sub": user.username})
    return TokenResponse(access_token=token)
