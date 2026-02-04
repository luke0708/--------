from __future__ import annotations

from typing import Iterable, Optional

FINANCE_KEYWORDS = {
    "美联储": 0.3,
    "利率": 0.25,
    "美元": 0.2,
    "关税": 0.2,
    "股市": 0.2,
    "股价": 0.2,
    "债券": 0.2,
    "国债": 0.2,
    "黄金": 0.3,
    "原油": 0.2,
    "通胀": 0.25,
    "就业": 0.15,
    "GDP": 0.2,
    "汇率": 0.2,
    "央行": 0.2,
    "监管": 0.15,
    "银行": 0.15,
    "财政": 0.2,
    "税": 0.1,
}

NEGATIVE_KEYWORDS = {
    "八卦": 0.3,
    "娱乐": 0.3,
    "体育": 0.2,
    "影视": 0.2,
    "绯闻": 0.3,
}


def rule_score(title: str, summary: Optional[str], extra_keywords: Optional[Iterable[str]] = None) -> float:
    text = f"{title} {summary or ''}"
    text_lower = text.lower()
    score = 0.0
    for keyword, weight in FINANCE_KEYWORDS.items():
        if keyword in text or keyword.lower() in text_lower:
            score += weight
    if extra_keywords:
        for kw in extra_keywords:
            if kw and (kw in text or kw.lower() in text_lower):
                score += 0.3

    for keyword, weight in NEGATIVE_KEYWORDS.items():
        if keyword in text or keyword.lower() in text_lower:
            score -= weight

    return max(0.0, min(1.0, score))


def should_use_llm(score: float) -> bool:
    return 0.3 <= score <= 0.7
