from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Iterable, Optional, Tuple

from sqlmodel import Session, select, delete

from ..models import Article, ArticleEnriched, ArticleTopic, FetchRun, Source, Topic
from ..services.dedupe import build_dedupe_key, normalize_text, similarity
from ..services.filter import rule_score, should_use_llm
from ..services.llm import llm_client
from ..services.rss import parse_feed

logger = logging.getLogger(__name__)

RECENT_DAYS = 3
SIMILARITY_THRESHOLD = 0.86


def _split_keywords(raw: str) -> list[str]:
    if not raw:
        return []
    return [kw.strip() for kw in raw.split(",") if kw.strip()]


def _recent_cutoff() -> datetime:
    return datetime.utcnow() - timedelta(days=RECENT_DAYS)


def cleanup_old_articles(session: Session) -> int:
    cutoff = _recent_cutoff()
    old_articles = session.exec(select(Article).where(Article.published_at < cutoff)).all()
    removed = 0
    for article in old_articles:
        session.exec(delete(ArticleEnriched).where(ArticleEnriched.article_id == article.id))
        session.exec(delete(ArticleTopic).where(ArticleTopic.article_id == article.id))
        session.delete(article)
        removed += 1
    session.commit()
    return removed


def _find_similar_enriched(
    session: Session, title_zh: str, published_at: Optional[datetime]
) -> Optional[ArticleEnriched]:
    normalized = normalize_text(title_zh)
    cutoff = _recent_cutoff()
    statement = (
        select(ArticleEnriched, Article)
        .join(Article, Article.id == ArticleEnriched.article_id)
        .where(Article.published_at >= cutoff)
    )
    for enriched, article in session.exec(statement).all():
        if published_at and article.published_at:
            if article.published_at.date() != published_at.date():
                continue
        score = similarity(normalize_text(enriched.title_zh), normalized)
        if score >= SIMILARITY_THRESHOLD:
            return enriched
    return None


def _should_keep(title: str, summary: Optional[str], keywords: Iterable[str]) -> Tuple[bool, float, str]:
    score = rule_score(title, summary, keywords)
    if score < 0.3:
        return False, score, "irrelevant"
    if should_use_llm(score):
        result = llm_client.classify_finance(title, summary)
        label = result.get("relevance_label", "unknown")
        llm_score = float(result.get("finance_score", score))
        if label == "irrelevant" and llm_score < 0.5:
            return False, llm_score, label
        return True, llm_score, label
    return True, score, "relevant"


def _translate_if_needed(lang: str, title: str, summary: Optional[str]) -> Tuple[str, Optional[str]]:
    if lang == "zh":
        return title, summary
    title_zh = llm_client.translate_to_zh(title)
    summary_zh = llm_client.translate_to_zh(summary or "") if summary else None
    return title_zh, summary_zh


def _ensure_primary_lang(
    session: Session, existing: Optional[ArticleEnriched], new_lang: str
) -> bool:
    if not existing:
        return True
    if new_lang == "zh" and not existing.is_primary_lang:
        return True
    if new_lang == "zh":
        existing.is_primary_lang = False
        session.add(existing)
        return True
    return False


def fetch_for_topic(session: Session, topic: Topic) -> int:
    sources = session.exec(select(Source).where(Source.enabled == True)).all()  # noqa: E712
    entries_added = 0
    keywords = _split_keywords(topic.keywords)

    for source in sources:
        if source.topic_id and source.topic_id != topic.id:
            continue

        run = FetchRun(topic_id=topic.id, source_id=source.id, status="running")
        session.add(run)
        session.commit()

        try:
            feed_entries = parse_feed(source.url)
            for entry in feed_entries:
                url = entry.get("link") or ""
                if not url:
                    continue
                exists = session.exec(select(Article).where(Article.url == url)).first()
                if exists:
                    continue

                title = entry.get("title", "").strip()
                summary = (entry.get("summary") or "").strip() or None
                if not title:
                    continue

                if source.topic_id is None and keywords:
                    text_blob = f"{title} {summary or ''}"
                    if not any(kw in text_blob for kw in keywords):
                        continue

                keep, finance_score, label = _should_keep(title, summary, keywords)
                if not keep:
                    continue

                published_at = entry.get("published") or datetime.utcnow()
                title_zh, summary_zh = _translate_if_needed(source.lang, title, summary)
                dedupe_key = build_dedupe_key(title_zh, published_at)

                existing = _find_similar_enriched(session, title_zh, published_at)
                if existing:
                    dedupe_key = existing.dedupe_key

                is_primary = _ensure_primary_lang(session, existing, source.lang)

                article = Article(
                    source_id=source.id,
                    url=url,
                    title_orig=title,
                    summary_orig=summary,
                    lang_orig=source.lang,
                    published_at=published_at,
                )
                session.add(article)
                session.commit()
                session.refresh(article)

                enriched = ArticleEnriched(
                    article_id=article.id,
                    title_zh=title_zh,
                    summary_zh=summary_zh,
                    finance_score=finance_score,
                    relevance_label=label,
                    dedupe_key=dedupe_key,
                    is_primary_lang=is_primary,
                )
                session.add(enriched)
                session.add(ArticleTopic(article_id=article.id, topic_id=topic.id))
                session.commit()
                entries_added += 1

            run.status = "success"
            run.finished_at = datetime.utcnow()
            session.add(run)
            session.commit()
        except Exception as exc:  # pragma: no cover - 网络/解析异常
            logger.exception("抓取失败: %s", exc)
            run.status = "failed"
            run.error = str(exc)
            run.finished_at = datetime.utcnow()
            session.add(run)
            session.commit()

    return entries_added


def fetch_all(session: Session) -> int:
    topics = session.exec(select(Topic).where(Topic.enabled == True)).all()  # noqa: E712
    total = 0
    for topic in topics:
        total += fetch_for_topic(session, topic)
    cleanup_old_articles(session)
    return total
