"""测试 Product Hunt 采集器"""
from unittest.mock import patch, MagicMock
from collectors.producthunt import collect


def _mock_entry():
    entry = MagicMock()
    entry.title = "AI Code Assistant - Write code 10x faster"
    entry.link = "https://www.producthunt.com/posts/ai-code-assistant"
    entry.published = "Wed, 12 Feb 2026 08:00:00 GMT"
    entry.summary = "An AI-powered code assistant"
    entry.tags = []
    return entry


class TestProductHuntCollect:
    @patch("collectors.producthunt.parse_rss")
    def test_returns_unified_format(self, mock_rss):
        mock_rss.return_value = [_mock_entry()]

        items = collect(hours=24)
        assert len(items) == 1
        item = items[0]
        assert item["source"] == "producthunt"
        assert item["content_type"] == "product"
        assert "AI Code Assistant" in item["title"]
