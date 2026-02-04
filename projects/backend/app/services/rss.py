from __future__ import annotations

from datetime import datetime
from typing import Any
import feedparser
from dateutil import parser as dateparser


def parse_feed(url: str) -> list[dict[str, Any]]:
    feed = feedparser.parse(url)
    entries = []
    for entry in feed.entries:
        published = None
        if entry.get("published"):
            try:
                published = dateparser.parse(entry.published)
            except (ValueError, TypeError):
                published = None
        summary = entry.get("summary") or entry.get("description")
        entries.append(
            {
                "title": entry.get("title", ""),
                "summary": summary,
                "link": entry.get("link", ""),
                "published": published,
            }
        )
    return entries
