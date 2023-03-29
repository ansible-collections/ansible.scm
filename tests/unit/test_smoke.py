"""Some basic smoke tests."""

from __future__ import absolute_import, division, print_function


# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

from typing import Union

import pytest

from ansible.errors import AnsibleActionFail

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
    action = module(**action_init)
    with pytest.raises(AnsibleActionFail):
        action.run()
