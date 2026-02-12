"""Product Hunt 采集器 — Atom Feed"""
import re

from collectors.utils import parse_rss, make_id, to_iso_date, strip_html

FEED_URL = "https://www.producthunt.com/feed"

AI_KEYWORDS = re.compile(
    r"\b(ai|artificial intelligence|machine learning|ml|deep learning|llm|gpt|"
    r"chatgpt|openai|claude|gemini|copilot|agent|neural|transformer|diffusion|"
    r"stable diffusion|midjourney|generative|nlp|computer vision|model)\b",
    re.IGNORECASE,
)


def _is_ai_related(entry) -> bool:
    text = f"{getattr(entry, 'title', '')} {getattr(entry, 'summary', '')}"
    return AI_KEYWORDS.search(text) is not None


def collect(hours: int = 24) -> list[dict]:
    entries = parse_rss(FEED_URL)
    return [_normalize(e) for e in entries if _is_ai_related(e)]


def _normalize(entry) -> dict:
    url = getattr(entry, "link", "")
    return {
        "id": make_id("producthunt", url),
        "title": getattr(entry, "title", ""),
        "url": url,
        "source": "producthunt",
        "content_type": "product",
        "date": to_iso_date(getattr(entry, "published", "")),
        "summary": strip_html(getattr(entry, "summary", "")),
        "score": 0,
        "metadata": {
            "votes": 0,
        },
    }
