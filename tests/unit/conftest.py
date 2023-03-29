"""Shared fixtures for unit tests."""

from __future__ import absolute_import, division, print_function


# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name


import pytest

from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play_context import PlayContext
from ansible.playbook.task import Task
from ansible.plugins import loader as Loader
from ansible.plugins.connection.local import Connection
from ansible.template import Templar

from .definitions import ActionModuleInit


@pytest.fixture
def action_init() -> ActionModuleInit:
    """Provide a fixture for action initialization.

    :returns: A dictionary of action initialization arguments.
    """
    play_context = PlayContext()
    loader = DataLoader()

    return {
        "connection": Connection(play_context=play_context, new_stdin=None),
        "loader": loader,
        "play_context": PlayContext(),
        "shared_loader_obj": Loader,
        "task": Task(),
        "templar": Templar(loader=loader),
    }
