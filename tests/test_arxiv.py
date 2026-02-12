"""测试 ArXiv 采集器"""
from unittest.mock import patch, MagicMock
from collectors.arxiv import collect


def _mock_entry():
    entry = MagicMock()
    entry.title = "Attention Is All You Need v2"
    entry.link = "https://arxiv.org/abs/2026.12345"
    entry.published = "2026-02-12T00:00:00Z"
    entry.summary = "We propose a new transformer architecture..."
    author_a = MagicMock()
    author_a.name = "Author A"
    author_b = MagicMock()
    author_b.name = "Author B"
    entry.authors = [author_a, author_b]
    entry.tags = [MagicMock(term="cs.AI"), MagicMock(term="cs.CL")]
    return entry


class TestArxivCollect:
    @patch("collectors.arxiv.parse_rss")
    def test_returns_unified_format(self, mock_rss):
        mock_rss.return_value = [_mock_entry()]

        items = collect(hours=24)
        assert len(items) == 1
        item = items[0]
        assert item["source"] == "arxiv"
        assert item["content_type"] == "paper"
        assert "Attention" in item["title"]
        assert item["metadata"]["authors"] == ["Author A", "Author B"]
        assert "pdf_url" in item["metadata"]
