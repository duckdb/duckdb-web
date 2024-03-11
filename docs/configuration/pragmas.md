---
layout: docu
title: Pragmas
redirect_from:
  - /docs/sql/pragmas
  - /docs/sql/pragmas/
---

The `PRAGMA` statement is an SQL extension adopted by DuckDB from SQLite. `PRAGMA` statements can be issued in a similar manner to regular SQL statements. `PRAGMA` commands may alter the internal state of the database engine, and can influence the subsequent execution or behavior of the engine.

`PRAGMA` statements that assign a value to an option can also be issued using the [`SET` statement](../sql/statements/set) and the value of an option can be retrieved using `SELECT current_setting(option_name)`.

For DuckDB's built in configuration options, see the [Configuration Reference](overview#configuration-reference).
DuckDB [extensions](../extensions/overview) may register additional configuration options.
These are documented in the respective extension's documentation page.

## List of Supported `PRAGMA` Statements

Below is a list of supported `PRAGMA` statements.

### Schema Information

List all databases:

```sql
PRAGMA database_list;
```

List all tables:

```sql
PRAGMA show_tables;
```

List all tables, with extra information, similarly to [`DESCRIBE`](../guides/meta/describe):

```sql
PRAGMA show_tables_expanded;
```

To list all functions:

```sql
PRAGMA functions;
```

### Table Information

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

To also show table structure, but in a slightly different format (included for compatibility):

```sql
PRAGMA show('table_name');
```

### Memory Limit

Set the memory limit for the buffer manager:

```sql
SET memory_limit = '1GB';
SET max_memory = '1GB';
```

> Warning The specified memory limit is only applied to the buffer manager.
> For most queries, the buffer manager handles the majority of the data processed.
> However, certain in-memory data structures such as [vectors](/internals/vector) and query results are allocated outside of the buffer manager.
> Additionally, [aggregate functions](../sql/aggregates) with complex state (e.g., `list`, `mode`, `quantile`, `string_agg`, and `approx` functions) use memory outside of the buffer manager.
> Therefore, the actual memory consumption can be higher than the specified memory limit.

### Threads

Set the amount of threads for parallel query execution:

```sql
SET threads = 4;
```

### Database Size

Get the file and memory size of each database:

```sql
SET database_size;
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

### Collations

List all available collations:

```sql
PRAGMA collations;
```

Set the default collation to one of the available ones:

```sql
SET default_collation = 'nocase';
```

### Implicit Casting to `VARCHAR`

Prior to version 0.10.0, DuckDB would automatically allow any type to be implicitly cast to `VARCHAR` during function binding. As a result it was possible to e.g., compute the substring of an integer without using an implicit cast. For version v0.10.0 and later an explicit cast is needed instead. To revert to the old behaviour that performs implicit casting, set the `old_implicit_casting` variable to `true`.

```sql
SET old_implicit_casting = true;
```

### Default Ordering for NULLs

Set the default ordering for NULLs to be either `NULLS FIRST` or `NULLS LAST`:

```sql
SET default_null_order = 'NULLS FIRST';
SET default_null_order = 'NULLS LAST';
```

Set the default result set ordering direction to `ASCENDING` or `DESCENDING`:

```sql
SET default_order = 'ASCENDING';
SET default_order = 'DESCENDING';
```

### Version

Show DuckDB version:

```sql
PRAGMA version;
CALL pragma_version();
```

### Platform

`platform` returns an identifier for the platform the current DuckDB executable has been compiled for, e.g., `osx_arm64`.
The format of this identifier matches the platform name as described [on the extension loading explainer](../extensions/working_with_extensions#platforms).

```sql
PRAGMA platform;
CALL pragma_platform();
```

### Progress Bar

Show progress bar when running queries:

```sql
PRAGMA enable_progress_bar;
```

Don't show a progress bar for running queries:

```sql
PRAGMA disable_progress_bar;
```

### Profiling

#### Enable Profiling

To enable profiling:

```sql
PRAGMA enable_profiling;
PRAGMA enable_profile;
```

#### Profiling Format

The format of the resulting profiling information can be specified as either `json`, `query_tree`, or `query_tree_optimizer`. The default format is `query_tree`, which prints the physical operator tree together with the timings and cardinalities of each operator in the tree to the screen.

To return the logical query plan as JSON:

```sql
SET enable_profiling = 'json';
```

To return the logical query plan:

```sql
SET enable_profiling = 'query_tree';
```

To return the physical query plan:

```sql
SET enable_profiling = 'query_tree_optimizer';
```

#### Disable Profiling

To disable profiling:

```sql
PRAGMA disable_profiling;
PRAGMA disable_profile;
```

#### Profiling Output

By default, profiling information is printed to the console. However, if you prefer to write the profiling information to a file the `PRAGMA` `profiling_output` can be used to write to a specified file. **Note that the file contents will be overwritten for every new query that is issued, hence the file will only contain the profiling information of the last query that is run.**

```sql
SET profiling_output = '/path/to/file.json';
SET profile_output = '/path/to/file.json';
```

#### Profiling Mode

By default, a limited amount of profiling information is provided (`standard`).
For more details, use the detailed profiling mode by setting `profiling_mode` to `detailed`.
The output of this mode shows how long it takes to apply certain optimizers on the query tree and how long physical planning takes.

```sql
SET profiling_mode = 'detailed';
```

### Optimizer

To disable the query optimizer:

```sql
PRAGMA disable_optimizer;
```

To enable the query optimizer:

```sql
PRAGMA enable_optimizer;
```

### Logging

Set a path for query logging:

```sql
SET log_query_path = '/tmp/duckdb_log/';
```

Disable query logging:

```sql
SET log_query_path = '';
```

### Explain Plan Output

The output of [`EXPLAIN`](../sql/statements/profiling) output can be configured to show only the physical plan. This is the default configuration.

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

### Full-Text Search Indexes

The `create_fts_index` and `drop_fts_index` options are only available when the [`fts` extension](../extensions/full_text_search) is loaded. Their usage is documented on the [Full-Text Search extension page](../extensions/full_text_search).

### Verification of External Operators

Enable verification of external operators:

```sql
PRAGMA verify_external;
```

Disable verification of external operators:

```sql
PRAGMA disable_verify_external;
```

### Verification of Round-Trip Capabilities

Enable verification of round-trip capabilities for supported logical plans:

```sql
PRAGMA verify_serializer;
```

Disable verification of round-trip capabilities:

```sql
PRAGMA disable_verify_serializer;
```

### Object Cache

Enable caching of objects for e.g., Parquet metadata:

```sql
PRAGMA enable_object_cache;
```

Disable caching of objects:

```sql
PRAGMA disable_object_cache;
```

### Checkpoint

#### Force Checkpoint

When [`CHECKPOINT`](../sql/statements/checkpoint) is called when no changes are made, force a checkpoint regardless.

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

### Progress Bar

Enable printing of the progress bar (if it's possible):

```sql
PRAGMA enable_print_progress_bar;
```

Disable printing of the progress bar:

```sql
PRAGMA disable_print_progress_bar;
```

### Temp Directory for Spilling Data to Disk

By default, DuckDB uses a temporary directory named `⟨database_file_name⟩.tmp` to spill to disk, located in the same directory as the database file. To change this, use:

```sql
SET temp_directory = '/path/to/temp_dir.tmp/'
```

### Storage Information

To get storage information:

```sql
PRAGMA storage_info('table_name');
CALL pragma_storage_info('table_name');
```

This call returns the following information for the given table:

<div class="narrow_table"></div>

| Name           | Type      | Description                                           |
|----------------|-----------|-------------------------------------------------------|
| `row_group_id` | `BIGINT`  ||
| `column_name`  | `VARCHAR` ||
| `column_id`    | `BIGINT`  ||
| `column_path`  | `VARCHAR` ||
| `segment_id`   | `BIGINT`  ||
| `segment_type` | `VARCHAR` ||
| `start`        | `BIGINT`  | The start row id of this chunk                        |
| `count`        | `BIGINT`  | The amount of entries in this storage chunk           |
| `compression`  | `VARCHAR` | Compression type used for this column - see [blog post](/2022/10/28/lightweight-compression) |
| `stats`        | `VARCHAR` ||
| `has_updates`  | `BOOLEAN` ||
| `persistent`   | `BOOLEAN` | `false` if temporary table                            |
| `block_id`     | `BIGINT`  | empty unless persistent                               |
| `block_offset` | `BIGINT`  | empty unless persistent                               |

See [Storage](/internals/storage) for more information.

### Show Databases

The following statement is equivalent to the [`SHOW DATABASES` statement](../sql/statements/attach):

```sql
PRAGMA show_databases;
```

### User Agent

The following statement returns the user agent information, e.g., `duckdb/v0.10.0(osx_arm64)`.

```sql
PRAGMA user_agent;
```

### Metadata Information

The following statement returns information on the metadata store (`block_id`, `total_blocks`, `free_blocks`, and `free_list`).

```sql
PRAGMA metadata_info;
```

### Selectively Disabling Optimizers

The `disabled_optimizers` option allows selectively disabling optimization steps.
For example, to disable `filter_pushdown` and `statistics_propagation`, run:

```sql
SET disabled_optimizers = 'filter_pushdown,statistics_propagation';
```

The available optimizations can be queried using the [`duckdb_optimizers()` table function](../sql/duckdb_table_functions#duckdb_optimizers).

> Warning The `disabled_optimizers` option should only be used for debugging performance issues and should be avoided in production.

### Returning Errors as JSON

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

### Query Verification (for Development)

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
