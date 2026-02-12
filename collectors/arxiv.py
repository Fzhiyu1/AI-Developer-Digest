"""ArXiv 采集器 — RSS Feed"""
from collectors.utils import parse_rss, make_id, to_iso_date

FEED_URLS = [
    "https://rss.arxiv.org/rss/cs.AI",
    "https://rss.arxiv.org/rss/cs.CL",
    "https://rss.arxiv.org/rss/cs.CV",
    "https://rss.arxiv.org/rss/cs.LG",
]

# 保留单一 FEED_URL 用于向后兼容
FEED_URL = FEED_URLS[0]

MAX_ITEMS = 50
MAX_SUMMARY = 300


def collect(hours: int = 24) -> list[dict]:
    seen_urls: set[str] = set()
    items: list[dict] = []
    for feed_url in FEED_URLS:
        entries = parse_rss(feed_url)
        for e in entries:
            url = getattr(e, "link", "")
            if url in seen_urls:
                continue
            seen_urls.add(url)
            items.append(_normalize(e))
            if len(items) >= MAX_ITEMS:
                return items
    return items


def _normalize(entry) -> dict:
    url = getattr(entry, "link", "")
    # 从 abs URL 推导 pdf URL
    pdf_url = url.replace("/abs/", "/pdf/") + ".pdf" if "/abs/" in url else ""

    authors = []
    for a in getattr(entry, "authors", []):
        name = getattr(a, "name", str(a))
        if name:
            authors.append(name)

    categories = [t.term for t in getattr(entry, "tags", [])]

    return {
        "id": make_id("arxiv", url),
        "title": getattr(entry, "title", ""),
        "url": url,
        "source": "arxiv",
        "content_type": "paper",
        "date": to_iso_date(getattr(entry, "published", "")),
        "summary": getattr(entry, "summary", "")[:MAX_SUMMARY],
        "score": 0,
        "metadata": {
            "authors": authors,
            "categories": categories,
            "pdf_url": pdf_url,
        },
    }
