"""测试 Runner 编排"""
import json
import os
from unittest.mock import patch, MagicMock
import pytest
from collectors.runner import run, retry_with_backoff


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


class TestRun:
    @patch("collectors.runner.COLLECTORS")
    def test_merges_and_deduplicates(self, mock_collectors):
        mock_a = MagicMock()
        mock_a.collect.return_value = [
            {"id": "a:1", "url": "https://example.com/1", "title": "A"},
            {"id": "a:2", "url": "https://example.com/2", "title": "B"},
        ]
        mock_b = MagicMock()
        mock_b.collect.return_value = [
            {"id": "b:1", "url": "https://example.com/1", "title": "A dup"},
            {"id": "b:3", "url": "https://example.com/3", "title": "C"},
        ]
        mock_collectors.__iter__ = MagicMock(return_value=iter([
            ("source_a", mock_a),
            ("source_b", mock_b),
        ]))

        items = run(hours=24, output_dir=None)
        urls = [i["url"] for i in items]
        assert len(urls) == 3
        assert len(set(urls)) == 3

    @patch("collectors.runner.COLLECTORS")
    def test_skips_failed_collector(self, mock_collectors):
        mock_ok = MagicMock()
        mock_ok.collect.return_value = [{"id": "1", "url": "https://example.com/1", "title": "OK"}]
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
            "source": "test", "content_type": "news", "date": "", "summary": "", "score": 0, "metadata": {},
        }]
        mock_collectors.__iter__ = MagicMock(return_value=iter([("test", mock_c)]))

        items = run(hours=24, output_dir=str(tmp_path))
        json_files = list(tmp_path.glob("*.json"))
        assert len(json_files) == 2  # full + slim

        full_file = [f for f in json_files if "slim" not in f.name][0]
        with open(full_file) as f:
            data = json.load(f)
        assert len(data) == 1
