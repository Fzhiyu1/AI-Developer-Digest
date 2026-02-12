"""测试 Hacker News 采集器"""
from unittest.mock import patch, MagicMock
from collectors.hackernews import collect


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
