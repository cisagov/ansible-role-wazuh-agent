# ansible-role-wazuh-agent #

[![GitHub Build Status](https://github.com/cisagov/ansible-role-wazuh-agent/workflows/build/badge.svg)](https://github.com/cisagov/ansible-role-wazuh-agent/actions)
[![License](https://img.shields.io/github/license/cisagov/ansible-role-wazuh-agent)](https://spdx.org/licenses/)
[![CodeQL](https://github.com/cisagov/ansible-role-wazuh-agent/workflows/CodeQL/badge.svg)](https://github.com/cisagov/ansible-role-wazuh-agent/actions/workflows/codeql-analysis.yml)

This is an Ansible role for installing the [Wazuh
agent](https://documentation.wazuh.com/current/installation-guide/wazuh-agent/index.html).

> [!NOTE]
> We do not enable or start the service in this Ansible role.  This is
> done by a user-data script run by cloud-init after it has injected
> the Wazuh agent name into the Wazuh configuration file.

## Requirements ##

None.

## Role Variables ##

| Variable | Description | Default | Required |
| -------- | ----------- | ------- | -------- |
| wazuh_agent_manager | The hostname or IP address of the Wazuh manager to which the agent should connect. | n/a | Yes |

## Dependencies ##

None.

## Installation ##

This role can be installed via the command:

```console
ansible-galaxy install --role-file path/to/requirements.yml
```

where `requirements.yml` looks like:

```yaml
---
- name: wazuh_agent
  src: https://github.com/cisagov/ansible-role-wazuh-agent
```

and may contain other roles as well.

For more information about installing Ansible roles via a YAML file,
please see [the `ansible-galaxy`
documentation](https://docs.ansible.com/ansible/latest/galaxy/user_guide.html#installing-multiple-roles-from-a-file).

## Example Playbook ##

Here's how to use it in a playbook:

```yaml
- hosts: all
  become: true
  become_method: sudo
  tasks:
    - name: Include Wazuh agent
      ansible.builtin.include_role:
        name: wazuh_agent
      vars:
        wazuh_agent_manager: example.com
```

## Contributing ##

We welcome contributions!  Please see [`CONTRIBUTING.md`](CONTRIBUTING.md) for
details.

## License ##

This project is in the worldwide [public domain](LICENSE).

This project is in the public domain within the United States, and
copyright and related rights in the work worldwide are waived through
the [CC0 1.0 Universal public domain
dedication](https://creativecommons.org/publicdomain/zero/1.0/).

All contributions to this project will be released under the CC0
dedication. By submitting a pull request, you are agreeing to comply
with this waiver of copyright interest.

## Author Information ##

Shane Frasier - <jeremy.frasier@gwe.cisa.dhs.gov>
