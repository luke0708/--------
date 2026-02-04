from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..database import get_session
from ..deps import require_admin, get_current_user
from ..models import User
from ..models import Topic
from ..schemas import TopicCreate, TopicRead, TopicUpdate
from ..services.scheduler import schedule_topics

router = APIRouter(prefix="/topics", tags=["topics"])


@router.get("", response_model=list[TopicRead])
def list_topics(session: Session = Depends(get_session), _: User = Depends(get_current_user)):
    topics = session.exec(select(Topic)).all()
    return topics


@router.post("", response_model=TopicRead)
def create_topic(
    data: TopicCreate,
    session: Session = Depends(get_session),
    _: User = Depends(require_admin),
):
    topic = Topic(**data.model_dump())
    session.add(topic)
    session.commit()
    session.refresh(topic)
    schedule_topics()
    return topic


@router.patch("/{topic_id}", response_model=TopicRead)
def update_topic(
    topic_id: int,
    data: TopicUpdate,
    session: Session = Depends(get_session),
    _: User = Depends(require_admin),
):
    topic = session.get(Topic, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="主题不存在")
    updates = data.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(topic, key, value)
    session.add(topic)
    session.commit()
    session.refresh(topic)
    schedule_topics()
    return topic
