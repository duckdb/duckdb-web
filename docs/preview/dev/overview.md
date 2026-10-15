---
layout: docu
title: Overview
---

The pages in this section are intended for developers who contribute to DuckDB or build extensions for it. If you would like to contribute, please also read the [contributing guidelines](https://github.com/duckdb/duckdb/blob/main/CONTRIBUTING.md).

## Project Structure and Processes

* [DuckDB Repositories]({% link docs/preview/dev/repositories.md %}) lists the repositories that host DuckDB's components, such as clients and extensions.
* [Release Cycle]({% link docs/preview/dev/release_cycle.md %}) describes the release process of DuckDB and its core extensions.

## Building DuckDB

* [Building DuckDB from Source]({% link docs/preview/dev/building/overview.md %}) explains how to compile DuckDB on different platforms and how to build extensions.
* [Build Configuration]({% link docs/preview/dev/building/build_configuration.md %}) lists the build types and options.
* [Troubleshooting]({% link docs/preview/dev/building/troubleshooting.md %}) covers common build issues.

## Testing

* [Testing]({% link docs/preview/dev/sqllogictest/overview.md %}) gives an overview of how DuckDB is tested.
* [sqllogictest Introduction]({% link docs/preview/dev/sqllogictest/intro.md %}) introduces the sqllogictest format used for most of DuckDB's tests.
* [Writing Tests]({% link docs/preview/dev/sqllogictest/writing_tests.md %}) describes how to write new tests.
* [Internal Errors]({% link docs/preview/dev/internal_errors.md %}) explains what internal errors are and how to debug them.

## Performance

* [Profiling]({% link docs/preview/dev/profiling.md %}) shows how to use DuckDB's built-in query profiler.
* [Metrics]({% link docs/preview/dev/metrics.md %}) lists the metrics collected by the profiler.
* [Benchmark Suite]({% link docs/preview/dev/benchmark.md %}) describes how to run DuckDB's benchmarks to detect performance regressions.
