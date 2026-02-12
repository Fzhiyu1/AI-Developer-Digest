"""Hugging Face 采集器 — /api/trending"""
from collectors.utils import fetch_url, make_id, to_iso_date

API_URL = "https://huggingface.co/api/trending"


def collect(hours: int = 24) -> list[dict]:
    resp = fetch_url(API_URL)
    data = resp.json()
    items = []

    for entry in data.get("recentlyTrending", []):
        repo = entry.get("repoData", {})
        repo_type = entry.get("repoType", "model")
        item = _normalize(repo, repo_type)
        if item:
            items.append(item)

    return items


def _normalize(repo: dict, repo_type: str) -> dict:
    repo_id = repo.get("id", "")
    if not repo_id:
        return None
    url = f"https://huggingface.co/{repo_id}"
    return {
        "id": make_id("huggingface", url),
        "title": repo_id,
        "url": url,
        "source": "huggingface",
        "content_type": "model",
        "date": to_iso_date(repo.get("createdAt", "")),
        "summary": "",
        "score": repo.get("likes", 0),
        "metadata": {
            "type": repo_type,
            "likes": repo.get("likes", 0),
            "downloads": repo.get("downloads", 0),
            "pipeline_tag": repo.get("pipeline_tag", ""),
        },
    }
