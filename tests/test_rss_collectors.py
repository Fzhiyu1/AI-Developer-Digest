"""测试 RSS 采集器（TechCrunch + The Verge）"""
from unittest.mock import patch, MagicMock
from collectors.techcrunch import collect as tc_collect
from collectors.theverge import collect as tv_collect


def _mock_entry(**kwargs):
    entry = MagicMock()
    entry.title = kwargs.get("title", "Test Article")
    entry.link = kwargs.get("link", "https://example.com/article")
    entry.published = kwargs.get("published", "Wed, 12 Feb 2026 08:00:00 GMT")
    entry.summary = kwargs.get("summary", "A test article summary")
    entry.get = lambda k, d=None: kwargs.get(k, d)
    # 模拟 tags
    if "tags" in kwargs:
        entry.tags = [MagicMock(term=t) for t in kwargs["tags"]]
    else:
        entry.tags = []
    # 模拟 author
    entry.author = kwargs.get("author", "")
    return entry


class TestTechCrunch:
    @patch("collectors.techcrunch.parse_rss")
    def test_returns_unified_format(self, mock_rss):
        mock_rss.return_value = [
            _mock_entry(title="OpenAI raises $10B", link="https://techcrunch.com/openai",
                        tags=["AI", "Funding"], author="John")
        ]
        items = tc_collect(hours=24)
        assert len(items) == 1
        item = items[0]
        assert item["source"] == "techcrunch"
        assert item["content_type"] == "news"
        assert item["title"] == "OpenAI raises $10B"
        assert item["metadata"]["author"] == "John"


class TestTheVerge:
    @patch("collectors.theverge.parse_rss")
    def test_returns_unified_format(self, mock_rss):
        mock_rss.return_value = [
            _mock_entry(title="AI News", link="https://theverge.com/ai-news",
                        author="Sarah")
        ]
        items = tv_collect(hours=24)
        assert len(items) == 1
        item = items[0]
        assert item["source"] == "theverge"
        assert item["content_type"] == "news"
