---
layout: docu
redirect_from:
- /docs/current/dev/overview
- /docs/lts/dev/overview
- /docs/preview/dev/overview
title: Overview
---

The pages in this section are intended for developers who contribute to DuckDB or build extensions for it. If you would like to contribute, please also read the [contributing guidelines](https://github.com/duckdb/duckdb/blob/main/CONTRIBUTING.md).

## Project Structure and Processes

* [DuckDB Repositories]({% link docs/2.0/dev/repositories.md %}) lists the repositories that host DuckDB's components, such as clients and extensions.
* [Release Cycle]({% link docs/2.0/dev/release_cycle.md %}) describes the release process of DuckDB and its core extensions.

## Building DuckDB

* [Building DuckDB from Source]({% link docs/2.0/dev/building/overview.md %}) explains how to compile DuckDB on different platforms and how to build extensions.
* [Build Configuration]({% link docs/2.0/dev/building/build_configuration.md %}) lists the build types and options.
* [Troubleshooting]({% link docs/2.0/dev/building/troubleshooting.md %}) covers common build issues.

## Testing

* [Testing]({% link docs/2.0/dev/sqllogictest/overview.md %}) gives an overview of how DuckDB is tested.
* [sqllogictest Introduction]({% link docs/2.0/dev/sqllogictest/intro.md %}) introduces the sqllogictest format used for most of DuckDB's tests.
* [Writing Tests]({% link docs/2.0/dev/sqllogictest/writing_tests.md %}) describes how to write new tests.
* [Internal Errors]({% link docs/2.0/dev/internal_errors.md %}) explains what internal errors are and how to debug them.

## Performance

* [Profiling]({% link docs/2.0/dev/profiling.md %}) shows how to use DuckDB's built-in query profiler.
* [Metrics]({% link docs/2.0/dev/metrics.md %}) lists the metrics collected by the profiler.
* [Benchmark Suite]({% link docs/2.0/dev/benchmark.md %}) describes how to run DuckDB's benchmarks to detect performance regressions.
