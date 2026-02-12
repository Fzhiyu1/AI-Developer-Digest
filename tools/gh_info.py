"""GitHub 项目信息查询工具。

用法: python -m tools.gh_info owner/repo
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime


def api_get(url):
    """发送 GitHub API GET 请求，返回解析后的 JSON。"""
    headers = {"Accept": "application/vnd.github.v3+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def fmt_date(iso_str):
    """将 ISO 8601 日期字符串截取为 YYYY-MM-DD。"""
    if not iso_str:
        return "N/A"
    return iso_str[:10]


def main():
    if len(sys.argv) < 2:
        print("usage: python -m tools.gh_info owner/repo")
        sys.exit(1)

    slug = sys.argv[1].strip("/")
    base = f"https://api.github.com/repos/{slug}"

    try:
        # 基础信息
        repo = api_get(base)
        print(f"repo: {slug}")
        print(f"desc: {repo.get('description') or 'N/A'}")
        print(
            f"stars: {repo.get('stargazers_count', 0)} | "
            f"forks: {repo.get('forks_count', 0)} | "
            f"issues: {repo.get('open_issues_count', 0)} | "
            f"lang: {repo.get('language') or 'N/A'}"
        )
        print(
            f"created: {fmt_date(repo.get('created_at'))} | "
            f"last_push: {fmt_date(repo.get('pushed_at'))}"
        )

        # 最新 release
        try:
            rel = api_get(f"{base}/releases/latest")
            tag = rel.get("tag_name", "N/A")
            pub = fmt_date(rel.get("published_at"))
            print(f"latest_release: {tag} ({pub})")
        except urllib.error.HTTPError:
            print("latest_release: N/A")

        # 最近提交
        try:
            commits = api_get(f"{base}/commits?per_page=5")
            if commits:
                print("recent_commits:")
                for c in commits:
                    commit_info = c.get("commit", {})
                    date = fmt_date(
                        commit_info.get("committer", {}).get("date")
                    )
                    msg = commit_info.get("message", "").split("\n")[0]
                    print(f"  {date} {msg}")
        except urllib.error.HTTPError:
            print("recent_commits: N/A")

    except urllib.error.HTTPError as e:
        print(f"error: HTTP {e.code} — {e.reason}")
    except urllib.error.URLError as e:
        print(f"error: {e.reason}")
    except Exception as e:
        print(f"error: {e}")


if __name__ == "__main__":
    main()
