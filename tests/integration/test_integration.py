"""Run the integration tests."""
from __future__ import absolute_import, division, print_function  # noqa: I001, UP010

import subprocess

from typing import Dict

import pytest

from pytest_ansible_network_integration import AnsibleProject


# pylint: disable=invalid-name
__metaclass__ = type  # noqa: UP001
# pylint: enable=invalid-name


def run(localhost_project: AnsibleProject, environment: Dict[str, str]) -> None:
    """Run the integration tests.

    :param localhost_project: The localhost project.
    :param environment: The environment.
    """
    __tracebackhide__ = True  # pylint: disable=unused-variable
    args = [
        "ansible-navigator",
        "run",
        str(localhost_project.playbook),
        "--ee",
        "false",
        "--mode",
        "stdout",
        "--pas",
        str(localhost_project.playbook_artifact),
        "--ll",
        "debug",
        "--lf",
        str(localhost_project.log_file),
        "--cdcp",
        str(localhost_project.collection_doc_cache),
        "-vvvv",
    ]
    process = subprocess.run(
        args=args,
        env=environment,
        capture_output=True,
        check=False,
        shell=False,
    )
    if process.returncode:
        print(process.stdout.decode("utf-8"))
        print(process.stderr.decode("utf-8"))

        pytest.fail(msg=f"Integration test failed: {localhost_project.role}")


def test_integration(
    localhost_project: AnsibleProject,
    environment: Dict[str, str],
) -> None:
    """Run the integration tests.

    :param localhost_project: The localhost project.
    :param environment: The environment.
    """
    run(localhost_project, environment)
