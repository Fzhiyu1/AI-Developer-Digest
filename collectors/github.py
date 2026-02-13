"""GitHub 采集器 — Trending HTML 抓取 + Search API"""
import os
import re
from datetime import datetime, timedelta
from urllib.parse import quote

from bs4 import BeautifulSoup

from collectors.utils import fetch_url, make_id, to_iso_date


def collect(hours: int = 24) -> list[dict]:
    """拉取 GitHub trending + 近期高 star 新项目"""
    seen_urls = set()
    items = []

    # 主源：HTML 抓取 trending
    for repo in _scrape_trending():
        url = repo["url"]
        if url not in seen_urls:
            seen_urls.add(url)
            items.append(repo)

    # 备源：Search API 新项目
    days = max(1, hours // 24)
    for repo_data in _search_api(days=days):
        url = repo_data["html_url"]
        if url not in seen_urls:
            seen_urls.add(url)
            items.append(_normalize_search(repo_data))

    return items


def _scrape_trending() -> list[dict]:
    """抓取 github.com/trending HTML"""
    try:
        resp = fetch_url("https://github.com/trending?since=daily")
        soup = BeautifulSoup(resp.text, "html.parser")
        items = []
        for article in soup.select("article.Box-row"):
            h2 = article.select_one("h2 a")
            if not h2:
                continue
            href = h2.get("href", "").strip()
            full_name = href.lstrip("/")
            url = f"https://github.com{href}"

            desc_el = article.select_one("p")
            description = desc_el.get_text(strip=True) if desc_el else ""

            # 解析 star 数
            star_el = article.select_one("a[href$='/stargazers']")
            stars = 0
            if star_el:
                stars_text = star_el.get_text(strip=True).replace(",", "")
                stars = int(stars_text) if stars_text.isdigit() else 0

            # 解析今日 star
            today_el = article.select_one("span.d-inline-block.float-sm-right")
            today_stars = 0
            if today_el:
                match = re.search(r"([\d,]+)", today_el.get_text())
                if match:
                    today_stars = int(match.group(1).replace(",", ""))

            # 语言
            lang_el = article.select_one("span[itemprop='programmingLanguage']")
            language = lang_el.get_text(strip=True) if lang_el else ""

            items.append({
                "id": make_id("github", url),
                "title": full_name,
                "url": url,
                "source": "github",
                "content_type": "project",
                "date": to_iso_date(datetime.now().isoformat()),
                "summary": description,
                "score": stars,
                "metadata": {
                    "language": language,
                    "today_stars": today_stars,
                    "full_name": full_name,
                    "topics": [],
                },
            })
        return items
    except Exception:
        return []


MIN_STARS = 50  # 过滤 Search API 中低 star 噪音


def _search_api(days: int = 7, per_page: int = 20) -> list[dict]:
    """GitHub Search API — 近期高 star 新项目（≥ MIN_STARS）"""
    date_str = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    q = f"created:>{date_str} stars:>={MIN_STARS}"
    url = f"https://api.github.com/search/repositories?q={quote(q, safe=':>=')}&sort=stars&order=desc&per_page={per_page}"

    headers = {"Accept": "application/vnd.github.v3+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        resp = fetch_url(url, headers=headers)
        return resp.json().get("items", [])
    except Exception:
        return []


def _normalize_search(repo: dict) -> dict:
    url = repo["html_url"]
    return {
        "id": make_id("github", url),
        "title": repo["full_name"],
        "url": url,
        "source": "github",
        "content_type": "project",
        "date": to_iso_date(repo.get("created_at", "")),
        "summary": repo.get("description", "") or "",
        "score": repo.get("stargazers_count", 0),
        "metadata": {
            "language": repo.get("language", "") or "",
            "today_stars": 0,
            "full_name": repo["full_name"],
            "topics": repo.get("topics", []),
        },
    }
