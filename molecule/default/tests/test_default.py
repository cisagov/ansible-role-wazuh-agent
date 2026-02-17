"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_wazuh_agent_installed(host):
    """Test that Wazuh agent was installed."""
    assert host.package("wazuh-agent").is_installed, "Wazuh agent is not installed."


def test_wazuh_agent_enabled(host):
    """Test that Wazuh agent is enabled."""
    svc = host.service("wazuh-agent")
    assert svc.is_enabled, "Wazuh agent is not enabled."
