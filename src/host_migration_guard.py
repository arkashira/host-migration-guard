import json
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class DeploymentStatus:
    cpu_usage: float
    memory_usage: float
    network_usage: float
    health_indicators: Dict[str, bool]

class HostMigrationGuard:
    def __init__(self):
        self.deployments = {}

    def add_deployment(self, deployment_id: str, status: DeploymentStatus):
        self.deployments[deployment_id] = status

    def get_deployment_status(self, deployment_id: str) -> DeploymentStatus:
        return self.deployments.get(deployment_id)

    def get_dashboard_data(self) -> List[Dict]:
        dashboard_data = []
        for deployment_id, status in self.deployments.items():
            dashboard_data.append({
                "deployment_id": deployment_id,
                "cpu_usage": status.cpu_usage,
                "memory_usage": status.memory_usage,
                "network_usage": status.network_usage,
                "health_indicators": status.health_indicators
            })
        return dashboard_data

    def alert(self, deployment_id: str, message: str):
        print(f"Alert: {deployment_id} - {message}")

    def collect_metrics(self, deployment_id: str) -> Dict:
        status = self.get_deployment_status(deployment_id)
        if status:
            return {
                "cpu_usage": status.cpu_usage,
                "memory_usage": status.memory_usage,
                "network_usage": status.network_usage
            }
        else:
            return {}
