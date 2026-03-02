"""Runner — 编排所有采集器，合并去重，输出 JSON"""
import json
import logging
import re
import string
import time
from datetime import datetime
from pathlib import Path

from collectors import hackernews, github, techcrunch, theverge, huggingface, reddit, arxiv, producthunt
from collectors.utils import normalize_url

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

COLLECTORS = [
    ("hackernews", hackernews),
    ("github", github),
    ("techcrunch", techcrunch),
    ("theverge", theverge),
    ("huggingface", huggingface),
    ("reddit", reddit),
    ("producthunt", producthunt),
]


def retry_with_backoff(fn, max_retries: int = 3, base_delay: float = 2):
    """指数退避重试"""
    for attempt in range(max_retries):
        try:
            return fn()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            log.warning(f"重试 {attempt + 1}/{max_retries}，等待 {delay}s: {e}")
            time.sleep(delay)


def _title_words(title: str) -> set[str]:
    """标题转小写、去标点，返回词集合"""
    lowered = title.lower()
    cleaned = lowered.translate(str.maketrans("", "", string.punctuation))
    return set(cleaned.split())


def _titles_similar(t1: str, t2: str, threshold: float = 0.6) -> bool:
    """Jaccard 相似度判断两个标题是否描述同一事件"""
    w1, w2 = _title_words(t1), _title_words(t2)
    if not w1 or not w2:
        return False
    intersection = w1 & w2
    union = w1 | w2
    return len(intersection) / len(union) >= threshold


def _merge_items(existing: dict, new_item: dict) -> dict:
    """合并两条描述同一事件的数据，保留所有来源和最高 score"""
    sources = existing.get("sources", [existing["source"]])
    new_source = new_item["source"]
    if new_source not in sources:
        sources.append(new_source)
    existing["sources"] = sources
    if (new_item.get("score") or 0) > (existing.get("score") or 0):
        existing["score"] = new_item["score"]
    return existing


def _compute_quality_signal(item: dict) -> int:
    """计算质量信号分数"""
    signal = 0
    # 多源出现：每个来源 +2
    sources = item.get("sources", [item.get("source", "")])
    signal += len(sources) * 2
    # score 评分
    score = item.get("score") or 0
    if score >= 500:
        signal += 2
    elif score >= 100:
        signal += 1
    # GitHub stars
    stars = (item.get("metadata") or {}).get("stars") or 0
    if stars >= 10000:
        signal += 2
    elif stars >= 1000:
        signal += 1
    return signal


def run(hours: int = 24, output_dir: str = None) -> list[dict]:
    """执行所有采集器，合并去重，输出 JSON"""
    all_items = []
    source_counts = {}

    for name, collector in COLLECTORS:
        try:
            log.info(f"采集 {name}...")
            items = retry_with_backoff(lambda c=collector: c.collect(hours=hours))
            log.info(f"  {name}: {len(items)} 条")
            source_counts[name] = len(items)
            all_items.extend(items)
        except Exception as e:
            log.error(f"  {name} 失败，跳过: {e}")
            source_counts[name] = 0
            continue

    # URL 归一化 + 标题相似度去重
    seen_urls: dict[str, int] = {}  # normalized_url -> index in unique_items
    unique_items: list[dict] = []
    for item in all_items:
        url = normalize_url(item.get("url", ""))
        title = item.get("title", "")

        # 1) URL 精确匹配
        if url and url in seen_urls:
            idx = seen_urls[url]
            unique_items[idx] = _merge_items(unique_items[idx], item)
            continue

        # 2) 标题相似度匹配
        merged = False
        if title:
            for idx, existing in enumerate(unique_items):
                if _titles_similar(existing.get("title", ""), title):
                    unique_items[idx] = _merge_items(existing, item)
                    if url:
                        seen_urls[url] = idx
                    merged = True
                    break
        if merged:
            continue

        # 新条目
        idx = len(unique_items)
        unique_items.append(item)
        if url:
            seen_urls[url] = idx

    # 计算质量信号
    for item in unique_items:
        item["quality_signal"] = _compute_quality_signal(item)

    log.info(f"总计: {len(all_items)} 条 → 去重后: {len(unique_items)} 条")

    # 输出 JSON
    if output_dir is not None:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        today = datetime.now().strftime("%Y-%m-%d")

        # 完整版（备份）
        full_file = output_path / f"{today}.json"
        with open(full_file, "w", encoding="utf-8") as f:
            json.dump(unique_items, f, ensure_ascii=False, indent=2)
        log.info(f"已保存完整版: {full_file}")

        # 标记前几天出现过的条目
        prev_urls = _load_prev_ids(output_path, today, days=3)
        if prev_urls:
            for item in unique_items:
                if item.get("url") in prev_urls:
                    item["_prev_seen"] = True
            marked = sum(1 for i in unique_items if i.get("_prev_seen"))
            log.info(f"跨天标记: {marked}/{len(unique_items)} 条已在前 3 天出现")

        # 精简版 + 统计摘要（喂给 Claude）
        slim_items = [_slim(item) for item in unique_items]
        type_counts = {}
        for item in unique_items:
            ct = item.get("content_type", "unknown")
            type_counts[ct] = type_counts.get(ct, 0) + 1
        meta = {
            "total_raw": len(all_items),
            "total_deduped": len(unique_items),
            "by_source": source_counts,
            "by_type": type_counts,
            "top_by_source": _top_by_source(unique_items),
        }
        slim_output = {"_meta": meta, "items": slim_items}
        slim_file = output_path / f"{today}-slim.json"
        with open(slim_file, "w", encoding="utf-8") as f:
            json.dump(slim_output, f, ensure_ascii=False, separators=(",", ":"))
        log.info(f"已保存精简版: {slim_file} ({len(slim_items)} 条)")

    return unique_items


def _load_prev_ids(output_path: Path, today: str, days: int = 3) -> set[str]:
    """读取前几天的 slim JSON，收集所有 item ID"""
    from datetime import datetime, timedelta
    prev_ids: set[str] = set()
    today_dt = datetime.strptime(today, "%Y-%m-%d")
    for d in range(1, days + 1):
        date_str = (today_dt - timedelta(days=d)).strftime("%Y-%m-%d")
        prev_file = output_path / f"{date_str}-slim.json"
        if prev_file.exists():
            try:
                with open(prev_file, encoding="utf-8") as f:
                    data = json.load(f)
                items = data.get("items", data) if isinstance(data, dict) else data
                for item in items:
                    if "url" in item:
                        prev_ids.add(item["url"])
            except Exception:
                continue
    return prev_ids


def _top_by_source(items: list[dict], n: int = 3) -> dict[str, list[dict]]:
    """每个数据源的 top N 条目（按 score 降序）"""
    by_source: dict[str, list[dict]] = {}
    for item in items:
        source = item.get("source", "unknown")
        by_source.setdefault(source, []).append(item)
    result = {}
    for source, source_items in by_source.items():
        sorted_items = sorted(source_items, key=lambda x: x.get("score", 0), reverse=True)
        result[source] = [
            {"title": i["title"], "score": i.get("score", 0)}
            for i in sorted_items[:n]
        ]
    return result


def _slim(item: dict) -> dict:
    """精简单条数据，去掉 Claude 日报不需要的字段"""
    s = {
        "title": item["title"],
        "url": item["url"],
        "source": item["source"],
        "type": item["content_type"],
        "date": item["date"],
    }
    if item.get("sources"):
        s["sources"] = item["sources"]
    if item.get("summary"):
        s["summary"] = item["summary"]
    if item.get("score"):
        s["score"] = item["score"]
    if "quality_signal" in item:
        s["qs"] = item["quality_signal"]
    if item.get("_prev_seen"):
        s["prev_seen"] = True
    meta = item.get("metadata", {})
    if meta.get("stars"):
        s["stars"] = meta["stars"]
    if meta.get("ups"):
        s["ups"] = meta["ups"]
    if meta.get("authors"):
        s["authors"] = meta["authors"][:3]
    if meta.get("subreddit"):
        s["sub"] = meta["subreddit"]
    return s


if __name__ == "__main__":
    run(hours=24, output_dir="data")
