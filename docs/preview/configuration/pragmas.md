---
layout: docu
title: Pragmas
---

<!-- markdownlint-disable MD001 -->

The `PRAGMA` statement is a SQL extension adopted by DuckDB from SQLite. `PRAGMA` statements can be issued in a similar manner to regular SQL statements. `PRAGMA` commands may alter the internal state of the database engine, and can influence the subsequent execution or behavior of the engine.

`PRAGMA` statements that assign a value to an option can also be issued using the [`SET` statement]({% link docs/preview/sql/statements/set.md %}) and the value of an option can be retrieved using `SELECT current_setting(option_name)`.

For DuckDB's built in configuration options, see the [Configuration Reference]({% link docs/preview/configuration/overview.md %}#configuration-reference).
DuckDB [extensions]({% link docs/preview/extensions/overview.md %}) may register additional configuration options.
These are documented in the respective extensions' documentation pages.

This page contains the supported `PRAGMA` settings.

## Metadata

#### Schema Information

List all databases:

```sql
PRAGMA database_list;
```

List all tables:

```sql
PRAGMA show_tables;
```

List all tables, with extra information, similarly to [`DESCRIBE`]({% link docs/preview/guides/meta/describe.md %}):

```sql
PRAGMA show_tables_expanded;
```

To list all functions:

```sql
PRAGMA functions;
```

For queries targeting non-existing schemas, DuckDB generates “did you mean...” style error messages.
When there are thousands of attached databases, these errors can take a long time to generate.
To limit the number of schemas DuckDB looks through, use the `catalog_error_max_schemas` option:

```sql
SET catalog_error_max_schemas = 10;
```

#### Table Information

Get info for a specific table:

```sql
PRAGMA table_info('table_name');
CALL pragma_table_info('table_name');
```

`table_info` returns information about the columns of the table with name `table_name`. The exact format of the table returned is given below:

```sql
cid INTEGER,        -- cid of the column
name VARCHAR,       -- name of the column
type VARCHAR,       -- type of the column
notnull BOOLEAN,    -- if the column is marked as NOT NULL
dflt_value VARCHAR, -- default value of the column, or NULL if not specified
pk BOOLEAN          -- part of the primary key or not
```

#### Database Size

Get the file and memory size of each database:

```sql
PRAGMA database_size;
CALL pragma_database_size();
```

`database_size` returns information about the file and memory size of each database. The column types of the returned results are given below:

```sql
database_name VARCHAR, -- database name
database_size VARCHAR, -- total block count times the block size
block_size BIGINT,     -- database block size
total_blocks BIGINT,   -- total blocks in the database
used_blocks BIGINT,    -- used blocks in the database
free_blocks BIGINT,    -- free blocks in the database
wal_size VARCHAR,      -- write ahead log size
memory_usage VARCHAR,  -- memory used by the database buffer manager
memory_limit VARCHAR   -- maximum memory allowed for the database
```

#### Storage Information

To get storage information:

```sql
PRAGMA storage_info('table_name');
CALL pragma_storage_info('table_name');
```

This call returns the following information for the given table:

| Name           | Type      | Description                                           |
|----------------|-----------|-------------------------------------------------------|
| `row_group_id` | `BIGINT`  |                                                                                                                                                    |
| `column_name`  | `VARCHAR` |                                                                                                                                                    |
| `column_id`    | `BIGINT`  |                                                                                                                                                    |
| `column_path`  | `VARCHAR` |                                                                                                                                                    |
| `segment_id`   | `BIGINT`  |                                                                                                                                                    |
| `segment_type` | `VARCHAR` |                                                                                                                                                    |
| `start`        | `BIGINT`  | The start row id of this chunk                                                                                                                     |
| `count`        | `BIGINT`  | The amount of entries in this storage chunk                                                                                                        |
| `compression`  | `VARCHAR` | Compression type used for this column – see the [“Lightweight Compression in DuckDB” blog post]({% post_url 2022-10-28-lightweight-compression %}) |
| `stats`        | `VARCHAR` |                                                                                                                                                    |
| `has_updates`  | `BOOLEAN` |                                                                                                                                                    |
| `persistent`   | `BOOLEAN` | `false` if temporary table                                                                                                                         |
| `block_id`     | `BIGINT`  | Empty unless persistent                                                                                                                            |
| `block_offset` | `BIGINT`  | Empty unless persistent                                                                                                                            |

See [Storage]({% link docs/preview/internals/storage.md %}) for more information.

#### Show Databases

The following statement is equivalent to the [`SHOW DATABASES` statement]({% link docs/preview/sql/statements/attach.md %}):

```sql
PRAGMA show_databases;
```

## Resource Management

#### Memory Limit

Set the memory limit for the buffer manager:

```sql
SET memory_limit = '1GB';
```

> Warning The specified memory limit is only applied to the buffer manager.
> For most queries, the buffer manager handles the majority of the data processed.
> However, certain in-memory data structures such as [vectors]({% link docs/preview/internals/vector.md %}) and query results are allocated outside of the buffer manager.
> Additionally, [aggregate functions]({% link docs/preview/sql/functions/aggregates.md %}) with complex state (e.g., `list`, `mode`, `quantile`, `string_agg`, and `approx` functions) use memory outside of the buffer manager.
> Therefore, the actual memory consumption can be higher than the specified memory limit.

#### Threads

Set the amount of threads for parallel query execution:

```sql
SET threads = 4;
```

## Collations

List all available collations:

```sql
PRAGMA collations;
```

Set the default collation to one of the available ones:

```sql
SET default_collation = 'nocase';
```

## Default Ordering for NULLs

Set the default ordering for NULLs to be either `NULLS_FIRST`, `NULLS_LAST`, `NULLS_FIRST_ON_ASC_LAST_ON_DESC` or `NULLS_LAST_ON_ASC_FIRST_ON_DESC`:

```sql
SET default_null_order = 'NULLS_FIRST';
SET default_null_order = 'NULLS_LAST_ON_ASC_FIRST_ON_DESC';
```

Set the default result set ordering direction to `ASCENDING` or `DESCENDING`:

```sql
SET default_order = 'ASCENDING';
SET default_order = 'DESCENDING';
```

## Ordering by Non-Integer Literals

By default, ordering by non-integer literals is not allowed:

```sql
SELECT 42 ORDER BY 'hello world';
```

```console
-- Binder Error: ORDER BY non-integer literal has no effect.
```

To allow this behavior, use the `order_by_non_integer_literal` option:

```sql
SET order_by_non_integer_literal = true;
```

## Implicit Casting to `VARCHAR`

Prior to version 0.10.0, DuckDB would automatically allow any type to be implicitly cast to `VARCHAR` during function binding. As a result it was possible to e.g., compute the substring of an integer without using an explicit cast. For version v0.10.0 and later an explicit cast is needed instead. To revert to the old behavior that performs implicit casting, set the `old_implicit_casting` variable to `true`:

```sql
SET old_implicit_casting = true;
```

## Python: Scan All Dataframes

Prior to version 1.1.0, DuckDB's [replacement scan mechanism]({% link docs/preview/clients/c/replacement_scans.md %}) in Python scanned the global Python namespace. To revert to this old behavior, use the following setting:

```sql
SET python_scan_all_frames = true;
```

## Information on DuckDB

#### Version

Show DuckDB version:

```sql
PRAGMA version;
CALL pragma_version();
```

#### Platform

`platform` returns an identifier for the platform the current DuckDB executable has been compiled for, e.g., `osx_arm64`.
The format of this identifier matches the platform name as described in the [extension loading explainer]({% link docs/preview/extensions/extension_distribution.md %}#platforms):

```sql
PRAGMA platform;
CALL pragma_platform();
```

#### User Agent

The following statement returns the user agent information, e.g., `duckdb/v0.10.0(osx_arm64)`:

```sql
PRAGMA user_agent;
```

#### Metadata Information

The following statement returns information on the metadata store (`block_id`, `total_blocks`, `free_blocks`, and `free_list`):

```sql
PRAGMA metadata_info;
```

## Progress Bar

Show progress bar when running queries:

```sql
PRAGMA enable_progress_bar;
```

Or:

```sql
PRAGMA enable_print_progress_bar;
```

Don't show a progress bar for running queries:

```sql
PRAGMA disable_progress_bar;
```

Or:

```sql
PRAGMA disable_print_progress_bar;
```

## EXPLAIN Output

The output of [`EXPLAIN`]({% link docs/preview/sql/statements/profiling.md %}) can be configured to show only the physical plan.

The default configuration of `EXPLAIN`:

```sql
SET explain_output = 'physical_only';
```

To only show the optimized query plan:

```sql
SET explain_output = 'optimized_only';
```

To show all query plans:

```sql
SET explain_output = 'all';
```

## Profiling

### Enable Profiling

The following query enables profiling with the default format, `query_tree`.
Independent of the format, `enable_profiling` is **mandatory** to enable profiling.

```sql
PRAGMA enable_profiling;
PRAGMA enable_profile;
```

### Profiling Coverage

By default, the profiling coverage is set to `SELECT`.
`SELECT` runs the profiler for each operator in the physical plan of a `SELECT` statement.

```sql
SET profiling_coverage = 'SELECT';
```

By default, the profiler **does not** emit profiling information for other statement types (`INSERT INTO`, `ATTACH`, etc.).
To run the profiler for all statement types, change this setting to `ALL`.

```sql
SET profiling_coverage = 'ALL';
```

### Profiling Format

The format of `enable_profiling` can be specified as `query_tree`, `json`, `query_tree_optimizer`, or `no_output`.
Each format prints its output to the configured output, except `no_output`.

The default format is `query_tree`.
It prints the physical query plan and the metrics of each operator in the tree.

```sql
SET enable_profiling = 'query_tree';
```

Alternatively, `json` returns the physical query plan as JSON:

```sql
SET enable_profiling = 'json';
```

> Tip To visualize query plans, consider using the [DuckDB execution plan visualizer](https://db.cs.uni-tuebingen.de/explain/) developed by the [Database Systems Research Group at the University of Tübingen](https://github.com/DBatUTuebingen).

To return the physical query plan, including optimizer and planner metrics:

```sql
SET enable_profiling = 'query_tree_optimizer';
```

Database drivers and other applications can also access profiling information through API calls, in which case users can disable any other output.
Even though the parameter reads `no_output`, it is essential to note that this **only** affects printing to the configurable output.
When accessing profiling information through API calls, it is still crucial to enable profiling:

```sql
SET enable_profiling = 'no_output';
```

### Profiling Output

By default, DuckDB prints profiling information to the standard output.
However, if you prefer to write the profiling information to a file, you can use `PRAGMA` `profiling_output` to specify a filepath.

> Warning The file contents will be overwritten for every newly issued query.
> Hence, the file will only contain the profiling information of the last run query:

```sql
SET profiling_output = '/path/to/file.json';
SET profile_output = '/path/to/file.json';
```

### Profiling Mode

By default, a limited amount of profiling information is provided (`standard`).

```sql
SET profiling_mode = 'standard';
```

For more details, use the detailed profiling mode by setting `profiling_mode` to `detailed`.
The output of this mode includes profiling of the planner and optimizer stages.

```sql
SET profiling_mode = 'detailed';
```

### Custom Metrics

By default, profiling enables all metrics except those activated by detailed profiling.

Using the `custom_profiling_settings` `PRAGMA`, each metric, including those from detailed profiling, can be individually enabled or disabled.
This `PRAGMA` accepts a JSON object with metric names as keys and Boolean values to toggle them on or off.
Settings specified by this `PRAGMA` override the default behavior.

> Note This only affects the metrics when the `enable_profiling` is set to `json` or `no_output`.
> The `query_tree` and `query_tree_optimizer` always use a default set of metrics.

In the following example, the `CPU_TIME` metric is disabled.
The `EXTRA_INFO`, `OPERATOR_CARDINALITY`, and `OPERATOR_TIMING` metrics are enabled.

```sql
SET custom_profiling_settings = '{"CPU_TIME": "false", "EXTRA_INFO": "true", "OPERATOR_CARDINALITY": "true", "OPERATOR_TIMING": "true"}';
```

The profiling documentation contains an overview of the available [metrics]({% link docs/preview/dev/profiling.md %}#metrics).

### Disable Profiling

To disable profiling:

```sql
PRAGMA disable_profiling;
PRAGMA disable_profile;
```

## Query Optimization

#### Optimizer

To disable the query optimizer:

```sql
PRAGMA disable_optimizer;
```

To enable the query optimizer:

```sql
PRAGMA enable_optimizer;
```

#### Selectively Disabling Optimizers

The `disabled_optimizers` option allows selectively disabling optimization steps.
For example, to disable `filter_pushdown` and `statistics_propagation`, run:

```sql
SET disabled_optimizers = 'filter_pushdown,statistics_propagation';
```

The available optimizations can be queried using the [`duckdb_optimizers()` table function]({% link docs/preview/sql/meta/duckdb_table_functions.md %}#duckdb_optimizers).

To re-enable the optimizers, run:

```sql
SET disabled_optimizers = '';
```

> Warning The `disabled_optimizers` option should only be used for debugging performance issues and should be avoided in production.

## Logging

Set a path for query logging:

```sql
SET log_query_path = '/tmp/duckdb_log/';
```

Disable query logging:

```sql
SET log_query_path = '';
```

## Full-Text Search Indexes

The `create_fts_index` and `drop_fts_index` options are only available when the [`fts` extension]({% link docs/preview/core_extensions/full_text_search.md %}) is loaded. Their usage is documented on the [Full-Text Search extension page]({% link docs/preview/core_extensions/full_text_search.md %}).

## Verification

#### Verification of External Operators

Enable verification of external operators:

```sql
PRAGMA verify_external;
```

Disable verification of external operators:

```sql
PRAGMA disable_verify_external;
```

#### Verification of Round-Trip Capabilities

Enable verification of round-trip capabilities for supported logical plans:

```sql
PRAGMA verify_serializer;
```

Disable verification of round-trip capabilities:

```sql
PRAGMA disable_verify_serializer;
```

## Object Cache

Enable caching of objects for e.g., Parquet metadata:

```sql
PRAGMA enable_object_cache;
```

Disable caching of objects:

```sql
PRAGMA disable_object_cache;
```

## Checkpointing

#### Compression

During checkpointing, the existing column data + any new changes get compressed.
There exist a couple of pragmas to influence which compression functions are considered.

##### Force Compression

Prefer using this compression method over any other method if possible:

```sql
PRAGMA force_compression = 'bitpacking';
```

##### Disabled Compression Methods

Avoid using any of the listed compression methods from the comma separated list:

```sql
PRAGMA disabled_compression_methods = 'fsst,rle';
```

#### Force Checkpoint

When [`CHECKPOINT`]({% link docs/preview/sql/statements/checkpoint.md %}) is called when no changes are made, force a checkpoint regardless:

```sql
PRAGMA force_checkpoint;
```

#### Checkpoint on Shutdown

Run a `CHECKPOINT` on successful shutdown and delete the WAL, to leave only a single database file behind:

```sql
PRAGMA enable_checkpoint_on_shutdown;
```

Don't run a `CHECKPOINT` on shutdown:

```sql
PRAGMA disable_checkpoint_on_shutdown;
```

## Temp Directory for Spilling Data to Disk

By default, DuckDB uses a temporary directory named `⟨database_file_name⟩.tmp`{:.language-sql .highlight} to spill to disk, located in the same directory as the database file. To change this, use:

```sql
SET temp_directory = '/path/to/temp_dir.tmp/';
```

## Returning Errors as JSON

The `errors_as_json` option can be set to obtain error information in raw JSON format. For certain errors, extra information or decomposed information is provided for easier machine processing. For example:

```sql
SET errors_as_json = true;
```

Then, running a query that results in an error produces a JSON output:

```sql
SELECT * FROM nonexistent_tbl;
```

```json
{
   "exception_type":"Catalog",
   "exception_message":"Table with name nonexistent_tbl does not exist!\nDid you mean \"temp.information_schema.tables\"?",
   "name":"nonexistent_tbl",
   "candidates":"temp.information_schema.tables",
   "position":"14",
   "type":"Table",
   "error_subtype":"MISSING_ENTRY"
}
```

## IEEE Floating-Point Operation Semantics

DuckDB follows IEEE floating-point operation semantics. If you would like to turn this off, run:

```sql
SET ieee_floating_point_ops = false;
```

In this case, floating point division by zero (e.g., `1.0 / 0.0`, `0.0 / 0.0` and `-1.0 / 0.0`) will all return `NULL`.

## Query Verification (for Development)

The following `PRAGMA`s are mostly used for development and internal testing.

Enable query verification:

```sql
PRAGMA enable_verification;
```

Disable query verification:

```sql
PRAGMA disable_verification;
```

Enable force parallel query processing:

```sql
PRAGMA verify_parallelism;
```

Disable force parallel query processing:

```sql
PRAGMA disable_verify_parallelism;
```

## Block Sizes

When persisting a database to disk, DuckDB writes to a dedicated file containing a list of blocks holding the data.
In the case of a file that only holds very little data, e.g., a small table, the default block size of 256 kB might not be ideal.
Therefore, DuckDB's storage format supports different block sizes.

There are a few constraints on possible block size values.

* Must be a power of two.
* Must be greater or equal to 16384 (16 kB).
* Must be lesser or equal to 262144 (256 kB).

You can set the default block size for all new DuckDB files created by an instance like so:

```sql
SET default_block_size = '16384';
```

It is also possible to set the block size on a per-file basis, see [`ATTACH`]({% link docs/preview/sql/statements/attach.md %}) for details.
