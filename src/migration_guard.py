from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Tuple


@dataclass
class MigrationResult:
    """Result of migrating a single service."""
    service: str
    success: bool
    error: str | None = None


@dataclass
class MigrationReport:
    """Overall migration report."""
    total: int
    succeeded: int
    failed: int
    details: List[MigrationResult] = field(default_factory=list)

    def __bool__(self) -> bool:
        """Truthiness reflects whether all services migrated successfully."""
        return self.failed == 0


class MigrationGuard:
    """
    Simulates an automated migration between two hosting platforms.

    The platforms are simple ``Dict[str, Any]`` mappings where the key is a
    service identifier and the value is an opaque configuration object.
    """

    def __init__(self, *, batch_size: int = 1):
        """
        :param batch_size: Number of services to migrate in a single batch.
                           A batch size of 1 models minimal‑downtime cut‑over.
        """
        if batch_size < 1:
            raise ValueError("batch_size must be >= 1")
        self.batch_size = batch_size

    def _migrate_batch(
        self,
        batch: List[Tuple[str, Any]],
        target: Dict[str, Any],
    ) -> List[MigrationResult]:
        """Attempt to copy a batch of services to the target platform."""
        results: List[MigrationResult] = []
        for service, config in batch:
            try:
                # Simulate a possible failure if config is not serialisable.
                # For the demo we treat any value that raises TypeError on
                # ``str()`` as a failure.
                _ = str(config)
                target[service] = config
                results.append(MigrationResult(service, True))
            except Exception as exc:
                results.append(MigrationResult(service, False, str(exc)))
        return results

    def run(self, source: Dict[str, Any], target: Dict[str, Any]) -> MigrationReport:
        """
        Perform the migration.

        :param source: The current hosting platform.
        :param target: The destination platform (will be mutated).
        :return: MigrationReport summarising the operation.
        """
        if not isinstance(source, dict) or not isinstance(target, dict):
            raise TypeError("source and target must be dictionaries")

        services = list(source.items())
        total = len(services)
        succeeded = 0
        failed = 0
        details: List[MigrationResult] = []

        # Process in batches to respect the configured batch size.
        for i in range(0, total, self.batch_size):
            batch = services[i : i + self.batch_size]
            batch_results = self._migrate_batch(batch, target)
            for res in batch_results:
                if res.success:
                    succeeded += 1
                else:
                    failed += 1
                details.append(res)

        return MigrationReport(total, succeeded, failed, details)
