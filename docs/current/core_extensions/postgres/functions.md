---
layout: docu
redirect_from:
- /docs/preview/core_extensions/postgres/functions
- /docs/stable/core_extensions/postgres/functions
title: PostgreSQL Extension Functions
---

- [`pg_clear_cache`](#pg_clear_cache)
- [`postgres_attach`](#postgres_attach)
- [`postgres_configure_pool`](#postgres_configure_pool)
- [`postgres_execute`](#postgres_execute)
- [`postgres_hstore_get`](#postgres_hstore_get)
- [`postgres_hstore_to_json`](#postgres_hstore_to_json)
- [`postgres_query`](#postgres_query)
- [`postgres_scan`](#postgres_scan)
- [`postgres_scan_pushdown`](#postgres_scan_pushdown)
- [`read_postgres_binary`](#read_postgres_binary)

### pg_clear_cache

```sql
pg_clear_cache() -> TABLE
```

Clears cached schema entries (like table names with column lists) for all attached PostgreSQL catalogs. Attached schema is going to be re-read on the next access.

#### Parameters

None.

#### Returns

A table with the following columns:

 - `Success` (`BOOLEAN`): a flag whether the cache clearing was successful

> Currently the table result is always returned with zero rows, so the flag value is not available.

#### Example

```sql
CALL pg_clear_cache()
```

### postgres_attach

> Warning 
> This function is deprecated and is planned to be removed in future versions.
> The `ATTACH` statement is intended to be used instead.

```sql
postgres_attach(connection_string VARCHAR [, <optional named parameters>]) -> TABLE
```

### postgres_configure_pool

```sql
FROM postgres_configure_pool([<optional named parameters>]) -> TABLE
```

When a PostgreSQL database is attached, a connection pool is created for this database. This function allows to change the configuration options of a connection pool for the specified attached database. It also allows to list the current effective configuration options and the collected runtime statistics of a connection pool.

#### Parameters

 - `catalog_name` (`VARCHAR`): the name (alias) of the attached Postgres database to which pool the configuration change is applied and details are returned. When `NULL` (default) returns the current state of pools for all attached catalogs without changing their configuration. Must be specified and non-NULL when any other option is specified.
 - `acquire_mode` (`VARCHAR`, default: 'force'): how to acquire connections from the pool: 'force' (always connect, ignore pool limit), 'wait' (block until available), 'try' (fail immediately if unavailable)
 - `max_connections` (`UBIGINT`): maximum number of connections that are allowed to be cached in a connection pool for each attached Postgres database. This number can be temporary exceeded when parallel scans are used.
 - `wait_timeout_millis` (`UBIGINT`): maximum number of milliseconds to wait when acquiring a connection from a pool where all available connections are already taken.
 - `enable_thread_local_cache` (`BOOLEAN`): whether to enable the connection caching in thread-local cache. Such connections are getting pinned to the threads and are not made available to other threads, while still taking the place in the pool.
 - `max_lifetime_millis` (`UBIGINT`): maximum number of milliseconds the connection can be kept open. This number is checked when the connection is taken from the pool and returned to the pool. When the connection pool reaper thread is enabled ('enable_reaper_thread' argument), then this number is checked in background periodically.
 - `idle_timeout_millis` (`UBIGINT`): maximum number of milliseconds the connection can be kept idle in the pool. This number is checked when the connection is taken from the pool. When the connection pool reaper thread is enabled ('enable_reaper_thread' option), then this number is checked in background periodically.
 - `enable_reaper_thread` (`BOOLEAN`): whether to enable the connection pool reaper thread, that periodically scans the pool to check the 'max_lifetime_millis' and 'idle_timeout_millis' and closes the connection which exceed the specified values. Either 'max_lifetime_millis' or 'idle_timeout_millis' must be set to a non-zero value for this option to be effective.
 - `health_check_query` (`VARCHAR`): the query that is used to check that the connection is healthy. Setting this option to an empty string disables the health check.

#### Returns

A table with the following columns:

 - `catalog_name` (`VARCHAR`): the name (alias) of the attached Postgres database
 - `acquire_mode` (`VARCHAR`): how to acquire connections from the pool: 'force' (always connect, ignore pool limit), 'wait' (block until available), 'try' (fail immediately if unavailable)
 - `available_connections` (`UBIGINT`): the number of idle connection that are currently available in the pool
 - `max_connections` (`UBIGINT`): maximum number of connections that are allowed to be cached in the pool.
 - `wait_timeout_millis` (`UBIGINT`): maximum number of milliseconds to wait when acquiring a connection from a pool where all available connections are already taken; only applicable to the `wait` acquire-mode
 - `cache_hits` (`UBIGINT`): number of times a cached connection was successfully returned from the pool
 - `cache_misses` (`UBIGINT`): number of times a new connection was created by the pool
 - `try_failures` (`UBIGINT`): number of times a connection was requested by the pool in `try` acquire-mode and no connection was available at the time - so no connection was provided by the pool; note that when the parallel scans are performed by the Postgres extension - worker threads always use the `try` acquire mode; when `SET threads = <number_higher_then_pool_size>` is used, then some of the worker threads are unable to obtain a connection - they return without doing any work and without throwing an error
 - `thread_local_cache_enabled` (`BOOLEAN`): whether caching the connections caching in thread-local cache is enabled; thread-local connections are **NOT** cleared by the reaper thread
 - `thread_local_cache_hits` (`UBIGINT`): the number of times connections were successfully acquired from a thread-local cache without going to the main pool
 - `thread_local_cache_misses` (`UBIGINT`): the number of times connections were not available in a thread-local cache and were taken from the main pool instead
 - `max_lifetime_millis` (`UBIGINT`): maximum number of milliseconds a connection can be kept open
 - `idle_timeout_millis` (`UBIGINT`): maximum number of milliseconds a connection can be kept idle in the pool
 - `reaper_thread_running` (`BOOLEAN`): whether the pool reaper thread is running; this thread periodically scans the pool to check the 'max_lifetime_millis' and 'idle_timeout_millis' and closes connections which exceed the specified values
 - `reaper_thread_period_millis` (`UBIGINT`): the period of time when a reaper thread performs the checks
 - `health_check_query` (`VARCHAR`): the query that is used to check that the connection is healthy

#### Examples

List the current effective configuration options and the collected runtime statistics of all connections pools (for all attached databases):

```sql
FROM postgres_configure_pool()
```

Change one or more configuration option for the connection pool of the specified attached database:

```sql
FROM postgres_configure_pool(catalog_name='db1', acquire_mode='wait', max_connections=42)
```

### postgres_execute

```sql
postgres_execute(attached_db_name VARCHAR, sql_query VARCHAR[, <optional named parameters>]) -> TABLE
```

Executes the query in the speicifed remote DB that was previosly attached with `ATTACH .. AS <attached_db_name>`.
Does not return the query result.

#### Parameters

 - `attached_db_name` (`VARCHAR`):  the name of the attached PostgreSQL database
 - `sql_query` (`VARCHAR`): query that is passed to PostgreSQL for execution; no transformation or analysis of this query is performed by DuckDB

Optional named parameters:

 - `use_transaction` (`BOOLEAN`, default: `TRUE`): whether to start a PostgreSQL transaction if it was not started before.

#### Returns

A table with the following columns:

 - `Success` (`BOOLEAN`): a flag whether the cache clearing was successful

> Currently the table result is always returned with zero rows, so the flag value is not available.

#### Example

```sql
CALL postgres_execute('db1', 'VACUUM ANALYZE', use_transaction=FALSE)
```

### postgres_hstore_get

```sql
postgres_hstore_get(hstore_string VARCHAR, hstore_key VARCHAR) -> VARCHAR
```

Parses the external representation of and [PostgreSQL hstore column](https://www.postgresql.org/docs/18/hstore.html) and returns the value of the specified hstore key.

#### Parameters

 - `hstore_string` (`VARCHAR`): PostgreSQL `hstore` value in `key => value` form.
 - `hstore_kay` (`VARCHAR`): Key name to return the value for.

#### Returns

The value for the specified key. `NULL` if the key not found.

#### Example

```sql
SELECT postgres_hstore_get('a=>b, c=>d', 'a')
```

### postgres_hstore_to_json

```sql
postgres_hstore_to_json(hstore_string VARCHAR) -> JSON
```

Converts the external representation of and [PostgreSQL hstore column](https://www.postgresql.org/docs/18/hstore.html) into `JSON`.

#### Parameters

 - `hstore_string` (`VARCHAR`): PostgreSQL `hstore` value in `key => value` form.

#### Returns

JSON dictionary with the same key/value pairs as the input `hstore` string. All values are returned as strings.

#### Example

```sql
SELECT postgres_hstore_to_json('z=>1, a=>2, m=>3')
```

### postgres_query

```sql
postgres_query(attached_db_name VARCHAR, sql_query VARCHAR[, <optional named parameters>]) -> TABLE
```

Executes the query in the speicifed remote DB that was previosly attached with `ATTACH .. AS <attached_db_name>` and return the query result as a table.

#### Parameters

 - `attached_db_name` (`VARCHAR`):  the name of the attached PostgreSQL database
 - `sql_query` (`VARCHAR`): query that is passed to PostgreSQL for execution; no transformation or analysis of this query is performed by DuckDB

Optional named parameters:

 - `use_transaction` (`BOOLEAN`, default: `TRUE`): whether to start a PostgreSQL transaction if it was not started before.
 - `params` (`STRUCT`): query parameters that are passed to the PostgreSQL server; only supported when the text protocol is used

#### Returns

A table with the query result.

#### Example

```sql
FROM postgres_query('db11', 'SELECT $1::INTEGER, $2::TEXT', params=row(42::INTEGER, 'foo'::VARCHAR))
```

### postgres_scan

> Warning 
> This function is deprecated and is planned to be removed in future versions.
> Direct SQL queries over the attached PostgreSQL database are intended to be used instead.

```sql
postgres_scan(connection_string VARCHAR, schema_name VARCHAR, table_name VARCHAR) -> TABLE
```

### postgres_scan_pushdown

> Warning 
> This function is deprecated and is planned to be removed in future versions.
> Direct SQL queries over the attached PostgreSQL database are intended to be used instead.

```sql
postgres_scan_pushdown(connection_string VARCHAR, schema_name VARCHAR, table_name VARCHAR) -> TABLE
```

### read_postgres_binary

```sql
FROM read_postgres_binary(file_path VARCHAR[, <optional named parameters>]) -> TABLE
```

Reads PostgreSQL binary dump files from file system.

#### Parameters

 - `file_path` (`VARCHAR`): FS path to the binary dump file in a PostgreSQL format.

Optional named parameters:

 - `columns` (`STRUCT`): type mapping in form of the `column_name -> column_type` structure.
 - `buffer_size` (`UBIGINT`, default: 32KB): size of the read buffer in bytes.

#### Returns

Contents of the binary dump file as a table.

#### Example

```sql
COPY (SELECT 42::INTEGER AS a, 'foo'::VARCHAR AS b) TO 'path/to/test.bin' (FORMAT postgres_binary);

FROM read_postgres_binary('path/to/test.bin', columns={a: 'INTEGER', b: 'VARCHAR'});
```
