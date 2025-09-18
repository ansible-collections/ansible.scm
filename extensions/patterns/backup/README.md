# Ansible SCM (Source Code Management) Collection

This repository contains the `ansible.scm` Ansible Collection that allows you to manage Git repositories via Ansible.

<!--start requires_ansible-->

## Ansible version compatibility

This collection has been tested against the following Ansible versions: **>=2.15.0**.

Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

## Included content

<!--start collection content-->
### Modules
Name | Description
--- | ---
[ansible.scm.git_publish](https://github.com/ansible-collections/ansible.scm/blob/main/docs/ansible.scm.git_publish_module.rst)|Publish changes from a repository available on the execution node to a distant location
[ansible.scm.git_retrieve](https://github.com/ansible-collections/ansible.scm/blob/main/docs/ansible.scm.git_retrieve_module.rst)|Retrieve a repository from a distant location and make it available on the execution node
<!--end collection content-->
