.. _ansible.scm.git_retrieve_module:


************************
ansible.scm.git_retrieve
************************

**Retrieve a repository from a distant location and make it available on the execution node**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Retrieve a repository from a distant location and make it available on the execution node




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
                    <b>branch</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">{}</div>
                </td>
                <td>
                        <div>Details about the new branch that will be created</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>duplicate_detection</b>
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
                        <div>Reusing an existing branch can introduce unexpected behavior</div>
                        <div>If set to true, the task will fail if the remote branch already exists</div>
                        <div>If set to false and the branch exists the task will use and be updated to the existing branch</div>
                        <div>If set to false and the branch does not exist, the branch will be created</div>
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
                        <b>Default:</b><br/><div style="color: blue">"ansible-{play_name}-{timestamp}"</div>
                </td>
                <td>
                        <div>Once retrieved, create a new branch using this name.</div>
                </td>
            </tr>

            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>host_key_checking</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>accept-new</li>
                                    <li>no</li>
                                    <li><div style="color: blue"><b>system</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Configure strict host key checking for ssh based connections</div>
                        <div>accept-new will accept new host keys (StrictHostKeyChecking=accept-new)</div>
                        <div>no will disable strict host key checking (StrictHostKeyChecking=no)</div>
                        <div>system will use the global system setting and not configure the git repository</div>
                        <div>yes will enable strict host key checking (StrictHostKeyChecking=yes)</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>origin</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Details about the origin</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>tag</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specify the tag</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>url</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The URL for the origin repository</div>
                </td>
            </tr>

            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>parent_directory</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"{temporary_directory}"</div>
                </td>
                <td>
                        <div>The local directory where the repository will be placed</div>
                        <div>If the parent directory does not exist, it will be created</div>
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
                    <b>upstream</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">{}</div>
                </td>
                <td>
                        <div>Details about the upstream</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>branch</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"main"</div>
                </td>
                <td>
                        <div>The branch to use for the upstream</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
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
                        <div>The token to use to authenticate to the upstream repository</div>
                        <div>If provided, an &#x27;http.extraheader&#x27; will be added to the commands interacting with the upstream repository</div>
                        <div>Will only be used for https based connections</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>url</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The URL for the upstream repository</div>
                        <div>If provided, the local copy of the repository will be updated, rebased from the upstream</div>
                        <div>The update will happen after the branch is created</div>
                        <div>Conflicts will cause the task to fail and the local copy will be removed</div>
                </td>
            </tr>

    </table>
    <br/>


Notes
-----

.. note::
   - This plugin always runs on the execution node
   - This plugin will not run on a managed node
   - To persist changes to the remote repository, use the git_publish plugin



Examples
--------

.. code-block:: yaml

    - name: Retrieve Github Repo
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

    # TASK [Retrieve a repository from a distant location and make it available locally] ***********************************
    # changed: [localhost] => {
    #     "branch_name": "ansible-localhost-2022-06-05T075705.453080-0700",
    #     "branches": [
    #         "main",
    #     ],
    #     "changed": true,
    #     "msg": "Successfully retrieved repository: git@github.com:cidrblock/scm_testing.git",
    #     "name": "scm_testing",
    #     "output": [
    #         {
    #             "command": "git -C /tmp/tmpvtm6_ejo clone --depth=1 --progress --no-single-branch git@github.com:cidrblock/scm_testing.git",
    #             "return_code": 0,
    #             "stderr_lines": [
    #                 "Cloning into 'scm_testing'...",
    #                 "remote: Counting objects: 100% (15/15), done.        ",
    #                 "remote: Compressing objects: 100% (13/13), done.        ",
    #                 "Receiving objects: 100% (15/15), 15.69 KiB | 15.69 MiB/s, done.",
    #                 "Resolving deltas: 100% (8/8), done."
    #             ],
    #             "stdout_lines": []
    #         },
    #         {
    #             "command": "git -C /tmp/tmpvtm6_ejo/scm_testing branch -a",
    #             "return_code": 0,
    #             "stderr_lines": [],
    #             "stdout_lines": [
    #                 "* main",
    #                 "  remotes/origin/HEAD -> origin/main",
    #                 "  remotes/origin/main"
    #             ]
    #         },
    #         {
    #             "command": "git -C /tmp/tmpvtm6_ejo/scm_testing checkout -t -b ansible-localhost-2022-06-05T075705.453080-0700",
    #             "return_code": 0,
    #             "stderr_lines": [
    #                 "Switched to a new branch 'ansible-localhost-2022-06-05T075705.453080-0700'"
    #             ],
    #             "stdout_lines": [
    #                 "branch 'ansible-localhost-2022-06-05T075705.453080-0700' set up to track 'main'."
    #             ]
    #         },
    #         {
    #             "command": "git -C /tmp/tmpvtm6_ejo/scm_testing remote add upstream git@github.com:ansible-network/scm_testing.git",
    #             "return_code": 0,
    #             "stderr_lines": [],
    #             "stdout_lines": []
    #         },
    #         {
    #             "command": "git -C /tmp/tmpvtm6_ejo/scm_testing pull upstream main --rebase",
    #             "return_code": 0,
    #             "stderr_lines": [
    #                 "From github.com:ansible-network/scm_testing",
    #                 " * branch            main       -> FETCH_HEAD",
    #                 " * [new branch]      main       -> upstream/main"
    #             ],
    #             "stdout_lines": [
    #                 "Updating 17212e0..6abefd2",
    #                 "Fast-forward",
    #                 " README.md | 4 ++++",
    #                 " 1 file changed, 4 insertions(+)"
    #             ]
    #         }
    #     ],
    #     "path": "/tmp/tmpvtm6_ejo/scm_testing"
    # }




Status
------


Authors
~~~~~~~

- Bradley Thornton (@cidrblock)
