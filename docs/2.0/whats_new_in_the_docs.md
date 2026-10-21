---
layout: docu
redirect_from:
- /docs/current/whats_new_in_the_docs
- /docs/lts/whats_new_in_the_docs
- /docs/preview/whats_new_in_the_docs
title: What's New in the Docs for 2.0
---

This page tracks the documentation for the features introduced in DuckDB 2.0, organized around the themes of the [DuckDB 2.0 highlights blog post]({% post_url 2026-08-17-duckdb-20-highlights %}). Each section links to the relevant documentation.

## DuckDB as a Server: Quack and `CONNECT`

DuckDB 2.0 can run as a server, letting multiple clients connect to a shared instance over the network. The `quack` extension provides the remote protocol, and the new `CONNECT` and `DISCONNECT` statements open and close connections from SQL. The command line client can start a server and attach to one directly.

* [Quack extension]({% link docs/2.0/core_extensions/quack.md %}#usage)
* [`CONNECT` and `DISCONNECT` statements]({% link docs/2.0/sql/statements/connect.md %})
* [CLI `-serve` and `-connect` arguments]({% link docs/2.0/clients/cli/arguments.md %}#serving-and-connecting-to-remote-databases)

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
* [Nested schemas]({% link docs/2.0/sql/statements/create_schema.md %})
* [The `$⟨variable⟩` variable shorthand]({% link docs/2.0/sql/statements/set_variable.md %}#the-name-shorthand), including [session variables as default parameter values]({% link docs/2.0/sql/query_syntax/prepared_statements.md %}#session-variables-as-default-values)
* [JSON mutation functions]({% link docs/2.0/data/json/json_functions.md %})
* [Grouping by `UNNEST`]({% link docs/2.0/sql/query_syntax/groupby.md %})
* [The SQL-standard `FETCH FIRST` syntax]({% link docs/2.0/sql/query_syntax/limit.md %})
* [`SECURE VIEW`]({% link docs/2.0/sql/statements/create_view.md %}#examples)
* [`SHOW` statement]({% link docs/2.0/sql/statements/show.md %}#show-statement)
* [Setting a sequence value]({% link docs/2.0/sql/statements/create_sequence.md %}#setting-the-sequence-value)
* [`regexp_extract` additions]({% link docs/2.0/sql/functions/regular_expressions.md %}#using-regexp_extract)

## Asynchronous I/O

DuckDB 2.0 issues reads in the background and keeps multiple requests in flight, which speeds up queries that read from object storage such as S3. The behavior is controlled by the `async_threads` and read-ahead settings.

* [Asynchronous I/O overview]({% link docs/2.0/data/io.md %})
* [Thread pools]({% link docs/2.0/data/io.md %}#thread-pools) and [read-ahead]({% link docs/2.0/data/io.md %}#read-ahead)
* [Asynchronous I/O configuration settings]({% link docs/2.0/configuration/overview.md %})

## Faster Queries Across the Board

DuckDB 2.0 included optimizer and engine improvements, including faster recursive CTEs and better row-group pruning.

## Storage Format v2.0

New database files use the v2.0.0 storage format by default. The format adds lazy metadata loading, better compression, and corruption validation. Because the format is not forward compatible (older DuckDB versions cannot read files written by v2.0), a migration guide covers upgrading existing deployments.

* [Default storage version]({% link docs/2.0/internals/storage.md %}#default-storage-version)
* [Storage version table]({% link docs/2.0/internals/storage.md %}#storage-version-table)
* Migrating existing deployments: see the [DuckDB 2.0 migration guide]({% link docs/2.0/operations_manual/migration.md %})

## A Brand New SQL Parser

DuckDB 2.0 introduced a PEG-based SQL parser that replaces the PostgreSQL-derived one and allows extensions to contribute grammar.

* [PEG parser]({% link docs/2.0/sql/peg_parser.md %})

## Timezones, Calendars, and Collations Without ICU

DuckDB 2.0 provides a smaller, faster native implementation of timezone, calendar, and collation support, replacing the ICU library with a native implementation in the `icu` extension.

## Write Extensions Once, Host Them Yourself

DuckDB 2.0 shipped a revamped C API (C API v2), which is not yet stable. You can also register and host your own extension repositories, including static linking into custom builds.

* [C API]({% link docs/2.0/clients/c/overview.md %})
* [Extension repositories]({% link docs/2.0/extensions/extension_repositories.md %})
* Statically linking extensions: see [Statically Linking Extensions]({% link docs/2.0/dev/building/linking_extensions.md %})

## Other Documentation Updates

Additional 2.0 features documented across the site, grouped by area.

### SQL

* [`TIMESTAMPTZ_NS`]({% link docs/2.0/sql/data_types/timestamp.md %}#timestamp-types), time zone aware timestamps with nanosecond precision
* [The `lttb` aggregate]({% link docs/2.0/sql/functions/aggregates.md %}#lttbx-y-n) for downsampling time series data
* [The new `extension_name` column in `duckdb_functions`]({% link docs/2.0/sql/meta/duckdb_table_functions.md %}#duckdb_functions)
* [The `duckdb_secret_type_parameters()` function]({% link docs/2.0/sql/meta/duckdb_table_functions.md %}#duckdb_secret_type_parameters) listing the parameters each secret type accepts
* [The `is_generated` and `generation_expression` columns]({% link docs/2.0/sql/meta/duckdb_table_functions.md %}#duckdb_columns) in `duckdb_columns()` and `information_schema.columns`
* [The `decimal_division` function]({% link docs/2.0/sql/functions/numeric.md %}#decimal_divisionx-y) for exact decimal division
* [The `decimal_average` aggregate]({% link docs/2.0/sql/functions/aggregates.md %}#decimal_averagearg) for exact decimal averages
* [The `variant_group_object` aggregate]({% link docs/2.0/sql/functions/variant.md %}#variant_group_objectkey-value) for building `VARIANT` objects
* [The `variant_group_array` function]({% link docs/2.0/sql/functions/variant.md %}#variant_group_arrayx) for collecting values into a `VARIANT` array
* [Renaming a view with `ALTER TABLE ... RENAME TO`]({% link docs/2.0/sql/statements/alter_table.md %}#rename-table) for PostgreSQL compatibility
* [`EXCEPT` as a synonym for `EXCLUDE`]({% link docs/2.0/sql/expressions/star.md %}#exclude-clause) in star expressions
* [No-argument `GROUPING_ID()` and `GROUPING()`]({% link docs/2.0/sql/query_syntax/grouping_sets.md %}#identifying-grouping-sets-with-grouping_id) defaulting to all `GROUP BY` columns
* [Backtick-quoted identifiers]({% link docs/2.0/sql/dialect/keywords_and_identifiers.md %}#identifiers) as an alternative to double quotes
* [`EXPLAIN (SQL)`]({% link docs/2.0/sql/statements/profiling.md %}#explain-sql) rendering the optimized plan as executable SQL
* [Empty `STRUCT` types]({% link docs/2.0/sql/data_types/struct.md %}#creating-structs)

### Data Import and Export

* [Writing GeoJSON]({% link docs/2.0/data/json/writing_json.md %}#geojson) and [loading GeoJSON]({% link docs/2.0/data/json/loading_json.md %}#geojson)
* [The Parquet `schema` parameter]({% link docs/2.0/data/parquet/overview.md %}#using-the-schema-parameter) and [new Parquet writing options]({% link docs/2.0/data/parquet/overview.md %}#writing-to-parquet-files)
* [The `PARTITION_PATH` copy option]({% link docs/2.0/data/partitioning/partitioned_writes.md %}#custom-partition-paths) for computing custom partition subdirectories
* [The `ORDER_BY` copy option]({% link docs/2.0/data/partitioning/partitioned_writes.md %}#sorting-rows-within-partitions) for sorting rows before writing
* [The `TIMESTAMP_IS_ADJUSTED_TO_UTC` and `WRITE_TIMESTAMP_AS_INT96` Parquet writing options]({% link docs/2.0/sql/statements/copy.md %}#parquet-options) for controlling how timestamps are written
* [The `file_row_group_number` virtual column]({% link docs/2.0/data/parquet/overview.md %}#the-file_row_group_number-virtual-column) for Parquet row group pruning
* [The `rejects_line_size_limit` CSV parameter]({% link docs/2.0/data/csv/reading_faulty_csv_files.md %}#parameters) for bounding stored rejected lines

### Clients

* [CLI agent mode]({% link docs/2.0/clients/cli/agent_mode.md %}), which produces compact, machine-readable output when the CLI is driven by an AI coding agent
* [CLI command history]({% link docs/2.0/clients/cli/dot_commands.md %}#command-history): the `.history` command and the `shell_history()` table function
* [Pretty-printed, highlighted `.schema` output]({% link docs/2.0/clients/cli/dot_commands.md %}#querying-the-database-schema) with `--no-indent` to restore the single-line form

### Configuration and Profiling

* [Setting `max_memory` as a percentage]({% link docs/2.0/configuration/pragmas.md %}#memory-limit) of total system memory
* [The `max_execution_time` setting]({% link docs/2.0/configuration/pragmas.md %}#maximum-execution-time) for bounding query wall-clock time
* [The `checkpoint_on_detach` setting]({% link docs/2.0/configuration/pragmas.md %}#checkpoint-on-detach) controlling checkpoints when detaching a database
* [Deprecation of implicit identifier-to-string conversion]({% link docs/2.0/sql/dialect/sql_quirks.md %}#implicit-conversion-of-identifiers-in-table-function-arguments) in table function arguments, with the `table_function_identifier_conversion` setting
* [Removal of the `enable_http_logging` and `http_logging_output` settings]({% link docs/2.0/operations_manual/logging/overview.md %}#logging-specific-types) in favor of the unified logging framework
* [The `http_client_pool_capacity` setting]({% link docs/2.0/data/io.md %}#tuning) for sizing the asynchronous HTTP client pool
* [The metrics layer]({% link docs/2.0/dev/profiling.md %}#metrics) and the [`tracked_metrics` setting]({% link docs/2.0/configuration/pragmas.md %}#custom-metrics)
* [Integer division by zero]({% link docs/2.0/configuration/pragmas.md %}#ieee-floating-point-operation-semantics) now raises an error
* [The `web` profiling format]({% link docs/2.0/dev/profiling.md %}#the-format-option) and the CLI [`.web`]({% link docs/2.0/clients/cli/dot_commands.md %}) command for opening query graphs in a browser

### Building

* [A C++17 compiler]({% link docs/2.0/dev/building/overview.md %}#prerequisites) is now required to build DuckDB
