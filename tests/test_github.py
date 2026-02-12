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
