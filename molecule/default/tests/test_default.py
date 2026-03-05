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


def test_wazuh_agent_path_enabled(host):
    """Test that Wazuh agent path unit is enabled."""
    svc = host.service("wazuh-agent.path")
    assert svc.is_enabled, "Wazuh agent systemd path unit is not enabled."


def test_dropin_dir(host):
    """Test that the wazuh-agent drop-in directory was created as expected."""
    f = host.file("/etc/systemd/system/wazuh-agent.service.d")

    assert f.exists
    assert f.is_directory
    assert f.user == "root"
    assert f.group == "root"
    assert f.mode == 0o755


def test_dropin_file(host):
    """Test that the wazuh-agent drop-in file was created as expected."""
    f = host.file("/etc/systemd/system/wazuh-agent.service.d/wazuh-agent.conf")

    assert f.exists
    assert f.is_file
    assert f.user == "root"
    assert f.group == "root"
    assert f.mode == 0o644
