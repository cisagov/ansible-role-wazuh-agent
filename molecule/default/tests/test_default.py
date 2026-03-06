"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize("pkg", ["wazuh-agent", "xmlstarlet"])
def test_packages_installed(host, pkg):
    """Test that expected packages were installed."""
    assert host.package(pkg).is_installed, f"System package {pkg} is not installed."


def test_wazuh_agent_not_enabled_or_started(host):
    """Test that Wazuh agent is not enabled or started."""
    svc = host.service("wazuh-agent")
    assert svc.exists, "Wazuh agent does not exist."
    assert not svc.is_enabled, "Wazuh agent is enabled."
    assert not svc.is_running, "Wazuh agent is started."
