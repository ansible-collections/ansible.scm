"""GitLab Snippet API client."""

from __future__ import absolute_import, division, print_function


# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

import json

from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from .http_request import HttpResponse, http_request_safe


JSONTypes = Union[bool, int, str, Dict[str, Any], list]  # type: ignore

HttpRequestCallable = Callable[..., Tuple[Optional[HttpResponse], str]]


class GitLabSnippet:
    """Client for the GitLab Snippets REST API."""

    def __init__(
        self,
        token: str,
        api_url: str = "https://gitlab.com/api/v4",
        timeout: int = 30,
        validate_certs: bool = True,
        http_request_func: Optional[HttpRequestCallable] = None,
    ) -> None:
        """Initialize the client."""
        self.token = token
        self.api_url = api_url.rstrip("/")
        self.timeout = timeout
        self.validate_certs = validate_certs
        self._http_request = http_request_func or http_request_safe

    def _headers(self) -> Dict[str, str]:
        """Return request headers including authorization."""
        return {
            "PRIVATE-TOKEN": self.token,
            "Content-Type": "application/json",
        }

    def _request(
        self,
        method: str,
        path: str,
        payload: Optional[Dict[str, JSONTypes]] = None,
    ) -> Tuple[Optional[Dict[str, JSONTypes]], str]:
        """Perform an API request."""
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

    def _snippet_path(self, snippet_id: str, project_id: Optional[str]) -> str:
        if project_id:
            return f"/projects/{project_id}/snippets/{snippet_id}"
        return f"/snippets/{snippet_id}"

    def get(
        self,
        snippet_id: str,
        project_id: Optional[str] = None,
    ) -> Tuple[Optional[Dict[str, JSONTypes]], str]:
        """Retrieve a snippet by id."""
        return self._request("GET", self._snippet_path(snippet_id, project_id))

    def create(
        self,
        title: str,
        description: str,
        visibility: str,
        files: Dict[str, str],
        project_id: Optional[str] = None,
    ) -> Tuple[Optional[Dict[str, JSONTypes]], str]:
        """Create a new snippet."""
        file_entries: List[Dict[str, str]] = [
            {"file_path": name, "content": content} for name, content in files.items()
        ]
        payload: Dict[str, JSONTypes] = {
            "title": title,
            "description": description,
            "visibility": visibility,
            "files": file_entries,
        }
        path = f"/projects/{project_id}/snippets" if project_id else "/snippets"
        return self._request("POST", path, payload)

    def update(
        self,
        snippet_id: str,
        title: Optional[str],
        description: Optional[str],
        visibility: Optional[str],
        files: Dict[str, str],
        project_id: Optional[str] = None,
    ) -> Tuple[Optional[Dict[str, JSONTypes]], str]:
        """Update an existing snippet."""
        payload: Dict[str, JSONTypes] = {
            "files": [
                {"file_path": name, "content": content} for name, content in files.items()
            ],
        }
        if title is not None:
            payload["title"] = title
        if description is not None:
            payload["description"] = description
        if visibility is not None:
            payload["visibility"] = visibility
        return self._request(
            "PUT",
            self._snippet_path(snippet_id, project_id),
            payload,
        )

    def delete(
        self,
        snippet_id: str,
        project_id: Optional[str] = None,
    ) -> Tuple[bool, str]:
        """Delete a snippet."""
        response, error = self._http_request(
            method="DELETE",
            url=f"{self.api_url}{self._snippet_path(snippet_id, project_id)}",
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
    def extract_files(snippet: Dict[str, JSONTypes]) -> Dict[str, str]:
        """Extract file contents from a snippet response."""
        files = snippet.get("files", {})
        if isinstance(files, dict):
            extracted: Dict[str, str] = {}
            for name, details in files.items():
                if isinstance(details, dict):
                    extracted[name] = str(details.get("content", ""))
                else:
                    extracted[name] = str(details)
            return extracted

        file_name = snippet.get("file_name")
        if file_name:
            return {str(file_name): str(snippet.get("content", ""))}
        return {}

    @staticmethod
    def files_match(existing: Dict[str, str], desired: Dict[str, str]) -> bool:
        """Return True when desired file contents match the existing snippet."""
        return existing == desired

    @staticmethod
    def normalize_result(snippet: Dict[str, JSONTypes]) -> Dict[str, JSONTypes]:
        """Normalize snippet API response for module return values."""
        web_url = snippet.get("web_url", "")
        return {
            "id": snippet.get("id", ""),
            "html_url": web_url,
            "description": snippet.get("description", ""),
            "title": snippet.get("title", ""),
            "visibility": snippet.get("visibility", ""),
            "files": GitLabSnippet.extract_files(snippet),
        }
