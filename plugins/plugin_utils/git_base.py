"""A base class for the git action plugins."""
from __future__ import absolute_import, division, print_function


# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

import base64
import subprocess

from dataclasses import dataclass, field, fields
from types import ModuleType
from typing import Dict, List, Tuple, TypeVar, Union

from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play_context import PlayContext
from ansible.playbook.task import Task
from ansible.plugins import loader as plugin_loader
from ansible.plugins.action import ActionBase
from ansible.plugins.connection.local import Connection
from ansible.template import Templar

from .command import Command


JSONTypes = Union[bool, int, str, Dict, List]

T = TypeVar("T", bound="ActionInit")


@dataclass(frozen=False)
class ActionInit:
    """The keyword arguments for action base."""

    connection: Connection
    loader: DataLoader
    play_context: PlayContext
    shared_loader_obj: plugin_loader
    task: Task
    templar: Templar

    @property
    def asdict(
        self: T,
    ) -> Dict[str, Union[Connection, DataLoader, PlayContext, ModuleType, Task, Templar]]:
        """Create a dictionary, avoiding the deepcopy with dataclass.asdict.

        :return: A dictionary of the keyword arguments.
        """
        return {field.name: getattr(self, field.name) for field in fields(self)}


@dataclass(frozen=False)
class ResultBase:
    """Data structure for the task result."""

    changed: bool = True
    failed: bool = False
    msg: str = ""
    output: List[Dict[str, Union[int, Dict[str, str], List[str], str]]] = field(
        default_factory=list,
    )


U = TypeVar("U", bound="GitBase")


class GitBase(ActionBase):  # type: ignore[misc] # parent has type Any
    """Base class for the git paction plugins."""

    def __init__(self: U, action_init: ActionInit) -> None:
        """Initialize the action plugin.

        :param action_init: The keyword arguments for action base
        """
        super().__init__(**action_init.asdict)
        self._result: ResultBase = ResultBase()
        self._timeout: int

    @staticmethod
    def _git_auth_header(token: str) -> Tuple[str, List[str]]:
        """Create the authorization header.

        helpful: https://github.com/actions/checkout/blob/main/src/git-auth-helper.ts#L56

        :param token: The token
        :return: The base64 encoded token and the authorization header cli parameter
        """
        basic = f"x-access-token:{token}"
        basic_encoded = base64.b64encode(basic.encode("utf-8")).decode("utf-8")
        cli_parameters = [
            "-c",
            f"http.extraheader=AUTHORIZATION: basic {basic_encoded}",
        ]
        return basic_encoded, cli_parameters

    def _run_command(self: U, command: Command, ignore_errors: bool = False) -> None:
        """Run a command and append the command result to the results.

        :param command: The command to run
        :param ignore_errors: If errors should be ignored
        """
        try:
            result = subprocess.run(
                command.command_parts,
                env=command.env,
                check=True,
                capture_output=True,
                timeout=self._timeout,
            )
            command.return_code = result.returncode
            command.stdout = result.stdout.decode("utf-8") or ""
            command.stderr = result.stderr.decode("utf-8") or ""

        except subprocess.CalledProcessError as exc:
            command.return_code = exc.returncode
            command.stdout = exc.stdout.decode("utf-8") if exc.stdout else ""
            command.stderr = exc.stderr.decode("utf-8") if exc.stderr else ""
            if not ignore_errors:
                self._result.failed = True
                self._result.msg = command.fail_msg

        except subprocess.TimeoutExpired as exc:
            command.return_code = 62  # ETIME, Timer expired
            command.stdout = exc.stdout.decode("utf-8") if exc.stdout else ""
            command.stderr = exc.stderr.decode("utf-8") if exc.stderr else ""
            if not ignore_errors:
                self._result.failed = True
                self._result.msg = f"Timeout: {command.fail_msg}"

        command.stdout_lines = command.stdout.splitlines()
        command.stderr_lines = command.stderr.splitlines()

        self._result.output.append(command.cleaned)
