"""Definitions for the command runner."""

from __future__ import absolute_import, division, print_function


# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

import subprocess

from dataclasses import dataclass, field
from typing import Dict, List, Union


JSONTypes = Union[bool, int, str, Dict, List]


@dataclass(frozen=False)
class Command:
    """Data structure for details of a command to be run.

    A ``Command`` is updated after instantiated with details from either
    ``stdout`` or ``stderr``.
    """

    command: str
    fail_msg: str
    return_code: int = -1
    stdout: str = ""
    stderr: str = ""
    errors: List[str] = field(default_factory=list)

    @property
    def stderr_lines(self) -> List[str]:
        """Produce a list of stderr lines.

        :returns: A list of stderr lines
        """
        return self.stderr.splitlines()

    @property
    def stdout_lines(self) -> List[str]:
        """Produce a list of stdout lines.

        :returns: A list of stdout lines
        """
        return self.stdout.splitlines()

    def run(self) -> None:
        """Run the command."""
        try:
            proc_out = subprocess.run(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                universal_newlines=True,
                shell=True,
            )

            self.return_code = proc_out.returncode
            self.stdout = proc_out.stdout
            self.stderr = proc_out.stderr
        except subprocess.CalledProcessError as exc:
            self.stderr = str(exc.stderr)
            self.errors = [str(exc.stderr)]
            self.return_code = exc.returncode
