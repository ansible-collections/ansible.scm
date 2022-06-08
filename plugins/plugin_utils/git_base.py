"""A base class for the git action plugins."""
from __future__ import absolute_import, division, print_function


# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

from dataclasses import dataclass, field, fields
from types import ModuleType
from typing import Dict, List, Union

from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play_context import PlayContext
from ansible.playbook.task import Task
from ansible.plugins import loader as Loader
from ansible.plugins.action import ActionBase
from ansible.plugins.connection.local import Connection
from ansible.template import Templar

from .command import Command


JSONTypes = Union[bool, int, str, Dict, List]


@dataclass(frozen=False)
class ActionInit:
    """The keyword arguments for action base."""

    connection: Connection
    loader: DataLoader
    play_context: PlayContext
    shared_loader_obj: Loader
    task: Task
    templar: Templar

    @property
    def asdict(
        self,
    ) -> Dict[str, Union[Connection, DataLoader, PlayContext, ModuleType, Task, Templar]]:
        """Create a dictionary, avoiding the deepcopy with dataclass.asdict.

        :return: A dictionary of the keyword arguments.
        """
        return {field.name: getattr(self, field.name) for field in fields(self)}


@dataclass(frozen=False)
class ResultBase:
    """Data structure for the task result."""

    # pylint: disable=too-many-instance-attributes

    changed: bool = True
    failed: bool = False
    msg: str = ""
    output: List[Dict[str, JSONTypes]] = field(default_factory=list)


class GitBase(ActionBase):  # type: ignore[misc] # parent has type Any
    """Base class for the git paction plugins."""

    def __init__(self, action_init: ActionInit) -> None:
        """Initialize the action plugin.

        :param action_init: The keyword arguments for action base
        """
        super().__init__(**action_init.asdict)
        self._result: ResultBase = ResultBase()

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

    def _run_command(self, command: Command, ignore_errors: bool = False) -> None:
        """Run a command and append the command result to the results.

        :param command: The command to run
        :param ignore_errors: If errors should be ignored
        """
        result = self._low_level_execute_command(cmd=command.command)
        command.return_code = result["rc"]
        command.stdout = result["stdout"]
        command.stdout_lines = result["stdout_lines"]
        command.stderr = result["stderr"]
        command.stderr_lines = result["stderr_lines"]
        self._append_result(command)

        if command.return_code != 0 and not ignore_errors:
            self._result.failed = True
            self._result.msg = command.fail_msg
