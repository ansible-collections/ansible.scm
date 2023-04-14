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
from typing import List, TypeVar

import yaml

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


def custom_sort(string: str) -> tuple:
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
    global TOX_WORK_DIR  # pylint: disable=global-statement # noqa: PLW0603
    TOX_WORK_DIR = state.conf.work_dir
    if not state.conf.options.ansible:
        return

    env_list = add_ansible_matrix(state)

    if state.conf.options.gh_matrix == "1234":
        return

    generate_gh_matrix(env_list=env_list, state=state)
    sys.exit(0)


@impl
def tox_add_env_config(env_conf: EnvConfigSet, state: State) -> None:
    """Add the test requirements and ansible-core to the virtual environment.

    :param env_conf: The environment configuration object.
    :param state: The state object.
    """
    # pylint: disable=unused-argument

    test_type = env_conf.name.split("-")[0]
    if test_type not in ["integration", "sanity", "unit"]:
        return
    add_deps_to_env(env_conf=env_conf, test_type=test_type)


@impl
def tox_before_run_commands(tox_env: ToxEnv) -> None:
    """Run the ansible-test sanity command before the other commands.

    :param tox_env: The tox environment object.
    """
    if not tox_env.options.ansible:
        return

    # Add the allowed external commands to the tox environment
    tox_env.conf["allowlist_externals"].extend(ALLOWED_EXTERNALS)

    # Add the environment variables to the tox environment
    add_env_vars_to_env(tox_env=tox_env)

    galaxy_path = TOX_WORK_DIR / "galaxy.yml"

    c_name, c_namespace = get_collection_name(galaxy_path=galaxy_path)

    build_install_collection(tox_env, c_name, c_namespace)

    test_type = tox_env.name.split("-")[0]
    if test_type not in ["unit", "integration", "sanity"]:
        return

    if test_type in ["unit", "integration"]:
        cmds_for_integration_unit(
            c_name=c_name,
            c_namespace=c_namespace,
            galaxy_path=galaxy_path,
            test_type=test_type,
            tox_env=tox_env,
        )

    if test_type == "sanity":
        cmds_for_sanity(
            c_name=c_name,
            c_namespace=c_namespace,
            tox_env=tox_env,
        )


def add_ansible_matrix(state: State) -> EnvList:
    """Add the ansible matrix to the state.

    :param state: The state object.
    :return: The environment list.
    """
    ansible_config = state.conf.get_section_config(
        Section(None, "ansible"),
        base=[],
        of_type=AnsibleConfigSet,
        for_env=None,
    )
    env_list = StrConvert().to_env_list(ENV_LIST)
    env_list.envs = [
        env for env in env_list.envs if all(skip not in env for skip in ansible_config["skip"])
    ]
    env_list.envs = sorted(env_list.envs, key=custom_sort)
    state.conf.core.loaders.insert(
        0,
        MemoryLoader(env_list=env_list),
    )
    return env_list


T = TypeVar("T", bound=ConfigSet)


class AnsibleConfigSet(ConfigSet):
    """The ansible configuration."""

    def register_config(self: T) -> None:
        """Register the ansible configuration."""
        self.add_config(
            "skip",
            of_type=List[str],
            default=[],
            desc="ansible configuration",
        )


def generate_gh_matrix(env_list: EnvList, state: State) -> None:
    """Generate the github matrix.

    :param env_list: The environment list.
    :param state: The state object.
    :raises RuntimeError: If multiple python versions are found in an environment.
    """
    results = []

    for env_name in env_list.envs:
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


def add_env_vars_to_env(tox_env: ToxEnv) -> None:
    """Add environment variables to the tox environment.

    :param tox_env: The tox environment object.
    """
    setenv = {"ANSIBLE_COLLECTIONS_PATHS": f"{tox_env.env_tmp_dir}/collections/"}
    tox_env.conf["setenv"].update(setenv)
    tox_env.conf["passenv"].append("GITHUB_TOKEN")


def add_deps_to_env(env_conf: EnvConfigSet, test_type: str) -> None:
    """Add dependencies to the tox environment.

    :param env_conf: The environment configuration.
    :param test_type: The test type.
    """
    deps = []
    if test_type in ["integration", "unit"]:
        try:
            with (TOX_WORK_DIR / "test-requirements.txt").open() as fileh:
                deps.extend(fileh.readlines())
        except FileNotFoundError:
            pass

    ansible_version = env_conf.name.split("-")[2]
    base_url = "https://github.com/ansible/ansible/archive/"
    if ansible_version in ["devel", "milestone"]:
        ansible_package = f"{base_url}{ansible_version}.tar.gz"
    else:
        ansible_package = f"{base_url}stable-{ansible_version}.tar.gz"
    deps.append(ansible_package)

    loader = MemoryLoader(deps="\n".join(deps), package="skip")
    env_conf.loaders.insert(0, loader)


def get_collection_name(galaxy_path: Path) -> tuple[str, str]:
    """Extract collection information from the galaxy.yml file.

    :param galaxy_path: The path to the galaxy.yml file.
    :return: The collection name.
    :raises RuntimeError: If the galaxy.yml file is not found.
    """
    try:
        with galaxy_path.open() as galaxy_file:
            galaxy = yaml.safe_load(galaxy_file)
    except FileNotFoundError as exc:
        err = f"Unable to find galaxy.yml file at {galaxy_path}"
        raise RuntimeError(err) from exc

    try:
        c_name = galaxy["name"]
        c_namespace = galaxy["namespace"]
    except KeyError as exc:
        err = f"Unable to find {exc} in galaxy.yml"
        raise RuntimeError(err) from exc
    return c_name, c_namespace


def build_install_collection(tox_env: ToxEnv, c_name: str, c_namespace: str) -> None:
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
    end_group = "echo ::endgroup::"

    group = "echo ::group::Make the galaxy build dir"
    commands_pre.append(Command(args=shlex.split(group)))
    commands_pre.append(Command(args=shlex.split(f"mkdir {galaxy_build_dir}")))
    commands_pre.append(Command(args=shlex.split(end_group)))

    group = "echo ::group::Copy the collection to the galaxy build dir"
    commands_pre.append(Command(args=shlex.split(group)))
    cd_tox_dir = f"cd {TOX_WORK_DIR}"
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


def cmds_for_integration_unit(
    c_name: str,
    c_namespace: str,
    galaxy_path: Path,
    test_type: str,
    tox_env: ToxEnv,
) -> None:
    """Add commands for integration and unit tests.

    :param c_name: The collection name.
    :param c_namespace: The collection namespace.
    :param galaxy_path: The path to the galaxy.yml file.
    :param test_type: The test type, either "integration" or "unit".
    :param tox_env: The tox environment object.
    """
    if tox_env.name == "unit-py3.8-2.9":
        # We rely on pytest-ansible-unit and need the galaxy.yml file to be in the
        # collections directory. The unit tests will be run from inside the installed collection
        # directory.
        coll_dir = f"{tox_env.env_tmp_dir}/collections/ansible_collections/{c_namespace}/{c_name}"
        cp_cmd = f"cp {galaxy_path} {coll_dir}"
        tox_env.conf["commands"].append(Command(args=shlex.split(cp_cmd)))
        command = UNIT_3_8_2_9.format(
            toxinidir=TOX_WORK_DIR,
            test_type=test_type,
        )
        unit_ch_dir = coll_dir
    else:
        # pytest-ansible-units is not needed, because if the unit tests are run
        # from the root of the collections directory, the collection
        # will be found natively by ansible-core
        command = UNIT_INT_TST_CMD.format(
            toxinidir=TOX_WORK_DIR,
            test_type=test_type,
        )
        unit_ch_dir = f"{tox_env.env_tmp_dir}/collections/"
    if test_type == "unit":
        command = f"bash -c 'cd {unit_ch_dir} && {command}'"
    tox_env.conf["commands"].append(Command(args=shlex.split(command)))


def cmds_for_sanity(c_name: str, c_namespace: str, tox_env: ToxEnv) -> None:
    """Add commands for sanity tests.

    :param c_name: The collection name.
    :param c_namespace: The collection namespace.
    :param tox_env: The tox environment object.
    :raises RuntimeError: If the python version is not valid.
    """
    py_ver = tox_env.conf["basepython"][0].replace("py", "")
    if "." not in py_ver:
        py_ver = f"{py_ver[0]}.{py_ver[1:]}"
    if py_ver not in VALID_SANITY_PY_VERS:
        err = f"Invalid python version for sanity tests: {py_ver}"
        raise RuntimeError(err)
    command = SANITY_TST_CMD.format(py_ver=py_ver)
    ch_dir = f"cd {tox_env.env_tmp_dir}/collections/ansible_collections/{c_namespace}/{c_name}"
    full_command = shlex.split(f"bash -c '{ch_dir} && {command}'")
    tox_env.conf["commands"].append(Command(args=full_command))
