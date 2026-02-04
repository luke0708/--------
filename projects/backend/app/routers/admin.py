from __future__ import annotations

import asyncio
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..auth import get_password_hash
from ..database import get_session
from ..deps import require_admin
from ..models import User
from ..schemas import UserCreateRequest
from ..services.scheduler import trigger_all_fetch, schedule_topics

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/users")
def create_user(
    data: UserCreateRequest,
    session: Session = Depends(get_session),
    _: User = Depends(require_admin),
):
    existing = session.exec(select(User).where(User.username == data.username)).first()
    if existing:
        return {"ok": False, "message": "用户已存在"}
    user = User(
        username=data.username,
        password_hash=get_password_hash(data.password),
        role=data.role,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"ok": True, "id": user.id}


@router.post("/fetch")
async def manual_fetch(_: User = Depends(require_admin)):
    asyncio.create_task(trigger_all_fetch())
    schedule_topics()
    return {"ok": True}
