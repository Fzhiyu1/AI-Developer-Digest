"""采集器共享工具函数"""
import hashlib
import os
import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import urlparse, urlencode, parse_qs

import requests
import feedparser

# 需要绕过代理的域名（本机直连可达的域名）
NO_PROXY_DOMAINS: set[str] = set()


def make_id(source: str, url: str) -> str:
    """生成 source:url_hash 格式的唯一 ID"""
    url_hash = hashlib.md5(url.encode()).hexdigest()[:12]
    return f"{source}:{url_hash}"


TRACKING_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "ref", "source", "fbclid", "gclid", "mc_cid", "mc_eid",
}


def normalize_url(url: str) -> str:
    """URL 归一化：去掉跟踪参数"""
    parsed = urlparse(url)
    params = parse_qs(parsed.query, keep_blank_values=False)
    filtered = {k: v for k, v in params.items() if k.lower() not in TRACKING_PARAMS}
    clean_query = urlencode(filtered, doseq=True) if filtered else ""
    return parsed._replace(query=clean_query).geturl()


def to_iso_date(value) -> str:
    """将各种日期格式统一为 ISO 8601 字符串"""
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=timezone.utc).isoformat()
    if isinstance(value, str):
        s = value.strip()
        if not s:
            return ""
        # 已经是 ISO 格式 (e.g. 2026-02-12T08:00:00Z)
        if re.match(r"\d{4}-\d{2}-\d{2}T", s):
            return s
        # RSS 日期格式 (RFC 2822)
        try:
            return parsedate_to_datetime(s).isoformat()
        except Exception:
            pass
        # 尝试常见格式
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                return datetime.strptime(s, fmt).replace(tzinfo=timezone.utc).isoformat()
            except ValueError:
                continue
    return str(value)


def strip_html(text: str) -> str:
    """去除 HTML 标签和实体，返回纯文本"""
    if not text:
        return ""
    clean = re.sub(r"<[^>]+>", "", text)
    clean = clean.replace("&#8230;", "...").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"')
    return clean.strip()


USER_AGENT = "AI-Daily-Paper/1.0 (https://github.com/AI-Daily-Paper)"


def _needs_no_proxy(url: str) -> bool:
    """检查 URL 是否需要绕过代理"""
    host = urlparse(url).hostname or ""
    return any(host.endswith(d) for d in NO_PROXY_DOMAINS)


def fetch_url(url: str, timeout: int = 15, **kwargs) -> requests.Response:
    """HTTP GET 请求封装，自动对特定域名绕过代理"""
    headers = kwargs.pop("headers", {})
    headers.setdefault("User-Agent", USER_AGENT)
    if _needs_no_proxy(url):
        kwargs.setdefault("proxies", {"http": None, "https": None})
    return requests.get(url, headers=headers, timeout=timeout, **kwargs)


def parse_rss(url: str) -> list:
    """RSS/Atom feed 解析，返回 feedparser entries 列表"""
    feed = feedparser.parse(url, agent=USER_AGENT)
    return feed.entries
