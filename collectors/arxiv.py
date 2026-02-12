"""ArXiv 采集器 — RSS Feed"""
from collectors.utils import parse_rss, make_id, to_iso_date

FEED_URL = "https://rss.arxiv.org/rss/cs.AI"


MAX_ITEMS = 50
MAX_SUMMARY = 300


def collect(hours: int = 24) -> list[dict]:
    entries = parse_rss(FEED_URL)
    return [_normalize(e) for e in entries[:MAX_ITEMS]]


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
