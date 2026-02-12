"""Reddit 采集器 — JSON 端点"""
import logging

from collectors.utils import fetch_url, make_id, to_iso_date

log = logging.getLogger(__name__)

SUBREDDITS = ["MachineLearning", "LocalLLaMA"]


def collect(hours: int = 24) -> list[dict]:
    items = []
    seen_urls = set()

    for sub in SUBREDDITS:
        url = f"https://www.reddit.com/r/{sub}/hot.json?limit=25"
        try:
            resp = fetch_url(url)
            listing = resp.json()
            for child in listing.get("data", {}).get("children", []):
                post = child.get("data", {})
                post_url = post.get("url", "")
                if not post_url or post_url in seen_urls:
                    continue
                seen_urls.add(post_url)
                items.append(_normalize(post))
        except Exception as e:
            log.warning(f"Reddit r/{sub} 采集失败: {e}")
            continue

    return items


def _normalize(post: dict) -> dict:
    url = post.get("url", "")
    permalink = post.get("permalink", "")
    return {
        "id": make_id("reddit", url),
        "title": post.get("title", ""),
        "url": url,
        "source": "reddit",
        "content_type": "discussion",
        "date": to_iso_date(post.get("created_utc")),
        "summary": (post.get("selftext", "") or "")[:300],
        "score": post.get("score", 0),
        "metadata": {
            "num_comments": post.get("num_comments", 0),
            "flair": post.get("link_flair_text", "") or "",
            "subreddit": post.get("subreddit", ""),
        },
    }
