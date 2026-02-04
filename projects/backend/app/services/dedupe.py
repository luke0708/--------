from __future__ import annotations

import hashlib
import re
from datetime import datetime
from typing import Optional
from difflib import SequenceMatcher


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[\W_]+", "", text)
    return text


def date_bucket(dt: Optional[datetime]) -> str:
    if not dt:
        dt = datetime.utcnow()
    return dt.strftime("%Y-%m-%d")


def build_dedupe_key(title_zh: str, published_at: Optional[datetime]) -> str:
    normalized = normalize_text(title_zh)
    bucket = date_bucket(published_at)
    raw = f"{normalized}:{bucket}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def similarity(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()
