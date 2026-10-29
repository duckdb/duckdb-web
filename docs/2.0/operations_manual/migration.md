---
layout: docu
redirect_from:
- /docs/current/operations_manual/migration
- /docs/lts/operations_manual/migration
- /docs/preview/operations_manual/migration
- /docs/stable/operations_manual/migration
title: Migrating to DuckDB 2.0
---

DuckDB 2.0.0 is packed with new features and performance improvements, including query optimization and asynchronous I/O.
It also ships a small set of breaking changes, most notably a new default storage format, which DuckDB versions before 2.0.0 cannot read, and the next step of the lambda syntax transition.
This page provides guidance on migrating existing deployments to DuckDB 2.0.0.

## Before You Migrate

Before migrating to DuckDB 2.0.0, assess whether your workload is mission-critical.
For such workloads, consider waiting for upcoming patch releases, which address issues that surface shortly after a major release.
To help facilitate this, the DuckDB development team extended [support for DuckDB 1.5 until March 2027]({% link release_calendar.md %}#lts-releases).
Note that DuckDB 1.4 LTS reaches its end of life on November 17, 2026.

> Bestpractice In all cases, we recommend setting up a shadow system that tracks your existing workload. This lets you test DuckDB 2.0.0 in an environment outside of your production system before switching over.

For simple deployments, migrating is straightforward.
Complex deployments, especially those that run many DuckDB processes, require more care.
We expect the most common source of issues to be the storage format, which is described first below.

## Breaking Changes

### Storage Format

DuckDB versions before 2.0.0 _cannot read_ database files that use the DuckDB 2.0.0 storage format.
By default, every new database file created by v2.0.0 uses this format ([storage version 69]({% link docs/2.0/internals/storage.md %}#storage-version-table)).

The other direction keeps working: DuckDB 2.0.0 can read and write existing database files created by earlier versions.
These files keep their storage version when v2.0.0 writes to them, so they remain readable by the earlier version.

For example, creating a database with v2.0.0 and then opening it with v1.5.6 results in an error:

```bash
~/.duckdb/cli/latest/duckdb my.db -c "CREATE TABLE t (x INT);"
~/.duckdb/cli/1.5.6/duckdb my.db
```

```console
IO Error: Trying to read a database file with version number 69, but we can only read versions between 64 and 68.
The database file was created with a newer version of DuckDB.

Newer DuckDB version might introduce backward incompatible changes (possibly guarded by compatibility settings).
See the storage page for migration strategy and more information: https://duckdb.org/internals/storage
```

> Warning In a deployment with many DuckDB processes running different versions, a database file created by a v2.0.0 process is unreadable by the remaining older processes. Roll out the upgrade carefully and verify that every process that touches a shared database file is on a compatible version.

#### Writing Files for Older Versions

If you need database files that remain readable by an older DuckDB version, write them with an explicit storage version using the `-storage-version` command line argument:

```bash
~/.duckdb/cli/latest/duckdb my.db -storage-version v1.5.6 -c "CREATE TABLE t (x INT);"
~/.duckdb/cli/1.5.6/duckdb my.db
```

The storage version can also be set with the `storage_compatibility_version` configuration option or the `STORAGE_VERSION` option of the [`ATTACH` statement]({% link docs/2.0/sql/statements/attach.md %}).
For the full set of methods and the mapping between DuckDB versions and storage versions, see the [Storage Versions and Format page]({% link docs/2.0/internals/storage.md %}).

#### Converting Existing Databases

To move an existing database file to the v2.0.0 storage format, open it with the older DuckDB version and export it, then import it with v2.0.0:

```bash
/older/duckdb mydata.old.db -c "EXPORT DATABASE 'tmp'"
/newer/duckdb mydata.new.db -c "IMPORT DATABASE 'tmp'"
```

For details on this and other conversion methods, including `COPY FROM DATABASE`, see [How to Move between Storage Formats]({% link docs/2.0/internals/storage.md %}#how-to-move-between-storage-formats).

### Lambda Syntax

DuckDB 2.0.0 takes the next step in the lambda syntax transition that began in [v1.3]({% post_url 2025-05-21-announcing-duckdb-130 %}).
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

This flag is a temporary bridge: DuckDB 2.1 will remove it and the single arrow syntax entirely.
For details, see [Deprecated Syntax]({% link docs/2.0/sql/functions/lambda.md %}#deprecated-syntax).

### SQL Parser

DuckDB 2.0.0 replaced the PostgreSQL-derived parser with a new [PEG-based parser]({% link docs/2.0/sql/peg_parser.md %}).
It is designed to be compatible with the previous parser, so queries that parsed before should continue to parse, and error messages now include more precise source locations.
If a query that parsed on an earlier version fails on v2.0.0, please [file an issue](https://github.com/duckdb/duckdb/issues).
For details, see the [PEG parser page]({% link docs/2.0/sql/peg_parser.md %}).

A few expressions deliberately behave differently in v2.0.0, which can silently change query results:

* The `~` and `!~` operators now perform [partial regular expression matching]({% link docs/2.0/sql/functions/pattern_matching.md %}#regular-expressions), following PostgreSQL: `'abc' ~ 'b'` now returns `true` (previously `false`). The deprecated `regex_match_operator_semantics` setting restores full matching: `SET regex_match_operator_semantics = 'full';`{:.language-sql .highlight}
* The [factorial operator `!`]({% link docs/2.0/sql/functions/numeric.md %}#factorialx) binds more tightly: `2 * 3!` now returns `12` (previously `720`). Use parentheses to get the old behavior, e.g., `(2 * 3)!`.
* `X'…'` and `B'…'` literals now produce [`BLOB`]({% link docs/2.0/sql/data_types/blob.md %}) and [`BITSTRING`]({% link docs/2.0/sql/data_types/bitstring.md %}) values instead of the `VARCHAR` strings `'x…'` and `'b…'`.

If you would like to revert to the old parser, use the [`legacy_parser` extension]({% link docs/2.0/core_extensions/legacy_parser.md %}).
To install and activate it, run the following commands:

```sql
INSTALL AND LOAD legacy_parser;
SET enable_legacy_parser = true;
```

### C API v2

DuckDB 2.0.0 ships a revamped [C API]({% link docs/2.0/clients/c/overview.md %}#c-api-v2), which is considerably more powerful than its predecessor and exposes components such as file systems and table functions to extensions.
The C API v2 is not yet stable: its interface may change in upcoming releases.
For background on extension stability levels, see [Versioning of Extensions]({% link docs/2.0/extensions/versioning_of_extensions.md %}); for the C API reference, see the [C API page]({% link docs/2.0/clients/c/api.md %}).

### ICU Removed from the Core Build

DuckDB 2.0.0 removed the dependency on the [ICU library](https://github.com/unicode-org/icu).
Time zones, calendars and collations are now implemented natively by the [`icu` extension]({% link docs/2.0/core_extensions/icu.md %}), and will continue to behave as before.
No query changes are required, but if you ship a custom build, note that ICU is no longer bundled.
If you find that ICU's behavior changed, please [file an issue](https://github.com/duckdb/duckdb/issues).

### Division by Zero

Integer division (`//`) and modulo (`%`) by zero, e.g., `1 // 0` and `1 % 0`, now throw an error instead of returning `NULL`:

```console
Invalid Input Error: Division by zero in expression (1 // 0). Use TRY(...) to return NULL for this expression, or SET error_on_division_by_zero=false to return NULL for all divisions by zero.
```

To get `NULL` for a single expression, wrap it in `TRY`, e.g., `TRY(1 // 0)`.
Regular division (`1 / 0`) still returns `inf`.

### `MERGE INTO` with Multiple Matching Source Rows

A [`MERGE INTO` statement]({% link docs/2.0/sql/statements/merge_into.md %}#multiple-matching-source-rows) that would update or delete the same target row more than once, because the row matches multiple source rows, now throws an error instead of silently using one of the source rows.
Deduplicate the source rows or make the `ON` condition unique.

### Untyped `NULL` Columns

An untyped `NULL` now keeps the `NULL` type instead of defaulting to `INTEGER`.
For example, `CREATE TABLE t AS SELECT NULL AS x` creates a column of type `"NULL"`, which rejects subsequent inserts of non-`NULL` values.
Cast the `NULL` to the intended type, e.g., `NULL::VARCHAR AS x`, or restore the previous behavior with `SET legacy_disable_null_type = true;`{:.language-sql .highlight}.

### Identifier Case Setting

The [`preserve_identifier_case` setting]({% link docs/2.0/configuration/overview.md %}) changed from a `BOOLEAN` to a `VARCHAR` with the values `'preserve_case'` (default), `'lowercase'` and `'uppercase'`.
The old values `true` and `false` are still accepted and map to `'preserve_case'` and `'lowercase'`, respectively.

### S3 URL Parameters

Passing S3 settings as URL parameters (e.g., `s3://bucket/file.csv?s3_access_key_id=...`) is disabled by default: the `?` and the following text are now treated as part of the object key.
Use [secrets]({% link docs/2.0/configuration/secrets_manager.md %}) instead or, if you need the legacy behavior, opt in with `SET s3_enable_deprecated_url_parameters = true` (available after loading the `httpfs` extension).

### Removed and Deprecated Settings

* The `custom_profiling_settings` setting was removed. Use `tracked_metrics` instead, see [Profiling]({% link docs/2.0/dev/profiling.md %}).
* The `enable_http_logging` and `http_logging_output` settings were removed. Use `CALL enable_logging('HTTP')` instead, see [Logging]({% link docs/2.0/operations_manual/logging/overview.md %}).
* The `profiling_mode` setting is deprecated and its value has no effect: detailed profiling information is always collected. Use `PRAGMA enable_profiling` to enable profiling.

### Log Storage in the CLI

Since v1.5.0, the CLI uses the `shell_log_storage` log storage by default, which prints warnings to the console but cannot be queried.
To query logs via `duckdb_logs` in the CLI, enable logging with `CALL enable_logging(storage = 'memory')`. Clients other than the CLI still default to the `memory` log storage.

### Client APIs

Some client APIs ship their own breaking changes with DuckDB 2.0.
In particular, the Python client requires Python 3.11 or newer and changes several APIs, see [Migrating Python Code to DuckDB 2.0]({% link docs/2.0/clients/python/migration.md %}).

## What's New in v2.0

Beyond the breaking changes above, DuckDB 2.0.0 added a large set of new features.
Rather than repeat the feature documentation here, this section points to where each new feature is covered in full.
For the complete tour, see the [preview announcement]({% post_url 2026-08-17-duckdb-20-highlights %}) and the [detailed release announcement]({% post_url 2026-10-21-announcing-duckdb-200 %}).
The [What's New in the Docs for 2.0 page]({% link docs/2.0/whats_new_in_the_docs.md %}) links every high-level new feature to its documentation, organized by theme:

* DuckDB as a server with the [`quack` extension]({% link docs/2.0/core_extensions/quack.md %}) and the [`CONNECT` statement]({% link docs/2.0/sql/statements/connect.md %})
* The [`VARIANT` type]({% link docs/2.0/sql/data_types/variant.md %}) for semi-structured data
* [Triggers]({% link docs/2.0/sql/statements/create_trigger.md %}) that run actions automatically in response to table changes
* SQL dialect additions, including [data-modifying CTEs]({% link docs/2.0/sql/query_syntax/with.md %}#data-modifying-ctes) and [nested schemas]({% link docs/2.0/sql/statements/create_schema.md %}#nested-schemas)
* [Asynchronous I/O]({% link docs/2.0/data/io.md %}) for faster reads from object storage
* Optimizer and engine improvements that speed up existing queries, including on Windows
* Self-hostable [extension repositories]({% link docs/2.0/extensions/extension_repositories.md %}) for signing and distributing your own extensions

Several of the headline v2.0.0 changes are covered in [Breaking Changes](#breaking-changes) above: the new default [storage format](#storage-format), the [PEG-based SQL parser](#sql-parser), the revamped [C API v2](#c-api-v2) and the native timezone, calendar and collation support left after [ICU was removed from the core build](#icu-removed-from-the-core-build).

## See Also

* [Storage Versions and Format]({% link docs/2.0/internals/storage.md %})
* [Operations Manual]({% link docs/2.0/operations_manual/overview.md %})
