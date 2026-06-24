import argparse
import dataclasses
import json
import time
from typing import List

@dataclasses.dataclass
class Deployment:
    id: str
    cloud_provider: str
    status: str
    uptime: int

def get_deployments(provider: str = None, status: str = None) -> List[Deployment]:
    # Simulate a database or API call
    deployments = [
        Deployment("1", "AWS", "running", 3600),
        Deployment("2", "GCP", "running", 7200),
        Deployment("3", "AWS", "stopped", 0),
        Deployment("4", "GCP", "running", 3600),
    ]
    if provider:
        deployments = [d for d in deployments if d.cloud_provider == provider]
    if status:
        deployments = [d for d in deployments if d.status == status]
    return deployments

def print_deployments(deployments: List[Deployment]) -> None:
    print("ID\tCloud Provider\tStatus\tUptime")
    for deployment in deployments:
        print(f"{deployment.id}\t{deployment.cloud_provider}\t{deployment.status}\t{deployment.uptime}")

def watch_deployments(provider: str = None, status: str = None) -> None:
    while True:
        deployments = get_deployments(provider, status)
        print_deployments(deployments)
        time.sleep(10)
        print("\033[2J\033[1;1H")  # Clear the screen

def main() -> None:
    parser = argparse.ArgumentParser(description="Host Migration Guard CLI")
    parser.add_argument("--provider", help="Filter by cloud provider")
    parser.add_argument("--status", help="Filter by deployment status")
    parser.add_argument("--watch", action="store_true", help="Watch mode")
    args = parser.parse_args()
    if args.watch:
        try:
            watch_deployments(args.provider, args.status)
        except KeyboardInterrupt:
            pass
    else:
        deployments = get_deployments(args.provider, args.status)
        print_deployments(deployments)

if __name__ == "__main__":
    main()
