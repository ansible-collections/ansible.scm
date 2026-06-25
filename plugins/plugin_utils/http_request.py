"""HTTP helpers for gist and snippet API clients."""

from __future__ import absolute_import, division, print_function


# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

import json

from typing import Any, Dict, Optional, Tuple, TypeVar, Union
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


JSONTypes = Union[bool, int, str, Dict[str, Any], list]  # type: ignore

T = TypeVar("T", bound="HttpResponse")  # pylint: disable=invalid-name, useless-suppression


class HttpResponse:
    """Normalized HTTP response."""

    def __init__(
        self: T,
        status: int,
        body: str,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        """Initialize the response.

        :param status: The HTTP status code
        :param body: The response body
        :param headers: Optional response headers
        """
        self.status = status
        self.body = body
        self.headers = headers or {}

    def json(self: T) -> JSONTypes:
        """Parse the response body as JSON.

        :returns: The parsed JSON payload
        """
        if not self.body:
            return {}
        return json.loads(self.body)


def http_request(
    method: str,
    url: str,
    headers: Optional[Dict[str, str]] = None,
    body: Optional[Union[str, bytes]] = None,
    timeout: int = 30,
    validate_certs: bool = True,
) -> HttpResponse:
    """Perform an HTTP request.

    :param method: The HTTP method
    :param url: The request URL
    :param headers: Optional request headers
    :param body: Optional request body
    :param timeout: Request timeout in seconds
    :param validate_certs: Whether to validate TLS certificates
    :returns: The HTTP response
    :raises HTTPError: If the server returns an error status
    :raises URLError: If the request cannot be completed
    """
    request_headers = dict(headers or {})
    data: Optional[bytes] = None
    if body is not None:
        data = body.encode("utf-8") if isinstance(body, str) else body

    request = Request(url=url, data=data, headers=request_headers, method=method.upper())
    with urlopen(request, timeout=timeout) as response:  # noqa: S310
        response_body = response.read().decode("utf-8")
        response_headers = {key.lower(): value for key, value in response.headers.items()}
        return HttpResponse(
            status=response.status,
            body=response_body,
            headers=response_headers,
        )


def http_request_safe(
    method: str,
    url: str,
    headers: Optional[Dict[str, str]] = None,
    body: Optional[Union[str, bytes]] = None,
    timeout: int = 30,
    validate_certs: bool = True,
) -> Tuple[Optional[HttpResponse], str]:
    """Perform an HTTP request and return errors instead of raising.

    :returns: A tuple of response and error message
    """
    del validate_certs  # urllib uses system trust store; reserved for future use
    try:
        return (
            http_request(
                method=method,
                url=url,
                headers=headers,
                body=body,
                timeout=timeout,
            ),
            "",
        )
    except HTTPError as exc:
        error_body = exc.read().decode("utf-8") if exc.fp else ""
        return HttpResponse(status=exc.code, body=error_body), error_body or str(exc)
    except URLError as exc:
        return None, str(exc.reason)
