"""Definitions for the command runner."""

from __future__ import absolute_import, division, print_function


# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name


from dataclasses import dataclass, field
from typing import List


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
    stdout_lines: List[str] = field(default_factory=list)
    stderr_lines: List[str] = field(default_factory=list)
