from __future__ import annotations

import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlmodel import Session, select

from ..database import engine
from ..models import Topic
from ..tasks.fetch import fetch_for_topic, cleanup_old_articles

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def _run_fetch_topic(topic_id: int) -> None:
    def _task():
        with Session(engine) as session:
            topic = session.exec(select(Topic).where(Topic.id == topic_id)).first()
            if not topic or not topic.enabled:
                return
            fetch_for_topic(session, topic)

    await asyncio.to_thread(_task)


def schedule_topics() -> None:
    scheduler.remove_all_jobs()
    with Session(engine) as session:
        topics = session.exec(select(Topic).where(Topic.enabled == True)).all()  # noqa: E712
        for topic in topics:
            minutes = 15 if topic.is_core else 60
            scheduler.add_job(
                _run_fetch_topic,
                "interval",
                minutes=minutes,
                args=[topic.id],
                id=f"topic-{topic.id}",
                replace_existing=True,
            )
            logger.info("已调度主题 %s (%s 分钟)", topic.name_zh, minutes)

    scheduler.add_job(_run_cleanup, "interval", hours=6, id="cleanup", replace_existing=True)


async def _run_cleanup() -> None:
    def _task():
        with Session(engine) as session:
            cleanup_old_articles(session)

    await asyncio.to_thread(_task)


async def trigger_all_fetch() -> None:
    def _task():
        from ..tasks.fetch import fetch_all

        with Session(engine) as session:
            fetch_all(session)

    await asyncio.to_thread(_task)
