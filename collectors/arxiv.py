"""ArXiv 采集器 — RSS Feed + API 充实"""
import logging
import re
import time
import xml.etree.ElementTree as ET

from collectors.utils import fetch_url, parse_rss, make_id, to_iso_date

log = logging.getLogger(__name__)

FEED_URLS = [
    "https://rss.arxiv.org/rss/cs.AI",
    "https://rss.arxiv.org/rss/cs.CL",
]

# 保留单一 FEED_URL 用于向后兼容
FEED_URL = FEED_URLS[0]

MAX_ITEMS = 50
MAX_SUMMARY = 300
ATOM_NS = "{http://www.w3.org/2005/Atom}"


def collect(hours: int = 24) -> list[dict]:
    seen_urls: set[str] = set()
    items: list[dict] = []
    for feed_url in FEED_URLS:
        try:
            entries = parse_rss(feed_url)
        except Exception:
            continue
        for e in entries:
            url = getattr(e, "link", "")
            if url in seen_urls:
                continue
            seen_urls.add(url)
            items.append(_normalize(e))
            if len(items) >= MAX_ITEMS:
                break
        if len(items) >= MAX_ITEMS:
            break
    try:
        _enrich_abstracts(items)
    except Exception as ex:
        log.warning(f"arxiv enrich skipped: {ex}")
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


def _extract_paper_id(url: str) -> str:
    """从 ArXiv URL 提取论文 ID（去版本号）"""
    m = re.search(r"/abs/(\d{4}\.\d{4,6})", url)
    return m.group(1) if m else ""


BATCH_SIZE = 20  # ArXiv API 每批查询数量，避免触发限流


def _enrich_abstracts(items: list[dict]) -> None:
    """批量查询 ArXiv API，用完整摘要和作者替换 RSS 截断数据"""
    base_to_idx: dict[str, int] = {}
    raw_ids: list[str] = []
    for i, item in enumerate(items):
        pid = _extract_paper_id(item.get("url", ""))
        if pid:
            raw_ids.append(pid)
            base_to_idx[pid] = i

    if not raw_ids:
        return

    # 分批查询
    enriched = 0
    for batch_start in range(0, len(raw_ids), BATCH_SIZE):
        batch = raw_ids[batch_start:batch_start + BATCH_SIZE]
        if batch_start > 0:
            time.sleep(1)  # 批间间隔，避免限流

        id_list = ",".join(batch)
        api_url = f"http://export.arxiv.org/api/query?id_list={id_list}&max_results={len(batch)}"

        try:
            resp = fetch_url(api_url, timeout=30)
            if resp.status_code != 200:
                log.warning(f"ArXiv API 返回 {resp.status_code}，跳过本批")
                continue
            if not resp.text.strip().startswith("<?xml"):
                log.warning(f"ArXiv API 返回非 XML: {resp.text[:200]}")
                continue
            root = ET.fromstring(resp.text)
        except Exception as e:
            log.warning(f"ArXiv API 批次 {batch_start // BATCH_SIZE + 1} 失败: {e}")
            continue

        for entry in root.findall(f"{ATOM_NS}entry"):
            id_el = entry.find(f"{ATOM_NS}id")
            if id_el is None or not id_el.text:
                continue
            api_pid = _extract_paper_id(id_el.text.strip())
            idx = base_to_idx.get(api_pid)
            if idx is None:
                continue

            # 充实摘要
            summary_el = entry.find(f"{ATOM_NS}summary")
            if summary_el is not None and summary_el.text:
                abstract = " ".join(summary_el.text.split())
                if len(abstract) > 500:
                    abstract = abstract[:500] + "..."
                items[idx]["summary"] = abstract

            # 充实作者
            authors = []
            for author_el in entry.findall(f"{ATOM_NS}author"):
                name_el = author_el.find(f"{ATOM_NS}name")
                if name_el is not None and name_el.text:
                    authors.append(name_el.text.strip())
            if authors:
                items[idx]["metadata"]["authors"] = authors

            enriched += 1

    log.info(f"ArXiv API 充实: {enriched}/{len(raw_ids)} 篇论文")
