#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""The git_here module stub."""
from __future__ import absolute_import, division, print_function


# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

DOCUMENTATION = """
module: git_here
short_description: Retrieve a repository from a distant location and make it available locally
version_added: "1.0.0"
description:
    - Retrieve a repository from a distant location and make available locally
options:
  origin:
    description:
      - Details about the origin
    type: dict
    required: true
    suboptions:
      url:
        description:
          - The URL for the origin repository
        type: str
  upstream:
    description:
      - Details about the upstream
    default: {}
    type: dict
    suboptions:
      branch:
        description:
          - The branch to use for the upstream
        default: main
        type: str
      url:
        description:
          - The URL for the upstream repository
          - If provided, the local copy of the repository will be updated, rebased from the upstream
          - The update will happen after the branch is created
          - Conflicts will cause the task to fail and the local copy will be removed
        type: str
  branch:
    description:
      - Details about the new branch that will be created
    default: {}
    type: dict
    suboptions:
      name:
        description:
        - Once retrieved, create a new branch using this name.
        default: 'ansible-{play_name}-{timestamp}'
        type: str
      duplicate_detection:
        description:
        - Reusing an existing branch can introduce unexpected behavior
        - If set to true, the task will fail if the remote branch already exists
        - >-
          If set to false and the branch exists the task will use and be updated
          to the existing branch
        - If set to false and the branch does not exist, the branch will be created
        default: true
        type: bool
  parent_directory:
    description:
      - The local directory where the repository will be placed
      - If the parent directory does not exist, it will be created
    default: '{temporary_directory}'
    type: str


notes:

author:
- Bradley Thornton (@cidrblock)
"""

EXAMPLES = r"""
# TO-DO: Enter examples here
"""

RETURN = r"""
# TO-DO: Enter return values here
"""
