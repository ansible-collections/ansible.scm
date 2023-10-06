"""Some basic smoke tests."""

from __future__ import absolute_import, annotations, division, print_function


# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

from typing import TYPE_CHECKING

import pytest

from ansible.errors import AnsibleActionFail
from ansible_collections.ansible.scm.plugins.action.git_publish import (
    ActionModule as GitPublishActionModule,
)
from ansible_collections.ansible.scm.plugins.action.git_retrieve import (
    ActionModule as GitRetrieveActionModule,
)


if TYPE_CHECKING:
    from .definitions import ActionModuleInit


@pytest.mark.parametrize(
    "module",
    (GitRetrieveActionModule, GitPublishActionModule),
    ids=("git_retrieve", "git_publish"),
)
def test_fail_argspec(
    action_init: ActionModuleInit,
    module: GitPublishActionModule | GitRetrieveActionModule,
) -> None:
    """Test an argspec failure.

    :param action_init: A fixture for action initialization.
    :param module: The module to test.
    """
    action = module(**action_init)
    with pytest.raises(AnsibleActionFail):
        action.run()
