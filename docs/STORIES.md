# STORIES.md – Host Migration Guard

## Overview

**Host Migration Guard** is a lightweight, pure‑Python utility that orchestrates a “cut‑over” migration of services between hosting platforms with minimal downtime. The core API is `MigrationGuard.run(source, target)`, which copies services one‑by‑one while keeping the source service alive until the target copy succeeds. The result is a `MigrationReport` summarising successes and failures.

The following backlog is organized into **epics** that reflect the logical phases of the product: **Core Migration Logic**, **Reporting & Analytics**, **Resilience & Recovery**, **Configuration & Extensibility**, and **Developer Experience**. Each story is written in the classic *As a …, I want …, so that …* format and includes acceptance criteria that are concrete, testable, and shippable.

> **MVP Order** – The stories are ordered to deliver a minimal viable product first (core migration + basic reporting), then add resilience, configurability, and developer tooling.

---

## Epics & User Stories

### Epic 1 – Core Migration Logic

| # | Story | Acceptance Criteria |
|---|-------|---------------------|
| **1.1** | **As a DevOps engineer, I want the migration to copy services one at a time, so that I can avoid downtime on the source platform.** | • `MigrationGuard.run` iterates over services in the source dict.<br>• Each service is copied to the target before the next service is processed.<br>• The source service remains available until the target copy succeeds. |
| **1.2** | **As a DevOps engineer, I want the migration to skip services that already exist on the target, so that I avoid unnecessary work.** | • Before copying, the guard checks if the service key exists in the target dict.<br>• If present, the service is marked as *skipped* in the report. |
| **1.3** | **As a DevOps engineer, I want the migration to stop and report an error if a copy fails, so that I can investigate and retry.** | • If a copy operation raises an exception, the guard stops further processing.<br>• The failure is recorded in the report with the exception message. |
| **1.4** | **As a DevOps engineer, I want the migration to be idempotent, so that running it multiple times yields the same final state.** | • Re‑running `run` with the same source/target yields the same report and target state. |

### Epic 2 – Reporting & Analytics

| # | Story | Acceptance Criteria |
|---|-------|---------------------|
| **2.1** | **As a product owner, I want a `MigrationReport` that lists successes, failures, and skips, so that I can quickly assess the migration outcome.** | • `MigrationReport` contains lists: `successes`, `failures`, `skipped`.<br>• Each entry includes the service name and relevant details. |
| **2.2** | **As a product owner, I want the report to include timestamps for each operation, so that I can audit the migration timeline.** | • Each entry in the report records `start_time` and `end_time` (ISO 8601). |
| **2.3** | **As a product owner, I want the report to expose a summary method, so that I can get a quick overview.** | • `MigrationReport.summary()` returns a dict: `{total, successes, failures, skipped}`. |
| **2.4** | **As a product owner, I want the report to be serialisable to JSON, so that it can be logged or sent to downstream systems.** | • `MigrationReport.to_json()` returns a JSON string with all report data. |

### Epic 3 – Resilience & Recovery

| # | Story | Acceptance Criteria |
|---|-------|---------------------|
| **3.1** | **As a DevOps engineer, I want the migration to retry a failed copy up to N times, so that transient errors do not abort the whole process.** | • A configurable `max_retries` parameter (default 3).<br>• On failure, the guard retries until success or retries exhausted.<br>• Each retry is logged. |
| **3.2** | **As a DevOps engineer, I want exponential back‑off between retries, so that I avoid hammering the target.** | • Delay between retries follows `base_delay * 2**attempt` (configurable `base_delay`). |
| **3.3** | **As a DevOps engineer, I want a rollback option, so that I can revert the target to its original state if the migration fails.** | • `MigrationGuard.run` accepts `rollback_on_failure=True`.<br>• On failure, services copied before the failure are removed from the target. |
| **3.4** | **As a DevOps engineer, I want the migration to support a dry‑run mode, so that I can validate the plan without making changes.** | • `dry_run=True` causes the guard to simulate copies, logging actions but not modifying the target. |

### Epic 4 – Configuration & Extensibility

| # | Story | Acceptance Criteria |
|---|-------|---------------------|
| **4.1** | **As a system integrator, I want to plug in custom copy logic per service type, so that I can handle complex payloads.** | • `MigrationGuard` accepts a `copy_strategy` callable per service key.<br>• The strategy receives source payload and returns target payload. |
| **4.2** | **As a system integrator, I want to specify a whitelist of services to migrate, so that I can exclude legacy services.** | • `MigrationGuard.run` accepts an optional `service_filter` predicate.<br>• Only services satisfying the predicate are processed. |
| **4.3** | **As a system integrator, I want to provide a custom logger, so that I can integrate with existing observability stacks.** | • `MigrationGuard` accepts a `logger` instance (must implement `info`, `warning`, `error`). |
| **4.4** | **As a system integrator, I want to export the migration plan before execution, so that I can audit it.** | • `MigrationGuard.plan(source, target)` returns a list of planned actions (service names, copy strategy). |

### Epic 5 – Developer Experience

| # | Story | Acceptance Criteria |
|---|-------|---------------------|
| **5.1** | **As a developer, I want a CLI wrapper, so that I can run migrations from the command line.** | • `host-migration-guard --source=src.json --target=dst.json` executes the migration.<br>• CLI accepts flags for `--dry-run`, `--max-retries`, `--log-level`. |
| **5.2** | **As a developer, I want unit tests covering all core paths, so that I can trust the implementation.** | • Tests cover success, failure, skip, retry, rollback, dry‑run, and custom strategies.<br>• Test coverage ≥ 90%. |
| **5.3** | **As a developer, I want type hints and mypy compliance, so that I can catch errors early.** | • All public APIs are fully annotated.<br>• `mypy` passes with `--strict`. |
| **5.4** | **As a developer, I want documentation in the README, so that new users can get started quickly.** | • README includes usage examples, configuration options, and a troubleshooting section. |

---

## MVP Release Plan

1. **Core Migration Logic** (Stories 1.1–1.4)
2. **Reporting & Analytics** (Stories 2.1–2.4)
3. **Resilience & Recovery – Basic** (Stories 3.1–3.2)
4. **Developer Experience – CLI & Tests** (Stories 5.1–5.3)

> **Post‑MVP Enhancements**: Rollback, dry‑run, custom strategies, whitelist, advanced logging, and full configuration support.

---

## Acceptance Test Skeleton (Python)

```python
import pytest
from host_migration_guard import MigrationGuard, MigrationReport

def test_basic_migration():
    source = {"svcA": {"cfg": 1}, "svcB": {"cfg": 2}}
    target = {}
    report: MigrationReport = MigrationGuard.run(source, target)
    assert set(report.successes) == {"svcA", "svcB"}
    assert target == source
```

*(Full test suite will be added in the repo.)*

---

**End of STORIES.md**
