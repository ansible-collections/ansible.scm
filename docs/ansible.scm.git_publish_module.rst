.. _ansible.scm.git_publish_module:


***********************
ansible.scm.git_publish
***********************

**Publish changes from a repository available on the execution node to a distant location**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Publish changes from a repository available on the execution node to a distant location




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="2">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>commit</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">{}</div>
                </td>
                <td>
                        <div>Details for the the commit</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>message</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"Updates made by ansible with play: {play_name}"</div>
                </td>
                <td>
                        <div>The commit message</div>
                </td>
            </tr>

            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>include</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">["--all"]</div>
                </td>
                <td>
                        <div>A list of files to include (add) in the commit</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>open_browser</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Open the default browser to the pull-request page</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The path to the repository</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>remove</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                        <div>Remove the local copy of the repository if the push is successful</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ssh_key_content</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The content of the SSH private key for authentication with git.</div>
                        <div>Ideal for use with Ansible Vault or other secret management systems.</div>
                        <div>Used only for SSH-based repository URLs.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ssh_key_file</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Path to the SSH private key file to use for authentication with git.</div>
                        <div>Used only for SSH-based repository URLs (e.g., git@github.com:...).</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>tag</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify the tag details associated with the commit.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>annotation</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify annotate</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>message</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify tag message</div>
                </td>
            </tr>

            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>timeout</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">30</div>
                </td>
                <td>
                        <div>The timeout in seconds for each command issued</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>token</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The token to use to authenticate to the origin repository</div>
                        <div>If provided, an &#x27;http.extraheader&#x27; will be added to the commands interacting with the origin repository</div>
                        <div>Will only be used for https based connections</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>user</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">{}</div>
                </td>
                <td>
                        <div>Details for the user to be used for the commit</div>
                        <div>Will only be used if not already configured</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>email</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"ansible@localhost"</div>
                </td>
                <td>
                        <div>The email of the user</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"ansible"</div>
                </td>
                <td>
                        <div>The name of the user</div>
                </td>
            </tr>

    </table>
    <br/>


Notes
-----

.. note::
   - This plugin always runs on the execution node
   - This plugin will not run on a managed node
   - The push will always be to the current branch



Examples
--------

.. code-block:: yaml

    - name: Perform Retrieve Operation
      hosts: localhost
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
            mode: '0644'

        - name: Publish the changes
          ansible.scm.git_publish:
            path: "{{ repository['path'] }}"
    
.. code-block:: yaml
    
    - name: Perform Retrieve Operation via SSH
      hosts: localhost
      gather_facts: true
      vars:
       git_ssh_private_key: |
        -----BEGIN OPENSSH PRIVATE KEY-----
        <enter your key>
        -----END OPENSSH PRIVATE KEY-----
      tasks:
        - name: 0. Explicitly gather facts for localhost
          ansible.builtin.setup:

        - name: "1. Retrieve the repository"
          ansible.scm.git_retrieve:
            origin:
              url: "git@github.com:nickbhasin/backup_ssh.git"
              ssh_key_content: "{{ git_ssh_private_key }}"
          register: ssh_repo_info

        - name: "2. Create a new file in the local repository"
          ansible.builtin.copy:
            content: "This file was published via SSH at {{ ansible_date_time.iso8601 }}."
            dest: "{{ ssh_repo_info.path }}/ssh_update_{{ ansible_date_time.epoch }}.txt"

        - name: "3. Publish the changes using an SSH key"
          ansible.scm.git_publish:
            path: "{{ ssh_repo_info.path }}"
            ssh_key_content: "{{ git_ssh_private_key }}"
            commit:
              message: "Automated update via Ansible (SSH)"
          register: ssh_publish_result

        - name: "4. Display the Pull Request URL"
          ansible.builtin.debug:
            msg: "SSH push complete. Create a Pull Request here - {{ ssh_publish_result.pr_url }}"
          when: ssh_publish_result.pr_url

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




Status
------


Authors
~~~~~~~

- Bradley Thornton (@cidrblock)
