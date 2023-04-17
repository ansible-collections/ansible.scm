# cspell:ignore envlist
"""tox plugin to emit a github matrix."""
from __future__ import absolute_import, division, print_function

import json
import os
import re
import sys
import uuid

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import List, Tuple, TypeVar

import yaml

from tox.config.cli.parser import ToxParser
from tox.config.loader.memory import MemoryLoader
from tox.config.loader.section import Section
from tox.config.loader.str_convert import StrConvert
from tox.config.sets import ConfigSet, CoreConfigSet, EnvConfigSet
from tox.config.types import EnvList
from tox.plugin import impl
from tox.session.state import State
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
TOX_WORK_DIR = Path()


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


@dataclass
class AnsibleTestConf:
    """Ansible test configuration."""

    deps: str
    passenv: str
    setenv: str
    skip_install: bool
    allowlist_externals: list[str] = field(default_factory=list)
    commands_pre: list[str] = field(default_factory=list)
    commands: list[str] = field(default_factory=list)


def custom_sort(string: str) -> tuple[int, ...]:
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

    galaxy_path = TOX_WORK_DIR / "galaxy.yml"
    c_name, c_namespace = get_collection_name(galaxy_path=galaxy_path)

    conf = AnsibleTestConf(
        allowlist_externals=ALLOWED_EXTERNALS,
        commands_pre=conf_commands_pre(
            c_name=c_name,
            c_namespace=c_namespace,
            env_conf=env_conf,
        ),
        commands=conf_commands(
            c_name=c_name,
            c_namespace=c_namespace,
            env_conf=env_conf,
            galaxy_path=galaxy_path,
            test_type=test_type,
        ),
        deps=conf_deps(env_conf=env_conf, test_type=test_type),
        passenv=conf_passenv(),
        setenv=conf_setenv(env_conf),
        skip_install=True,
    )
    loader = MemoryLoader(**asdict(conf))
    env_conf.loaders.insert(0, loader)


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


def get_collection_name(galaxy_path: Path) -> Tuple[str, str]:
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


def conf_commands(
    c_name: str,
    c_namespace: str,
    env_conf: EnvConfigSet,
    galaxy_path: Path,
    test_type: str,
) -> list[str]:
    """Build the commands for the tox environment.

    :param c_name: The collection name.
    :param c_namespace: The collection namespace.
    :param galaxy_path: The path to the galaxy.yml file.
    :param test_type: The test type, either "integration", "unit", or "sanity".
    :param env_conf: The tox environment configuration object.
    :raises RuntimeError: If the test type is unknown.
    :return: The commands to run.
    """
    if test_type in ["integration", "unit"]:
        return conf_commands_for_integration_unit(
            c_name=c_name,
            c_namespace=c_namespace,
            env_conf=env_conf,
            galaxy_path=galaxy_path,
            test_type=test_type,
        )
    if test_type == "sanity":
        return conf_commands_for_sanity(
            c_name=c_name,
            c_namespace=c_namespace,
            env_conf=env_conf,
        )
    err = f"Unknown test type {test_type}"
    raise RuntimeError(err)


def conf_commands_for_integration_unit(
    c_name: str,
    c_namespace: str,
    env_conf: EnvConfigSet,
    galaxy_path: Path,
    test_type: str,
) -> list[str]:
    """Build the commands for integration and unit tests.

    :param c_name: The collection name.
    :param c_namespace: The collection namespace.
    :param galaxy_path: The path to the galaxy.yml file.
    :param test_type: The test type, either "integration" or "unit".
    :param env_conf: The tox environment configuration object.
    :return: The command to run.
    """
    commands = []
    envtmpdir = env_conf["envtmpdir"]

    if env_conf.name == "unit-py3.8-2.9":
        # We rely on pytest-ansible-unit and need the galaxy.yml file to be in the
        # collections directory. The unit tests will be run from inside the installed collection
        # directory.
        coll_dir = f"{envtmpdir}/collections/ansible_collections/{c_namespace}/{c_name}"
        cp_cmd = f"cp {galaxy_path} {coll_dir}"
        commands.append(cp_cmd)
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
        unit_ch_dir = f"{envtmpdir}/collections/"
    if test_type == "unit":
        commands.append(f"bash -c 'cd {unit_ch_dir} && {command}'")
    else:
        commands.append(command)
    return commands


def conf_commands_for_sanity(
    c_name: str,
    c_namespace: str,
    env_conf: EnvConfigSet,
) -> list[str]:
    """Add commands for sanity tests.

    :param c_name: The collection name.
    :param c_namespace: The collection namespace.
    :param env_conf: The tox environment configuration object.
    :raises RuntimeError: If the python version is not valid.
    :return: The commands to run.
    """
    commands = []
    envtmpdir = env_conf["envtmpdir"]

    py_ver = env_conf["basepython"][0].replace("py", "")
    if "." not in py_ver:
        py_ver = f"{py_ver[0]}.{py_ver[1:]}"
    if py_ver not in VALID_SANITY_PY_VERS:
        err = f"Invalid python version for sanity tests: {py_ver}"
        raise RuntimeError(err)
    command = SANITY_TST_CMD.format(py_ver=py_ver)
    ch_dir = f"cd {envtmpdir}/collections/ansible_collections/{c_namespace}/{c_name}"
    full_command = f"bash -c '{ch_dir} && {command}'"
    commands.append(full_command)
    return commands


def conf_commands_pre(
    env_conf: EnvConfigSet,
    c_name: str,
    c_namespace: str,
) -> list[str]:
    """Build and install the collection.

    :param env_conf: The tox environment configuration object.
    :param c_name: The collection name.
    :param c_namespace: The collection namespace.
    :return: The commands to pre run.
    """
    # pylint: disable=too-many-locals
    commands = []

    # Define some directories"
    envtmpdir = env_conf["envtmpdir"]
    collections_root = f"{envtmpdir}/collections"
    collection_installed_at = f"{collections_root}/ansible_collections/{c_namespace}/{c_name}"
    galaxy_build_dir = f"{envtmpdir}/collection_build"
    end_group = "echo ::endgroup::"

    group = "echo ::group::Make the galaxy build dir"
    commands.append(group)
    commands.append(f"mkdir {galaxy_build_dir}")
    commands.append(end_group)

    group = "echo ::group::Copy the collection to the galaxy build dir"
    commands.append(group)
    cd_tox_dir = f"cd {TOX_WORK_DIR}"
    rsync_cmd = f'rsync -r --cvs-exclude --filter=":- .gitignore" . {galaxy_build_dir}'
    full_cmd = f"bash -c '{cd_tox_dir} && {rsync_cmd}'"
    commands.append(full_cmd)
    commands.append(end_group)

    group = "echo ::group::Remove the toxfile.py"
    commands.append(group)
    rm_toxfile = f"rm {galaxy_build_dir}/toxfile.py"
    commands.append(rm_toxfile)
    commands.append(end_group)

    group = "echo ::group::Build and install the collection"
    commands.append(group)
    cd_build_dir = f"cd {galaxy_build_dir}"
    build_cmd = "ansible-galaxy collection build"
    tar_file = f"{c_namespace}-{c_name}-*.tar.gz"
    install_cmd = f"ansible-galaxy collection install {tar_file} -p {collections_root}"
    full_cmd = f"bash -c '{cd_build_dir} && {build_cmd} && {install_cmd}'"
    commands.append(full_cmd)
    commands.append(end_group)

    group = "echo ::group::Initialize the collection to avoid ansible #68499"
    commands.append(group)
    cd_install_dir = f"cd {collection_installed_at}"
    git_cfg = "git config --global init.defaultBranch main"
    git_init = "git init ."
    full_cmd = f"bash -c '{cd_install_dir} && {git_cfg} && {git_init}'"
    commands.append(full_cmd)
    commands.append(end_group)

    if env_conf.name == "sanity-py3.8-2.9":
        # Avoid "Setuptools is replacing distutils"
        group = "echo ::group::Use old setuptools for sanity-py3.8-2.9"
        commands.append(group)
        pip_install = "pip install setuptools==57.5.0"
        commands.append(pip_install)
        commands.append(end_group)

    return commands


def conf_deps(env_conf: EnvConfigSet, test_type: str) -> str:
    """Add dependencies to the tox environment.

    :param env_conf: The environment configuration.
    :param test_type: The test type.
    :return: The dependencies.
    """
    deps = []
    if test_type in ["integration", "unit"]:
        try:
            with (TOX_WORK_DIR / "test-requirements.txt").open() as fileh:
                deps.extend(fileh.read().splitlines())
        except FileNotFoundError:
            pass

    ansible_version = env_conf.name.split("-")[2]
    base_url = "https://github.com/ansible/ansible/archive/"
    if ansible_version in ["devel", "milestone"]:
        ansible_package = f"{base_url}{ansible_version}.tar.gz"
    else:
        ansible_package = f"{base_url}stable-{ansible_version}.tar.gz"
    deps.append(ansible_package)
    return "\n".join(deps)


def conf_passenv() -> str:
    """Build the pass environment variables for the tox environment.

    :return: The pass environment variables.
    """
    passenv = []
    passenv.append("GITHUB_TOKEN")
    return "\n".join(passenv)


def conf_setenv(env_conf: EnvConfigSet) -> str:
    """Build the set environment variables for the tox environment.

    :param env_conf: The environment configuration.
    :return: The set environment variables.
    """
    envtmpdir = env_conf["envtmpdir"]
    setenv = []
    setenv.append(f"ANSIBLE_COLLECTIONS_PATHS={envtmpdir}/collections/")
    return "\n".join(setenv)
