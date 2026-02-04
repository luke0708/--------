from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..database import get_session
from ..deps import get_current_user
from ..models import User
from ..models import Article, ArticleEnriched, ArticleTopic, Source
from ..schemas import ArticleRead

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("", response_model=list[ArticleRead])
def list_articles(
    topic_id: Optional[int] = None,
    days: int = 3,
    query: Optional[str] = None,
    limit: int = 200,
    session: Session = Depends(get_session),
):
    cutoff = datetime.utcnow() - timedelta(days=days)

    statement = (
        select(Article, ArticleEnriched, Source, ArticleTopic)
        .join(ArticleEnriched, ArticleEnriched.article_id == Article.id)
        .join(Source, Source.id == Article.source_id)
        .join(ArticleTopic, ArticleTopic.article_id == Article.id, isouter=True)
        .where(Article.published_at >= cutoff)
    )
    if topic_id:
        statement = statement.where(ArticleTopic.topic_id == topic_id)
    if query:
        statement = statement.where(Article.title_orig.contains(query))
    statement = statement.order_by(Article.published_at.desc()).limit(limit)

    results = []
    for article, enriched, source, rel in session.exec(statement).all():
        results.append(
            ArticleRead(
                id=article.id,
                source_id=article.source_id,
                url=article.url,
                title_orig=article.title_orig,
                summary_orig=article.summary_orig,
                lang_orig=article.lang_orig,
                published_at=article.published_at,
                fetched_at=article.fetched_at,
                title_zh=enriched.title_zh,
                summary_zh=enriched.summary_zh,
                finance_score=enriched.finance_score,
                relevance_label=enriched.relevance_label,
                is_primary_lang=enriched.is_primary_lang,
                topic_id=rel.topic_id if rel else None,
                source_name=source.name,
            )
        )
    return results


@router.get("/{article_id}", response_model=ArticleRead)
def get_article(
    article_id: int,
    session: Session = Depends(get_session),
):
    statement = (
        select(Article, ArticleEnriched, Source, ArticleTopic)
        .join(ArticleEnriched, ArticleEnriched.article_id == Article.id)
        .join(Source, Source.id == Article.source_id)
        .join(ArticleTopic, ArticleTopic.article_id == Article.id, isouter=True)
        .where(Article.id == article_id)
    )
    row = session.exec(statement).first()
    if not row:
        raise HTTPException(status_code=404, detail="文章不存在")
    article, enriched, source, rel = row
    return ArticleRead(
        id=article.id,
        source_id=article.source_id,
        url=article.url,
        title_orig=article.title_orig,
        summary_orig=article.summary_orig,
        lang_orig=article.lang_orig,
        published_at=article.published_at,
        fetched_at=article.fetched_at,
        title_zh=enriched.title_zh,
        summary_zh=enriched.summary_zh,
        finance_score=enriched.finance_score,
        relevance_label=enriched.relevance_label,
        is_primary_lang=enriched.is_primary_lang,
        topic_id=rel.topic_id if rel else None,
        source_name=source.name,
    )
