---
layout: docu
title: Migrating to DuckDB v2.0
---

DuckDB v2.0.0 is packed with new features and performance improvements, including query optimization and asynchronous I/O.
It also ships a small set of breaking changes, most notably a new default storage format and the completed lambda syntax transition.
This page provides guidance on migrating existing deployments to DuckDB v2.0.0.

## Before You Migrate

Before migrating to DuckDB v2.0.0, assess whether your workload is mission-critical.
For such workloads, consider waiting for upcoming patch releases, which address issues that surface shortly after a major release.
To help facilitate this, the DuckDB development team extended [support for DuckDB v1.5 into early 2027]({% link release_calendar.md %}).

> Bestpractice In all cases, we recommend setting up a shadow system that tracks your existing workload. This lets you test DuckDB v2.0.0 in an environment outside of your production system before switching over.

For simple deployments, migrating is straightforward.
Complex deployments, especially those that run many DuckDB processes, require more care.
We expect the most common source of issues to be the storage format, which is described first below.

## Breaking Changes

### Storage Format

The DuckDB v2.0.0 storage format is _not backward compatible_ with earlier versions.
A database file created or modified by v2.0.0 uses [storage version 69]({% link docs/preview/internals/storage.md %}#storage-version-table), which older DuckDB versions cannot read.

For example, creating a database with v2.0.0 and then opening it with v1.5.6 results in an error:

```bash
~/.duckdb/cli/latest/duckdb my.db -c "CREATE TABLE t (x INT);"
~/.duckdb/cli/1.5.6/duckdb my.db
```

```console
IO Error:
Trying to read a database file with version number 69, but we can only read versions between 64 and 68.
The database file was created with a newer version of DuckDB.

Newer DuckDB version might introduce backward incompatible changes (possibly guarded by compatibility settings).
See the storage page for migration strategy and more information: https://duckdb.org/docs/preview/internals/storage
```

> Warning In a deployment with many DuckDB processes running different versions, a single write by a v2.0.0 process can make a database file unreadable by the remaining older processes. Roll out the upgrade carefully and verify that every process that touches a shared database file is on a compatible version.

#### Writing Files for Older Versions

If you need database files that remain readable by an older DuckDB version, write them with an explicit storage version using the `-storage-version` command line argument:

```bash
~/.duckdb/cli/latest/duckdb my.db -storage-version v1.5.6 -c "CREATE TABLE t (x INT);"
~/.duckdb/cli/1.5.5/duckdb my.db
```

The storage version can also be set with the `storage_compatibility_version` configuration option or the `STORAGE_VERSION` option of the [`ATTACH` statement]({% link docs/preview/sql/statements/attach.md %}).
For the full set of methods and the mapping between DuckDB versions and storage versions, see the [Storage Versions and Format page]({% link docs/preview/internals/storage.md %}).

#### Converting Existing Databases

To move an existing database file to the v2.0.0 storage format, open it with the older DuckDB version and export it, then import it with v2.0.0:

```bash
/older/duckdb mydata.old.db -c "EXPORT DATABASE 'tmp'"
/newer/duckdb mydata.new.db -c "IMPORT DATABASE 'tmp'"
```

For details on this and other conversion methods, including `COPY FROM DATABASE`, see [How to Move between Storage Formats]({% link docs/preview/internals/storage.md %}#how-to-move-between-storage-formats).

> This section is tracking the following pull request: [duckdb#22875](https://github.com/duckdb/duckdb/pull/22875).

### Lambda Syntax

DuckDB v2.0.0 completes the lambda syntax transition that began in [v1.3]({% post_url 2025-05-21-announcing-duckdb-130 %}).
The old single arrow syntax (`x -> x + 1`) is now disabled by default in favor of the Python-style syntax (`lambda x : x + 1`).

```sql
-- disabled by default in v2.0.0
SELECT list_transform([1, 2, 3], x -> x + 1);
-- use the Python-style syntax instead
SELECT list_transform([1, 2, 3], lambda x : x + 1);
```

If you cannot update your queries yet, you can re-enable the old syntax for the session:

```sql
SET lambda_syntax = 'enable_single_arrow';
```

This flag is a temporary bridge: DuckDB v2.1 will remove it and the single arrow syntax entirely.
For details, see [Deprecated Syntax]({% link docs/preview/sql/functions/lambda.md %}#deprecated-syntax).

> This section is tracking the following pull requests: [duckdb#22682](https://github.com/duckdb/duckdb/pull/22682), [duckdb#13389](https://github.com/duckdb/duckdb/pull/13389).

### SQL Parser

DuckDB v2.0.0 replaces the PostgreSQL-derived parser with a new [PEG-based parser]({% link docs/preview/sql/peg_parser.md %}).
It is designed to be compatible with the previous parser, so queries that parsed before should continue to parse, and error messages now include more precise source locations.
If a query that parsed on an earlier version fails on v2.0.0, please [file an issue](https://github.com/duckdb/duckdb/issues).
For details, see the [PEG parser page]({% link docs/preview/sql/peg_parser.md %}).

If you would like to revert to the old parser, use the [`legacy_parser` extension]({% link docs/preview/core_extensions/legacy_parser.md %}).
To install and activate it, run the following commands:

```sql
INSTALL legacy_parser;
LOAD legacy_parser;
SET enable_legacy_parser = true;
```

> This section is tracking the following pull request: [duckdb#22194](https://github.com/duckdb/duckdb/pull/22194), reported in issue [duckdb#7675](https://github.com/duckdb/duckdb/issues/7675).

### C and C++ Extension API

DuckDB v2.0.0 ships a reworked, versioned C API with a stable ABI, along with a C++ API layered on top of it.
Extensions built against the previous unstable C++ API must be rebuilt for v2.0.0.
If you depend on third-party extensions, confirm that a v2.0.0-compatible build is available before upgrading.
For background on extension stability levels, see [Versioning of Extensions]({% link docs/preview/extensions/versioning_of_extensions.md %}); for the C API reference, see the [C API page]({% link docs/preview/clients/c/api.md %}).

> This section is tracking the following pull requests: [duckdb#24702](https://github.com/duckdb/duckdb/pull/24702), [duckdb#24135](https://github.com/duckdb/duckdb/pull/24135), [duckdb#24435](https://github.com/duckdb/duckdb/pull/24435).

### ICU Removed from the Core Build

DuckDB v2.0.0 removes the dependency on the [ICU library](https://github.com/unicode-org/icu).
Time zones, calendars, and collations are now implemented natively by the [`icu` extension]({% link docs/preview/core_extensions/icu.md %}), and will continue to behave as before.
No query changes are required, but if you ship a custom build, note that ICU is no longer bundled.
If you find that ICU's behavior changed, please [file an issue](https://github.com/duckdb/duckdb/issues).

> This section is tracking the following pull requests: [duckdb#24463](https://github.com/duckdb/duckdb/pull/24463), [duckdb#24403](https://github.com/duckdb/duckdb/pull/24403).

## What's New in v2.0

Beyond the breaking changes above, DuckDB v2.0.0 adds a large set of new features.
Rather than repeat the feature documentation here, this section points to where each new feature is covered in full.
For the complete tour, see the [preview announcement]({% post_url 2026-08-17-duckdb-20-highlights %}) and the detailed release announcement.
The [What's New in the Docs for 2.0 page]({% link docs/preview/whats_new_in_the_docs.md %}) links every high-level new feature to its documentation, organized by theme:

* DuckDB as a server with the [`quack` extension]({% link docs/preview/core_extensions/quack.md %}) and the [`CONNECT` statement]({% link docs/preview/sql/statements/connect.md %})
* The [`VARIANT` type]({% link docs/preview/sql/data_types/variant.md %}) for semi-structured data
* [Triggers]({% link docs/preview/sql/statements/create_trigger.md %}) that run actions automatically in response to table changes
* SQL dialect additions, including [data-modifying CTEs]({% link docs/preview/sql/query_syntax/with.md %}#data-modifying-ctes) and [nested schemas]({% link docs/preview/sql/statements/create_schema.md %}#nested-schemas)
* [Asynchronous I/O]({% link docs/preview/data/io.md %}) for faster reads from object storage
* Optimizer and engine improvements that speed up existing queries, including on Windows
* Self-hostable [extension repositories]({% link docs/preview/extensions/extension_distribution.md %}) for signing and distributing your own extensions

Several of the headline v2.0.0 changes are covered in [Breaking Changes](#breaking-changes) above: the new default [storage format](#storage-format), the [PEG-based SQL parser](#sql-parser), the reworked [C and C++ extension API](#c-and-c-extension-api), and the native timezone, calendar and collation support left after [ICU was removed from the core build](#icu-removed-from-the-core-build).

## Linux: Performance Differences between CLI and Python Clients

On Linux, you may experience a slight performance difference between the CLI and the Python clients, with the CLI client outperforming the Python client. The reason for this is that the CLI's build uses Link Time Optimization (LTO), while the Python client is currently built without this option. This is subject to change in [upcoming versions]({% link release_calendar.md %}).

## See Also

* [Storage Versions and Format]({% link docs/preview/internals/storage.md %})
* [Operations Manual]({% link docs/preview/operations_manual/overview.md %})
