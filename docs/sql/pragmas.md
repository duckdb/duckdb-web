---
layout: docu
title: Pragmas
selected: Documentation/Pragmas
---
The `PRAGMA` statement is an SQL extension adopted by DuckDB from SQLite. `PRAGMA` statements can be issued in a similar manner to regular SQL statements. `PRAGMA` commands may alter the internal state of the database engine, and can influence the subsequent execution or behavior of the engine.

# List of supported PRAGMA statements
Below is a list of supported `PRAGMA` statements.


### database_list, show_tables, show_tables_expanded, table_info, show, functions
```sql
-- List all databases, usually one
PRAGMA database_list;
-- List all tables
PRAGMA show_tables;
-- List all tables, with extra information, similar to DESCRIBE
PRAGMA show_tables_expanded;
-- Get info for a specific table
PRAGMA table_info('table_name');
CALL pragma_table_info('table_name');
-- Also show table structure, but slightly different format (for compatibility)
PRAGMA show('table_name');
-- List all functions
PRAGMA functions;
```

`table_info` returns information about the columns of the table with name *table_name*. The exact format of the table returned is given below:

```sql
cid INTEGER,        -- cid of the column
name VARCHAR,       -- name of the column
type VARCHAR,       -- type of the column
notnull BOOLEAN,    -- if the column is marked as NOT NULL
dflt_value VARCHAR, -- default value of the column, or NULL if not specified
pk BOOLEAN          -- part of the primary key or not
```

### memory_limit, threads
```sql
-- set the memory limit
PRAGMA memory_limit='1GB';
-- set the amount of threads for parallel query execution
PRAGMA threads=4;
```

### database_size
```sql
-- get the file and memory size of each database
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

### collations, default_collation
```sql
-- list all available collations
PRAGMA collations;
-- set the default collation to one of the available ones
PRAGMA default_collation='nocase';
```


### default_null_order, default_order
```sql
-- set the ordering for NULLs to be either NULLS FIRST or NULLS LAST
PRAGMA default_null_order='NULLS LAST';
-- set the default result set ordering direction to ASCENDING or DESCENDING
PRAGMA default_order='DESCENDING';
```

### version
```sql
-- show DuckDB version
PRAGMA version;
CALL pragma_version();
```

### platform
`platform` returns an identifier for the platform the current DuckDB executable has been compiled for.
This matches the platform_name as described [on the extension loading explainer](../extensions/overview#downloading-extensions-directly-from-s3).
```sql
-- show platform of current DuckDB executable
PRAGMA platform;
CALL pragma_platform();
```

### enable_progress_bar, disable_progress_bar, enable_profiling, disable_profiling, profiling_output
```sql
-- Show progress bar when running queries
PRAGMA enable_progress_bar;
-- Don't show a progress bar for running queries
PRAGMA disable_progress_bar;
-- Enable profiling
PRAGMA enable_profiling;
-- Enable profiling in a specified format
PRAGMA enable_profiling=[json, query_tree, query_tree_optimizer]
-- Disable profiling
PRAGMA disable_profiling;
-- Specify a file to save the profiling output to
PRAGMA profiling_output='/path/to/file.json';
PRAGMA profile_output='/path/to/file.json';
```

Enable the gathering and printing of profiling information after the execution of a query. Optionally, the format of the resulting profiling information can be specified as either *json*, *query_tree*, or *query_tree_optimizer*. The default format is *query_tree*, which prints the physical operator tree together with the timings and cardinalities of each operator in the tree to the screen.

Below is an example output of the profiling information for the simple query ```SELECT 42```:

```
┌─────────────────────────────────────┐
│┌───────────────────────────────────┐│
││    Query Profiling Information    ││
│└───────────────────────────────────┘│
└─────────────────────────────────────┘
SELECT 42;
┌─────────────────────────────────────┐
│┌───────────────────────────────────┐│
││        Total Time: 0.0001s        ││
│└───────────────────────────────────┘│
└─────────────────────────────────────┘
┌───────────────────────────┐
│         PROJECTION        │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             42            │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             1             │
│          (0.00s)          │
└─────────────┬─────────────┘
┌─────────────┴─────────────┐
│         DUMMY_SCAN        │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│             1             │
│          (0.00s)          │
└───────────────────────────┘
```

The printing of profiling information can be disabled again using *disable_profiling*.

By default, profiling information is printed to the console. However, if you prefer to write the profiling information to a file the `PRAGMA` **profiling_output** can be used to write to a specified file. **Note that the file contents will be overwritten for every new query that is issued, hence the file will only contain the profiling information of the last query that is run.**

### disable_optimizer, enable_optimizer
```sql
-- disables the query optimizer
PRAGMA disable_optimizer;
-- enables the query optimizer
PRAGMA enable_optimizer;
```

### log_query_path, explain_output, enable_verification, disable_verification, verify_parallelism, disable_verify_parallelism
```sql
-- Set a path for query logging
PRAGMA log_query_path='/tmp/duckdb_log/';
-- Disable query logging again
PRAGMA log_query_path='';
-- either show 'all' or only 'optimized' plans in the EXPLAIN output
PRAGMA explain_output='optimized';
-- Enable query verification (for development)
PRAGMA enable_verification;
-- Disable query verification (for development)
PRAGMA disable_verification;
-- Enable force parallel query processing (for development)
PRAGMA verify_parallelism;
-- Disable force parallel query processing (for development)
PRAGMA disable_verify_parallelism;
-- Force index joins where applicable
PRAGMA force_index_join;
```

These are `PRAGMA`s mostly used for development and internal testing.

### create_fts_index, drop_fts_index
Only available when the FTS extension is built, [documented here](../extensions/full_text_search).

### verify_external, disable_verify_external
```sql
-- Enable verification of external operators
PRAGMA verify_external;
-- Disable verification of external operators
PRAGMA disable_verify_external;
```

### verify_serializer, disable_verify_serializer
```sql
-- Enable verification of round-trip capabilities for supported Logical Plans
PRAGMA verify_serializer;
-- Disable verification of round-trip capabilities
PRAGMA disable_verify_serializer;
```

### enable_object_cache, disable_object_cache
```sql
-- Enable caching of objects for e.g. Parquet metadata
PRAGMA enable_object_cache;
-- Disable caching of objects
PRAGMA disable_object_cache;
```

### force_checkpoint
```sql
-- When CHECKPOINT is called when no changes are made, force a CHECKPOINT regardless.
PRAGMA force_checkpoint;
```

### enable_print_progress_bar, disable_print_progress_bar
```sql
-- Enable printing of the progress bar, if it's enabled
PRAGMA enable_print_progress_bar;
-- Disable printing of the progress bar
PRAGMA disable_print_progress_bar;
```

### enable_checkpoint_on_shutdown, disable_checkpoint_on_shutdown
```sql
-- Run a CHECKPOINT on successful shutdown and delete the WAL, to leave only a single database file behind
PRAGMA enable_checkpoint_on_shutdown;
-- Don't run a CHECKPOINT on shutdown
PRAGMA disable_checkpoint_on_shutdown;
```

### temp directory for spilling data to disk -- defaults to .tmp
```sql
PRAGMA temp_directory='/path/to/temp.tmp'
```

### storage_info

```sql
PRAGMA storage_info('table_name');
CALL pragma_storage_info('table_name');
```

returns the following, per column in the given table

| name           | type      | description                                           |
|----------------|-----------|-------------------------------------------------------|
| `row_group_id` | `BIGINT`  ||
| `column_name`  | `VARCHAR` ||
| `column_id`    | `BIGINT`  ||
| `column_path`  | `VARCHAR` ||
| `segment_id`   | `BIGINT`  ||
| `segment_type` | `VARCHAR` ||
| `start`        | `BIGINT`  | The start row id of this chunk                        |
| `count`        | `BIGINT`  | The amount of entries in this storage chunk           |
| `compression`  | `VARCHAR` | Compression type used for this column - see blog post |
| `stats`        | `VARCHAR` ||
| `has_updates`  | `BOOLEAN` ||
| `persistent`   | `BOOLEAN` | false if temporary table                              |
| `block_id`     | `BIGINT`  | empty unless persistent                               |
| `block_offset` | `BIGINT`  | empty unless persistent                               |

See [Storage](/internals/storage) for more information.
