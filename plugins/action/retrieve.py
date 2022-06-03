# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""The retrieve action plugin."""

from __future__ import absolute_import, division, print_function

import datetime
import tempfile

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Union

from ansible.errors import AnsibleActionFail
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play_context import PlayContext
from ansible.playbook.task import Task
from ansible.plugins import loader as Loader
from ansible.plugins.action import ActionBase
from ansible.plugins.connection.local import Connection
from ansible.template import Templar
from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)

from ..modules.retrieve import DOCUMENTATION
from ..plugin_utils.command_runner import Command, CommandRunner


# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

JSONTypes = Union[bool, int, str, Dict, List]


@dataclass(frozen=False)
class Result:
    """Data structure for the task result."""

    # pylint: disable=too-many-instance-attributes
    branch_name: str = ""
    branches: List[str] = field(default_factory=list)
    changed: bool = True
    failed: bool = False
    name: str = ""
    msg: str = ""
    path: str = ""
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
                "stdout_lines": command.stdout.splitlines(),
                "stderr_lines": command.stderr.splitlines(),
                "return_code": command.return_code,
            },
        )

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
        # pylint: disable=too-many-branches
        # pylint: disable=too-many-locals
        # pylint: disable=too-many-return-statements
        # pylint: disable=too-many-statements
        self._task.diff = False
        super().run(task_vars=task_vars)
        self._check_argspec()
        if self._result.failed:
            return asdict(self._result)

        command_runner = CommandRunner()
        # pylint: disable=consider-using-with
        parent_directory = self._task.args["parent_directory"].format(
            temporary_directory=tempfile.TemporaryDirectory().name,
        )
        # pylint: enable=consider-using-with

        Path(parent_directory).mkdir(parents=True, exist_ok=True)

        base_command = f"git -C {parent_directory}"
        command = (
            f"{base_command} clone --depth=1 --progress --no-single-branch"
            f" {self._task.args['origin']['url']}"
        )
        commands = [Command(identity="clone", command=command)]
        command_runner.run_multi_thread(commands)
        self._append_result(commands[0])

        if commands[0].return_code != 0:
            self._result.failed = True
            self._result.msg = f"Failed to clone repository: {self._task.args['origin']['url']}"
            return asdict(self._result)

        repo_name = commands[0].stderr.splitlines()[0].split("'")[1]
        self._result.name = repo_name
        repo_path = Path(parent_directory) / repo_name
        self._result.path = str(repo_path)

        base_command = f"git -C {repo_path}"
        command = f"{base_command} branch -a"
        commands = [Command(identity="branch list", command=command)]
        command_runner.run_multi_thread(commands)
        self._append_result(commands[0])

        if commands[0].return_code != 0 or commands[0].stdout is None:
            self._result.failed = True
            self._result.msg = f"Failed to list branches: {self._task.args['origin']['url']}"
            return asdict(self._result)

        branches = []
        for line in commands[0].stdout.splitlines():
            if line.startswith("*"):
                branches.append(line.split()[1])
            else:
                branches.append(line.split("/")[-1])
        self._result.branches = branches

        branch_name = self._task.args["branch"]["name"]
        timestamp = (
            datetime.datetime.now(tz=datetime.timezone.utc)
            .astimezone()
            .isoformat()
            .replace(":", "")
        )

        branch_name = branch_name.format(
            play_name=self._task.play,
            timestamp=timestamp,
        )
        self._result.branch_name = branch_name

        duplicate_detection = self._task.args["branch"]["duplicate_detection"]
        branch_exists = branch_name in branches
        if duplicate_detection and branch_exists:
            self._result.failed = True
            self._result.msg = f"Branch '{branch_name}' already exists"
            return asdict(self._result)

        if branch_exists:
            command = f"{base_command} switch {branch_name}"
        else:
            command = f"{base_command} checkout -t -b {branch_name}"
        commands = [Command(identity="branch", command=command)]
        command_runner.run_multi_thread(commands)
        self._append_result(commands[0])

        if commands[0].return_code != 0:
            self._result.failed = True
            self._result.msg = f"Failed to change branches to: {branch_name}"
            return asdict(self._result)

        if self._task.args["upstream"].get("url"):
            command = f"{base_command} remote add upstream {self._task.args['upstream']['url']}"
            commands = [Command(identity="remote add upstream", command=command)]
            command_runner.run_multi_thread(commands)
            self._append_result(commands[0])

            if commands[0].return_code != 0:
                self._result.failed = True
                self._result.msg = f"Failed to add upstream: {self._task.args['upstream']['url']}"
                return asdict(self._result)

            command = (
                f"{base_command} pull upstream {self._task.args['upstream']['branch']} --rebase"
            )
            commands = [Command(identity="pull upstream", command=command)]
            command_runner.run_multi_thread(commands)
            self._append_result(commands[0])

            if commands[0].return_code != 0:
                self._result.failed = True
                self._result.msg = f"Failed to pull upstream: {self._task.args['upstream']['url']}"
                return asdict(self._result)

        return asdict(self._result)
