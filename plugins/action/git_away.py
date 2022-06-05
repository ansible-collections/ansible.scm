# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""The git_away action plugin."""

from __future__ import absolute_import, division, print_function

import shutil

from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional, Union

from ansible.errors import AnsibleActionFail
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play_context import PlayContext
from ansible.playbook.task import Task
from ansible.plugins import loader as Loader
from ansible.plugins.action import ActionBase
from ansible.plugins.connection.local import Connection
from ansible.template import Templar

# pylint: disable=import-error
from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)

from ..modules.git_away import DOCUMENTATION
from ..plugin_utils.command import Command


# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

JSONTypes = Union[bool, int, str, Dict, List]


@dataclass(frozen=False)
class Result:
    """Data structure for the task result."""

    changed: bool = True
    failed: bool = False
    msg: str = ""
    output: List[Dict[str, JSONTypes]] = field(default_factory=list)


class ActionModule(ActionBase):  # type: ignore[misc] # parent has type Any
    """The retrieve action plugin."""

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        connection: Connection,
        loader: DataLoader,
        play_context: PlayContext,
        shared_loader_obj: Loader,
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
            connection=connection,
            loader=loader,
            play_context=play_context,
            shared_loader_obj=shared_loader_obj,
            templar=templar,
            task=task,
        )

        self._base_command: str
        self._path_to_repo: str
        self._supports_async = True
        self._result: Result = Result()

    def _check_argspec(self) -> None:
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

    def _append_result(self, command: Command) -> None:
        """Append the result of the command to the result.

        :param command: The command to append
        """
        self._result.output.append(
            {
                "command": command.command,
                "stdout_lines": command.stdout_lines,
                "stderr_lines": command.stderr_lines,
                "return_code": command.return_code,
            },
        )

    def _add(self) -> None:
        """Add files for the pending commit."""
        base = self._base_command
        files = " ".join(self._task.args["include"])
        command = Command(
            command=f"{base} add {files}",
            fail_msg=f"Failed to add the file to the pending commit: {files}",
        )
        self._run_command(command=command)

    def _commit(self) -> None:
        """Perform a commit for the pending push."""
        base = self._base_command
        message = self._task.args["commit"]["message"].format(play_name=self._task.play)
        message = message.replace("'", '"')
        command = Command(
            command=f"{base} commit --allow-empty -m '{message}'",
            fail_msg=f"Failed to perform the commit: {message}",
        )
        self._run_command(command=command)

    def _push(self) -> None:
        """Push the commit to the origin."""
        base = self._base_command
        command = Command(
            command=f"{base} push origin",
            fail_msg="Failed to perform the push",
        )
        self._run_command(command=command)

    def _remove_repo(self) -> None:
        """Remove the temporary directory."""
        if not self._task.args["remove"]:
            return
        try:
            shutil.rmtree(self._task.args["path"])
        except OSError:
            self._result.failed = True
            self._result.msg = "Failed to remove repository"

    def _run_command(self, command: Command) -> None:
        """Run a command and append the command result to the results.

        :param command: The command to run
        """
        command.run()
        self._append_result(command)

        if command.return_code != 0:
            self._result.failed = True
            self._result.msg = command.fail_msg

    def run(
        self,
        tmp: None = None,
        task_vars: Optional[Dict[str, JSONTypes]] = None,
    ) -> Dict[str, JSONTypes]:
        """Run the action plugin.

        :param tmp: The temporary directory
        :param task_vars: The task variables
        :returns: The result
        """
        self._task.diff = False
        super().run(task_vars=task_vars)

        self._check_argspec()
        if self._result.failed:
            return asdict(self._result)

        self._path_to_repo = self._task.args["path"]

        self._base_command = f"git -C {self._path_to_repo}"

        steps = (
            self._add,
            self._commit,
            self._push,
            self._remove_repo,
        )

        for step in steps:
            step()
            if self._result.failed:
                shutil.rmtree(self._parent_directory)
                return asdict(self._result)

        self._result.msg = f"Successfully published local changes from: {self._path_to_repo}"
        return asdict(self._result)
