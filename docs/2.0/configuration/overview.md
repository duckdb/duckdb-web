---
layout: docu
redirect_from:
- /docs/configuration
- /docs/configuration/overview
- /docs/sql/configuration
- /docs/stable/configuration/overview
- /docs/current/configuration/overview
- /docs/lts/configuration/overview
- /docs/preview/configuration/overview
title: Configuration
---

DuckDB has a number of configuration options that can be used to change the behavior of the system.

The configuration options can be set using either the [`SET` statement]({% link docs/2.0/sql/statements/set.md %}) or the [`PRAGMA` statement]({% link docs/2.0/configuration/pragmas.md %}).
They can be reset to their original values using the [`RESET` statement]({% link docs/2.0/sql/statements/set.md %}#reset).

The values of configuration options can be queried via the [`current_setting()` scalar function]({% link docs/2.0/sql/functions/utility.md %}) or using the [`duckdb_settings()` table function]({% link docs/2.0/sql/meta/duckdb_table_functions.md %}#duckdb_settings). For example:

```sql
SELECT current_setting('memory_limit') AS memlimit;
```

Or:

```sql
SELECT value AS memlimit
FROM duckdb_settings()
WHERE name = 'memory_limit';
```

## Examples

Set the memory limit of the system to 10 GB.

```sql
SET memory_limit = '10GB';
```

Configure the system to use 1 thread.

```sql
SET threads TO 1;
```

Turn logging on and set the logging level to `debug`.
For additional details on logging levels, see [Log Level]({% link docs/2.0/operations_manual/logging/overview.md %}#log-level).

In the CLI client, the default log storage (`shell_log_storage`) prints logs to the console but cannot be queried, so we switch to the `memory` log storage first:

```sql
SET logging_storage = 'memory';
SET enable_logging = true;
SET logging_level = 'debug';
```

Write a single log message with the `debug` level and a `connection` scope:

```sql
SELECT write_log('A new client has connected.', level := 'debug', scope := 'connection');
```

Write a single log message with a `debug` level and a `connection` scope and a custom `log_type`:

```sql
SELECT write_log(
        'A new duck has connected to the lake.', 
        level := 'debug', 
        scope := 'connection', 
        log_type := 'duckdb.docs.example.quack'
    );
```

Check logs with the `DEBUG` log level:

```sql
SELECT * FROM duckdb_logs WHERE log_level = 'DEBUG';
```

Check logs with the `QueryLog` type:

```sql
SELECT * FROM duckdb_logs WHERE type = 'QueryLog';
```

Check current logging settings:

```sql
SELECT * FROM duckdb_settings() WHERE name LIKE '%logging%';
```

Enable printing of a progress bar during long-running queries:

```sql
SET enable_progress_bar = true;
```

Set the default null order to `NULLS LAST`:

```sql
SET default_null_order = 'nulls_last';
```

Return the current value of a specific setting:

```sql
SELECT current_setting('threads') AS threads;
```

| threads |
| ------: |
|      10 |

Query a specific setting:

```sql
SELECT *
FROM duckdb_settings()
WHERE name = 'threads';
```

| name    | value | description                                     | input_type | scope  |
| ------- | ----- | ----------------------------------------------- | ---------- | ------ |
| threads | 1     | The number of total threads used by the system. | BIGINT     | GLOBAL |

Show a list of all available settings:

```sql
SELECT *
FROM duckdb_settings();
```

Reset the memory limit of the system back to the default:

```sql
RESET memory_limit;
```

## Secrets Manager

DuckDB has a [Secrets manager]({% link docs/2.0/sql/statements/create_secret.md %}), which provides a unified user interface for secrets across all backends (e.g., AWS S3) that use them.

## Schema and Search Path

The `schema` and `search_path` configuration options both control the *search path*: the ordered list of schemas that DuckDB consults to resolve unqualified table, view, and function names. Despite the difference in their descriptions, both options operate on this same search path:

* `search_path` sets the entire search path as a comma-separated list of entries.
* `schema` is a convenience option that sets the search path to a single entry.

Each entry in the search path is a schema. An entry may be qualified with a catalog (attached database) name in the form `⟨catalog⟩.⟨schema⟩` to select a schema in a specific database; an unqualified entry refers to a schema in the current catalog. This is why the descriptions mention both schemas and catalogs: the path is a list of schemas, whose entries may optionally be catalog-qualified.

## Asynchronous I/O Settings

> New Asynchronous I/O, along with the settings that tune it, was introduced in DuckDB 2.0.

The `async_threads` and `read_ahead_depth` settings control the size of the asynchronous thread pool and the read-ahead budget used when reading from object storage and HTTP servers. They are listed in the [reference below](#configuration-reference) and documented in more detail on the [I/O page]({% link docs/2.0/data/io.md %}), together with the related `http_client_pool_capacity` setting.

## Configuration Reference

<!-- This section is generated by scripts/generate_config_docs.py -->

Configuration options come with different default [scopes]({% link docs/2.0/sql/statements/set.md %}#scopes): `GLOBAL` and `LOCAL`. Below is a list of all available configuration options by scope.

### Global Configuration Options

| Name | Description | Type | Default value |
|----|--------|--|---|
| `Calendar` | The current calendar | `VARCHAR` | System (locale) calendar |
| `TimeZone` | The current time zone | `VARCHAR` | System (locale) timezone |
| `access_mode` | Access mode of the database (`AUTOMATIC`, `READ_ONLY` or `READ_WRITE`). | `VARCHAR` | `automatic` |
| `allocator_background_threads` | Whether to enable the allocator background threads. | `BOOLEAN` | `false` |
| `allocator_bulk_deallocation_flush_threshold` | If a bulk deallocation larger than this occurs, flush outstanding allocations. | `VARCHAR` | `512.0 MiB` |
| `allocator_flush_threshold` | Peak allocation threshold at which to flush the allocator after completing a task. | `VARCHAR` | `134217728B` |
| `allow_asterisks_in_http_paths` | Allow '*' character in URLs users can query | `BOOLEAN` | `false` |
| `allow_community_extensions` | Allow loading extensions build by the community. | `BOOLEAN` | `true` |
| `allow_extension_repositories` | Whether custom trusted extension repositories are 'allowed', 'forbidden' (which also distrusts existing repositories) or 'undecided' (the default: blocks adding new repositories, but keeps trusting existing ones). While the database is running the setting can only move from 'undecided' to 'allowed' or 'forbidden', or from 'allowed' to 'forbidden'. | `VARCHAR` | `undecided` |
| `allow_extensions_metadata_mismatch` | Allow to load extensions with no compatible metadata. | `BOOLEAN` | `false` |
| `allow_parser_override_extension` | Allow extensions to override the current parser. | `VARCHAR` | `DEFAULT` |
| `allow_persistent_secrets` | Allow the creation of persistent secrets that are stored and loaded on restarts. | `BOOLEAN` | `true` |
| `allow_unredacted_secrets` | Allow printing unredacted secrets. | `BOOLEAN` | `false` |
| `allow_unsigned_extensions` | Allow to load extensions with invalid or missing signatures. | `BOOLEAN` | `false` |
| `allowed_configs` | List of configuration options that are ALWAYS allowed to be changed, even when lock_configuration is true. | `VARCHAR[]` | `[]` |
| `allowed_directories` | List of directories, and directory prefixes, that are ALWAYS allowed to be queried, even when enable_external_access is false. | `VARCHAR[]` | `[]` |
| `allowed_paths` | List of files that are ALWAYS allowed to be queried, even when enable_external_access is false. | `VARCHAR[]` | `[]` |
| `approximate_join_order_threshold` | The minimum number of tables in a join to determine the optimal join order approximately instead of exactly. | `UBIGINT` | `12` |
| `arrow_large_buffer_size` | Whether Arrow buffers for strings, blobs, UUIDs and bits should be exported using large buffers. | `BOOLEAN` | `false` |
| `arrow_lossless_conversion` | Whenever a DuckDB type does not have a clear native or canonical extension match in Arrow, export the types with a duckdb.type_name extension name. | `BOOLEAN` | `false` |
| `arrow_output_list_view` | Whether the export to the Arrow format should use ListView as the physical layout for LIST columns. | `BOOLEAN` | `false` |
| `arrow_output_version` | Whether strings should be produced by DuckDB in Utf8View format instead of Utf8. | `VARCHAR` | `1.0` |
| `asof_loop_join_threshold` | The maximum number of rows we need on the left side of an ASOF join to use a nested loop join. | `UBIGINT` | `64` |
| `async_threads` | The number of total async threads used by the system for tasks like I/O. | `BIGINT` | 4 × # CPU cores (max. 256) |
| `auto_checkpoint_skip_wal_threshold` | The estimated WAL write size at which point we will skip writing to the WAL and only checkpoint. Skipping writing to the WAL means concurrent commits are blocked while the checkpoint is happening. | `UBIGINT` | `100000` |
| `auto_fallback_to_full_download` | Allows automatically falling back to full file downloads when possible. | `BOOLEAN` | `true` |
| `autoinstall_extension_repository` | Overrides the custom endpoint for extension installation on autoloading. Falls back to custom_extension_repository, if not specified. | `VARCHAR` |  |
| `autoinstall_known_extensions` | Whether known extensions are allowed to be automatically installed when a query depends on them. | `BOOLEAN` | `true` |
| `autoload_known_extensions` | Whether known extensions are allowed to be automatically loaded when a query depends on them. | `BOOLEAN` | `true` |
| `binary_as_string` | In Parquet files, interpret binary data as a string. | `BOOLEAN` | `false` |
| `block_allocator_memory` | Physical memory that the block allocator is allowed to use. This memory is allocated once, never freed, and cannot be reduced. | `VARCHAR` | `0 bytes` |
| `ca_cert_file` | Path to a custom certificate file for self-signed certificates. | `VARCHAR` |  |
| `cache_local_files` | Whether the external file cache also caches local files. Remote files are always cached. | `BOOLEAN` | `false` |
| `catalog_error_max_schemas` | The maximum number of schemas in the catalog that the system will scan to generate the "did you mean..." error message. | `UBIGINT` | `100` |
| `checkpoint_on_detach` | Override checkpoint behavior when detaching a database. ENABLED requests a checkpoint, but the checkpoint does not occur if another connection still references the database. DISABLED never checkpoints, DEFAULT defers to the global checkpoint_on_shutdown setting. | `VARCHAR` | `DEFAULT` |
| `checkpoint_threshold`, `wal_autocheckpoint` | The WAL size threshold at which to automatically trigger a checkpoint, e.g., 1GB. | `VARCHAR` | `16.0 MiB` |
| `current_transaction_invalidation_policy` | Which types of exceptions invalidate the database for the current transaction. | `VARCHAR` | `STANDARD_POLICY` |
| `custom_extension_repository` | Overrides the custom endpoint for extension installation. | `VARCHAR` |  |
| `custom_user_agent` | HTTP request metadata that can be set by callers/wrappers to tag their own traffic when DuckDB makes a request. | `VARCHAR` |  |
| `default_block_size` | The default block size for new duckdb database files. New means that the file is being created and does not yet exist. | `UBIGINT` | `262144` |
| `default_collation` | The collation setting used when none is specified. | `VARCHAR` |  |
| `default_null_order`, `null_order` | The NULL ordering used when none is specified (`NULLS_FIRST` or `NULLS_LAST`). | `VARCHAR` | `NULLS_LAST` |
| `default_order` | The order type used when none is specified (`ASC` or `DESC`). | `VARCHAR` | `ASCENDING` |
| `default_secret_storage` | Allows switching the default storage for secrets. | `VARCHAR` | `local_file` |
| `default_transaction_invalidation_policy` | When to invalidate transactions when errors occur. SYNTACTIC_ERRORS_DO_NOT_INVALIDATE means that parser and binder exceptions do not invalidate. `ALL`_ERRORS_INVALIDATE_TRANSACTION means all errors invalidate a transaction. | `VARCHAR` | `ALL_ERRORS_INVALIDATE_TRANSACTION` |
| `delim_join_as_cte` | Rewrite delim joins to materialized CTEs during dependent join flattening. | `BOOLEAN` | `true` |
| `dialect_compatibility_mode` | Enable SQL dialect compatibility for a certain engine, e.g., `SET dialect_compatibility_mode='spark'`. | `VARCHAR` | `NONE` |
| `disable_database_invalidation` | Disables invalidating the database instance when encountering a fatal error. Should be used with great care, as DuckDB cannot guarantee correct behavior after a fatal error. | `BOOLEAN` | `false` |
| `disable_parquet_prefetching` | Disable the prefetching mechanism in Parquet | `BOOLEAN` | `false` |
| `disable_timestamptz_casts` | Disable casting from timestamp to timestamptz. | `BOOLEAN` | `false` |
| `disabled_compression_methods` | Disable a specific, comma-separated set of compression methods. | `VARCHAR` |  |
| `disabled_filesystems` | Disable specific file systems, thereby preventing their access, e.g., LocalFileSystem. | `VARCHAR` |  |
| `disabled_log_types` | Sets the list of disabled log types. | `VARCHAR` |  |
| `disabled_optimizers` | Disable a specific, comma-separated set of optimizers. | `VARCHAR` |  |
| `duckdb_api` | Specifies which client API/binding opened the database connection, e.g., cpp, capi, cli. The value gets folded into the HTTP User-Agent string DuckDB sends on any HTTP request. | `VARCHAR` | `cli` |
| `dynamic_or_filter_threshold` | The maximum amount of OR filters that are generated dynamically from a hash join. | `UBIGINT` | `50` |
| `enable_external_access` | Allow the database to access external state, e.g., through loading/installing modules, COPY TO/FROM, CSV readers, pandas replacement scans, etc. | `BOOLEAN` | `true` |
| `enable_external_file_cache` | Allow the database to cache external files like Parquet in memory. | `BOOLEAN` | `true` |
| `enable_fsst_vectors` | Allow scans on FSST compressed segments to emit compressed vectors to utilize late decompression. | `BOOLEAN` | `false` |
| `enable_geoparquet_conversion` | Attempt to decode/encode geometry data in/as GeoParquet files if the spatial extension is present. | `BOOLEAN` | `true` |
| `enable_global_s3_configuration` | Automatically fetch AWS credentials from environment variables. | `BOOLEAN` | `true` |
| `enable_http_metadata_cache` | Whether or not the global http metadata is used to cache HTTP metadata. | `BOOLEAN` | `false` |
| `enable_logging` | Enables the logger. | `BOOLEAN` | `false` (`true` in the CLI) |
| `enable_macro_dependencies` | Enables created MACROs to create dependencies on the referenced objects, such as tables. | `BOOLEAN` | `false` |
| `enable_optimistic_write` | Whether or not to optimistically write large appends to disk before committing. Disable this to keep bulk appends in memory, e.g., for in-memory benchmarks. | `BOOLEAN` | `true` |
| `enable_optimizer` | Whether the query optimizer is enabled. | `BOOLEAN` | `true` |
| `enable_server_cert_verification` | Enable server side certificate verification. | `BOOLEAN` | `false` |
| `enable_view_dependencies` | Enable created VIEWs to create dependencies on the referenced objects, such as tables. | `BOOLEAN` | `false` |
| `enabled_log_types` | Sets the list of enabled log types. | `VARCHAR` |  |
| `error_on_division_by_zero` | Throw an error instead of returning NULL when dividing by zero. | `BOOLEAN` | `true` |
| `errors_as_json` | Output error messages as structured `JSON` instead of as a raw string. | `BOOLEAN` | `false` |
| `experimental_metadata_reuse` | EXPERIMENTAL: Re-use row group and table metadata when checkpointing. | `BOOLEAN` | `true` |
| `explain_output` | Configure the output of EXPLAIN statements (`ALL`, `OPTIMIZED_ONLY`, `PHYSICAL_ONLY`). | `VARCHAR` | `PHYSICAL_ONLY` |
| `extension_directories` | Set the directories to store extensions in. | `VARCHAR[]` | `[]` |
| `extension_repository_directory` | Set the directory in which trusted extension repositories are stored. This is the trust anchor for user-provided repositories, so while signature checking is enabled (allow_unsigned_extensions=false) it can only be set at startup, not while the database is running. | `VARCHAR` |  |
| `external_file_cache_local_max_block_size` | Maximum size in bytes of an external file cache block for local (non-remote) files. Larger reads are split into blocks of this size, which are fetched in parallel. | `UBIGINT` | `16384` |
| `external_file_cache_remote_max_block_size` | Maximum size in bytes of an external file cache block for remote files (e.g., HTTP/S3). Larger reads are split into blocks of this size, which are fetched in parallel. | `UBIGINT` | `2097152` |
| `external_file_cache_remote_min_block_size` | Reads of remote files are rounded out to aligned blocks of this size, so tiny reads do not each cost a request. | `UBIGINT` | `4096` |
| `external_file_cache_request_sizing` | How reads of cached files are sized: AUTO lets each reader choose, GRID reads the aligned blocks of the cache block size around each read, EXACT reads exactly the requested bytes. Reads of files that are not cached are always exact. | `VARCHAR` | `AUTO` |
| `external_file_cache_spill` | Whether evicted external file cache blocks of remote files spill to the temporary directory instead of being dropped, so that they are re-read from there rather than re-fetched from the source. | `BOOLEAN` | `false` |
| `external_threads` | The number of external threads that work on DuckDB tasks. | `UBIGINT` | `1` |
| `extra_http_headers` | Extra HTTP headers added to every request | `MAP(VARCHAR, VARCHAR)` | `{}` |
| `file_search_path` | A comma separated list of directories to search for input files. | `VARCHAR` |  |
| `force_column_metadata_reuse` | Force re-use of row group metadata on a column-level when checkpointing on older storage versions 6 and 7. This breaks storage backward-compatibility with older DuckDB versions. | `BOOLEAN` | `false` |
| `force_compression` | Forces the usage of a specific compression method. | `VARCHAR` | `auto` |
| `force_download_threshold` | Forces upfront download of files smaller than the given size in bytes | `UBIGINT` | `0` |
| `force_download` | Forces upfront download of file | `BOOLEAN` | `false` |
| `fsync_mode` | How to synchronize database file changes to stable storage (`STANDARD`, NONE or FULL). NONE may cause database corruption after an operating system or hardware crash. FULL uses fullfsync on macOS. | `VARCHAR` | `STANDARD` |
| `geometry_minimum_shredding_size` | Minimum size of a row group to enable GEOMETRY shredding. Set to -1 to disable shredding entirely. Defaults to 1/4th of a row group. | `BIGINT` | `30000` |
| `home_directory` | Sets the home directory of the database instance. | `VARCHAR` |  |
| `http_client_pool_capacity` | HTTP client pool capacity derived from CPU and async thread counts unless explicitly set | `BIGINT` | Derived automatically (max. 256) |
| `http_keep_alive` | Keep alive connections. Setting this to false can help when running into connection failures | `BOOLEAN` | `true` |
| `http_proxy_password` | The password for the HTTP proxy. | `VARCHAR` |  |
| `http_proxy_username` | The username for the HTTP proxy. | `VARCHAR` |  |
| `http_proxy` | The HTTP proxy host. Defaults to the HTTP_PROXY environment variable. | `VARCHAR` |  |
| `http_retries` | HTTP retries on I/O error | `UBIGINT` | `3` |
| `http_retry_backoff` | Backoff factor for exponentially increasing retry wait time | `FLOAT` | `4.0` |
| `http_retry_wait_ms` | Time between retries | `UBIGINT` | `100` |
| `http_timeout` | HTTP timeout read/write/connection/retry (in seconds) | `UBIGINT` | `30` |
| `httpfs_client_implementation` | Select which HTTP client implementation is used | `VARCHAR` | `default` |
| `httpfs_connection_caching` | Enable connection caching for HTTP requests | `BOOLEAN` | `true` |
| `httpfs_enable_credential_refresh` | Enable credential refresh for HTTPFS S3 secrets | `BOOLEAN` | `true` |
| `ieee_floating_point_ops` | Use IEEE 754 behavior for supported floating point operations, returning NAN/INF instead of errors/NULL. | `BOOLEAN` | `true` |
| `ignore_unknown_crs` | Ignore unknown Coordinate Reference Systems (CRS) when creating geometry types or importing geospatial data. | `BOOLEAN` | `false` |
| `immediate_transaction_mode` | Whether transactions should be started lazily when needed, or immediately when BEGIN TRANSACTION is called. | `BOOLEAN` | `false` |
| `index_scan_max_count` | The maximum index scan count sets a threshold for index scans. If fewer than MAX(index_scan_max_count, index_scan_percentage * total_row_count) rows match, we perform an index scan instead of a table scan. | `UBIGINT` | `2048` |
| `index_scan_percentage` | The index scan percentage sets a threshold for index scans. If fewer than MAX(index_scan_max_count, index_scan_percentage * total_row_count) rows match, we perform an index scan instead of a table scan. | `DOUBLE` | `0.001` |
| `initial_column_segment_size` | The initial memory (in bytes) reserved for the first transient column segment. Must be a power of two. Internally, we subtract the block header size (typically 8 bytes) for segments with or exceeding 1024 bytes. Subsequent segments double in size until reaching the block size. | `UBIGINT` | `2048` |
| `integer_division` | Whether or not the / operator defaults to integer division, or to floating point division. | `BOOLEAN` | `false` |
| `json_geometry_format` | How GEOMETRY values are written to `JSON`: 'wkt' for Well-Known Text, or 'geojson' for Geo`JSON` geometry objects. COPY ... TO ... (FORMAT GEO`JSON`) always writes Geo`JSON` regardless of this setting. | `VARCHAR` | `wkt` |
| `late_materialization_max_rows` | The maximum amount of rows in the LIMIT/SAMPLE operator for which we trigger late materialization. | `UBIGINT` | `50` |
| `legacy_disable_null_type` | When enabled, prevent the NULL type from leaving the binder. This was the default behavior prior to DuckDB v2.0. | `BOOLEAN` | `false` |
| `lock_configuration` | Whether configurations can be altered. | `BOOLEAN` | `false` |
| `log_query_path` | Specifies the path to which queries should be logged. The default is NULL, meaning queries are not logged. | `VARCHAR` |  |
| `logging_level` | Determines which 'severity' of log messages will be logged. | `VARCHAR` | `INFO` (`WARNING` in the CLI) |
| `logging_mode` | Determines which types of log messages are logged. | `VARCHAR` | `LEVEL_ONLY` |
| `logging_storage` | Set the logging storage, options are 'memory', 'stdout', 'file', '<custom>'. | `VARCHAR` | `memory` (`shell_log_storage` in the CLI) |
| `max_execution_time` | The maximum execution time per query in milliseconds (0 = no limit). | `BIGINT` | `0` |
| `max_expression_depth` | The maximum expression depth limit in the parser. WARNING: increasing this setting and using very deep expressions might lead to stack overflow errors. | `UBIGINT` | `1000` |
| `max_memory`, `memory_limit` | The maximum memory of the system (e.g., 1GB). | `VARCHAR` | 80% of RAM |
| `max_temp_directory_size` | The maximum amount of data stored inside the 'temp_directory' (when set) (e.g., 1GB). | `VARCHAR` | `90% of available disk space` |
| `max_vacuum_tasks` | The maximum number of vacuum tasks to schedule during a checkpoint. | `UBIGINT` | `100` |
| `merge_http_secret_into_s3_request` | Merges HTTP secret parameters into S3 requests | `BOOLEAN` | `true` |
| `merge_join_threshold` | The maximum number of rows on either table to choose a merge join. | `UBIGINT` | `1000` |
| `nested_loop_join_threshold` | The maximum number of rows on either table to choose a nested loop join. | `UBIGINT` | `5` |
| `order_by_non_integer_literal` | Allow ordering by non-integer literals. Ordering by such literals has no effect. Enabling this relaxes the check to a silent no-op instead of a binder error. | `BOOLEAN` | `false` |
| `ordered_aggregate_threshold` | The number of rows to accumulate before sorting. | `UBIGINT` | `262144` |
| `parquet_metadata_cache` | Cache Parquet metadata - useful when reading the same files multiple times | `BOOLEAN` | `false` |
| `parquet_prefetch_column_gap` | Byte gap under which Parquet prefetch I/O ranges are coalesced (NULL lets the cost model adapt it) | `UBIGINT` | NULL |
| `partitioned_write_flush_threshold` | The number of rows threshold after which a thread state is flushed when writing using `PARTITION_BY`. | `UBIGINT` | `524288` |
| `partitioned_write_max_open_files` | The maximum amount of files the system can keep open before flushing to disk when writing using `PARTITION_BY`. | `UBIGINT` | `100` |
| `password` | The password to use. Kept for legacy compatibility. | `VARCHAR` |  |
| `perfect_ht_threshold` | Threshold in bytes for when to use a perfect hash table. | `UBIGINT` | `12` |
| `pin_threads` | Whether to pin threads to cores. Linux only, and the default is AUTO. AUTO means the setting is on when there are more than 64 cores. | `VARCHAR` | `auto` |
| `pivot_filter_threshold` | The threshold determining when a dedicated pivot operator switches from using filtered aggregates to LIST. | `UBIGINT` | `20` |
| `pivot_limit` | The maximum number of pivot columns in a pivot statement. | `UBIGINT` | `100000` |
| `prefer_range_joins` | Force the use of range joins with mixed predicates. | `BOOLEAN` | `false` |
| `prefetch_all_parquet_files` | (deprecated) Parquet files are now always prefetched, this setting has no effect | `BOOLEAN` | `false` |
| `preserve_identifier_case` | How to fold non-quoted identifiers. 'preserve_case' keeps the case as written, 'lowercase' lowercases them, 'uppercase' uppercases them. | `VARCHAR` | `preserve_case` |
| `preserve_insertion_order` | Whether or not to preserve insertion order. If set to false, then the system is allowed to re-order any results that do not contain ORDER BY clauses. | `BOOLEAN` | `true` |
| `read_ahead_depth` | The number of scan jobs prefetched ahead of decoding. -1 = automatic, with the backlog being bound by a memory budget, 0 = disabled. | `BIGINT` | `-1` |
| `redact_http_logs` | Redact HTTP header values in logs unless their names are explicitly allowed. | `BOOLEAN` | `true` |
| `regex_match_operator_semantics` | Configures whether regex match operators use partial or full string matching. | `VARCHAR` | `partial` |
| `s3_allow_recursive_globbing` | Whether globs on S3-like storage are optimized with recursive strategy (alternative is listing) | `BOOLEAN` | `true` |
| `s3_enable_deprecated_url_parameters` | Enable deprecated S3 URL parameters. NULL disables them by default; false permanently disables them for this database instance. | `BOOLEAN` | NULL |
| `s3_list_concurrency` | Maximum number of concurrent LIST requests issued while expanding an S3 glob. The window is also bounded by async_threads + 1 and shrinks automatically when the server throttles. | `UBIGINT` | `256` |
| `s3_uploader_max_filesize` | Maximum size of an S3 upload | `VARCHAR` | `80GB` |
| `s3_uploader_max_parts_per_file` | Maximum number of parts in an S3 multipart upload | `UBIGINT` | `10000` |
| `s3_url_scheme_aliases` | Additional URL schemes routed to the S3-compatible filesystem (e.g., ['oss', 'cos']). Can only be set globally; secrets for aliased schemes need an explicit SCOPE. | `VARCHAR[]` | `[]` |
| `s3_version_id_pinning` | Pin S3 reads to a specific object version for consistency | `BOOLEAN` | `false` |
| `scalar_subquery_error_on_multiple_rows` | Deprecated setting. Throw an error when a scalar subquery returns more than one row. This will become the default behavior. When disabled, an arbitrary row is returned instead. | `BOOLEAN` | `true` |
| `scheduler_process_partial` | Partially process tasks before rescheduling. Enabling this allows for more scheduler fairness between separate queries. | `BOOLEAN` | `false` |
| `secret_directory` | Set the directory in which persistent secrets are stored. | `VARCHAR` | `~/.duckdb/stored_secrets` |
| `show_behavior` | Configures how SHOW resolves a bare identifier. 'auto' describes a table if one exists, else it describes a setting (deprecated). 'table' always describes a table, and 'setting' always describes a setting. | `VARCHAR` | `AUTO` |
| `standard_vector_size` | The compiled-in `STANDARD`_VECTOR_SIZE (read-only). | `UBIGINT` | `2048` |
| `storage_block_prefetch` | Configures the scenario in which to use storage block prefetching. | `VARCHAR` | `REMOTE_ONLY` |
| `storage_compatibility_version` | Sets the DuckDB version for which data is serialized to the DuckDB file during checkpointing. Can differ from the version of the DuckDB instance. | `VARCHAR` | `latest` |
| `table_function_identifier_conversion` | Configures the use of deprecated implicit conversion of unbound identifiers to strings in table function arguments. | `VARCHAR` | `DEFAULT` |
| `temp_directory` | Set the directory to which temporary files are written. | `VARCHAR` | `⟨database_name⟩.tmp` or `.tmp` (in in-memory mode) |
| `temp_file_encryption` | Encrypt all temporary files, if the database is encrypted. | `BOOLEAN` | `false` |
| `threads`, `worker_threads` | The number of total background threads used by the system. | `BIGINT` | # CPU cores |
| `user`, `username` | The username to use. Kept for legacy compatibility. | `VARCHAR` |  |
| `validate_external_file_cache` | The cache validation mode. VALIDATE_`ALL` is the default, it validates all cache entries., VALIDATE_REMOTE only validates remote cache entries. NO_VALIDATION disables cache validation. | `VARCHAR` | `VALIDATE_ALL` |
| `variant_minimum_shredding_size` | Minimum size of a row group to have VARIANT shredding enabled. Set to -1 to disable shredding entirely. Defaults to 1/4th of the row group size. | `BIGINT` | `30000` |
| `wal_autocheckpoint_entries` | Trigger automatic checkpoint when WAL entry count reaches or exceeds N (0 = disabled). | `UBIGINT` | `0` |
| `warnings_as_errors` | Escalate all warnings to errors. | `BOOLEAN` | `false` |
| `write_buffer_row_group_count` | The amount of row groups to buffer in bulk ingestion prior to flushing them together. Reducing this setting can reduce memory consumption. | `UBIGINT` | `5` |
| `write_buffer_row_group_memory_limit` | The maximum data to buffer in row groups (in bytes) to buffer prior to flushing them together. When either this limit is reached, or write_buffer_row_group_count is reached, we flush the data to disk. Defaults to 20% of the memory limit divided by the thread count. | `VARCHAR` | `413.9 MiB` |
| `zstd_min_string_length` | The (average) minimum length at which to enable ZSTD compression, defaults to 4096. | `UBIGINT` | `4096` |

### Local Configuration Options

| Name | Description | Type | Default value |
|----|--------|--|---|
| `active_grammar_extensions` | The grammar extensions used by the parser. | `VARCHAR[]` | `[shell]` |
| `current_dialect` | The SQL dialect used by the parser. | `VARCHAR` | NULL |
| `enable_profiling` | Enables profiling and sets the output format, which can be `JSON`, `QUERY_TREE`, or `QUERY_TREE_OPTIMIZER`. | `VARCHAR` | NULL |
| `enable_progress_bar_print` | Controls the printing of the progress bar and requires 'enable_progress_bar' to be true. | `BOOLEAN` | `true` |
| `enable_progress_bar` | Enables the progress bar, which prints progress to the terminal during long queries. | `BOOLEAN` | `false` (`true` in the CLI) |
| `max_streaming_buffer_size`, `streaming_buffer_size` | The maximum number of bytes a streaming query result buffers (e.g., 1GB). Queued output stays under this cap, and each engine thread may hold, beyond the queue, the units it is still building or handing over from its current chunk. | `VARCHAR` | `10.0 MiB` |
| `operator_memory_limit` | The maximum memory available for query intermediates (sorts, hash tables) per connection (e.g., 256MB). | `VARCHAR` | NULL |
| `profile_output`, `profiling_output` | The file to which profiler output is written. When empty, the output is printed to the terminal. | `VARCHAR` |  |
| `profiling_coverage` | The profiling coverage, either SELECT (only SELECT queries) or `ALL` (all queries are profiled). | `VARCHAR` | `SELECT` |
| `profiling_renderer_settings` | A map of settings passed to the renderer of the profiler output, e.g., {'max_extra_lines': 100}. Settings not recognized by the active renderer are ignored. | `MAP(VARCHAR, VARCHAR)` | `{}` |
| `progress_bar_time` | Configures how long (in milliseconds) a query needs to take before we start printing a progress bar. | `BIGINT` | `2000` |
| `schema` | Sets the default search schema. Equivalent to setting search_path to a single value. | `VARCHAR` | `main` |
| `search_path` | Sets the default catalog search path as a comma-separated list of values. | `VARCHAR` |  |
| `tracked_metrics` | A list of metric glob patterns to enable for collection, e.g., ['query.*', 'optimizer.*']. | `VARCHAR[]` | `[*]` |

### Deprecated Configuration Options

The following configuration options are deprecated and will be removed in a future release.

| Name | Description | Type | Default value | Scope |
|----------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|---------------|--------|
| `enable_curl_server_cert_verification` | Enable server side certificate verification for CURL backend. | `BOOLEAN` | `true` | GLOBAL |
| `enable_object_cache` | Deprecated legacy setting, does nothing. | `BOOLEAN` | `false` | GLOBAL |
| `extension_directory` | Deprecated setting. Use extension_directories instead | `VARCHAR` |  | GLOBAL |
| `gcs_user_project` | GCS billing project for Requester Pays | `VARCHAR` | NULL | GLOBAL |
| `lambda_syntax` | Deprecated setting. Configures the use of the deprecated single arrow operator (->) for lambda functions. | `VARCHAR` | `DEFAULT` | GLOBAL |
| `legacy_metrics_format` | Deprecated setting. When enabled, profiling output uses the legacy flat format instead of the current grouped format. | `BOOLEAN` | `false` | GLOBAL |
| `old_implicit_casting` | Deprecated setting. Used for compatibility for the pre-0.10 implicit VARCHAR casting behavior. | `BOOLEAN` | `false` | GLOBAL |
| `produce_arrow_string_view` | Deprecated setting. Controlled via enable_arrow_string_view. | `BOOLEAN` | `false` | GLOBAL |
| `profiling_mode` | Deprecated setting. Use enable_profiling and profiling_coverage instead. | `VARCHAR` | NULL | LOCAL |
| `s3_access_key_id` | S3 Access Key ID | `VARCHAR` | NULL | GLOBAL |
| `s3_endpoint` | S3 Endpoint | `VARCHAR` | NULL | GLOBAL |
| `s3_kms_key_id` | S3 KMS Key ID | `VARCHAR` | NULL | GLOBAL |
| `s3_region` | S3 Region | `VARCHAR` | NULL | GLOBAL |
| `s3_requester_pays` | S3 use requester pays mode | `BOOLEAN` | `false` | GLOBAL |
| `s3_secret_access_key` | S3 Access Key | `VARCHAR` | NULL | GLOBAL |
| `s3_session_token` | S3 Session Token | `VARCHAR` | NULL | GLOBAL |
| `s3_url_compatibility_mode` | Disable Globs and Query Parameters on S3 URLs | `BOOLEAN` | `false` | GLOBAL |
| `s3_url_style` | S3 URL style | `VARCHAR` | `vhost` | GLOBAL |
| `s3_use_ssl` | S3 use SSL | `BOOLEAN` | `true` | GLOBAL |
| `vacuum_rebuild_indexes` | Deprecated compatibility setting: maximum table row count for rebuilding bound ART indexes when checkpoint vacuum cannot remap their row IDs. 0 disables the rebuild fallback but does not disable index remapping on v2.0 storage. The 'vacuum_rebuild_indexes' ATTACH option overrides this default per database. | `UBIGINT` | `0` | GLOBAL |
