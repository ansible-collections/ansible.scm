"""Shared definitions for unit tests."""

from __future__ import absolute_import, division, print_function  # noqa: I001, UP010


# pylint: disable=invalid-name
__metaclass__ = type  # noqa: UP001
# pylint: enable=invalid-name

import types

from typing import Dict
from typing import Union

from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play_context import PlayContext
from ansible.playbook.task import Task
from ansible.plugins.connection.local import Connection
from ansible.template import Templar


ActionModuleInit = Dict[
    str,
    Union[Connection, PlayContext, DataLoader, Task, types.ModuleType, Templar],
]
