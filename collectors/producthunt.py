"""Product Hunt 采集器 — Atom Feed"""
from collectors.utils import parse_rss, make_id, to_iso_date

FEED_URL = "https://www.producthunt.com/feed"


def collect(hours: int = 24) -> list[dict]:
    entries = parse_rss(FEED_URL)
    return [_normalize(e) for e in entries]


def _normalize(entry) -> dict:
    url = getattr(entry, "link", "")
    return {
        "id": make_id("producthunt", url),
        "title": getattr(entry, "title", ""),
        "url": url,
        "source": "producthunt",
        "content_type": "product",
        "date": to_iso_date(getattr(entry, "published", "")),
        "summary": getattr(entry, "summary", ""),
        "score": 0,
        "metadata": {
            "votes": 0,
        },
    }
