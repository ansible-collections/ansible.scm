# Ansible SCM Collection

This repository contains the `ansible.scm` Ansible Collection.

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.12**.

For collections that support Ansible 2.9, please ensure you update your `network_os` to use the
fully qualified collection name (for example, `cisco.ios.ios`).
Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

## External requirements

Some modules and plugins require external libraries. Please check the requirements for each plugin or module you use in the documentation to find out which requirements are needed.

## Included content

<!--start collection content-->
### Modules
Name | Description
--- | ---
[ansible.scm.git_away](https://github.com/ansible-collections/ansible.scm/blob/main/docs/ansible.scm.git_away_module.rst)|Publish changes from a repository available on the execution node to a distant location
[ansible.scm.git_here](https://github.com/ansible-collections/ansible.scm/blob/main/docs/ansible.scm.git_here_module.rst)|Retrieve a repository from a distant location and make it available on the execution node

<!--end collection content-->

## Using this collection

```
    ansible-galaxy collection install ansible.scm
```

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml` using the format:

```yaml
collections:
  - name: ansible.scm
```

To upgrade the collection to the latest available version, run the following command:

```bash
ansible-galaxy collection install ansible.scm --upgrade
```

You can also install a specific version of the collection, for example, if you need to downgrade when something is broken in the latest version (please report an issue in this repository). Use the following syntax where `X.Y.Z` can be any [available version](https://galaxy.ansible.com/ansible/scm):

```bash
ansible-galaxy collection install ansible.scm:==X.Y.Z
```

See [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Licensing

GNU General Public License v3.0 or later.

See [COPYING](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
