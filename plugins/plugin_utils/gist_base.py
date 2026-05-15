"""Base classes for gist and snippet action plugins."""

from __future__ import absolute_import, division, print_function


# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

import os

from dataclasses import dataclass, field
from typing import Dict, List, TypeVar, Union

from ansible.errors import AnsibleActionFail
from ansible.plugins.action import ActionBase

# pylint: disable=import-error
from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)

from .git_base import ActionInit
from .github_gist import GitHubGist
from .gitlab_snippet import GitLabSnippet


JSONTypes = Union[bool, int, str, Dict, List]  # type: ignore

T = TypeVar("T", bound="GistBase")  # pylint: disable=invalid-name, useless-suppression


@dataclass(frozen=False)
class GistResultBase:
    """Data structure for gist task results."""

    changed: bool = False
    failed: bool = False
    msg: str = ""
    id: str = ""  # pylint: disable=invalid-name
    html_url: str = ""
    description: str = ""
    files: Dict[str, str] = field(default_factory=dict)


class GistBase(ActionBase):  # type: ignore[misc]
    """Base class for gist and snippet action plugins."""

    _requires_connection = False

    def __init__(self: T, action_init: ActionInit) -> None:
        """Initialize the action plugin."""
        super().__init__(**action_init.asdict)
        self._result: GistResultBase = GistResultBase()
        self._timeout: int = 30

    def _check_argspec(self: T, documentation: str) -> None:
        """Validate task arguments against the module DOCUMENTATION."""
        aav = AnsibleArgSpecValidator(
            data=self._task.args,
            schema=documentation,
            name=self._task.action,
        )
        valid, errors, self._task.args = aav.validate()
        if not valid:
            raise AnsibleActionFail(errors)
        if self._task.args.get("token") == "":
            raise AnsibleActionFail("token can not be an empty string")

    def _resolve_token(self: T, provider: str, token: str) -> str:
        """Resolve API token from task args or environment."""
        if token:
            return token
        env_name = "GITHUB_TOKEN" if provider == "github" else "GITLAB_TOKEN"
        env_token = os.environ.get(env_name, "")
        if not env_token:
            raise AnsibleActionFail(
                f"token is required when {env_name} is not set in the environment",
            )
        return env_token

    def _github_client(self: T) -> GitHubGist:
        """Create a GitHub gist client from task arguments."""
        token = self._resolve_token("github", self._task.args.get("token", ""))
        return GitHubGist(
            token=token,
            api_url=self._task.args.get("api_url", "https://api.github.com"),
            timeout=self._timeout,
            validate_certs=self._task.args.get("validate_certs", True),
        )

    def _gitlab_client(self: T) -> GitLabSnippet:
        """Create a GitLab snippet client from task arguments."""
        token = self._resolve_token("gitlab", self._task.args.get("token", ""))
        return GitLabSnippet(
            token=token,
            api_url=self._task.args.get("api_url", "https://gitlab.com/api/v4"),
            timeout=self._timeout,
            validate_certs=self._task.args.get("validate_certs", True),
        )

    def _normalize_files(self: T, files: Dict[str, JSONTypes], required: bool = True) -> Dict[str, str]:
        """Normalize the files dictionary to string contents."""
        normalized: Dict[str, str] = {}
        for name, details in files.items():
            if isinstance(details, dict):
                normalized[name] = str(details.get("content", ""))
            else:
                normalized[name] = str(details)
        if required and not normalized:
            raise AnsibleActionFail("files must contain at least one file when state is present")
        return normalized
