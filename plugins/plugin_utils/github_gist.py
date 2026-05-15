"""GitHub Gist API client."""

from __future__ import absolute_import, division, print_function


# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

import json

from typing import Any, Callable, Dict, Optional, Tuple, Union

from .http_request import HttpResponse, http_request_safe


JSONTypes = Union[bool, int, str, Dict[str, Any], list]  # type: ignore

HttpRequestCallable = Callable[..., Tuple[Optional[HttpResponse], str]]


class GitHubGist:
    """Client for the GitHub Gist REST API."""

    def __init__(
        self,
        token: str,
        api_url: str = "https://api.github.com",
        timeout: int = 30,
        validate_certs: bool = True,
        http_request_func: Optional[HttpRequestCallable] = None,
    ) -> None:
        """Initialize the client.

        :param token: GitHub personal access token
        :param api_url: GitHub API base URL
        :param timeout: Request timeout in seconds
        :param validate_certs: Whether to validate TLS certificates
        :param http_request_func: Optional HTTP request callable for testing
        """
        self.token = token
        self.api_url = api_url.rstrip("/")
        self.timeout = timeout
        self.validate_certs = validate_certs
        self._http_request = http_request_func or http_request_safe

    def _headers(self) -> Dict[str, str]:
        """Return request headers including authorization."""
        return {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def _request(
        self,
        method: str,
        path: str,
        payload: Optional[Dict[str, JSONTypes]] = None,
    ) -> Tuple[Optional[Dict[str, JSONTypes]], str]:
        """Perform an API request.

        :returns: Parsed JSON response and error message
        """
        url = f"{self.api_url}{path}"
        body = json.dumps(payload) if payload is not None else None
        response, error = self._http_request(
            method=method,
            url=url,
            headers=self._headers(),
            body=body,
            timeout=self.timeout,
            validate_certs=self.validate_certs,
        )
        if response is None:
            return None, error
        if response.status >= 400:
            return None, error or response.body
        if not response.body:
            return {}, ""
        data = response.json()
        if isinstance(data, dict):
            return data, ""
        return {"data": data}, ""

    def get(self, gist_id: str) -> Tuple[Optional[Dict[str, JSONTypes]], str]:
        """Retrieve a gist by id."""
        return self._request("GET", f"/gists/{gist_id}")

    def create(
        self,
        description: str,
        public: bool,
        files: Dict[str, str],
    ) -> Tuple[Optional[Dict[str, JSONTypes]], str]:
        """Create a new gist."""
        payload = {
            "description": description,
            "public": public,
            "files": {name: {"content": content} for name, content in files.items()},
        }
        return self._request("POST", "/gists", payload)

    def update(
        self,
        gist_id: str,
        description: Optional[str],
        public: Optional[bool],
        files: Dict[str, str],
    ) -> Tuple[Optional[Dict[str, JSONTypes]], str]:
        """Update an existing gist."""
        payload: Dict[str, JSONTypes] = {
            "files": {name: {"content": content} for name, content in files.items()},
        }
        if description is not None:
            payload["description"] = description
        if public is not None:
            payload["public"] = public
        return self._request("PATCH", f"/gists/{gist_id}", payload)

    def delete(self, gist_id: str) -> Tuple[bool, str]:
        """Delete a gist."""
        response, error = self._http_request(
            method="DELETE",
            url=f"{self.api_url}/gists/{gist_id}",
            headers=self._headers(),
            timeout=self.timeout,
            validate_certs=self.validate_certs,
        )
        if response is None:
            return False, error
        if response.status in (204, 404):
            return True, ""
        return False, error or response.body

    @staticmethod
    def extract_files(gist: Dict[str, JSONTypes]) -> Dict[str, str]:
        """Extract file contents from a gist response."""
        files = gist.get("files", {})
        if not isinstance(files, dict):
            return {}
        extracted: Dict[str, str] = {}
        for name, details in files.items():
            if isinstance(details, dict):
                extracted[name] = str(details.get("content", ""))
        return extracted

    @staticmethod
    def files_match(existing: Dict[str, str], desired: Dict[str, str]) -> bool:
        """Return True when desired file contents match the existing gist."""
        return existing == desired

    @staticmethod
    def normalize_result(gist: Dict[str, JSONTypes]) -> Dict[str, JSONTypes]:
        """Normalize gist API response for module return values."""
        return {
            "id": gist.get("id", ""),
            "html_url": gist.get("html_url", ""),
            "git_pull_url": gist.get("git_pull_url", ""),
            "description": gist.get("description", ""),
            "public": gist.get("public", False),
            "files": GitHubGist.extract_files(gist),
        }
