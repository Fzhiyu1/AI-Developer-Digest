"""HackerNews 帖子信息查询工具。

用法: python -m tools.hn_info <item_id>
"""

import json
import sys
import urllib.request
import urllib.error
from datetime import datetime


def main():
    if len(sys.argv) < 2:
        print("usage: python -m tools.hn_info <item_id>")
        sys.exit(1)

    item_id = sys.argv[1].strip()
    url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())

        if not data:
            print(f"error: item {item_id} not found")
            sys.exit(1)

        title = data.get("title", "N/A")
        score = data.get("score", 0)
        comments = len(data.get("kids", []))  # descendants 更准确
        if "descendants" in data:
            comments = data["descendants"]
        ts = data.get("time", 0)
        time_str = datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S") if ts else "N/A"
        link = data.get("url", "N/A")

        print(f"title: {title}")
        print(f"score: {score} | comments: {comments}")
        print(f"time: {time_str}")
        print(f"url: {link}")

    except urllib.error.HTTPError as e:
        print(f"error: HTTP {e.code} — {e.reason}")
    except urllib.error.URLError as e:
        print(f"error: {e.reason}")
    except Exception as e:
        print(f"error: {e}")


if __name__ == "__main__":
    main()
