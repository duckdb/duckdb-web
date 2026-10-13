---
layout: docu
title: What's New in the Docs for 2.0
---

This page tracks the documentation for the features introduced in DuckDB 2.0, organized around the themes of the [DuckDB v2.0 highlights blog post]({% post_url 2026-08-17-duckdb-20-highlights %}). Each section links to the relevant documentation.

## DuckDB as a Server: Quack and `CONNECT`

DuckDB 2.0 can run as a server, letting multiple clients connect to a shared instance over the network. The `quack` extension provides the remote protocol, and the new `CONNECT` and `DISCONNECT` statements open and close connections from SQL. The command line client can start a server and attach to one directly.

* [Quack extension]({% link docs/preview/core_extensions/quack.md %}#usage)
* [`CONNECT` and `DISCONNECT` statements]({% link docs/preview/sql/statements/connect.md %})
* [CLI `-serve` and `-connect` arguments]({% link docs/preview/clients/cli/arguments.md %}#serving-and-connecting-to-remote-databases)

## `VARIANT` Becomes a First-Class Citizen

The `VARIANT` type stores semi-structured, schema-less data such as JSON while keeping the performance of columnar execution. A family of `variant_*` functions constructs and inspects variant values.

* [Variant type]({% link docs/preview/sql/data_types/variant.md %})
* [Variant functions]({% link docs/preview/sql/functions/variant.md %})

## Triggers

DuckDB 2.0 adds trigger support, so you can run actions automatically in response to table changes. This is useful for building audit tables and enforcing invariants.

* [`CREATE TRIGGER` statement]({% link docs/preview/sql/statements/create_trigger.md %})

## SQL Dialect Additions

DuckDB 2.0 extends the SQL dialect in several directions, from new join types to data-modifying CTEs and a friendlier variable syntax.

* [Explicit join type syntax, including nearest (`NEAREST`) joins]({% link docs/preview/sql/query_syntax/from.md %}#specifying-the-join-type-explicitly)
* [Data-modifying CTEs]({% link docs/preview/sql/query_syntax/with.md %}#data-modifying-ctes), including [`COPY ...` blocks in CTEs]({% link docs/preview/sql/statements/copy.md %}#copy--to)
* [Nested schemas]({% link docs/preview/sql/statements/create_schema.md %})
* [The `$⟨variable⟩` variable shorthand]({% link docs/preview/sql/statements/set_variable.md %}#the-name-shorthand), including [session variables as default parameter values]({% link docs/preview/sql/query_syntax/prepared_statements.md %}#session-variables-as-default-values)
* [JSON mutation functions]({% link docs/preview/data/json/json_functions.md %})
* [Grouping by `UNNEST`]({% link docs/preview/sql/query_syntax/groupby.md %})
* [The SQL-standard `FETCH FIRST` syntax]({% link docs/preview/sql/query_syntax/limit.md %})
* [`SECURE VIEW`]({% link docs/preview/sql/statements/create_view.md %}#examples)
* [`SHOW` statement]({% link docs/preview/sql/statements/show.md %}#show-statement)
* [Setting a sequence value]({% link docs/preview/sql/statements/create_sequence.md %}#setting-the-sequence-value)
* [`regexp_extract` additions]({% link docs/preview/sql/functions/regular_expressions.md %}#using-regexp_extract)

## Asynchronous I/O

DuckDB 2.0 issues reads in the background and keeps multiple requests in flight, which speeds up queries that read from object storage such as S3. The behavior is controlled by the `async_threads` and read-ahead settings.

* [Asynchronous I/O overview]({% link docs/preview/data/io.md %})
* [Thread pools]({% link docs/preview/data/io.md %}#thread-pools) and [read-ahead]({% link docs/preview/data/io.md %}#read-ahead)
* [Asynchronous I/O configuration settings]({% link docs/preview/configuration/overview.md %})

## Faster Queries Across the Board

DuckDB 2.0 includes optimizer and engine improvements, including faster recursive CTEs and better row-group pruning.

## Storage Format v2.0

New database files use the v2.0.0 storage format by default. The format adds lazy metadata loading, better compression, and corruption validation. Because the format is not backward compatible, a migration guide covers upgrading existing deployments.

* [Default storage version]({% link docs/preview/internals/storage.md %}#default-storage-version)
* [Storage version table]({% link docs/preview/internals/storage.md %}#storage-version-table)
* Migrating existing deployments: see the [DuckDB v2.0 migration guide](/docs/preview/operations_manual/migration)

## A Brand New SQL Parser

DuckDB 2.0 introduces a PEG-based SQL parser that replaces the PostgreSQL-derived one and allows extensions to contribute grammar.

* [PEG parser]({% link docs/preview/sql/peg_parser.md %})

## Timezones, Calendars, and Collations Without ICU

DuckDB 2.0 provides a smaller, faster native implementation of timezone, calendar, and collation support, reducing reliance on the ICU extension.

## Write Extensions Once, Host Them Yourself

DuckDB 2.0 ships a revamped, stable C API with a versioned ABI, so an extension built once keeps working across releases. You can also register and host your own extension repositories, including static linking into custom builds.

* [C API]({% link docs/preview/clients/c/overview.md %})
* [Extension repositories]({% link docs/preview/extensions/extension_repositories.md %})
* Statically linking extensions: see [Statically Linking Extensions](/docs/preview/dev/building/linking_extensions)

## Other Documentation Updates

Additional 2.0 features documented across the site, grouped by area.

### SQL

* [`TIMESTAMPTZ_NS`]({% link docs/preview/sql/data_types/timestamp.md %}#timestamp-types), time zone aware timestamps with nanosecond precision
* [The `lttb` aggregate]({% link docs/preview/sql/functions/aggregates.md %}#lttbx-y-n) for downsampling time series data
* [The new `extension_name` column in `duckdb_functions`]({% link docs/preview/sql/meta/duckdb_table_functions.md %}#duckdb_functions)
* [The `duckdb_secret_type_parameters()` function]({% link docs/preview/sql/meta/duckdb_table_functions.md %}#duckdb_secret_type_parameters) listing the parameters each secret type accepts
* [The `is_generated` and `generation_expression` columns]({% link docs/preview/sql/meta/duckdb_table_functions.md %}#duckdb_columns) in `duckdb_columns()` and `information_schema.columns`
* [The `decimal_division` function]({% link docs/preview/sql/functions/numeric.md %}#decimal_divisionx-y) for exact decimal division
* [The `decimal_average` aggregate]({% link docs/preview/sql/functions/aggregates.md %}#decimal_averagearg) for exact decimal averages
* [The `variant_group_object` aggregate]({% link docs/preview/sql/functions/variant.md %}#variant_group_objectkey-value) for building `VARIANT` objects
* [The `variant_group_array` function]({% link docs/preview/sql/functions/variant.md %}#variant_group_arrayx) for collecting values into a `VARIANT` array
* [Renaming a view with `ALTER TABLE ... RENAME TO`]({% link docs/preview/sql/statements/alter_table.md %}#rename-table) for PostgreSQL compatibility
* [`EXCEPT` as a synonym for `EXCLUDE`]({% link docs/preview/sql/expressions/star.md %}#exclude-clause) in star expressions
* [No-argument `GROUPING_ID()` and `GROUPING()`]({% link docs/preview/sql/query_syntax/grouping_sets.md %}#identifying-grouping-sets-with-grouping_id) defaulting to all `GROUP BY` columns
* [Backtick-quoted identifiers]({% link docs/preview/sql/dialect/keywords_and_identifiers.md %}#identifiers) as an alternative to double quotes
* [`DEFERRED` primary key and unique constraints]({% link docs/preview/sql/constraints.md %}#deferred-constraints) checked at commit time
* [`EXPLAIN (SQL)`]({% link docs/preview/sql/statements/profiling.md %}#explain-sql) rendering the optimized plan as executable SQL
* [Empty `STRUCT` types]({% link docs/preview/sql/data_types/struct.md %}#creating-structs)

### Data Import and Export

* [Writing GeoJSON]({% link docs/preview/data/json/writing_json.md %}#geojson) and [loading GeoJSON]({% link docs/preview/data/json/loading_json.md %}#geojson)
* [The Parquet `schema` parameter]({% link docs/preview/data/parquet/overview.md %}#using-the-schema-parameter) and [new Parquet writing options]({% link docs/preview/data/parquet/overview.md %}#writing-to-parquet-files)
* [The `PARTITION_PATH` copy option]({% link docs/preview/data/partitioning/partitioned_writes.md %}#custom-partition-paths) for computing custom partition subdirectories
* [The `ORDER_BY` copy option]({% link docs/preview/data/partitioning/partitioned_writes.md %}#sorting-rows-within-partitions) for sorting rows before writing
* [The `TIMESTAMP_IS_ADJUSTED_TO_UTC` and `WRITE_TIMESTAMP_AS_INT96` Parquet writing options]({% link docs/preview/sql/statements/copy.md %}#parquet-options) for controlling how timestamps are written
* [The `file_row_group_number` virtual column]({% link docs/preview/data/parquet/overview.md %}#the-file_row_group_number-virtual-column) for Parquet row group pruning

### Clients

* [CLI agent mode]({% link docs/preview/clients/cli/agent_mode.md %}), an interactive assistant in the command line client
* [CLI command history]({% link docs/preview/clients/cli/dot_commands.md %}#command-history): the `.history` command and the `shell_history()` table function
* [Pretty-printed, highlighted `.schema` output]({% link docs/preview/clients/cli/dot_commands.md %}#querying-the-database-schema) with `--no-indent` to restore the single-line form

### Configuration and Profiling

* [Setting `max_memory` as a percentage]({% link docs/preview/configuration/pragmas.md %}#memory-limit) of total system memory
* [The `max_execution_time` setting]({% link docs/preview/configuration/pragmas.md %}#maximum-execution-time) for bounding query wall-clock time
* [The `checkpoint_on_detach` setting]({% link docs/preview/configuration/pragmas.md %}#checkpoint-on-detach) controlling checkpoints when detaching a database
* [Deprecation of implicit identifier-to-string conversion]({% link docs/preview/sql/dialect/sql_quirks.md %}#implicit-conversion-of-identifiers-in-table-function-arguments) in table function arguments, with the `table_function_identifier_conversion` setting
* [Removal of the `enable_http_logging` and `http_logging_output` settings]({% link docs/preview/operations_manual/logging/overview.md %}#logging-specific-types) in favor of the unified logging framework
* [The `http_client_pool_capacity` setting]({% link docs/preview/data/io.md %}#tuning) for sizing the asynchronous HTTP client pool
* [The metrics layer]({% link docs/preview/dev/profiling.md %}#metrics) and the [`tracked_metrics` setting]({% link docs/preview/configuration/pragmas.md %}#custom-metrics)
* [IEEE floating-point operation semantics]({% link docs/preview/configuration/pragmas.md %}#ieee-floating-point-operation-semantics) for integer division by zero
* [The `web` profiling format]({% link docs/preview/dev/profiling.md %}#the-format-option) and the CLI [`.web`]({% link docs/preview/clients/cli/dot_commands.md %}) command for opening query graphs in a browser

### Building

* [A C++17 compiler]({% link docs/preview/dev/building/overview.md %}#prerequisites) is now required to build DuckDB
