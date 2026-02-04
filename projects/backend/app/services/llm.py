from __future__ import annotations

import json
import logging
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import httpx

from ..config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    def __init__(self):
        self.base_url = settings.deepseek.base_url
        self.api_key = settings.deepseek.api_key
        self.model = settings.deepseek.model

    @property
    def enabled(self) -> bool:
        return bool(self.api_key and self.base_url)

    def _endpoint(self) -> str:
        if "chat/completions" in self.base_url:
            return self.base_url
        if self.base_url.endswith("/v1"):
            return f"{self.base_url}/chat/completions"
        return urljoin(self.base_url.rstrip("/") + "/", "v1/chat/completions")

    def chat(self, messages: list[dict[str, str]], temperature: float = 0.2, max_tokens: int = 800) -> str:
        if not self.enabled:
            raise RuntimeError("DeepSeek API 未配置")
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        headers = {"Authorization": f"Bearer {self.api_key}"}
        endpoint = self._endpoint()
        with httpx.Client(timeout=30) as client:
            resp = client.post(endpoint, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as exc:
            raise RuntimeError(f"DeepSeek 响应解析失败: {data}") from exc

    def translate_to_zh(self, text: str) -> str:
        if not text:
            return text
        if not self.enabled:
            return text
        prompt = (
            "请把以下英文新闻标题或摘要翻译成简体中文，保留专有名词。"
            "仅输出译文，不要额外说明。\n\n"
            f"{text}"
        )
        content = self.chat(
            [
                {"role": "system", "content": "你是新闻翻译助手。"},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            max_tokens=500,
        )
        return content.strip()

    def classify_finance(self, title: str, summary: Optional[str]) -> Dict[str, Any]:
        if not self.enabled:
            return {"finance_score": 0.5, "relevance_label": "unknown"}
        prompt = (
            "请判断这条新闻与金融市场的相关性，输出 JSON："
            "{\"finance_score\": 0-1, \"relevance_label\": \"relevant|irrelevant\", \"reason\": \"...\"}."
            "仅输出 JSON。\n\n"
            f"标题: {title}\n摘要: {summary or ''}"
        )
        content = self.chat(
            [
                {"role": "system", "content": "你是金融新闻分类助手。"},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
            max_tokens=300,
        )
        try:
            data = json.loads(_extract_json(content))
            return {
                "finance_score": float(data.get("finance_score", 0.5)),
                "relevance_label": str(data.get("relevance_label", "unknown")),
            }
        except Exception as exc:  # pragma: no cover - LLM 输出异常
            logger.warning("LLM 分类解析失败: %s", exc)
            return {"finance_score": 0.5, "relevance_label": "unknown"}

    def analyze_titles(self, titles: list[str]) -> str:
        if not titles:
            return "未提供标题。"
        if not self.enabled:
            return "DeepSeek API 未配置，无法分析。"
        joined = "\n".join([f"- {title}" for title in titles])
        prompt = (
            "请分析以下新闻标题对经济和金融市场的意义，按标题逐条输出简短要点。"
            "使用简体中文。\n\n"
            f"{joined}"
        )
        content = self.chat(
            [
                {"role": "system", "content": "你是金融分析助手。"},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=800,
        )
        return content.strip()


def _extract_json(text: str) -> str:
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1]
    return text


llm_client = LLMClient()
