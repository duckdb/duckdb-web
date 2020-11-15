---
layout: docu
title: Pragmas
selected: Documentation/Pragmas
---
The PRAGMA statement is an SQL extension adopted by DuckDB from SQLite. PRAGMA statements can be issued in a similar manner to regular SQL statements. PRAGMA commands may alter the internal state of the database engine, and can influence the subsequent execution or behavior of the engine.

# List of supported PRAGMA statements
Below is a list of supported PRAGMA statements.


### database_list, show_tables, table_info, show
```sql
-- list all databases, usually one
PRAGMA database_list;
-- list all tables
PRAGMA show_tables;
-- get info for a specific table
PRAGMA table_info('table_name');
-- also show table structure, but slightly different format (for compatibility)
PRAGMA show('table_name');

```

`table_info` returns information about the columns of the table with name *table_name*. The exact format of the table returned is given below:

```sql
cid INTEGER,        -- cid of the column
name VARCHAR,       -- name fo the column
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
```
Note that this version currently shows the git short hash and not the release version (1.2.3 etc).

### enable_profiling, disable_profiling, profiling_output
```sql
-- enable profiling
PRAGMA enable_profiling;
-- enable profiling in a specified format
PRAGMA enable_profiling=[json, query_tree]
-- disable profiling
PRAGMA disable_profiling;
-- specifies a directory to save the profiling output to
PRAGMA profiling_output=/path/to/directory;
```

Enable the gathering and printing of profiling information after the execution of a query. Optionally, the format of the resulting profiling information can be specified as either *json* or *query_tree*. The default format is *query_tree*, which prints the physical operator tree together with the timings and cardinalities of each operator in the tree to the screen.

Below is an example output of the profiling information for the simple query ```SELECT 42```:

```
<<Query Profiling Information>>
SELECT 42;
<<Operator Tree>>
--------------------
|    PROJECTION    |
|        42        |
|      (0.00s)     |
|         1        |
--------------------
--------------------
|    DUMMY_SCAN    |
|      (0.00s)     |
|         1        |
--------------------
```

The printing of profiling information can be disabled again using *disable_profiling*.

By default, profiling information is printed to the console. However, if you prefer to write the profiling information to a file the pragma **profiling_output** can be used to write to a specified file. **Note that the file contents will be overwritten for every new query that is issued, hence the file will only contain the profiling information of the last query that is run.**


### log_query_path, explain_output, enable_verification, disable_verification, force_parallelism, disable_force_parallelism
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
PRAGMA force_parallelism;
-- Disable force parallel query processing (for development)
PRAGMA disable_force_parallelism;
-- Force index joins where applicable
PRAGMA force_index_join;
```

These are PRAGMAs mostly used for development and internal testing.
