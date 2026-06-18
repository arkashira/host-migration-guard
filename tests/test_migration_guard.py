import pytest
from migration_guard import MigrationGuard, MigrationReport, MigrationResult


def test_happy_path_single_service():
    source = {"web": {"port": 80, "ssl": True}}
    target = {}
    guard = MigrationGuard()
    report: MigrationReport = guard.run(source, target)

    assert isinstance(report, MigrationReport)
    assert report.total == 1
    assert report.succeeded == 1
    assert report.failed == 0
    assert report  # truthy because no failures
    assert target == source
    assert report.details[0] == MigrationResult(service="web", success=True, error=None)


def test_multiple_services_batch_size_two():
    source = {
        "api": {"port": 8080},
        "db": {"engine": "postgres"},
        "cache": {"type": "redis"},
    }
    target = {}
    guard = MigrationGuard(batch_size=2)
    report = guard.run(source, target)

    assert report.total == 3
    assert report.succeeded == 3
    assert report.failed == 0
    # Ensure all services are present in target
    assert set(target.keys()) == set(source.keys())
    # Verify ordering of details respects batch processing
    assert [r.service for r in report.details] == ["api", "db", "cache"]


def test_failure_on_unserialisable_config():
    class BadObj:
        def __str__(self):
            raise TypeError("cannot stringify")

    source = {"good": {"x": 1}, "bad": BadObj()}
    target = {}
    guard = MigrationGuard()
    report = guard.run(source, target)

    assert report.total == 2
    assert report.succeeded == 1
    assert report.failed == 1
    # The good service should be migrated
    assert "good" in target and target["good"] == {"x": 1}
    # The bad service must not be in target
    assert "bad" not in target
    # Check that the failure record contains the expected error message
    bad_result = next(r for r in report.details if r.service == "bad")
    assert not bad_result.success
    assert "cannot stringify" in bad_result.error


def test_invalid_input_types():
    guard = MigrationGuard()
    with pytest.raises(TypeError):
        guard.run([], {})  # source not a dict
    with pytest.raises(TypeError):
        guard.run({}, [])  # target not a dict


def test_invalid_batch_size():
    with pytest.raises(ValueError):
        MigrationGuard(batch_size=0)
