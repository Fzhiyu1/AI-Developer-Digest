"""测试 ArXiv 采集器"""
from unittest.mock import patch, MagicMock, call
from collectors.arxiv import collect, FEED_URLS


def _mock_entry(title="Attention Is All You Need v2", link="https://arxiv.org/abs/2026.12345"):
    entry = MagicMock()
    entry.title = title
    entry.link = link
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
        assert len(items) >= 1
        item = items[0]
        assert item["source"] == "arxiv"
        assert item["content_type"] == "paper"
        assert "Attention" in item["title"]
        assert item["metadata"]["authors"] == ["Author A", "Author B"]
        assert "pdf_url" in item["metadata"]

    @patch("collectors.arxiv.parse_rss")
    def test_fetches_multiple_feeds(self, mock_rss):
        mock_rss.return_value = [_mock_entry()]

        collect(hours=24)
        # 验证所有 4 个 AI 子领域 feed 都被请求
        assert mock_rss.call_count == len(FEED_URLS)
        called_urls = [c.args[0] for c in mock_rss.call_args_list]
        for feed_url in FEED_URLS:
            assert feed_url in called_urls

    @patch("collectors.arxiv.parse_rss")
    def test_deduplicates_across_feeds(self, mock_rss):
        # 同一篇论文在多个 feed 中出现，只保留一条
        same_entry = _mock_entry()
        mock_rss.return_value = [same_entry]

        items = collect(hours=24)
        assert len(items) == 1
