# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""The gist_publish action plugin."""

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

from ..modules.gist_publish import DOCUMENTATION
from ..plugin_utils.gist_base import ActionInit, GistBase, GistResultBase
from ..plugin_utils.github_gist import GitHubGist
from ..plugin_utils.gitlab_snippet import GitLabSnippet


JSONTypes = Union[bool, int, str, Dict, list]  # type: ignore

T = TypeVar("T", bound="ActionModule")  # pylint: disable=invalid-name, useless-suppression


class ActionModule(GistBase):
    """Publish content to a gist or snippet."""

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

    def _publish_github(self: T) -> None:
        """Create or update a GitHub gist."""
        client = self._github_client()
        files = self._normalize_files(self._task.args["files"])
        gist_id = self._task.args.get("gist_id")
        description = self._task.args.get("description", "")
        public = self._task.args.get("public", False)

        if gist_id:
            existing, error = client.get(gist_id)
            if existing is None:
                self._result.failed = True
                self._result.msg = f"Failed to retrieve gist {gist_id}: {error}"
                return
            if GitHubGist.files_match(GitHubGist.extract_files(existing), files):
                self._apply_result(GitHubGist.normalize_result(existing))
                self._result.changed = False
                self._result.msg = f"Gist {gist_id} already up to date"
                return
            updated, error = client.update(gist_id, description, public, files)
            if updated is None:
                self._result.failed = True
                self._result.msg = f"Failed to update gist {gist_id}: {error}"
                return
            self._apply_result(GitHubGist.normalize_result(updated))
            self._result.changed = True
            self._result.msg = f"Successfully updated gist {self._result.id}"
            return

        created, error = client.create(description, public, files)
        if created is None:
            self._result.failed = True
            self._result.msg = f"Failed to create gist: {error}"
            return
        self._apply_result(GitHubGist.normalize_result(created))
        self._result.changed = True
        self._result.msg = f"Successfully created gist {self._result.id}"

    def _publish_gitlab(self: T) -> None:
        """Create or update a GitLab snippet."""
        client = self._gitlab_client()
        files = self._normalize_files(self._task.args["files"])
        gist_id = self._task.args.get("gist_id")
        project_id = self._task.args.get("project_id")
        description = self._task.args.get("description", "")
        title = self._task.args.get("title") or description or "ansible snippet"
        visibility = self._task.args.get("visibility", "private")

        if gist_id:
            existing, error = client.get(gist_id, project_id=project_id)
            if existing is None:
                self._result.failed = True
                self._result.msg = f"Failed to retrieve snippet {gist_id}: {error}"
                return
            if GitLabSnippet.files_match(GitLabSnippet.extract_files(existing), files):
                self._apply_result(GitLabSnippet.normalize_result(existing))
                self._result.changed = False
                self._result.msg = f"Snippet {gist_id} already up to date"
                return
            updated, error = client.update(
                gist_id,
                title,
                description,
                visibility,
                files,
                project_id=project_id,
            )
            if updated is None:
                self._result.failed = True
                self._result.msg = f"Failed to update snippet {gist_id}: {error}"
                return
            self._apply_result(GitLabSnippet.normalize_result(updated))
            self._result.changed = True
            self._result.msg = f"Successfully updated snippet {self._result.id}"
            return

        created, error = client.create(
            title,
            description,
            visibility,
            files,
            project_id=project_id,
        )
        if created is None:
            self._result.failed = True
            self._result.msg = f"Failed to create snippet: {error}"
            return
        self._apply_result(GitLabSnippet.normalize_result(created))
        self._result.changed = True
        self._result.msg = f"Successfully created snippet {self._result.id}"

    def _delete(self: T) -> None:
        """Delete a gist or snippet."""
        gist_id = self._task.args.get("gist_id")
        if not gist_id:
            raise AnsibleActionFail("gist_id is required when state is absent")

        provider = self._task.args.get("provider", "github")
        if provider == "github":
            deleted, error = self._github_client().delete(gist_id)
        else:
            deleted, error = self._gitlab_client().delete(
                gist_id,
                project_id=self._task.args.get("project_id"),
            )

        if not deleted:
            self._result.failed = True
            self._result.msg = f"Failed to delete {provider} resource {gist_id}: {error}"
            return

        self._result.id = gist_id
        self._result.changed = True
        self._result.msg = f"Successfully deleted {provider} resource {gist_id}"

    def run(
        self: T,
        tmp: None = None,
        task_vars: Optional[Dict[str, JSONTypes]] = None,
    ) -> Dict[str, JSONTypes]:
        """Run the action plugin."""
        self._task.diff = False
        super().run(task_vars=task_vars)

        try:
            self._check_argspec(DOCUMENTATION)
            self._timeout = self._task.args.get("timeout", 30)
            state = self._task.args.get("state", "present")

            if state == "absent":
                self._delete()
            elif not self._task.args.get("files"):
                raise AnsibleActionFail(
                    "files must contain at least one file when state is present",
                )
            else:
                provider = self._task.args.get("provider", "github")
                if provider == "github":
                    self._publish_github()
                else:
                    self._publish_gitlab()
        except AnsibleActionFail:
            raise

        return asdict(self._result)
