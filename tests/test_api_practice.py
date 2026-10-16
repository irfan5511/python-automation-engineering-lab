import json

from api_practice import (
    summarize_repositories,
    clean_repository,
    save_report,
    fetch_repositories
)
from unittest.mock import patch
import pytest
import requests


def test_summarize_repositories_counts_statuses():
    repositories = [
        {"activity_status": "Active"},
        {"activity_status": "Active"},
        {"activity_status": "Stale"}
    ]

    result = summarize_repositories(repositories)

    assert result["total_repositories"] == 3
    assert result["active_repositories"] == 2
    assert result["stale_repositories"] == 1


def test_clean_repository_transforms_data():
    repo = {
        "full_name": "example/test-repo",
        "language": None,
        "html_url": "https://github.com/example/test-repo",
        "pushed_at": "2020-01-01T00:00:00Z",
        "open_issues_count": 3,
        "forks_count": 5,
        "stargazers_count": 10
    }

    result = clean_repository(repo)

    assert result["full_name"] == "example/test-repo"
    assert result["language"] == "Unknown"
    assert result["open_issues_count"] == 3
    assert result["forks_count"] == 5
    assert result["stargazers_count"] == 10
    assert result["activity_status"] == "Stale"


def test_save_report_writes_json_file(tmp_path):
    report = {
        "summary": {
            "total_repositories": 1,
            "active_repositories": 1,
            "stale_repositories": 0
        },
        "repositories": [
            {
                "full_name": "example/test_repo",
                "activity_status": "Active"
            }
        ]
    }

    filename = tmp_path / "report.json"

    save_report(report, filename)

    with open(filename, "r", encoding="utf-8") as file:
        save_data = json.load(file)

    assert save_data == report


def test_fetch_repositories_returns_api_data():
    fake_repositories = [
        {
            "name": "project-one",
            "language": "Python"
        },
        {
            "name": "project-two",
            "language": "JavaScript"
        }
    ]
    with patch("api_practice.requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.json.return_value = fake_repositories

        result = fetch_repositories("example-user")
        assert result == fake_repositories


        mock_get.assert_called_once_with(
            "https://api.github.com/users/example-user/repos",
             params={
                "sort": "updated",
                "per_page": 5
            },
            timeout=10
        )

        mock_response.raise_for_status.assert_called_once_with()


def test_fetch_respositories_raises_http_error():
    with patch("api_practice.requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.raise_for_status.side_effect = requests.HTTPError
        with pytest.raises(requests.HTTPError):
            fetch_repositories("example-user")