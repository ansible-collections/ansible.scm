#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function


# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

DOCUMENTATION = """
module: git_here
short_description: >-
  Retrieve a repository from a distant location and make it available on the execution node
version_added: "1.0.0"
description:
    - Retrieve a repository from a distant location and make it available on the execution node
options:
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
  origin:
    description:
      - Details about the origin
    type: dict
    required: true
    suboptions:
      token:
        description:
          - The token to use to authenticate to the origin repository
          - If provided, an 'http.extraheader' will be added to the commands interacting with the origin repository
          - Will only be used for https based connections
        type: str
      url:
        description:
          - The URL for the origin repository
        type: str

  parent_directory:
    description:
      - The local directory where the repository will be placed
      - If the parent directory does not exist, it will be created
    default: '{temporary_directory}'
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
      token:
        description:
          - The token to use to authenticate to the upstream repository
          - If provided, an 'http.extraheader' will be added to the commands interacting with the upstream repository
          - Will only be used for https based connections
        type: str
      url:
        description:
          - The URL for the upstream repository
          - If provided, the local copy of the repository will be updated, rebased from the upstream
          - The update will happen after the branch is created
          - Conflicts will cause the task to fail and the local copy will be removed
        type: str

notes:
- This plugin always runs on the execution node
- This plugin will not run on a managed node
- To persist changes to the remote repository, use the git_away plugin

author:
- Bradley Thornton (@cidrblock)
"""

EXAMPLES = r"""
- hosts: localhost
  gather_facts: true
  tasks:
    - name: Retrieve a repository from a distant location and make it available locally
      ansible.scm.git_here:
        origin:
          url: git@github.com:cidrblock/scm_testing.git
        upstream:
          url: git@github.com:ansible-network/scm_testing.git
      register: repository

# TASK [Retrieve a repository from a distant location and make it available locally] ***********************************
# changed: [localhost] => {
#     "branch_name": "ansible-localhost-2022-06-05T075705.453080-0700",
#     "branches": [
#         "main",
#     ],
#     "changed": true,
#     "msg": "Successfully retrieved repository: git@github.com:cidrblock/scm_testing.git",
#     "name": "scm_testing",
#     "output": [
#         {
#             "command": "git -C /tmp/tmpvtm6_ejo clone --depth=1 --progress --no-single-branch git@github.com:cidrblock/scm_testing.git",
#             "return_code": 0,
#             "stderr_lines": [
#                 "Cloning into 'scm_testing'...",
#                 "remote: Counting objects: 100% (15/15), done.        ",
#                 "remote: Compressing objects: 100% (13/13), done.        ",
#                 "Receiving objects: 100% (15/15), 15.69 KiB | 15.69 MiB/s, done.",
#                 "Resolving deltas: 100% (8/8), done."
#             ],
#             "stdout_lines": []
#         },
#         {
#             "command": "git -C /tmp/tmpvtm6_ejo/scm_testing branch -a",
#             "return_code": 0,
#             "stderr_lines": [],
#             "stdout_lines": [
#                 "* main",
#                 "  remotes/origin/HEAD -> origin/main",
#                 "  remotes/origin/main"
#             ]
#         },
#         {
#             "command": "git -C /tmp/tmpvtm6_ejo/scm_testing checkout -t -b ansible-localhost-2022-06-05T075705.453080-0700",
#             "return_code": 0,
#             "stderr_lines": [
#                 "Switched to a new branch 'ansible-localhost-2022-06-05T075705.453080-0700'"
#             ],
#             "stdout_lines": [
#                 "branch 'ansible-localhost-2022-06-05T075705.453080-0700' set up to track 'main'."
#             ]
#         },
#         {
#             "command": "git -C /tmp/tmpvtm6_ejo/scm_testing remote add upstream git@github.com:ansible-network/scm_testing.git",
#             "return_code": 0,
#             "stderr_lines": [],
#             "stdout_lines": []
#         },
#         {
#             "command": "git -C /tmp/tmpvtm6_ejo/scm_testing pull upstream main --rebase",
#             "return_code": 0,
#             "stderr_lines": [
#                 "From github.com:ansible-network/scm_testing",
#                 " * branch            main       -> FETCH_HEAD",
#                 " * [new branch]      main       -> upstream/main"
#             ],
#             "stdout_lines": [
#                 "Updating 17212e0..6abefd2",
#                 "Fast-forward",
#                 " README.md | 4 ++++",
#                 " 1 file changed, 4 insertions(+)"
#             ]
#         }
#     ],
#     "path": "/tmp/tmpvtm6_ejo/scm_testing"
# }

"""

RETURN = r"""
# TO-DO: Enter return values here
"""
