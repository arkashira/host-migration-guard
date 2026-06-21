# Technical Specification – Host Migration Guard

## 1. Overview

**Host Migration Guard** is a lightweight, pure‑Python library that orchestrates a *cut‑over* migration of services from one hosting platform to another with the goal of *minimal downtime*.  
The core idea is to copy each service configuration sequentially, leaving the source service running until the target copy succeeds, then optionally tearing down the source. The library is intentionally minimal to be easily embedded in CI/CD pipelines, infrastructure‑as‑code workflows, or as a standalone CLI tool.

---

## 2. Architecture

```
┌───────────────────────┐
│  MigrationGuard API   │
│  (public entry point) │
└─────────────┬─────────┘
              │
              ▼
┌───────────────────────┐
│  MigrationEngine      │
│  (core orchestration) │
└───────┬───────┬───────┘
        │       │       │
        ▼       ▼       ▼
┌───────┐ ┌───────┐ ┌───────┐
│ Copier│ │ Checker│ │ Reporter│
└───────┘ └───────┘ └───────┘
```

* **MigrationGuard** – Public façade exposing `run(source, target, options)` and `MigrationReport`.
* **MigrationEngine** – Handles sequencing, error handling, and state transitions.
* **Copier** – Performs the actual copy operation for a single service.
* **Checker** – Validates the target service after copy (optional health‑check).
* **Reporter** – Aggregates results into `MigrationReport`.

The library is *stateless* between runs; all state is kept in memory during a single `run` invocation.

---

## 3. Components

| Component | Responsibility | Key Methods |
|-----------|----------------|-------------|
| `MigrationGuard` | Public API | `run(source: Dict, target: Dict, options: MigrationOptions) -> MigrationReport` |
| `MigrationEngine` | Orchestrates copy sequence, retries, and rollback | `_process_services()`, `_handle_failure()` |
| `Copier` | Copies a single service configuration | `copy(service_name: str, src_cfg: dict, tgt_cfg: dict) -> bool` |
| `Checker` | Optional health‑check on target service | `check(service_name: str, cfg: dict) -> bool` |
| `Reporter` | Builds `MigrationReport` | `add_success()`, `add_failure()`, `to_dict()` |
| `MigrationOptions` | Configuration for the run | `retry_limit`, `check_after_copy`, `dry_run` |

---

## 4. Data Model

```python
# Service configuration
ServiceConfig = Dict[str, Any]

# Platform representation
Platform = Dict[str, ServiceConfig]

# Migration report entry
class MigrationResult:
    service: str
    status: Literal["success", "failure"]
    error: Optional[str] = None

# Full report
class MigrationReport:
    results: List[MigrationResult]
    summary: Dict[str, int]  # e.g., {"success": 5, "failure": 2}
```

*All data structures are JSON‑serialisable, enabling easy logging or API exposure.*

---

## 5. Key APIs / Interfaces

```python
# migration_guard.py

class MigrationOptions:
    retry_limit: int = 3
    check_after_copy: bool = True
    dry_run: bool = False

class MigrationGuard:
    @staticmethod
    def run(source: Platform, target: Platform, options: MigrationOptions = MigrationOptions()) -> MigrationReport:
        """
        Orchestrates the migration from `source` to `target`.
        Returns a MigrationReport summarising each service.
        """
```

**Copier API**

```python
class Copier:
    @staticmethod
    def copy(service_name: str, src_cfg: ServiceConfig, tgt_cfg: ServiceConfig, dry_run: bool) -> bool:
        """
        Simulates copying by merging src_cfg into tgt_cfg.
        Returns True on success, False on simulated failure.
        """
```

**Checker API**

```python
class Checker:
    @staticmethod
    def check(service_name: str, cfg: ServiceConfig) -> bool:
        """
        Performs a lightweight health check (e.g., schema validation).
        """
```

---

## 6. Technology Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Language | Python 3.11+ | Pure‑Python, no external runtime |
| Data handling | `typing`, `dataclasses` | Strong typing, easy serialization |
| Logging | `logging` | Configurable verbosity, stdout/stderr |
| Testing | `pytest`, `hypothesis` | Property‑based tests for copy logic |
| Packaging | `poetry` | Dependency management, virtual env |
| CI | GitHub Actions | Automated linting, tests, and release |

No external services or binaries are required; the library can run in any environment that supports Python.

---

## 7. Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| `typing-extensions` | ≥4.10 | Backport of `typing` features for older Python |
| `pydantic` | ≥2.0 | Optional: schema validation for `ServiceConfig` |
| `pytest` | ≥8.0 | Unit tests |
| `hypothesis` | ≥6.0 | Property‑based testing |
| `black` | ≥24.0 | Code formatting |
| `mypy` | ≥1.10 | Static type checking |

All dependencies are optional for runtime; only `typing-extensions` is required for type hints on older Python versions.

---

## 8. Deployment & Usage

### 8.1 Installation

```bash
pip install host-migration-guard
```

### 8.2 CLI (optional)

A minimal CLI is provided via `scripts/cli.py`:

```bash
host-migration-guard --source source.yaml --target target.yaml --dry-run
```

The CLI parses YAML/JSON files into the `Platform` structure and invokes `MigrationGuard.run`.

### 8.3 Integration Example

```python
from host_migration_guard import MigrationGuard, MigrationOptions

source = {
    "webapp": {"url": "https://old.example.com", "port": 80},
    "db": {"engine": "postgres", "version": "12"},
}

target = {
    "webapp": {},
    "db": {},
}

options = MigrationOptions(retry_limit=2, check_after_copy=True, dry_run=False)

report = MigrationGuard.run(source, target, options)
print(report.to_dict())
```

### 8.4 CI/CD Pipeline

Add a step in your pipeline:

```yaml
- name: Run Host Migration Guard
  run: |
    pip install host-migration-guard
    python -c "
    from host_migration_guard import MigrationGuard, MigrationOptions
    import yaml, sys
    source = yaml.safe_load(open('source.yaml'))
    target = yaml.safe_load(open('target.yaml'))
    report = MigrationGuard.run(source, target, MigrationOptions(dry_run=False))
    print(report.to_dict())
    "
```

---

## 9. Error Handling & Retries

* Each service copy is retried up to `retry_limit` times.
* On failure after all retries, the service is marked as `"failure"` and the engine proceeds to the next service.
* In `dry_run` mode, no actual mutation of `target` occurs; the function still simulates copy and health checks.

---

## 10. Extensibility

* **Custom Copier** – Users can subclass `Copier` to implement real API calls (e.g., AWS SDK, Terraform).
* **Custom Checker** – Replace `Checker` with a health‑check that pings the target service.
* **Event Hooks** – `MigrationEngine` exposes `on_success` and `on_failure` callbacks for logging or metrics.

---

## 11. Security & Compliance

* No credentials are stored; all secrets must be supplied externally (e.g., environment variables) if a custom copier is used.
* The library itself performs no network I/O; any network operations are delegated to user‑supplied copiers/checkers.

---

## 12. Testing Strategy

* **Unit Tests** – Verify copy logic, retry mechanism, and report aggregation.
* **Property Tests** – Use Hypothesis to generate random service configurations and ensure idempotence.
* **Integration Tests** – Simulate a full migration with mock copiers that randomly fail to test retry logic.

---

## 13. Release Notes

| Version | Release Date | Highlights |
|---------|--------------|------------|
| 0.1.0 | 2026‑06‑21 | Initial release, core migration engine |
| 0.2.0 | TBD | Optional `pydantic` validation, CLI support |
| 1.0.0 | TBD | Stable API, deprecation of legacy functions |

--- 

**End of Technical Specification**
