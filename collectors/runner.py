"""Runner — 编排所有采集器，合并去重，输出 JSON"""
import json
import logging
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
    ("arxiv", arxiv),
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


def run(hours: int = 24, output_dir: str = None) -> list[dict]:
    """执行所有采集器，合并去重，输出 JSON"""
    all_items = []

    for name, collector in COLLECTORS:
        try:
            log.info(f"采集 {name}...")
            items = retry_with_backoff(lambda c=collector: c.collect(hours=hours))
            log.info(f"  {name}: {len(items)} 条")
            all_items.extend(items)
        except Exception as e:
            log.error(f"  {name} 失败，跳过: {e}")
            continue

    # URL 归一化去重
    seen_urls = set()
    unique_items = []
    for item in all_items:
        url = normalize_url(item.get("url", ""))
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_items.append(item)

    log.info(f"总计: {len(all_items)} 条 → 去重后: {len(unique_items)} 条")

    # 输出 JSON
    if output_dir is not None:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        filename = output_path / f"{datetime.now().strftime('%Y-%m-%d')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(unique_items, f, ensure_ascii=False, indent=2)
        log.info(f"已保存: {filename}")

    return unique_items


if __name__ == "__main__":
    run(hours=24, output_dir="data")
