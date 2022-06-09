.. _ansible.scm.git_away_module:


********************
ansible.scm.git_away
********************

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
                        <span style="color: purple">-</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"yes"</div>
                </td>
                <td>
                        <div>Remove the local copy of the repository if the push is successful</div>
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

    - hosts: localhost
      gather_facts: true
      tasks:
        - name: Retrieve a repository from a distant location and make it available locally
          ansible.scm.git_here:
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
          ansible.scm.git_away:
            path: "{{ repository['path'] }}"

    # TASK [Publish the changes] ***************************************************************************************************
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
