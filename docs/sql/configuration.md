---
layout: docu
title: Configuration
selected: Documentation/Configuration
---
DuckDB has a number of configuration options that can be used to change the behavior of the system. The configuration options can be set using either the `SET` statement or the `PRAGMA` statement.

### Examples
```sql
-- set the memory limit of the system to 10GB
SET memory_limit='10GB';
-- configure the system to use 1 thread
SET threads TO 1;
-- enable printing of a progress bar during long-running queries
SET enable_progress_bar=true;
-- set the default null order to NULLS LAST
PRAGMA default_null_order='nulls_last';

-- show a list of all available settings
SELECT * FROM duckdb_settings();
```

## **Configuration Reference**

Below is a list of all available settings.

|                   name                   |                                                                   description                                                                   | input_type | default_value |
|------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|------------|---------------|
| access_mode                              | Access mode of the database (**AUTOMATIC**, **READ_ONLY** or **READ_WRITE**)                                                                    | VARCHAR    | AUTOMATIC     |
| checkpoint_threshold, wal_autocheckpoint | The WAL size threshold at which to automatically trigger a checkpoint (e.g. 1GB)                                                                | VARCHAR    | 16.7MB        |
| default_collation                        | The collation setting used when none is specified                                                                                               | VARCHAR    |               |
| default_null_order, null_order           | Null ordering used when none is specified (**NULLS_FIRST** or **NULLS_LAST**)                                                                   | VARCHAR    | NULLS_FIRST   |
| default_order                            | The order type used when none is specified (**ASC** or **DESC**)                                                                                | VARCHAR    | ASC           |
| enable_external_access                   | Allow the database to access external state (through e.g. loading/installing modules, COPY TO/FROM, CSV readers, pandas replacement scans, etc) | BOOLEAN    | TRUE          |
| enable_object_cache                      | Whether or not object cache is used to cache e.g. Parquet metadata                                                                              | BOOLEAN    | FALSE         |
| enable_profiling                         | Enables profiling, and sets the output format (**JSON**, **QUERY_TREE**, **QUERY_TREE_OPTIMIZER**)                                              | VARCHAR    | NONE          |
| enable_progress_bar                      | Enables the progress bar, printing progress to the terminal for long queries                                                                    | BOOLEAN    | FALSE         |
| explain_output                           | Output of EXPLAIN statements (**ALL**, **OPTIMIZED_ONLY**, **PHYSICAL_ONLY**)                                                                   | VARCHAR    | PHYSICAL_ONLY |
| log_query_path                           | Specifies the path to which queries should be logged (default: empty string, queries are not logged)                                            | VARCHAR    | NULL          |
| max_memory, memory_limit                 | The maximum memory of the system (e.g. 1GB)                                                                                                     | VARCHAR    | 75% of RAM    |
| perfect_ht_threshold                     | Threshold in bytes for when to use a perfect hash table (default: 12)                                                                           | BIGINT     | 12            |
| profile_output, profiling_output         | The file to which profile output should be saved, or empty to print to the terminal                                                             | VARCHAR    |               |
| profiler_history_size                    | Sets the profiler history size                                                                                                                  | BIGINT     | NULL          |
| profiling_mode                           | The profiling mode (**STANDARD** or **DETAILED**)                                                                                               | VARCHAR    | STANDARD      |
| progress_bar_time                        | Sets the time (in milliseconds) how long a query needs to take before we start printing a progress bar                                          | BIGINT     | 2000          |
| s3_access_key_id                         | S3 Access Key ID                                                                                                                                | VARCHAR    |               |
| s3_endpoint                              | S3 Endpoint (default s3.amazonaws.com)                                                                                                          | VARCHAR    |               |
| s3_region                                | S3 Region                                                                                                                                       | VARCHAR    |               |
| s3_secret_access_key                     | S3 Access Key                                                                                                                                   | VARCHAR    |               |
| s3_session_token                         | S3 Session Token                                                                                                                                | VARCHAR    |               |
| schema                                   | Sets the default search schema. Equivalent to setting search_path to a single value.                                                            | VARCHAR    |               |
| search_path                              | Sets the default search search path as a comma-separated list of values                                                                         | VARCHAR    |               |
| temp_directory                           | Set the directory to which to write temp files                                                                                                  | VARCHAR    |               |
| threads, worker_threads                  | The number of total threads used by the system.                                                                                                 | BIGINT     | # Cores       |
