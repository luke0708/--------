from __future__ import annotations

from datetime import datetime
from typing import Any
import feedparser
from dateutil import parser as dateparser


import httpx
import logging

logger = logging.getLogger(__name__)

def parse_feed(url: str) -> list[dict[str, Any]]:
    # Use httpx to fetch with User-Agent to avoid 403 Forbidden
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/rss+xml, application/xml, text/xml, */*"
    }
    
    content = None
    try:
        # verify=False to bypass SSL errors (WRONG_VERSION_NUMBER) caused by proxies or legacy servers
        with httpx.Client(timeout=15.0, follow_redirects=True, verify=False) as client:
            resp = client.get(url, headers=headers)
            resp.raise_for_status()
            content = resp.content
    except Exception as e:
        logger.warning(f"Failed to fetch RSS via httpx: {url} Error: {e}")
        # Fallback to feedparser's internal fetcher (unlikely to work if httpx failed due to 403)
        pass

    # Parse content if available, else let feedparser try URL directly
    if content:
        feed = feedparser.parse(content)
    else:
        feed = feedparser.parse(url)

    if not feed.entries and feed.bozo:
        logger.warning(f"Feedparser error for {url}: {feed.bozo_exception}")

    entries = []
    for entry in feed.entries:
        published = None
        if entry.get("published"):
            try:
                published = dateparser.parse(entry.published)
                # Ensure offset-naive datetime is handled or converted to UTC
                if published.tzinfo:
                    published = published.astimezone(datetime.utcnow().tzinfo).replace(tzinfo=None)
            except (ValueError, TypeError):
                published = None
        
        # Fallback to current time if no date
        if not published:
            published = datetime.utcnow()

        summary = entry.get("summary") or entry.get("description") or ""
        entries.append(
            {
                "title": entry.get("title", ""),
                "summary": summary,
                "link": entry.get("link", ""),
                "published": published,
            }
        )
    return entries
