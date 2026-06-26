from host_migration_guard import HostMigrationGuard, DeploymentStatus

def test_add_deployment():
    guard = HostMigrationGuard()
    deployment_id = "test_deployment"
    status = DeploymentStatus(cpu_usage=0.5, memory_usage=0.2, network_usage=0.1, health_indicators={"healthy": True})
    guard.add_deployment(deployment_id, status)
    assert guard.get_deployment_status(deployment_id) == status

def test_get_deployment_status():
    guard = HostMigrationGuard()
    deployment_id = "test_deployment"
    status = DeploymentStatus(cpu_usage=0.5, memory_usage=0.2, network_usage=0.1, health_indicators={"healthy": True})
    guard.add_deployment(deployment_id, status)
    assert guard.get_deployment_status(deployment_id) == status

def test_get_dashboard_data():
    guard = HostMigrationGuard()
    deployment_id1 = "test_deployment1"
    deployment_id2 = "test_deployment2"
    status1 = DeploymentStatus(cpu_usage=0.5, memory_usage=0.2, network_usage=0.1, health_indicators={"healthy": True})
    status2 = DeploymentStatus(cpu_usage=0.6, memory_usage=0.3, network_usage=0.2, health_indicators={"healthy": False})
    guard.add_deployment(deployment_id1, status1)
    guard.add_deployment(deployment_id2, status2)
    dashboard_data = guard.get_dashboard_data()
    assert len(dashboard_data) == 2
    assert dashboard_data[0]["deployment_id"] == deployment_id1
    assert dashboard_data[1]["deployment_id"] == deployment_id2

def test_alert():
    guard = HostMigrationGuard()
    deployment_id = "test_deployment"
    message = "Test alert message"
    guard.alert(deployment_id, message)
    # No assertion, just checking that the alert method runs without errors

def test_collect_metrics():
    guard = HostMigrationGuard()
    deployment_id = "test_deployment"
    status = DeploymentStatus(cpu_usage=0.5, memory_usage=0.2, network_usage=0.1, health_indicators={"healthy": True})
    guard.add_deployment(deployment_id, status)
    metrics = guard.collect_metrics(deployment_id)
    assert metrics == {"cpu_usage": 0.5, "memory_usage": 0.2, "network_usage": 0.1}

def test_collect_metrics_non_existent_deployment():
    guard = HostMigrationGuard()
    deployment_id = "non_existent_deployment"
    metrics = guard.collect_metrics(deployment_id)
    assert metrics == {}
