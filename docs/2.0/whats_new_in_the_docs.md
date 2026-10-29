---
layout: docu
redirect_from:
- /docs/current/whats_new_in_the_docs
- /docs/lts/whats_new_in_the_docs
- /docs/preview/whats_new_in_the_docs
- /docs/stable/whats_new_in_the_docs
title: What's New in the Docs for 2.0
---

This page tracks the documentation for the features introduced in DuckDB 2.0, organized around the themes of the [DuckDB 2.0.0 release announcement]({% post_url 2026-10-21-announcing-duckdb-200 %}). Each section links to the relevant documentation. For smaller features, see the [“Gems of DuckDB 2.0.0” blog post]({% post_url 2026-10-26-gems-of-duckdb-200 %}), which covers the Python appender, CLI usability improvements, secure views and custom partition paths.

## DuckDB as a Server: Quack and `CONNECT`

Since v1.5.3, DuckDB can run as a server via the Quack protocol, letting multiple clients connect to a shared instance over the network. DuckDB 2.0 ships a polished version of the `quack` extension, which provides the remote protocol, and adds the new `CONNECT` and `DISCONNECT` statements to open and close connections from SQL. The command line client can start a server and attach to one directly.

* [Quack extension]({% link docs/2.0/core_extensions/quack.md %}#usage)
* [`CONNECT` and `DISCONNECT` statements]({% link docs/2.0/sql/statements/connect.md %})
* [CLI `-serve` and `-connect` arguments]({% link docs/2.0/clients/cli/arguments.md %}#serving-and-connecting-to-remote-databases)
* [Securing Quack with a reverse proxy]({% link docs/2.0/quack/setup/reverse_proxy.md %})
* [Remote pushdown to PostgreSQL and MySQL]({% link docs/2.0/sql/statements/connect.md %}#supported-databases)

## `VARIANT` Becomes a First-Class Citizen

The `VARIANT` type stores semi-structured, schema-less data such as JSON while keeping the performance of columnar execution. A family of `variant_*` functions constructs and inspects variant values.

* [Variant type]({% link docs/2.0/sql/data_types/variant.md %})
* [Variant functions]({% link docs/2.0/sql/functions/variant.md %})

## Triggers

DuckDB 2.0 added trigger support, so you can run actions automatically in response to table changes. This is useful for building audit tables and enforcing invariants.

* [`CREATE TRIGGER` statement]({% link docs/2.0/sql/statements/create_trigger.md %})

## SQL Dialect Additions

DuckDB 2.0 extended the SQL dialect in several directions, from new join types to data-modifying CTEs and a friendlier variable syntax.

* [Explicit join type syntax, including nearest (`NEAREST`) joins]({% link docs/2.0/sql/query_syntax/from.md %}#nearest-joins)
* [Data-modifying CTEs]({% link docs/2.0/sql/query_syntax/with.md %}#data-modifying-ctes), including [`COPY ...` blocks in CTEs]({% link docs/2.0/sql/statements/copy.md %}#copy--to)
* [Nested schemas]({% link docs/2.0/sql/statements/create_schema.md %}#nested-schemas)
* [The `$⟨variable⟩` variable shorthand]({% link docs/2.0/sql/statements/set_variable.md %}#the-name-shorthand), including [session variables as default parameter values]({% link docs/2.0/sql/query_syntax/prepared_statements.md %}#session-variables-as-default-values)
* [JSON mutation functions]({% link docs/2.0/data/json/json_functions.md %}#json-mutation-functions)
* [Grouping by `UNNEST`]({% link docs/2.0/sql/query_syntax/groupby.md %}#grouping-by-unnest)
* [The SQL-standard `FETCH FIRST` syntax]({% link docs/2.0/sql/query_syntax/limit.md %}#fetch-first)
* Well-defined semantics for multiple matching source rows in [`MERGE INTO`]({% link docs/2.0/sql/statements/merge_into.md %}#multiple-matching-source-rows) and [`UPDATE ... FROM`]({% link docs/2.0/sql/statements/update.md %}#multiple-matching-source-rows)
* [`SECURE VIEW`]({% link docs/2.0/sql/statements/create_view.md %}#examples)
* [`SHOW` statement]({% link docs/2.0/sql/statements/show.md %}#show-statement)
* [Setting a sequence value]({% link docs/2.0/sql/statements/create_sequence.md %}#setting-the-sequence-value)
* [`regexp_extract` additions]({% link docs/2.0/sql/functions/regular_expressions.md %}#using-regexp_extract)

## Asynchronous I/O

DuckDB 2.0 issues reads in the background and keeps multiple requests in flight, which speeds up queries that read from object storage such as S3. The behavior is controlled by the `async_threads` and read-ahead settings.

* [Asynchronous I/O overview]({% link docs/2.0/data/io.md %})
* [Thread pools]({% link docs/2.0/data/io.md %}#thread-pools) and [read-ahead]({% link docs/2.0/data/io.md %}#read-ahead)
* [Asynchronous I/O configuration settings]({% link docs/2.0/configuration/overview.md %})

## Faster Queries across the Board

DuckDB 2.0 included optimizer and engine improvements, including faster recursive CTEs and better row-group pruning.

* [Recursive CTEs]({% link docs/2.0/sql/query_syntax/with.md %}#recursive-ctes) and the [blog post on how DuckDB runs them faster]({% post_url 2026-08-25-how-duckdb-runs-recursive-ctes-faster %})
* [Min-max indexes (zonemaps)]({% link docs/2.0/sql/indexes.md %}#min-max-index-zonemap) used for row-group pruning

## Storage Format v2.0

New database files use the v2.0.0 storage format by default. The format adds lazy metadata loading, better compression and corruption validation. DuckDB versions before 2.0 cannot read files in the new format, so a migration guide covers upgrading existing deployments.

* [Default storage version]({% link docs/2.0/internals/storage.md %}#default-storage-version)
* [Storage version table]({% link docs/2.0/internals/storage.md %}#storage-version-table)
* Migrating existing deployments: see the [DuckDB 2.0 migration guide]({% link docs/2.0/operations_manual/migration.md %})

## A Brand New SQL Parser

DuckDB 2.0 introduced a PEG-based SQL parser that replaces the PostgreSQL-derived one and allows extensions to contribute grammar.

* [PEG parser]({% link docs/2.0/sql/peg_parser.md %})
* [Legacy parser extension]({% link docs/2.0/core_extensions/legacy_parser.md %}) for switching back to the old parser

## Timezones, Calendars and Collations without ICU

DuckDB 2.0 replaces the ICU library with a smaller, faster native implementation of timezone, calendar and collation support in the `icu` extension.

* [ICU extension]({% link docs/2.0/core_extensions/icu.md %})

## Write Extensions Once, Host Them Yourself

DuckDB 2.0 shipped a revamped C API (C API v2), which is not yet stable. You can also register and host your own extension repositories or statically link extensions into custom builds.

* [C API v2]({% link docs/2.0/clients/c/overview.md %}#c-api-v2)
* [Extension repositories]({% link docs/2.0/extensions/extension_repositories.md %})
* Statically linking extensions: see [Statically Linking Extensions]({% link docs/2.0/dev/building/linking_extensions.md %})

## Core Extension Updates

Several core extensions shipped new features alongside DuckDB 2.0.

* [DuckLake extension]({% link docs/2.0/core_extensions/ducklake.md %}), the reference implementation of DuckLake 1.1
* [Iceberg extension `ATTACH` options]({% link docs/2.0/core_extensions/iceberg/iceberg_options.md %}#attach-options) for REST catalogs
* [Creating Delta tables]({% link docs/2.0/core_extensions/delta.md %}#creating-tables), [time travel]({% link docs/2.0/core_extensions/delta.md %}#time-travel) and [`VARIANT` columns]({% link docs/2.0/core_extensions/delta.md %}#variant-columns) in the Delta extension

## Deprecations

DuckDB 2.0 disables or phases out a few features, which will be removed in future releases.

* [The single-arrow lambda syntax]({% link docs/2.0/sql/functions/lambda.md %}#deprecated-syntax), now disabled by default
* [macOS x86_64 (`osx_amd64`)]({% link docs/2.0/operations_manual/installing_duckdb/requirements.md %}#supported-platforms), for which community extensions are only built on a best-effort basis

## Other Documentation Updates

Additional 2.0 features documented across the site, grouped by area.

### Data Import and Export

* [Writing GeoJSON]({% link docs/2.0/data/json/writing_json.md %}#geojson) and [loading GeoJSON]({% link docs/2.0/data/json/loading_json.md %}#geojson)
* [The Parquet `schema` parameter]({% link docs/2.0/data/parquet/overview.md %}#using-the-schema-parameter) and [new Parquet writing options]({% link docs/2.0/data/parquet/overview.md %}#writing-to-parquet-files)
* [The `PARTITION_PATH` copy option]({% link docs/2.0/data/partitioning/partitioned_writes.md %}#custom-partition-paths) for computing custom partition subdirectories
* [The `ORDER_BY` copy option]({% link docs/2.0/data/partitioning/partitioned_writes.md %}#sorting-rows-within-partitions) for sorting rows before writing

### Clients

* [CLI agent mode]({% link docs/2.0/clients/cli/agent_mode.md %}), which produces compact, machine-readable output when the CLI is driven by an AI coding agent
* [CLI command history]({% link docs/2.0/clients/cli/dot_commands.md %}#command-history): the `.history` command and the `shell_history()` table function
* [The `.manual` dot command]({% link docs/2.0/clients/cli/dot_commands.md %}#displaying-function-documentation), which shows the signatures, description and examples of a SQL function
* [Pretty-printed, highlighted `.schema` output]({% link docs/2.0/clients/cli/dot_commands.md %}#querying-the-database-schema) with `--no-indent` to restore the single-line form
* [The Python appender]({% link docs/2.0/clients/python/appender.md %}) for inserting rows that Python code produces

### Building

* [A C++17 compiler]({% link docs/2.0/dev/building/overview.md %}#prerequisites) is now required to build DuckDB
