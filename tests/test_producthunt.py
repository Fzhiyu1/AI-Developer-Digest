"""测试 Product Hunt 采集器"""
from unittest.mock import patch, MagicMock
from collectors.producthunt import collect


def _mock_ai_entry():
    entry = MagicMock()
    entry.title = "AI Code Assistant - Write code 10x faster"
    entry.link = "https://www.producthunt.com/posts/ai-code-assistant"
    entry.published = "Wed, 12 Feb 2026 08:00:00 GMT"
    entry.summary = "An AI-powered code assistant"
    entry.tags = []
    return entry


def _mock_non_ai_entry():
    entry = MagicMock()
    entry.title = "Todo List App - Organize your tasks"
    entry.link = "https://www.producthunt.com/posts/todo-list-app"
    entry.published = "Wed, 12 Feb 2026 08:00:00 GMT"
    entry.summary = "A simple and elegant todo list"
    entry.tags = []
    return entry


class TestProductHuntCollect:
    @patch("collectors.producthunt.parse_rss")
    def test_returns_unified_format(self, mock_rss):
        mock_rss.return_value = [_mock_ai_entry()]

        items = collect(hours=24)
        assert len(items) == 1
        item = items[0]
        assert item["source"] == "producthunt"
        assert item["content_type"] == "product"
        assert "AI Code Assistant" in item["title"]

    @patch("collectors.producthunt.parse_rss")
    def test_filters_non_ai_products(self, mock_rss):
        mock_rss.return_value = [_mock_ai_entry(), _mock_non_ai_entry()]

        items = collect(hours=24)
        assert len(items) == 1
        assert "AI Code Assistant" in items[0]["title"]
