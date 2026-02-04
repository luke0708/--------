from __future__ import annotations

from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password_hash: str
    role: str = Field(default="user")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Topic(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name_zh: str = Field(index=True)
    name_en: Optional[str] = None
    keywords: str = Field(default="")
    is_core: bool = Field(default=False)
    enabled: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Source(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    url: str
    lang: str = Field(default="en")
    enabled: bool = Field(default=True)
    priority: int = Field(default=0)
    topic_id: Optional[int] = Field(default=None, foreign_key="topic.id")


class Article(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    source_id: int = Field(foreign_key="source.id")
    url: str = Field(index=True)
    title_orig: str
    summary_orig: Optional[str] = None
    lang_orig: str = Field(default="en")
    published_at: Optional[datetime] = None
    fetched_at: datetime = Field(default_factory=datetime.utcnow)


class ArticleEnriched(SQLModel, table=True):
    article_id: int = Field(foreign_key="article.id", primary_key=True)
    title_zh: str
    summary_zh: Optional[str] = None
    finance_score: float = Field(default=0.0)
    relevance_label: str = Field(default="unknown")
    dedupe_key: str = Field(index=True)
    is_primary_lang: bool = Field(default=True)


class ArticleTopic(SQLModel, table=True):
    article_id: int = Field(foreign_key="article.id", primary_key=True)
    topic_id: int = Field(foreign_key="topic.id", primary_key=True)


class ManualRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    titles_json: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ManualResponse(SQLModel, table=True):
    request_id: int = Field(foreign_key="manualrequest.id", primary_key=True)
    model: str
    response_text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class FetchRun(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    topic_id: Optional[int] = Field(default=None, foreign_key="topic.id")
    source_id: Optional[int] = Field(default=None, foreign_key="source.id")
    status: str = Field(default="running")
    started_at: datetime = Field(default_factory=datetime.utcnow)
    finished_at: Optional[datetime] = None
    error: Optional[str] = None
