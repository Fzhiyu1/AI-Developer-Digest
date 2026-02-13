"""测试 GitHub 采集器"""
from unittest.mock import patch, MagicMock
from collectors.github import collect

MOCK_SEARCH_RESPONSE = {
    "total_count": 1,
    "items": [
        {
            "full_name": "openai/gpt5",
            "html_url": "https://github.com/openai/gpt5",
            "description": "GPT-5 model",
            "stargazers_count": 5000,
            "language": "Python",
            "created_at": "2026-02-10T00:00:00Z",
            "topics": ["ai", "llm"],
        }
    ],
}

MOCK_TRENDING_HTML = """
<article class="Box-row">
  <h2 class="h3 lh-condensed">
    <a href="/openai/gpt5">openai / gpt5</a>
  </h2>
  <p class="col-9 color-fg-muted my-1 pr-4">GPT-5 model</p>
  <span class="d-inline-block ml-0 mr-3"><span class="repo-language-color" style="background-color: #3572A5"></span>Python</span>
  <a class="Link--muted d-inline-block mr-3" href="/openai/gpt5/stargazers">5,000</a>
  <span class="d-inline-block float-sm-right">200 stars today</span>
</article>
"""


class TestGithubCollect:
    @patch("collectors.github._search_api")
    @patch("collectors.github._scrape_trending")
    def test_returns_unified_format(self, mock_scrape, mock_search):
        mock_search.return_value = [
            {
                "full_name": "openai/gpt5",
                "html_url": "https://github.com/openai/gpt5",
                "description": "GPT-5 model",
                "stargazers_count": 5000,
                "language": "Python",
                "created_at": "2026-02-10T00:00:00Z",
                "topics": ["ai", "llm"],
            }
        ]
        mock_scrape.return_value = []

        items = collect(hours=24)
        assert len(items) >= 1
        item = items[0]
        assert item["source"] == "github"
        assert item["content_type"] == "project"
        assert item["score"] == 5000
        assert item["metadata"]["language"] == "Python"
        assert item["metadata"]["full_name"] == "openai/gpt5"


class TestSearchApiStarsFilter:
    """验证 Search API 的 MIN_STARS 过滤"""

    @patch("collectors.github.fetch_url")
    def test_search_query_includes_min_stars(self, mock_fetch):
        """确认 Search API 请求 URL 包含 stars 过滤条件"""
        from collectors.github import _search_api, MIN_STARS

        mock_resp = MagicMock()
        mock_resp.json.return_value = {"items": []}
        mock_fetch.return_value = mock_resp

        _search_api(days=7)

        call_url = mock_fetch.call_args[0][0]
        assert f"stars%3E%3D{MIN_STARS}" in call_url or f"stars:>={MIN_STARS}" in call_url

    def test_min_stars_threshold(self):
        """MIN_STARS 应该 >= 50 以过滤噪音"""
        from collectors.github import MIN_STARS

        assert MIN_STARS >= 50
