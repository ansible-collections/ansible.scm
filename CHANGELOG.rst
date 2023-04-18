======================================================
The Ansible SCM (ansible.scm) Collection Release Notes
======================================================

.. contents:: Topics


v1.0.1
======

v1.0.0
======

Major Changes
-------------

- Rename git_away to git_publish (https://github.com/ansible-collections/ansible.scm/pull/75)
- Rename git_here to git_retrieve (https://github.com/ansible-collections/ansible.scm/pull/78)

Bugfixes
--------

- Correct sample playbook (https://github.com/ansible-collections/ansible.scm/pull/89)
- Create user specified parent directory (https://github.com/ansible-collections/ansible.scm/pull/81)

New Modules
-----------

- git_here - Retrieve a repository from a distant location and make it available on the execution node
- git_publish - Publish changes from a repository available on the execution node to a distant location

v0.1.0
======

Bugfixes
--------

- Enable branch protection rules (https://github.com/ansible-collections/ansible.scm/pull/73)
- Fix changelog collection name (https://github.com/ansible-collections/ansible.scm/pull/72)
- Fix string replacement (https://github.com/ansible-collections/ansible.scm/pull/70)
- Fix v replacement (https://github.com/ansible-collections/ansible.scm/pull/71)
- Fix version name in GHA (https://github.com/ansible-collections/ansible.scm/pull/69)
