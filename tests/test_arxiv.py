"""测试 ArXiv 采集器"""
from unittest.mock import patch, MagicMock, call
from collectors.arxiv import collect, FEED_URLS, _extract_paper_id, _enrich_abstracts


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


class TestArxivEnrich:
    def test_extract_paper_id(self):
        assert _extract_paper_id("https://arxiv.org/abs/2602.12345") == "2602.12345"
        assert _extract_paper_id("http://arxiv.org/abs/2602.12345v1") == "2602.12345"
        assert _extract_paper_id("https://example.com/no-paper") == ""

    @patch("collectors.arxiv.fetch_url")
    def test_enrich_updates_summary_and_authors(self, mock_fetch):
        items = [{
            "url": "https://arxiv.org/abs/2602.12345",
            "summary": "Short...",
            "metadata": {"authors": ["A"]},
        }]

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = (
            '<?xml version="1.0"?>'
            '<feed xmlns="http://www.w3.org/2005/Atom">'
            "<entry>"
            "<id>http://arxiv.org/abs/2602.12345v1</id>"
            "<summary>This is a much longer and more detailed abstract.</summary>"
            "<author><name>Author One</name></author>"
            "<author><name>Author Two</name></author>"
            "</entry>"
            "</feed>"
        )
        mock_fetch.return_value = mock_resp

        _enrich_abstracts(items)
        assert "much longer" in items[0]["summary"]
        assert items[0]["metadata"]["authors"] == ["Author One", "Author Two"]

    @patch("collectors.arxiv.fetch_url")
    def test_enrich_handles_api_failure(self, mock_fetch):
        items = [{
            "url": "https://arxiv.org/abs/2602.12345",
            "summary": "Original",
            "metadata": {"authors": ["A"]},
        }]
        mock_fetch.side_effect = Exception("API down")

        _enrich_abstracts(items)
        assert items[0]["summary"] == "Original"  # 不影响原数据

    @patch("collectors.arxiv.fetch_url")
    def test_enrich_skips_non_xml_response(self, mock_fetch):
        """API 返回非 XML（如 HTML 错误页）时跳过"""
        items = [{
            "url": "https://arxiv.org/abs/2602.12345",
            "summary": "Original",
            "metadata": {"authors": ["A"]},
        }]
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = "<html><body>Rate limited</body></html>"
        mock_fetch.return_value = mock_resp

        _enrich_abstracts(items)
        assert items[0]["summary"] == "Original"

    @patch("collectors.arxiv.fetch_url")
    def test_enrich_skips_non_200(self, mock_fetch):
        """API 返回非 200 状态码时跳过"""
        items = [{
            "url": "https://arxiv.org/abs/2602.12345",
            "summary": "Original",
            "metadata": {"authors": ["A"]},
        }]
        mock_resp = MagicMock()
        mock_resp.status_code = 503
        mock_fetch.return_value = mock_resp

        _enrich_abstracts(items)
        assert items[0]["summary"] == "Original"

    @patch("collectors.arxiv.time.sleep")
    @patch("collectors.arxiv.fetch_url")
    def test_enrich_batches_requests(self, mock_fetch, mock_sleep):
        """超过 BATCH_SIZE 时分批查询"""
        from collectors.arxiv import BATCH_SIZE
        items = [
            {
                "url": f"https://arxiv.org/abs/2602.{10000 + i}",
                "summary": "Short",
                "metadata": {"authors": []},
            }
            for i in range(BATCH_SIZE + 5)
        ]
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = '<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom"></feed>'
        mock_fetch.return_value = mock_resp

        _enrich_abstracts(items)
        assert mock_fetch.call_count == 2  # 分两批
        assert mock_sleep.call_count == 1  # 批间睡眠一次
