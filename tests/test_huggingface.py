"""测试 Hugging Face 采集器"""
from unittest.mock import patch, MagicMock
from collectors.huggingface import collect

MOCK_TRENDING = {
    "recentlyTrending": [
        {
            "repoData": {
                "id": "meta-llama/Llama-3",
                "likes": 1200,
                "downloads": 500000,
                "pipeline_tag": "text-generation",
                "tags": ["llm"],
            },
            "repoType": "model",
        }
    ]
}


class TestHuggingfaceCollect:
    @patch("collectors.huggingface.fetch_url")
    def test_returns_unified_format(self, mock_fetch):
        mock_resp = MagicMock()
        mock_resp.json.return_value = MOCK_TRENDING
        mock_fetch.return_value = mock_resp

        items = collect(hours=24)
        assert len(items) >= 1
        item = items[0]
        assert item["source"] == "huggingface"
        assert item["content_type"] == "model"
        assert "meta-llama/Llama-3" in item["title"]
        assert item["metadata"]["likes"] == 1200
