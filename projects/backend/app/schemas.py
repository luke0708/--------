from __future__ import annotations

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    username: str
    password: str


class UserCreateRequest(BaseModel):
    username: str
    password: str
    role: str = "user"


class TopicRead(BaseModel):
    id: int
    name_zh: str
    name_en: Optional[str]
    keywords: str
    is_core: bool
    enabled: bool


class TopicCreate(BaseModel):
    name_zh: str
    name_en: Optional[str] = None
    keywords: str = ""
    is_core: bool = False
    enabled: bool = True


class TopicUpdate(BaseModel):
    name_zh: Optional[str] = None
    name_en: Optional[str] = None
    keywords: Optional[str] = None
    is_core: Optional[bool] = None
    enabled: Optional[bool] = None


class SourceRead(BaseModel):
    id: int
    name: str
    url: str
    lang: str
    enabled: bool
    priority: int
    topic_id: Optional[int]


class SourceCreate(BaseModel):
    name: str
    url: str
    lang: str = "en"
    enabled: bool = True
    priority: int = 0
    topic_id: Optional[int] = None


class SourceUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    lang: Optional[str] = None
    enabled: Optional[bool] = None
    priority: Optional[int] = None
    topic_id: Optional[int] = None


class ArticleRead(BaseModel):
    id: int
    source_id: int
    url: str
    title_orig: str
    summary_orig: Optional[str]
    lang_orig: str
    published_at: Optional[datetime]
    fetched_at: datetime
    title_zh: str
    summary_zh: Optional[str]
    finance_score: float
    relevance_label: str
    is_primary_lang: bool
    topic_id: Optional[int] = None
    source_name: Optional[str] = None


class ManualAnalysisRequest(BaseModel):
    titles: list[str] = Field(default_factory=list)


class ManualAnalysisResponse(BaseModel):
    request_id: int
    model: str
    response_text: str
    created_at: datetime
