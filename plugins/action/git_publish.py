# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""The git_publish action plugin."""

from __future__ import absolute_import, division, print_function

import shutil
import webbrowser

from contextlib import suppress
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, TypeVar, Union

from ansible.errors import AnsibleActionFail
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play_context import PlayContext
from ansible.playbook.task import Task
from ansible.plugins import loader as plugin_loader
from ansible.plugins.connection.local import Connection
from ansible.template import Templar

# pylint: disable=import-error
from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)

from ..modules.git_publish import DOCUMENTATION
from ..plugin_utils.command import Command
from ..plugin_utils.git_base import ActionInit, GitBase, ResultBase


# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

JSONTypes = Union[bool, int, str, Dict, List]


@dataclass(frozen=False)
class Result(ResultBase):
    """Data structure for the task result."""

    user_name: str = ""
    user_email: str = ""
    pr_url: str = ""


T = TypeVar("T", bound="ActionModule")  # pylint: disable=invalid-name, useless-suppression


class ActionModule(GitBase):
    """The retrieve action plugin."""

    # pylint: disable=too-many-arguments
    def __init__(  # noqa: PLR0913
        self: T,
        connection: Connection,
        loader: DataLoader,
        play_context: PlayContext,
        shared_loader_obj: plugin_loader,
        task: Task,
        templar: Templar,
    ) -> None:
        """Initialize the action plugin.

        :param connection: The connection
        :param loader: The data loader
        :param play_context: The play context
        :param shared_loader_obj: The shared loader object
        :param task: The task
        :param templar: The templar
        """
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

        self._base_command: tuple[str, ...]
        self._path_to_repo: str
        self._play_name: str = ""
        self._supports_async = True
        self._result: Result = Result()

    def _check_argspec(self: T) -> None:
        """Check the argspec for the action plugin.

        :raises AnsibleActionFail: If the argspec is invalid
        """
        aav = AnsibleArgSpecValidator(
            data=self._task.args,
            schema=DOCUMENTATION,
            name=self._task.action,
        )
        valid, errors, self._task.args = aav.validate()
        if not valid:
            raise AnsibleActionFail(errors)
        if self._task.args.get("token") == "":  # noqa: PLC1901
            err = "Token can not be an empty string"
            raise AnsibleActionFail(err)

    def _configure_git_user_name(self: T) -> None:
        """Configure the git user name."""
        command_parts = list(self._base_command)
        command_parts.extend(["config", "--get", "user.name"])
        command = Command(
            command_parts=command_parts,
            fail_msg="Failed to get current user name for git.",
        )
        self._run_command(command=command, ignore_errors=True)
        if command.stdout:
            self._result.user_name = command.stdout
            return

        name = self._task.args["user"]["name"]
        command_parts = list(self._base_command)
        command_parts.extend(["config", "user.name", name])
        command = Command(
            command_parts=command_parts,
            fail_msg="Failed to configure git user name",
        )
        self._run_command(command=command)
        self._result.user_name = name

    def _configure_git_user_email(self: T) -> None:
        """Configure the git user email."""
        command_parts = list(self._base_command)
        command_parts.extend(["config", "--get", "user.email"])
        command = Command(
            command_parts=command_parts,
            fail_msg="Failed to get current user email for git.",
        )
        self._run_command(command=command, ignore_errors=True)
        if command.stdout:
            self._result.user_email = command.stdout
            return

        email = self._task.args["user"]["email"]
        command_parts = list(self._base_command)
        command_parts.extend(["config", "user.email", email])
        command = Command(
            command_parts=command_parts,
            fail_msg="Failed to configure git user email",
        )
        self._run_command(command=command)
        self._result.user_email = email

    def _add(self: T) -> None:
        """Add files for the pending commit."""
        command_parts = list(self._base_command)
        files = " ".join(self._task.args["include"])
        command_parts.extend(["add", files])
        command = Command(
            command_parts=command_parts,
            fail_msg=f"Failed to add the file to the pending commit: {files}",
        )
        self._run_command(command=command)

    def _commit(self: T) -> None:
        """Perform a commit for the pending push."""
        command_parts = list(self._base_command)
        message = self._task.args["commit"]["message"].format(play_name=self._play_name)
        message = message.replace("'", '"')
        command_parts.extend(["commit", "--allow-empty", "-m", message])
        command = Command(
            command_parts=command_parts,
            fail_msg=f"Failed to perform the commit: {message}",
        )
        self._run_command(command=command)

    def _push(self: T) -> None:
        """Push the commit to the origin."""
        command_parts = list(self._base_command)
        command_parts.extend(["remote", "-v"])
        command = Command(
            command_parts=command_parts,
            fail_msg="Failed to get remote",
        )

        self._run_command(command=command)
        try:
            push_line = next(
                line for line in command.stdout_lines if "push" in line and "origin" in line
            )
        except StopIteration:
            self._result.failed = True
            self._result.msg = "Failed to find the origin remote"
            return

        token = self._task.args.get("token")
        no_log = {}
        command_parts = list(self._base_command)

        if token is not None and "https" in push_line:
            token_base64, command_parameters = self._git_auth_header(token)
            command_parts.extend(command_parameters)
            no_log[token_base64] = "<TOKEN>"

        command_parts.extend(["push", "origin"])
        command = Command(
            command_parts=command_parts,
            fail_msg="Failed to perform the push",
            no_log=no_log,
        )
        self._run_command(command=command)
        with suppress(StopIteration):
            self._result.pr_url = next(
                line for line in command.stderr.split("remote:") if "https" in line
            ).strip()

    def _remove_repo(self: T) -> None:
        """Remove the temporary directory."""
        if not self._task.args["remove"]:
            return

        try:
            shutil.rmtree(self._task.args["path"])
        except OSError:
            self._result.failed = True
            self._result.msg = "Failed to remove repository"

    def run(
        self: T,
        tmp: None = None,
        task_vars: Optional[Dict[str, JSONTypes]] = None,
    ) -> Dict[str, JSONTypes]:
        """Run the action plugin.

        :param tmp: The temporary directory
        :param task_vars: The task variables
        :returns: The result
        """
        if isinstance(task_vars, dict):
            self._play_name = str(task_vars["ansible_play_name"])
        self._task.diff = False
        super().run(task_vars=task_vars)

        self._check_argspec()
        if self._result.failed:
            return asdict(self._result)

        self._path_to_repo = self._task.args["path"]
        self._base_command = ("git", "-C", self._path_to_repo)
        self._timeout = self._task.args["timeout"]

        steps = (
            self._configure_git_user_name,
            self._configure_git_user_email,
            self._add,
            self._commit,
            self._push,
            self._remove_repo,
        )

        for step in steps:
            step()
            if self._result.failed:
                return asdict(self._result)

        if self._result.pr_url and self._task.args["open_browser"]:
            webbrowser.open(self._result.pr_url, new=2)

        self._result.msg = f"Successfully published local changes from: {self._path_to_repo}"
        return asdict(self._result)
