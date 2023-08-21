# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

DOCUMENTATION = """
module: git_publish
short_description: >-
  Publish changes from a repository available on the execution node to a distant location
version_added: "1.0.0"
description:
    - Publish changes from a repository available on the execution node to a distant location
options:
  commit:
    description:
      - Details for the the commit
    default: {}
    type: dict
    suboptions:
      message:
        description:
          - The commit message
        default: 'Updates made by ansible with play: {play_name}'
        type: str
  include:
    description:
      - A list of files to include (add) in the commit
    default: ['--all']
    elements: str
    type: list
  open_browser:
    description:
      - Open the default browser to the pull-request page
    default: false
    type: bool
  path:
    description:
      - The path to the repository
    required: true
  remove:
    description:
      - Remove the local copy of the repository if the push is successful
    default: true
    type: bool
  timeout:
    description:
      - The timeout in seconds for each command issued
    default: 30
    type: int
  token:
    description:
      - The token to use to authenticate to the origin repository
      - >
        If provided, an 'http.extraheader' will be added to the commands
        interacting with the origin repository
      - Will only be used for https based connections
    type: str
  tag:
    description:
      - Specify the tag details associated with the commit.
    type: dict
    suboptions:
      annotation:
        description: Specify annotate
        type: str
      message:
        description: Specify tag message
        type: str
  user:
    description:
      - Details for the user to be used for the commit
      - Will only be used if not already configured
    default: {}
    type: dict
    suboptions:
      name:
        description: The name of the user
        default: 'ansible'
        type: str
      email:
        description: The email of the user
        default: 'ansible@localhost'
        type: str



notes:
- This plugin always runs on the execution node
- This plugin will not run on a managed node
- The push will always be to the current branch

author:
- Bradley Thornton (@cidrblock)
"""

EXAMPLES = r"""
- hosts: localhost
  gather_facts: true
  tasks:
    - name: Retrieve a repository from a distant location and make it available locally
      ansible.scm.git_retrieve:
        origin:
          url: git@github.com:cidrblock/scm_testing.git
        upstream:
          url: git@github.com:ansible-network/scm_testing.git
      register: repository

    - name: Add to the repository
      ansible.builtin.copy:
        content: "{{ repository | to_nice_yaml }}"
        dest: "{{ repository['path'] }}/details.yaml"

    - name: Publish the changes
      ansible.scm.git_publish:
        path: "{{ repository['path'] }}"

# TASK [Publish the changes] **********************************************************************
# changed: [localhost] => {
#     "changed": true,
#     "msg": "Successfully published local changes from: /tmp/tmpvtm6_ejo/scm_testing",
#     "output": [
#         {
#             "command": "git -C /tmp/tmpvtm6_ejo/scm_testing add --all",
#             "return_code": 0,
#             "stderr_lines": [],
#             "stdout_lines": []
#         },
#         {
#             "command": "git -C /tmp/tmpvtm6_ejo/scm_testing commit --allow-empty -m 'Updates made by ansible with play: localhost'",
#             "return_code": 0,
#             "stderr_lines": [],
#             "stdout_lines": [
#                 "[ansible-localhost-2022-06-05T075705.453080-0700 604eef6] Updates made by ansible with play: localhost",
#                 " 1 file changed, 109 insertions(+)",
#                 " create mode 100644 details.yaml"
#             ]
#         },
#         {
#             "command": "git -C /tmp/tmpvtm6_ejo/scm_testing push origin",
#             "return_code": 0,
#             "stderr_lines": [
#                 "remote: ",
#                 "remote: Create a pull request for 'ansible-localhost-2022-06-05T075705.453080-0700' on GitHub by visiting:        ",
#                 "remote:      https://github.com/cidrblock/scm_testing/pull/new/ansible-localhost-2022-06-05T075705.453080-0700        ",
#                 "remote: ",
#                 "To github.com:cidrblock/scm_testing.git",
#                 " * [new branch]      ansible-localhost-2022-06-05T075705.453080-0700 -> ansible-localhost-2022-06-05T075705.453080-0700"
#             ],
#             "stdout_lines": []
#         }
#     ]
# }
"""

RETURN = r"""
# TO-DO: Enter return values here
"""
