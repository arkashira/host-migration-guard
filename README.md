# Host Migration Guard

A minimal, pure‑Python utility that simulates an automated migration from one
hosting platform to another while aiming for *minimal downtime*.

## How it works

- The source and target platforms are represented as dictionaries that map
  service names to configuration payloads.
- `MigrationGuard.run(source, target)` copies each service from the source to
  the target **one at a time**, keeping the service alive on the source until
  the copy succeeds. This models a “cut‑over” with near‑zero downtime.
- The function returns a `MigrationReport` summarising successes and failures.

## Running the tests
