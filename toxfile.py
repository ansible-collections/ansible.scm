# cspell:ignore envlist
"""tox plugin to emit a github matrix."""
from __future__ import absolute_import, division, print_function

import json
import os
import re
import shlex
import sys
import uuid

from pathlib import Path
from typing import Tuple

from tox.config.cli.parser import ToxParser
from tox.config.loader.memory import MemoryLoader
from tox.config.loader.section import Section
from tox.config.loader.str_convert import StrConvert
from tox.config.sets import ConfigSet, CoreConfigSet, EnvConfigSet
from tox.config.types import Command, EnvList
from tox.plugin import impl
from tox.session.state import State
from tox.tox_env.api import ToxEnv
from tox.tox_env.python.api import PY_FACTORS_RE
from tox.tox_env.python.pip.req.file import ParsedRequirement


ALLOWED_EXTERNALS = [
    "bash",
    "cp",
    "git",
    "rm",
    "rsync",
    "mkdir",
    "cd",
    "echo",
]
ENV_LIST = """
{integration, sanity, unit}-py3.8-{2.9, 2.10, 2.11, 2.12, 2.13}
{integration, sanity, unit}-py3.9-{2.10, 2.11, 2.12, 2.13, 2.14, milestone, devel}
{integration, sanity, unit}-py3.10-{2.12, 2.13, 2.14, milestone, devel}
{integration, sanity, unit}-py3.11-{2.14, milestone, devel}
"""
UNIT_INT_TST_CMD = "python -m pytest -p no:ansible-units {toxinidir}/tests/{test_type}"
UNIT_3_8_2_9 = "python -m pytest {toxinidir}/tests/{test_type}"
SANITY_TST_CMD = "ansible-test sanity --local --requirements --python {py_ver}"
VALID_SANITY_PY_VERS = ["3.8", "3.9", "3.10", "3.11"]
TOX_WORK_DIR = ""


def custom_sort(string: str) -> Tuple[int, ...]:
    """Convert a env name into a tuple of ints.

    In the case of a string, use the ord() of the first two characters.

    :param string: The string to sort.
    :return: The tuple of converted values.
    """
    parts = re.split(r"\.|-|py", string)
    converted = []
    for part in parts:
        if not part:
            continue
        try:
            converted.append(int(part))
        except ValueError:
            num_part = "".join((str(ord(char)).rjust(3, "0")) for char in part[0:2])
            converted.append(int(num_part))
    return tuple(converted)


@impl
def tox_add_option(parser: ToxParser) -> None:
    """Add the --gh-matrix option to the tox CLI.

    :param parser: The tox CLI parser.
    """
    parser.add_argument(
        "--gh-matrix",
        action="store",
        default="1234",
        dest="gh_matrix",
        help="Emit a github matrix",
    )

    parser.add_argument(
        "--ansible",
        action="store_true",
        default=False,
        help="Enable ansible testing",
    )


@impl
def tox_add_core_config(
    core_conf: CoreConfigSet,  # pylint: disable=unused-argument
    state: State,
) -> None:
    """Dump the environment list and exit.

    :param core_conf: The core configuration object.
    :param state: The state object.
    """
    # pylint: disable=too-many-locals
    results = []
    if state.conf.options.gh_matrix == "1234":
        return
    env_list = sorted((state.envs.iter()), key=custom_sort)
    for env_name in env_list:
        candidates = []
        factors = env_name.split("-")
        for factor in factors:
            match = PY_FACTORS_RE.match(factor)
            if match:
                candidates.append(match[2])
        if len(candidates) > 1:
            err = f"Multiple python versions found in {env_name}"
            raise RuntimeError(err)
        if len(candidates) == 0:
            results.append(
                {
                    "name": env_name,
                    "factors": factors,
                    "python": state.conf.options.gh_matrix,
                },
            )
        else:
            if "." in candidates[0]:
                version = candidates[0]
            else:
                version = f"{candidates[0][0]}.{candidates[0][1:]}"
            results.append(
                {
                    "name": env_name,
                    "factors": factors,
                    "python": version,
                },
            )

    gh_output = os.getenv("GITHUB_OUTPUT")
    value = json.dumps(results)
    if not gh_output:
        err = "GITHUB_OUTPUT environment variable not set"
        raise RuntimeError(err)

    if "\n" in value:
        eof = f"EOF-{uuid.uuid4()}"
        encoded = f"envlist<<{eof}\n{value}\n{eof}\n"
    else:
        encoded = f"envlist={value}\n"

    with Path(gh_output).open("a", encoding="utf-8") as f:
        f.write(encoded)
    sys.exit(0)


def build_install_collection(tox_env: ToxEnv, c_name: str, c_namespace: str):
    """Build and install the collection.

    :param tox_env: The tox environment object.
    :param c_name: The collection name.
    :param c_namespace: The collection namespace.
    """
    # pylint: disable=too-many-locals
    commands_pre = []

    # Define some directories"
    collections_root = tox_env.env_tmp_dir / "collections"
    collection_installed_at = collections_root / f"ansible_collections/{c_namespace}/{c_name}"
    galaxy_build_dir = tox_env.env_tmp_dir / "collection_build"
    root_dir = tox_env.conf._conf.work_dir  # pylint: disable=protected-access
    end_group = "echo ::endgroup::"

    group = "echo ::group::Make the galaxy build dir"
    commands_pre.append(Command(args=shlex.split(group)))
    commands_pre.append(Command(args=shlex.split(f"mkdir {galaxy_build_dir}")))
    commands_pre.append(Command(args=shlex.split(end_group)))

    group = "echo ::group::Copy the collection to the galaxy build dir"
    commands_pre.append(Command(args=shlex.split(group)))
    cd_tox_dir = f"cd {root_dir}"
    rsync_cmd = f'rsync -r --cvs-exclude --filter=":- .gitignore" . {galaxy_build_dir}'
    full_cmd = f"bash -c '{cd_tox_dir} && {rsync_cmd}'"
    commands_pre.append(Command(args=shlex.split(full_cmd)))
    commands_pre.append(Command(args=shlex.split(end_group)))

    group = "echo ::group::Remove the toxfile.py"
    commands_pre.append(Command(args=shlex.split(group)))
    rm_toxfile = f"rm {galaxy_build_dir}/toxfile.py"
    commands_pre.append(Command(args=shlex.split(rm_toxfile)))
    commands_pre.append(Command(args=shlex.split(end_group)))

    group = "echo ::group::Build and install the collection"
    commands_pre.append(Command(args=shlex.split(group)))
    cd_build_dir = f"cd {galaxy_build_dir}"
    build_cmd = "ansible-galaxy collection build"
    tar_file = f"{c_namespace}-{c_name}-*.tar.gz"
    install_cmd = f"ansible-galaxy collection install {tar_file} -p {collections_root}"
    full_cmd = f"bash -c '{cd_build_dir} && {build_cmd} && {install_cmd}'"
    commands_pre.append(Command(args=shlex.split(full_cmd)))
    commands_pre.append(Command(args=shlex.split(end_group)))

    group = "echo ::group::Initialize the collection to avoid ansible #68499"
    commands_pre.append(Command(args=shlex.split(group)))
    cd_install_dir = f"cd {collection_installed_at}"
    git_cfg = "git config --global init.defaultBranch main"
    git_init = "git init ."
    full_cmd = f"bash -c '{cd_install_dir} && {git_cfg} && {git_init}'"
    commands_pre.append(Command(args=shlex.split(full_cmd)))
    commands_pre.append(Command(args=shlex.split(end_group)))

    if tox_env.name == "sanity-py3.8-2.9":
        # Avoid "Setuptools is replacing distutils"
        group = "echo ::group::Use old setuptools for sanity-py3.8-2.9"
        commands_pre.append(Command(args=shlex.split(group)))
        pip_install = "pip install setuptools==57.5.0"
        commands_pre.append(Command(args=shlex.split(pip_install)))
        commands_pre.append(Command(args=shlex.split(end_group)))

    tox_env.conf["commands_pre"].extend(commands_pre)
