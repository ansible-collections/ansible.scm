# cspell:ignore envlist
"""tox plugin to emit a github matrix."""

import json
import os
import re
import sys
import uuid

from pathlib import Path

from tox.config.cli.parser import ToxParser
from tox.config.sets import CoreConfigSet
from tox.plugin import impl
from tox.session.state import State
from tox.tox_env.python.api import PY_FACTORS_RE


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


def custom_sort(string: str):
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
def tox_add_core_config(
    core_conf: CoreConfigSet,  # pylint: disable=unused-argument
    state: State,
) -> None:
    """Dump the environment list and exit.

    :param core_conf: The core configuration object.
    :param state: The state object.
    :raises RuntimeError: If multiple python versions are found in an env.
    """
    results = []
    if state.conf.options.gh_matrix == "1234":
        return
    env_list = sorted(list(state.envs.iter()), key=custom_sort)
    for env_name in env_list:
        candidates = []
        factors = env_name.split("-")
        for factor in factors:
            match = PY_FACTORS_RE.match(factor)
            if match:
                candidates.append(match[2])
        if len(candidates) > 1:
            raise RuntimeError(f"Multiple python versions found in {env_name}")
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
        raise RuntimeError("GITHUB_OUTPUT environment variable not set")

    if "\n" in value:
        eof = f"EOF-{uuid.uuid4()}"
        encoded = f"envlist<<{eof}\n{value}\n{eof}\n"
    else:
        encoded = f"envlist={value}\n"

    with Path(gh_output).open("a", encoding="utf-8") as f:
        f.write(encoded)
    sys.exit(0)
