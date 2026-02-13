"""测试 Hacker News 采集器"""
from unittest.mock import patch, MagicMock
from collectors.hackernews import collect, KEYWORDS


MOCK_ALGOLIA_RESPONSE = {
    "hits": [
        {
            "title": "GPT-5 Released",
            "url": "https://openai.com/blog/gpt5",
            "points": 500,
            "num_comments": 300,
            "author": "pg",
            "created_at": "2026-02-12T08:00:00.000Z",
            "objectID": "12345",
        }
    ],
    "nbHits": 1,
}


class TestHackernewsCollect:
    @patch("collectors.hackernews.fetch_url")
    def test_returns_unified_format(self, mock_fetch):
        mock_resp = MagicMock()
        mock_resp.json.return_value = MOCK_ALGOLIA_RESPONSE
        mock_fetch.return_value = mock_resp

        items = collect(hours=24)
        assert len(items) >= 1
        item = items[0]
        assert item["source"] == "hackernews"
        assert item["content_type"] == "news"
        assert item["title"] == "GPT-5 Released"
        assert item["url"] == "https://openai.com/blog/gpt5"
        assert item["score"] == 500
        assert "id" in item
        assert "date" in item
        assert "metadata" in item
        assert item["metadata"]["num_comments"] == 300
        assert item["metadata"]["author"] == "pg"

    @patch("collectors.hackernews.fetch_url")
    def test_deduplicates_across_keywords(self, mock_fetch):
        mock_resp = MagicMock()
        mock_resp.json.return_value = MOCK_ALGOLIA_RESPONSE
        mock_fetch.return_value = mock_resp

        items = collect(hours=24)
        urls = [i["url"] for i in items]
        assert len(urls) == len(set(urls))

    @patch("collectors.hackernews.fetch_url")
    def test_front_page_filters_non_ai(self, mock_fetch):
        """首页热门应过滤非 AI 内容"""
        ai_hit = {
            "title": "New LLM benchmark released",
            "url": "https://example.com/llm",
            "points": 200,
            "num_comments": 50,
            "author": "user1",
            "created_at": "2026-02-12T08:00:00.000Z",
            "objectID": "11111",
        }
        non_ai_hit = {
            "title": "Ireland rolls out basic income for artists",
            "url": "https://example.com/ireland",
            "points": 300,
            "num_comments": 100,
            "author": "user2",
            "created_at": "2026-02-12T08:00:00.000Z",
            "objectID": "22222",
        }
        empty_resp = MagicMock()
        empty_resp.json.return_value = {"hits": []}
        front_resp = MagicMock()
        front_resp.json.return_value = {"hits": [ai_hit, non_ai_hit]}

        # 关键词搜索返回空，首页返回 2 条（1 AI + 1 非 AI）
        mock_fetch.side_effect = [empty_resp] * len(
            __import__("collectors.hackernews", fromlist=["KEYWORDS"]).KEYWORDS
        ) + [front_resp]

        items = collect(hours=24)
        titles = [i["title"] for i in items]
        assert "New LLM benchmark released" in titles
        assert "Ireland rolls out basic income for artists" not in titles

    @patch("collectors.hackernews.fetch_url")
    def test_keyword_search_filters_non_ai_title(self, mock_fetch):
        """关键词搜索结果也应过滤标题中无 AI 关键词的内容"""
        ai_hit = {
            "title": "GPT-5 Released",
            "url": "https://openai.com/blog/gpt5",
            "points": 500,
            "num_comments": 300,
            "author": "pg",
            "created_at": "2026-02-12T08:00:00.000Z",
            "objectID": "12345",
        }
        non_ai_hit = {
            "title": "FAA closes airspace over New Jersey",
            "url": "https://example.com/faa",
            "points": 200,
            "num_comments": 50,
            "author": "user1",
            "created_at": "2026-02-12T08:00:00.000Z",
            "objectID": "99999",
        }
        mixed_resp = MagicMock()
        mixed_resp.json.return_value = {"hits": [ai_hit, non_ai_hit]}
        empty_resp = MagicMock()
        empty_resp.json.return_value = {"hits": []}
        front_resp = MagicMock()
        front_resp.json.return_value = {"hits": []}

        # 第一个关键词返回混合结果，其余返回空，首页返回空
        mock_fetch.side_effect = [mixed_resp] + [empty_resp] * (len(KEYWORDS) - 1) + [front_resp]

        items = collect(hours=24)
        titles = [i["title"] for i in items]
        assert "GPT-5 Released" in titles
        assert "FAA closes airspace over New Jersey" not in titles
