# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""The gist_retrieve action plugin."""

from __future__ import absolute_import, division, print_function


# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

from dataclasses import asdict
from typing import Dict, Optional, TypeVar, Union

from ansible.errors import AnsibleActionFail
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play_context import PlayContext
from ansible.playbook.task import Task
from ansible.plugins import loader as plugin_loader
from ansible.plugins.connection.local import Connection
from ansible.template import Templar

from ..modules.gist_retrieve import DOCUMENTATION
from ..plugin_utils.gist_base import ActionInit, GistBase, GistResultBase
from ..plugin_utils.github_gist import GitHubGist
from ..plugin_utils.gitlab_snippet import GitLabSnippet


JSONTypes = Union[bool, int, str, Dict, list]  # type: ignore

T = TypeVar("T", bound="ActionModule")  # pylint: disable=invalid-name, useless-suppression


class ActionModule(GistBase):
    """Retrieve a gist or snippet."""

    def __init__(  # noqa: PLR0913
        self: T,
        connection: Connection,
        loader: DataLoader,
        play_context: PlayContext,
        shared_loader_obj: plugin_loader,
        task: Task,
        templar: Templar,
    ) -> None:
        """Initialize the action plugin."""
        super().__init__(
            ActionInit(
                connection=connection,
                loader=loader,
                play_context=play_context,
                shared_loader_obj=shared_loader_obj,
                templar=templar,
                task=task,
            ),
        )
        self._result: GistResultBase = GistResultBase()
        self._supports_async = True

    def _apply_result(self: T, normalized: Dict[str, JSONTypes]) -> None:
        """Populate the task result from a normalized API response."""
        self._result.id = str(normalized.get("id", ""))
        self._result.html_url = str(normalized.get("html_url", ""))
        self._result.description = str(normalized.get("description", ""))
        files = normalized.get("files", {})
        self._result.files = files if isinstance(files, dict) else {}

    def run(
        self: T,
        tmp: None = None,
        task_vars: Optional[Dict[str, JSONTypes]] = None,
    ) -> Dict[str, JSONTypes]:
        """Run the action plugin."""
        self._task.diff = False
        super().run(task_vars=task_vars)

        self._check_argspec(DOCUMENTATION)
        self._timeout = self._task.args.get("timeout", 30)
        gist_id = self._task.args.get("gist_id")
        if not gist_id:
            raise AnsibleActionFail("gist_id is required")
        provider = self._task.args.get("provider", "github")

        if provider == "github":
            gist, error = self._github_client().get(gist_id)
            if gist is None:
                raise AnsibleActionFail(f"Failed to retrieve gist {gist_id}: {error}")
            self._apply_result(GitHubGist.normalize_result(gist))
        else:
            snippet, error = self._gitlab_client().get(
                gist_id,
                project_id=self._task.args.get("project_id"),
            )
            if snippet is None:
                raise AnsibleActionFail(f"Failed to retrieve snippet {gist_id}: {error}")
            self._apply_result(GitLabSnippet.normalize_result(snippet))

        self._result.changed = False
        self._result.msg = f"Successfully retrieved {provider} resource {gist_id}"
        return asdict(self._result)
