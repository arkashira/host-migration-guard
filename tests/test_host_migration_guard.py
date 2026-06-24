import pytest
import time
from host_migration_guard import get_deployments, print_deployments, watch_deployments

def test_get_deployments() -> None:
    deployments = get_deployments()
    assert len(deployments) == 4

def test_get_deployments_filtered_by_provider() -> None:
    deployments = get_deployments(provider="AWS")
    assert len(deployments) == 2

def test_get_deployments_filtered_by_status() -> None:
    deployments = get_deployments(status="running")
    assert len(deployments) == 3

def test_get_deployments_filtered_by_provider_and_status() -> None:
    deployments = get_deployments(provider="AWS", status="running")
    assert len(deployments) == 1

def test_print_deployments(capsys) -> None:
    deployments = get_deployments()
    print_deployments(deployments)
    captured = capsys.readouterr()
    assert "ID\tCloud Provider\tStatus\tUptime" in captured.out

def test_watch_deployments(capsys, monkeypatch) -> None:
    # This test will not actually test the watch functionality, but rather that it doesn't crash
    def mock_sleep(_):
        raise KeyboardInterrupt
    monkeypatch.setattr(time, 'sleep', mock_sleep)
    try:
        watch_deployments()
    except KeyboardInterrupt:
        pass
    assert True
