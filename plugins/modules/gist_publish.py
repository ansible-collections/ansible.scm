# Copyright 2026 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

DOCUMENTATION = """
module: gist_publish
short_description: Publish content to a GitHub gist or GitLab snippet
version_added: "3.3.0"
description:
    - Create or update a GitHub gist or GitLab snippet from task content
    - Delete a gist or snippet when O(state=absent)
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
      - Existing gist or snippet id to update or delete
      - Required when O(state=absent)
    type: str
  description:
    description:
      - Description for the gist or snippet
    default: ""
    type: str
  title:
    description:
      - Title for GitLab snippets
      - Ignored for GitHub gists
    default: ""
    type: str
  public:
    description:
      - Whether the GitHub gist is public
      - Ignored for GitLab snippets
    default: false
    type: bool
  visibility:
    description:
      - Visibility for GitLab snippets
      - Ignored for GitHub gists
    choices:
      - private
      - internal
      - public
    default: private
    type: str
  project_id:
    description:
      - GitLab project id or URL-encoded path for project snippets
      - If omitted, a personal GitLab snippet is used
    type: str
  files:
    description:
      - Files to publish, keyed by filename
      - Required when O(state=present)
    type: dict
    default: {}
  state:
    description:
      - Whether the gist or snippet should be present or absent
    choices:
      - present
      - absent
    default: present
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
- name: Publish a report to a private GitHub gist
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Create gist
      ansible.scm.gist_publish:
        provider: github
        description: Meraki report
        public: false
        files:
          report.json:
            content: "{{ report | to_nice_json }}"
      register: gist

    - name: Show gist URL
      ansible.builtin.debug:
        msg: "{{ gist.html_url }}"
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
  description: Published file contents keyed by filename
  returned: on success
  type: dict
changed:
  description: Whether the remote gist or snippet changed
  returned: always
  type: bool
"""
