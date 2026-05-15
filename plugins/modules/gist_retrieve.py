# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

DOCUMENTATION = """
module: gist_retrieve
short_description: Retrieve a GitHub gist or GitLab snippet
version_added: "3.3.0"
description:
    - Retrieve file content from a GitHub gist or GitLab snippet
options:
  provider:
    description:
      - The hosting provider for the gist or snippet
    choices:
      - github
      - gitlab
    default: github
    type: str
  token:
    description:
      - API token used to authenticate to the provider
      - If omitted, the module uses C(GITHUB_TOKEN) or C(GITLAB_TOKEN) from the environment
    type: str
  api_url:
    description:
      - Base API URL for the provider
      - Defaults to C(https://api.github.com) for GitHub
      - Defaults to C(https://gitlab.com/api/v4) for GitLab
    type: str
  gist_id:
    description:
      - Gist or snippet id to retrieve
    required: true
    type: str
  project_id:
    description:
      - GitLab project id or URL-encoded path for project snippets
    type: str
  timeout:
    description:
      - Timeout in seconds for each API request
    default: 30
    type: int
  validate_certs:
    description:
      - Whether TLS certificates should be validated
    default: true
    type: bool
notes:
    - This plugin always runs on the execution node
    - This plugin will not run on a managed node
author:
    - Ansible Network Community (ansible-network)
"""

EXAMPLES = r"""
- name: Retrieve a gist
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Get gist content
      ansible.scm.gist_retrieve:
        provider: github
        gist_id: abc123def456
      register: gist

    - name: Show files
      ansible.builtin.debug:
        var: gist.files
"""

RETURN = r"""
id:
  description: Gist or snippet id
  returned: on success
  type: str
html_url:
  description: Web URL for the gist or snippet
  returned: on success
  type: str
description:
  description: Gist or snippet description
  returned: on success
  type: str
files:
  description: Retrieved file contents keyed by filename
  returned: on success
  type: dict
changed:
  description: Always false for retrieve operations
  returned: always
  type: bool
"""
