from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..database import get_session
from ..deps import require_admin, get_current_user
from ..models import Source, User
from ..schemas import SourceCreate, SourceRead, SourceUpdate

router = APIRouter(prefix="/sources", tags=["sources"])


@router.get("", response_model=list[SourceRead])
def list_sources(session: Session = Depends(get_session)):
    sources = session.exec(select(Source)).all()
    return sources


@router.post("", response_model=SourceRead)
def create_source(
    data: SourceCreate,
    session: Session = Depends(get_session),
):
    source = Source(**data.model_dump())
    session.add(source)
    session.commit()
    session.refresh(source)
    return source


@router.patch("/{source_id}", response_model=SourceRead)
def update_source(
    source_id: int,
    data: SourceUpdate,
    session: Session = Depends(get_session),
):
    source = session.get(Source, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="来源不存在")
    updates = data.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(source, key, value)
    session.add(source)
    session.commit()
    session.refresh(source)
    return source
