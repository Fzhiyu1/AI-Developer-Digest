"""测试 Runner 编排"""
import json
import os
from unittest.mock import patch, MagicMock
import pytest
from collectors.runner import (
    run, retry_with_backoff,
    _title_words, _titles_similar, _merge_items, _compute_quality_signal, _slim,
)


class TestRetryWithBackoff:
    def test_succeeds_first_try(self):
        fn = MagicMock(return_value=[{"id": "1"}])
        result = retry_with_backoff(fn, max_retries=3, base_delay=0)
        assert result == [{"id": "1"}]
        assert fn.call_count == 1

    def test_retries_on_failure(self):
        fn = MagicMock(side_effect=[Exception("fail"), [{"id": "1"}]])
        result = retry_with_backoff(fn, max_retries=3, base_delay=0)
        assert result == [{"id": "1"}]
        assert fn.call_count == 2

    def test_raises_after_max_retries(self):
        fn = MagicMock(side_effect=Exception("fail"))
        with pytest.raises(Exception):
            retry_with_backoff(fn, max_retries=3, base_delay=0)
        assert fn.call_count == 3


class TestTitleSimilarity:
    def test_title_words_basic(self):
        words = _title_words("Hello, World! Test-Case")
        assert words == {"hello", "world", "testcase"}

    def test_title_words_empty(self):
        assert _title_words("") == set()

    def test_similar_titles(self):
        assert _titles_similar(
            "OpenAI releases GPT-5 with major improvements",
            "OpenAI Releases GPT-5 With Major Improvements!",
        )

    def test_dissimilar_titles(self):
        assert not _titles_similar(
            "OpenAI releases GPT-5",
            "Google launches new Gemini model",
        )

    def test_similar_titles_different_wording(self):
        # Same event, slightly different wording — Jaccard should still pass
        assert _titles_similar(
            "Meta releases Llama 3 open source model",
            "Meta Llama 3: new open source AI model released",
        )

    def test_empty_title_not_similar(self):
        assert not _titles_similar("", "Some title")
        assert not _titles_similar("Some title", "")
        assert not _titles_similar("", "")


class TestMergeItems:
    def test_merge_adds_source(self):
        existing = {"source": "hackernews", "score": 100, "title": "Test"}
        new_item = {"source": "reddit", "score": 50, "title": "Test"}
        result = _merge_items(existing, new_item)
        assert result["sources"] == ["hackernews", "reddit"]
        assert result["score"] == 100  # keeps higher

    def test_merge_updates_score_if_higher(self):
        existing = {"source": "hackernews", "score": 50, "title": "Test"}
        new_item = {"source": "reddit", "score": 200, "title": "Test"}
        result = _merge_items(existing, new_item)
        assert result["score"] == 200

    def test_merge_does_not_duplicate_source(self):
        existing = {"source": "hn", "sources": ["hn", "reddit"], "score": 10, "title": "T"}
        new_item = {"source": "reddit", "score": 5, "title": "T"}
        result = _merge_items(existing, new_item)
        assert result["sources"] == ["hn", "reddit"]

    def test_merge_handles_none_scores(self):
        existing = {"source": "a", "score": None, "title": "T"}
        new_item = {"source": "b", "score": 100, "title": "T"}
        result = _merge_items(existing, new_item)
        assert result["score"] == 100


class TestQualitySignal:
    def test_single_source_low_score(self):
        item = {"source": "hackernews", "score": 50, "metadata": {}}
        assert _compute_quality_signal(item) == 2  # 1 source * 2

    def test_multi_source(self):
        item = {"sources": ["hn", "reddit", "techcrunch"], "score": 50, "metadata": {}}
        assert _compute_quality_signal(item) == 6  # 3 sources * 2

    def test_high_score(self):
        item = {"source": "hn", "score": 500, "metadata": {}}
        assert _compute_quality_signal(item) == 4  # 1*2 + 2 (score>=500)

    def test_medium_score(self):
        item = {"source": "hn", "score": 200, "metadata": {}}
        assert _compute_quality_signal(item) == 3  # 1*2 + 1 (score>=100)

    def test_high_stars(self):
        item = {"source": "github", "score": 0, "metadata": {"stars": 50000}}
        assert _compute_quality_signal(item) == 4  # 1*2 + 2 (stars>=10000)

    def test_medium_stars(self):
        item = {"source": "github", "score": 0, "metadata": {"stars": 5000}}
        assert _compute_quality_signal(item) == 3  # 1*2 + 1 (stars>=1000)

    def test_all_bonuses(self):
        item = {"sources": ["hn", "reddit"], "score": 600, "metadata": {"stars": 20000}}
        # 2*2 + 2 (score>=500) + 2 (stars>=10000) = 8
        assert _compute_quality_signal(item) == 8


class TestSlim:
    def test_slim_includes_quality_signal(self):
        item = {
            "title": "Test", "url": "https://example.com", "source": "hn",
            "content_type": "news", "date": "2026-01-01", "summary": "",
            "score": 0, "metadata": {}, "quality_signal": 5,
        }
        s = _slim(item)
        assert s["qs"] == 5

    def test_slim_includes_sources(self):
        item = {
            "title": "Test", "url": "https://example.com", "source": "hn",
            "sources": ["hn", "reddit"],
            "content_type": "news", "date": "2026-01-01", "summary": "",
            "score": 0, "metadata": {}, "quality_signal": 6,
        }
        s = _slim(item)
        assert s["sources"] == ["hn", "reddit"]
        assert s["qs"] == 6

    def test_slim_no_sources_field_when_single(self):
        item = {
            "title": "Test", "url": "https://example.com", "source": "hn",
            "content_type": "news", "date": "2026-01-01", "summary": "",
            "score": 0, "metadata": {},
        }
        s = _slim(item)
        assert "sources" not in s


class TestRun:
    @patch("collectors.runner.COLLECTORS")
    def test_merges_and_deduplicates(self, mock_collectors):
        mock_a = MagicMock()
        mock_a.collect.return_value = [
            {"id": "a:1", "url": "https://example.com/1", "title": "A", "source": "sa", "score": 10, "metadata": {}},
            {"id": "a:2", "url": "https://example.com/2", "title": "B", "source": "sa", "score": 5, "metadata": {}},
        ]
        mock_b = MagicMock()
        mock_b.collect.return_value = [
            {"id": "b:1", "url": "https://example.com/1", "title": "A dup", "source": "sb", "score": 20, "metadata": {}},
            {"id": "b:3", "url": "https://example.com/3", "title": "C", "source": "sb", "score": 3, "metadata": {}},
        ]
        mock_collectors.__iter__ = MagicMock(return_value=iter([
            ("source_a", mock_a),
            ("source_b", mock_b),
        ]))

        items = run(hours=24, output_dir=None)
        urls = [i["url"] for i in items]
        assert len(urls) == 3
        assert len(set(urls)) == 3
        # All items should have quality_signal
        for item in items:
            assert "quality_signal" in item

    @patch("collectors.runner.COLLECTORS")
    def test_title_similarity_dedup(self, mock_collectors):
        """同一事件不同 URL 但标题相似，应合并"""
        mock_a = MagicMock()
        mock_a.collect.return_value = [
            {"id": "a:1", "url": "https://hn.com/item1", "title": "OpenAI releases GPT-5 model",
             "source": "hackernews", "score": 300, "metadata": {}},
        ]
        mock_b = MagicMock()
        mock_b.collect.return_value = [
            {"id": "b:1", "url": "https://reddit.com/post1", "title": "OpenAI Releases GPT-5 Model!",
             "source": "reddit", "score": 100, "metadata": {}},
        ]
        mock_collectors.__iter__ = MagicMock(return_value=iter([
            ("hn", mock_a),
            ("reddit", mock_b),
        ]))

        items = run(hours=24, output_dir=None)
        assert len(items) == 1
        assert items[0]["sources"] == ["hackernews", "reddit"]
        assert items[0]["score"] == 300  # keeps higher
        # quality_signal: 2 sources * 2 + 1 (score>=100) = 5
        assert items[0]["quality_signal"] == 5

    @patch("collectors.runner.COLLECTORS")
    def test_url_dedup_merges_sources(self, mock_collectors):
        """同一 URL 不同源，应合并来源列表"""
        mock_a = MagicMock()
        mock_a.collect.return_value = [
            {"id": "a:1", "url": "https://example.com/post", "title": "Some Post",
             "source": "hn", "score": 50, "metadata": {}},
        ]
        mock_b = MagicMock()
        mock_b.collect.return_value = [
            {"id": "b:1", "url": "https://example.com/post", "title": "Some Post Reworded",
             "source": "reddit", "score": 200, "metadata": {}},
        ]
        mock_collectors.__iter__ = MagicMock(return_value=iter([
            ("hn", mock_a),
            ("reddit", mock_b),
        ]))

        items = run(hours=24, output_dir=None)
        assert len(items) == 1
        assert items[0]["sources"] == ["hn", "reddit"]
        assert items[0]["score"] == 200

    @patch("collectors.runner.COLLECTORS")
    def test_skips_failed_collector(self, mock_collectors):
        mock_ok = MagicMock()
        mock_ok.collect.return_value = [
            {"id": "1", "url": "https://example.com/1", "title": "OK", "source": "ok", "score": 0, "metadata": {}}
        ]
        mock_fail = MagicMock()
        mock_fail.collect.side_effect = Exception("API down")
        mock_collectors.__iter__ = MagicMock(return_value=iter([
            ("failing", mock_fail),
            ("working", mock_ok),
        ]))

        items = run(hours=24, output_dir=None)
        assert len(items) == 1

    @patch("collectors.runner.COLLECTORS")
    def test_outputs_json(self, mock_collectors, tmp_path):
        mock_c = MagicMock()
        mock_c.collect.return_value = [{
            "id": "1", "url": "https://example.com", "title": "Test",
            "source": "test", "content_type": "news", "date": "", "summary": "",
            "score": 0, "metadata": {},
        }]
        mock_collectors.__iter__ = MagicMock(return_value=iter([("test", mock_c)]))

        items = run(hours=24, output_dir=str(tmp_path))
        json_files = list(tmp_path.glob("*.json"))
        assert len(json_files) == 2  # full + slim

        full_file = [f for f in json_files if "slim" not in f.name][0]
        with open(full_file) as f:
            data = json.load(f)
        assert len(data) == 1
        assert "quality_signal" in data[0]

        slim_file = [f for f in json_files if "slim" in f.name][0]
        with open(slim_file) as f:
            slim_data = json.load(f)
        assert len(slim_data) == 1
        assert "qs" in slim_data[0]
