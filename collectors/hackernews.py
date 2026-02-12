"""Hacker News 采集器 — Algolia HN Search API"""
from datetime import datetime, timedelta
from urllib.parse import urlencode

from collectors.utils import fetch_url, make_id, to_iso_date

KEYWORDS = ["AI", "LLM", "GPT", "Claude", "machine learning", "deep learning"]
MIN_POINTS = 10


def collect(hours: int = 24) -> list[dict]:
    """拉取过去 N 小时的 HN AI 相关内容"""
    since = int((datetime.now() - timedelta(hours=hours)).timestamp())
    seen_urls = set()
    items = []

    for keyword in KEYWORDS:
        hits = _search(keyword, since, min_points=MIN_POINTS)
        for h in hits:
            url = h.get("url", "")
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            items.append(_normalize(h))

    # 补充首页热门
    front_hits = _front_page(since)
    for h in front_hits:
        url = h.get("url", "")
        if not url or url in seen_urls:
            continue
        seen_urls.add(url)
        items.append(_normalize(h))

    return items


def _search(query: str, since: int, min_points: int = 10, hits: int = 20) -> list:
    params = urlencode({
        "query": query,
        "tags": "story",
        "numericFilters": f"points>{min_points},created_at_i>{since}",
        "hitsPerPage": hits,
    })
    url = f"https://hn.algolia.com/api/v1/search_by_date?{params}"
    resp = fetch_url(url)
    return resp.json().get("hits", [])


def _front_page(since: int, hits: int = 30) -> list:
    params = urlencode({
        "tags": "front_page",
        "numericFilters": f"created_at_i>{since}",
        "hitsPerPage": hits,
    })
    url = f"https://hn.algolia.com/api/v1/search_by_date?{params}"
    resp = fetch_url(url)
    return resp.json().get("hits", [])


def _normalize(hit: dict) -> dict:
    object_id = hit.get("objectID", "")
    return {
        "id": make_id("hackernews", hit.get("url", object_id)),
        "title": hit.get("title", ""),
        "url": hit.get("url", ""),
        "source": "hackernews",
        "content_type": "news",
        "date": to_iso_date(hit.get("created_at", "")),
        "summary": "",
        "score": hit.get("points", 0),
        "metadata": {
            "num_comments": hit.get("num_comments", 0),
            "author": hit.get("author", ""),
            "hn_url": f"https://news.ycombinator.com/item?id={object_id}",
        },
    }
