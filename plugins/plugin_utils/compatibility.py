"""Function for compatibility."""
from __future__ import absolute_import, division, print_function


# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

import shlex
import sys

from typing import Iterable


def shlex_join(tokens: Iterable[str]) -> str:
    """Concatenate the tokens of a list and return a string.

    ``shlex.join`` was new in version 3.8

    :param tokens: The iterable of strings to join
    :returns: The iterable joined with spaces
    """
    if sys.version_info >= (3, 8):
        return shlex.join(split_command=tokens)
    return " ".join(shlex.quote(token) for token in tokens)
