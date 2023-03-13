---
layout: docu
title: Configuration
selected: Documentation/Configuration
---
DuckDB has a number of configuration options that can be used to change the behavior of the system.  
The configuration options can be set using either the `SET` statement or the `PRAGMA` statement.
They can also be reset to their original values using the `RESET` statement.

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

-- return the current value of a specific setting
-- this example returns 'automatic'
SELECT current_setting('access_mode');

-- reset the memory limit of the system back to the default
RESET memory_limit;
```

## **Configuration Reference**

Below is a list of all available settings.

|                   name                   |                                                                       description                                                                       | input_type |  default_value   |
|------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|------------|------------------|
| Calendar                                 | The current calendar                                                                                                                                    | VARCHAR    | GREGORIAN        |
| TimeZone                                 | The current time zone                                                                                                                                   | VARCHAR    | System timezone  |
| access_mode                              | Access mode of the database (**AUTOMATIC**, **READ_ONLY** or **READ_WRITE**)                                                                            | VARCHAR    | AUTOMATIC        |
| allow_unsigned_extensions                | Allow to load extensions with invalid or missing signatures                                                                                             | BOOLEAN    | FALSE            |
| binary_as_string                         | In Parquet files, interpret binary data as a string.                                                                                                    | BOOLEAN    |                  |
| checkpoint_threshold, wal_autocheckpoint | The WAL size threshold at which to automatically trigger a checkpoint (e.g. 1GB)                                                                        | VARCHAR    | 16.7MB           |
| custom_extension_repository              | Overrides the custom endpoint for remote extension installation                                                                                         | VARCHAR    |                  |
| default_collation                        | The collation setting used when none is specified                                                                                                       | VARCHAR    |                  |
| default_null_order, null_order           | Null ordering used when none is specified (**NULLS_FIRST** or **NULLS_LAST**)                                                                           | VARCHAR    | NULLS_FIRST      |
| default_order                            | The order type used when none is specified (**ASC** or **DESC**)                                                                                        | VARCHAR    | ASC              |
| enable_external_access                   | Allow the database to access external state (through e.g. loading/installing modules, COPY TO/FROM, CSV readers, pandas replacement scans, etc)         | BOOLEAN    | TRUE             |
| enable_fsst_vectors                      | Allow scans on FSST compressed segments to emit compressed vectors to utilize late decompression                                                        | BOOLEAN    | FALSE            |
| enable_http_metadata_cache               | Whether or not the global http metadata is used to cache HTTP metadata                                                                                  | BOOLEAN    | FALSE            |
| enable_object_cache                      | Whether or not object cache is used to cache e.g. Parquet metadata                                                                                      | BOOLEAN    | FALSE            |
| enable_profiling                         | Enables profiling, and sets the output format (**JSON**, **QUERY_TREE**, **QUERY_TREE_OPTIMIZER**)                                                      | VARCHAR    | NULL             |
| enable_progress_bar                      | Enables the progress bar, printing progress to the terminal for long queries                                                                            | BOOLEAN    | FALSE            |
| enable_progress_bar_print                | Controls the printing of the progress bar, when 'enable_progress_bar' is true                                                                           | BOOLEAN    | TRUE             |
| experimental_parallel_csv                | Whether or not to use the experimental parallel CSV reader                                                                                              | BOOLEAN    | 0                |
| explain_output                           | Output of EXPLAIN statements (**ALL**, **OPTIMIZED_ONLY**, **PHYSICAL_ONLY**)                                                                           | VARCHAR    | PHYSICAL_ONLY    |
| extension_directory                      | Set the directory to store extensions in                                                                                                                | VARCHAR    |                  |
| external_threads                         | The number of external threads that work on DuckDB tasks.                                                                                               | BIGINT     | 0                |
| file_search_path                         | A comma separated list of directories to search for input files                                                                                         | VARCHAR    |                  |
| force_download                           | Forces upfront download of file                                                                                                                         | BOOLEAN    | 0                |
| home_directory                           | Sets the home directory used by the system                                                                                                              | VARCHAR    |                  |
| http_retries                             | HTTP retries on I/O error (default 3)                                                                                                                   | UBIGINT    | 3                |
| http_retry_backoff                       | Backoff factor for exponentially increasing retry wait time (default 4)                                                                                 | FLOAT      | 4                |
| http_retry_wait_ms                       | Time between retries (default 100ms)                                                                                                                    | UBIGINT    | 100              |
| http_timeout                             | HTTP timeout read/write/connection/retry (default 30000ms)                                                                                              | UBIGINT    | 30000            |
| immediate_transaction_mode               | Whether transactions should be started lazily when needed, or immediately when BEGIN TRANSACTION is called                                              | BOOLEAN    | FALSE            |
| log_query_path                           | Specifies the path to which queries should be logged (default: empty string, queries are not logged)                                                    | VARCHAR    | NULL             |
| max_expression_depth                     | The maximum expression depth limit in the parser. WARNING: increasing this setting and using very deep expressions might lead to stack overflow errors. | UBIGINT    | 1000             |
| max_memory, memory_limit                 | The maximum memory of the system (e.g. 1GB)                                                                                                             | VARCHAR    | 75% of RAM       |
| password                                 | The password to use. Ignored for legacy compatibility.                                                                                                  | VARCHAR    | NULL             |
| perfect_ht_threshold                     | Threshold in bytes for when to use a perfect hash table (default: 12)                                                                                   | BIGINT     | 12               |
| preserve_identifier_case                 | Whether or not to preserve the identifier case, instead of always lowercasing all non-quoted identifiers                                                | BOOLEAN    | TRUE             |
| preserve_insertion_order                 | Whether or not to preserve insertion order. If set to false the system is allowed to re-order any results that do not contain ORDER BY clauses.         | BOOLEAN    | TRUE             |
| profile_output, profiling_output         | The file to which profile output should be saved, or empty to print to the terminal                                                                     | VARCHAR    |                  |
| profiler_history_size                    | Sets the profiler history size                                                                                                                          | BIGINT     | NULL             |
| profiling_mode                           | The profiling mode (**STANDARD** or **DETAILED**)                                                                                                       | VARCHAR    | NULL             |
| progress_bar_time                        | Sets the time (in milliseconds) how long a query needs to take before we start printing a progress bar                                                  | BIGINT     | 2000             |
| s3_access_key_id                         | S3 Access Key ID                                                                                                                                        | VARCHAR    |                  |
| s3_endpoint                              | S3 Endpoint (default 's3.amazonaws.com')                                                                                                                | VARCHAR    | S3.AMAZONAWS.COM |
| s3_region                                | S3 Region                                                                                                                                               | VARCHAR    |                  |
| s3_secret_access_key                     | S3 Access Key                                                                                                                                           | VARCHAR    |                  |
| s3_session_token                         | S3 Session Token                                                                                                                                        | VARCHAR    |                  |
| s3_uploader_max_filesize                 | S3 Uploader max filesize (between 50GB and 5TB, default 800GB)                                                                                          | VARCHAR    | 800GB            |
| s3_uploader_max_parts_per_file           | S3 Uploader max parts per file (between 1 and 10000, default 10000)                                                                                     | UBIGINT    | 10000            |
| s3_uploader_thread_limit                 | S3 Uploader global thread limit (default 50)                                                                                                            | UBIGINT    | 50               |
| s3_url_compatibility_mode                | Disable Globs and Query Parameters on S3 urls                                                                                                           | BOOLEAN    | 0                |
| s3_url_style                             | S3 url style ('vhost' (default) or 'path')                                                                                                              | VARCHAR    | VHOST            |
| s3_use_ssl                               | S3 use SSL (default true)                                                                                                                               | BOOLEAN    | 1                |
| schema                                   | Sets the default search schema. Equivalent to setting search_path to a single value.                                                                    | VARCHAR    | MAIN             |
| search_path                              | Sets the default search search path as a comma-separated list of values                                                                                 | VARCHAR    |                  |
| temp_directory                           | Set the directory to which to write temp files                                                                                                          | VARCHAR    |                  |
| threads, worker_threads                  | The number of total threads used by the system.                                                                                                         | BIGINT     | # Cores          |
| username, user                           | The username to use. Ignored for legacy compatibility.                                                                                                  | VARCHAR    | NULL             |
