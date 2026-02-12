"""TechCrunch 采集器 — AI 分类 RSS"""
from collectors.utils import parse_rss, make_id, to_iso_date

FEED_URL = "https://techcrunch.com/category/artificial-intelligence/feed/"


def collect(hours: int = 24) -> list[dict]:
    entries = parse_rss(FEED_URL)
    return [_normalize(e) for e in entries]


def _normalize(entry) -> dict:
    url = getattr(entry, "link", "")
    tags = [t.term for t in getattr(entry, "tags", [])]
    return {
        "id": make_id("techcrunch", url),
        "title": getattr(entry, "title", ""),
        "url": url,
        "source": "techcrunch",
        "content_type": "news",
        "date": to_iso_date(getattr(entry, "published", "")),
        "summary": getattr(entry, "summary", ""),
        "score": 0,
        "metadata": {
            "categories": tags,
            "author": getattr(entry, "author", ""),
        },
    }
