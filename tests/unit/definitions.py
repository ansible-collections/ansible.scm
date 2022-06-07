"""Shared definitions for unit tests."""

from __future__ import absolute_import, division, print_function


# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

import types

from typing import Dict, Union

from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play_context import PlayContext
from ansible.playbook.task import Task
from ansible.plugins import loader as Loader
from ansible.plugins.connection.local import Connection
from ansible.template import Templar


ActionModuleInit = Dict[
    str,
    Union[Connection, PlayContext, DataLoader, Task, types.ModuleType, Templar],
]
