"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os
import re

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


@pytest.mark.parametrize(
    "prop,regex",
    [
        ("After", r"^After=.*cloud-final\.service"),
        ("Wants", r"^Wants=.*cloud-final\.service"),
    ],
)
def test_unit_properties(host, prop, regex):
    """Test that unit properties were modified via drop-in as expected."""
    cmd = f"systemctl show --no-pager --property={prop} wazuh-agent.service"
    cmd_result = host.run(cmd)
    assert cmd_result.rc == 0, f"{cmd} command failed"
    assert (
        re.search(regex, cmd_result.stdout) is not None
    ), f"Regex {regex} does not match any line in {cmd} output."


@pytest.mark.parametrize(
    "unit,dependent_unit",
    [
        ("multi-user.target", "wazuh-agent.service"),
    ],
)
def test_dependency(host, unit, dependent_unit):
    """Test that dependent_unit is a dependency of unit."""
    cmd = f"systemctl list-dependencies {unit}"
    cmd_result = host.run(cmd)
    assert cmd_result.rc == 0, f"{cmd} command failed"
    assert (
        dependent_unit in cmd_result.stdout
    ), f"{dependent_unit} not listed as a dependency of {unit}."
