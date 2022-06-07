"""Some basic smoke tests."""

from typing import Union

import pytest

from ansible.errors import AnsibleActionFail
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play_context import PlayContext
from ansible.playbook.task import Task
from ansible.plugins import loader as Loader
from ansible.plugins.connection.local import Connection
from ansible.template import Templar

from ...plugins.action.git_away import ActionModule as GitAwayActionModule
from ...plugins.action.git_here import ActionModule as GitHereActionModule
from .definitions import ActionModuleInit


@pytest.mark.parametrize(
    "module",
    (GitHereActionModule, GitAwayActionModule),
    ids=("git_here", "git_away"),
)
def test_fail_argspec(
    action_init: ActionModuleInit,
    module: Union[GitAwayActionModule, GitHereActionModule],
) -> None:
    """Test an argspec failure.

    :param action_init: A fixture for action initialization.
    :param module: The module to test.
    """
    play_context = PlayContext()
    loader = DataLoader()

    action = module(**action_init)
    with pytest.raises(AnsibleActionFail):
        action.run()
