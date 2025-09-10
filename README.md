# Ansible SCM (Source Code Management) Collection

This repository contains the `ansible.scm` Ansible Collection that allows you to manage Git repositories via Ansible.

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against the following Ansible versions: **>=2.15.0**.

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
[ansible.scm.git_publish](https://github.com/ansible-collections/ansible.scm/blob/main/docs/ansible.scm.git_publish_module.rst)|Publish changes from a repository available on the execution node to a distant location
[ansible.scm.git_retrieve](https://github.com/ansible-collections/ansible.scm/blob/main/docs/ansible.scm.git_retrieve_module.rst)|Retrieve a repository from a distant location and make it available on the execution node

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

## Support

As a Red Hat Ansible [Certified Content](https://catalog.redhat.com/software/search?target_platforms=Red%20Hat%20Ansible%20Automation%20Platform), this collection is entitled to [support](https://access.redhat.com/support/) through [Ansible Automation Platform](https://www.redhat.com/en/technologies/management/ansible) (AAP).

If a support case cannot be opened with Red Hat and the collection has been obtained either from [Galaxy](https://galaxy.ansible.com/ui/) or [GitHub](https://github.com/ansible-collections/ansible.scm), there is community support available at no charge.

You can join us on [#network:ansible.com](https://matrix.to/#/#network:ansible.com) room or the [Ansible Forum Network Working Group](https://forum.ansible.com/g/network-wg).

## Licensing

GNU General Public License v3.0 or later.

See [COPYING](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
