"""Unit tests for gist API clients."""

from __future__ import absolute_import, division, print_function


# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

import json

from typing import Optional, Tuple, Union

from ansible_collections.ansible.scm.plugins.plugin_utils.github_gist import GitHubGist
from ansible_collections.ansible.scm.plugins.plugin_utils.gitlab_snippet import GitLabSnippet
from ansible_collections.ansible.scm.plugins.plugin_utils.http_request import HttpResponse


def _mock_response(status: int, payload: Union[dict, list]) -> Tuple[Optional[HttpResponse], str]:
    return HttpResponse(status=status, body=json.dumps(payload)), ""


def test_github_create_gist() -> None:
    """Test creating a GitHub gist."""

    def mock_request(method, url, headers, body=None, timeout=30, validate_certs=True):
        del headers, timeout, validate_certs
        assert method == "POST"
        assert url.endswith("/gists")
        payload = json.loads(body or "{}")
        assert payload["files"]["report.txt"]["content"] == "hello"
        return _mock_response(
            201,
            {
                "id": "abc123",
                "html_url": "https://gist.github.com/abc123",
                "description": "test gist",
                "public": False,
                "files": {"report.txt": {"content": "hello"}},
            },
        )

    client = GitHubGist(token="secret", http_request_func=mock_request)
    gist, error = client.create("test gist", False, {"report.txt": "hello"})
    assert error == ""
    assert gist is not None
    normalized = GitHubGist.normalize_result(gist)
    assert normalized["id"] == "abc123"
    assert normalized["files"]["report.txt"] == "hello"


def test_github_update_is_idempotent() -> None:
    """Test gist file comparison for idempotency."""

    existing = {"files": {"report.txt": {"content": "same"}}}
    assert GitHubGist.files_match(
        GitHubGist.extract_files(existing),
        {"report.txt": "same"},
    )
    assert not GitHubGist.files_match(
        GitHubGist.extract_files(existing),
        {"report.txt": "different"},
    )


def test_gitlab_create_snippet() -> None:
    """Test creating a GitLab snippet."""

    def mock_request(method, url, headers, body=None, timeout=30, validate_certs=True):
        del headers, timeout, validate_certs
        assert method == "POST"
        assert url.endswith("/snippets")
        payload = json.loads(body or "{}")
        assert payload["files"][0]["file_path"] == "report.txt"
        return _mock_response(
            201,
            {
                "id": 42,
                "web_url": "https://gitlab.com/snippets/42",
                "description": "test snippet",
                "title": "report",
                "visibility": "private",
                "files": {"report.txt": {"content": "hello"}},
            },
        )

    client = GitLabSnippet(token="secret", http_request_func=mock_request)
    snippet, error = client.create(
        "report",
        "test snippet",
        "private",
        {"report.txt": "hello"},
    )
    assert error == ""
    assert snippet is not None
    normalized = GitLabSnippet.normalize_result(snippet)
    assert normalized["id"] == 42
    assert normalized["html_url"] == "https://gitlab.com/snippets/42"
