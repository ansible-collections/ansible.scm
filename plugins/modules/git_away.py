<<<<<<< HEAD
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
module: git_away
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
    type: list
  path:
    description:
      - The path to the repository
    required: true
  remove:
    description:
      - Remove the local copy of the repository if the push is successful
    default: true

notes:
- This plugin always runs on the execution node
- This plugin will not run on a managed node
- The push will always be to the current branch

author:
- Bradley Thornton (@cidrblock)
"""

EXAMPLES = r"""
# TO-DO: Enter examples here
"""

RETURN = r"""
# TO-DO: Enter return values here
"""
||||||| parent of 4352627 (Move sample playbook)
=======
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
module: git_away
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
    type: list
  path:
    description:
      - The path to the repository
    required: true
  remove:
    description:
      - Remove the local copy of the repository if the push is successful
    default: true

notes:
- This plugin always runs on the execution node
- This plugin will not run on a managed node
- The push will always be to the current branch

author:
- Bradley Thornton (@cidrblock)
"""

EXAMPLES = r"""
# TO-DO: Enter examples here
"""

RETURN = r"""
# TO-DO: Enter return values here
"""
>>>>>>> 4352627 (Move sample playbook)
