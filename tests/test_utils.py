"""测试共享工具函数"""
import pytest
from unittest.mock import patch, MagicMock
from collectors.utils import make_id, normalize_url, to_iso_date, strip_html


class TestMakeId:
    def test_basic(self):
        result = make_id("hackernews", "https://example.com/article")
        assert result.startswith("hackernews:")
        assert len(result) > len("hackernews:")

    def test_same_input_same_output(self):
        a = make_id("github", "https://github.com/foo/bar")
        b = make_id("github", "https://github.com/foo/bar")
        assert a == b

    def test_different_source_different_id(self):
        a = make_id("hackernews", "https://example.com")
        b = make_id("reddit", "https://example.com")
        assert a != b


class TestNormalizeUrl:
    def test_strips_utm(self):
        url = "https://example.com/article?utm_source=twitter&utm_medium=social"
        assert normalize_url(url) == "https://example.com/article"

    def test_strips_ref(self):
        url = "https://example.com/article?ref=hn&id=123"
        assert normalize_url(url) == "https://example.com/article?id=123"

    def test_preserves_meaningful_params(self):
        url = "https://example.com/search?q=AI&page=2"
        assert normalize_url(url) == "https://example.com/search?q=AI&page=2"

    def test_no_params(self):
        url = "https://example.com/article"
        assert normalize_url(url) == "https://example.com/article"

    def test_trailing_slash(self):
        url = "https://example.com/article/"
        assert normalize_url(url) == "https://example.com/article/"


class TestToIsoDate:
    def test_iso_string_passthrough(self):
        assert to_iso_date("2026-02-12T08:00:00Z") == "2026-02-12T08:00:00Z"

    def test_unix_timestamp(self):
        result = to_iso_date(1739347200)  # 2025-02-12T08:00:00Z
        assert "2025-02-12" in result

    def test_rss_date(self):
        result = to_iso_date("Wed, 12 Feb 2026 08:00:00 GMT")
        assert "2026-02-12" in result

    def test_none_returns_empty(self):
        assert to_iso_date(None) == ""


class TestStripHtml:
    def test_removes_tags(self):
        assert strip_html("<p>Hello <b>world</b></p>") == "Hello world"

    def test_decodes_entities(self):
        assert strip_html("foo&#8230;bar") == "foo...bar"
        assert strip_html("a &amp; b") == "a & b"

    def test_empty(self):
        assert strip_html("") == ""
        assert strip_html(None) == ""

    def test_plain_text_passthrough(self):
        assert strip_html("no html here") == "no html here"


# --- Task 3: fetch_url, parse_rss ---

from collectors.utils import fetch_url, parse_rss


class TestFetchUrl:
    @patch("collectors.utils.requests.get")
    def test_returns_response(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"ok": True}
        mock_get.return_value = mock_resp

        resp = fetch_url("https://example.com/api")
        assert resp.status_code == 200
        mock_get.assert_called_once()

    @patch("collectors.utils.requests.get")
    def test_sets_user_agent(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200)
        fetch_url("https://example.com")
        call_kwargs = mock_get.call_args
        assert "User-Agent" in call_kwargs.kwargs.get("headers", {}) or \
               "User-Agent" in call_kwargs[1].get("headers", {})


class TestParseRss:
    @patch("collectors.utils.feedparser.parse")
    def test_returns_entries(self, mock_parse):
        mock_parse.return_value = MagicMock(
            entries=[
                MagicMock(title="Test Article", link="https://example.com/1",
                          published="Wed, 12 Feb 2026 08:00:00 GMT",
                          summary="A test article")
            ]
        )
        entries = parse_rss("https://example.com/feed")
        assert len(entries) == 1
        assert entries[0].title == "Test Article"
