======================================================
The Ansible SCM (ansible.scm) Collection Release Notes
======================================================

.. contents:: Topics


v2.0.0
======

Release Summary
---------------

Starting from this release, the minimum `ansible-core` version this collection requires is `2.14.0`. That last known version compatible with ansible-core<2.14 is `v1.2.2`.

Major Changes
-------------

- Bumping `requires_ansible` to `>=2.14.0`, since previous ansible-core versions are EoL now.

Minor Changes
-------------

- Fix directory creation to avoid tox failures.

v1.2.2
======

v1.2.1
======

v1.2.0
======

v1.1.1
======

v1.1.0
======

Minor Changes
-------------

- Avoid unnecessary use of a persistent connection (https://github.com/ansible-collections/ansible.scm/pull/215)

v1.0.11
=======

v1.0.10
=======

v1.0.9
======

v1.0.8
======

Bugfixes
--------

- Enable py38 tests (https://github.com/ansible-collections/ansible.scm/pull/175)

v1.0.7
======

Bugfixes
--------

- Allow git_publish when token is not defined (https://github.com/ansible-collections/ansible.scm/pull/163)
- Readme doc update (https://github.com/ansible-collections/ansible.scm/pull/147)

v1.0.6
======

v1.0.5
======

v1.0.3
======

v1.0.2
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
