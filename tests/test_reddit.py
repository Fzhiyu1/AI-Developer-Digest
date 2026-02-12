"""测试 Reddit 采集器"""
from unittest.mock import patch, MagicMock
from collectors.reddit import collect

MOCK_LISTING = {
    "data": {
        "children": [
            {
                "data": {
                    "title": "[R] New SOTA on ImageNet",
                    "url": "https://arxiv.org/abs/2026.12345",
                    "score": 450,
                    "num_comments": 120,
                    "link_flair_text": "Research",
                    "subreddit": "MachineLearning",
                    "created_utc": 1739347200,
                    "selftext": "",
                    "permalink": "/r/MachineLearning/comments/abc/new_sota/",
                }
            },
            {
                "data": {
                    "title": "Low quality post",
                    "url": "https://example.com/low-quality",
                    "score": 30,
                    "num_comments": 2,
                    "link_flair_text": "",
                    "subreddit": "MachineLearning",
                    "created_utc": 1739347200,
                    "selftext": "",
                    "permalink": "/r/MachineLearning/comments/xyz/low/",
                }
            },
        ]
    }
}


class TestRedditCollect:
    @patch("collectors.reddit.fetch_url")
    def test_returns_unified_format(self, mock_fetch):
        mock_resp = MagicMock()
        mock_resp.json.return_value = MOCK_LISTING
        mock_fetch.return_value = mock_resp

        items = collect(hours=24)
        assert len(items) >= 1
        item = items[0]
        assert item["source"] == "reddit"
        assert item["content_type"] == "discussion"
        assert item["score"] == 450
        assert item["metadata"]["num_comments"] == 120
        assert item["metadata"]["subreddit"] == "MachineLearning"

    @patch("collectors.reddit.fetch_url")
    def test_filters_low_upvote_posts(self, mock_fetch):
        mock_resp = MagicMock()
        mock_resp.json.return_value = MOCK_LISTING
        mock_fetch.return_value = mock_resp

        items = collect(hours=24)
        # 只有 score=450 的帖子通过，score=30 的被过滤
        assert len(items) == 1
        assert items[0]["score"] == 450
