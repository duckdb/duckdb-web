---
layout: docu
redirect_from:
- /docs/preview/core_extensions/postgres/connection_pool
- /docs/stable/core_extensions/postgres/connection_pool
title: PostgreSQL Extension Connection Pool
---

PostgreSQL server spawns a backend process for every incoming client connection. This model leads to the two following points with the `postgres` extension that can cause performance problems:

 - opening a new connection is relatively expensive
 - the number of the connections opened at the same time should not be too high

To deal with these points the extensions uses an in-memory connection pool. With it a limited number of connections are kept open (and idle) after use and can be reused for subsequent queries.

## Parallel Scans

Due to DuckDB's multithreaded query processing, `postgres` extension can open multiple connections
even for queries that performs a scan for a single PostgreSQL table. The number of parallel queries running for a single table scan can be as high as the number of worker threads of the current DB instance (`threads` global configuration option).

When the `threads` parameter is set too high (that may be necessary for local processing of other queries on DuckDB side) this can lead to attempts to open an excessive number of PostgreSQL connections. To prevent this, these parallel queries (for the same table scan) are additionally limited by the maximum number of allowed connection in the connection pool (no more than 32 by default).

Even when the connection pool is configured to allow opening additional connections when all connection slots are taken (`force` acquire mode), the addtional parallel queries are always use the `try` mode. If connection for them is not available (the maximum number of connection in the pool is exceeded) - then that worked thread does not participate futher in the processing of this table scan, that proceeds with the worker threads that were able to acquire a connection from the pool.

See the description of the [postgres_configure_pool]({% link docs/current/core_extensions/postgres/functions.md %}#postgres_configure_pool) function for details.

## Connection Proxies

Connection pool can be the most effective when DuckDB connects directly to a PostgreSQL server and a new backend process is started for every new connection. When an intermediate transparent proxy is used between DuckDB and PostgreSQL (for example, [PgBouncer](https://www.pgbouncer.org/)) then opening a new connections only causes a new networking socket to be opened, not a full backend process.

Thus in deployment environments with connection proxies it may be better to set the idle timeout to a lower value (using `pg_pool_idle_timeout_millis` configuration option or [postgres_configure_pool]({% link docs/current/core_extensions/postgres/functions.md %}#postgres_configure_pool) function) or to disable the pooling completely (by setting `pg_pool_max_connections = 0`).

## Reaper Thread

The `postgres` extension supports running a background thread (so called "reaper thread") that periodically scans idle connections in the pool and closes the ones of them that exceed `idle_timeout_millis` or `max_lifetime_millis` values.

Separate thread is run for each connections pool, it can be enabled/disabled using `pg_pool_enable_reaper_thread` configuraton option.

When the reaper thread is not running, `idle_timeout_millis` or `max_lifetime_millis` values of the connections still can be checked, but they are only checked when a connection is taken from the pool or returned to the pool.

## Thread-local Cache

Idle connection in a pool are available for any caller thread, be it a DuckDB internal worker thread or a new client thread. In some cases it may be beneficial to ensure, that subsequent queries from the same thread are run on the same connection as the first query.
To support this the `pg_pool_enable_thread_local_cache` configuration option can be used - it makes an idle connection to be returned to a thread-local (and thread-private) cache instead of the main cache shared between all threads.

> Warning 
> Thread-local connection are not checked and not cleaned up by the reaper thread. Thread-local cache should be used with caution as cached connections, while not available to other threads, are still take the place in the pool, so can cause a "pool startvation".

## Configuration Options

The following global configuration options can be used to configure the connection pool. These options are only effective for the databases attached after the option is set. To change the settings of a connection pool for a database that is already attached the [postgres_configure_pool]({% link docs/current/core_extensions/postgres/functions.md %}#postgres_configure_pool) function can be used instead.

 - `pg_pool_acquire_mode` (`VARCHAR`, default: 'force'): how to acquire connections from the pool: 'force' (always connect, ignore pool limit), 'wait' (block until available), 'try' (fail immediately if unavailable)
 - `pg_pool_max_connections` (`UBIGINT`, default: `4 <= cpu_count * 1.5 <= 32`): maximum number of connections that are allowed to be cached in a connection pool for each attached Postgres database. This number can be temporary exceeded when parallel scans are used.
 - `pg_pool_wait_timeout_millis` (`UBIGINT`, default: `30000`): maximum number of milliseconds to wait when acquiring a connection from a pool where all available connections are already taken.
 - `pg_pool_enable_thread_local_cache` (`BOOLEAN`, default: `FALSE`): whether to enable the connection caching in thread-local cache. Such connections are getting pinned to the threads and are not made available to other threads, while still taking the place in the pool.
 - `pg_pool_max_lifetime_millis` (`UBIGINT`, default: `0` not enforced): maximum number of milliseconds the connection can be kept open. This number is checked when the connection is taken from the pool and returned to the pool. When the connection pool reaper thread is enabled ('pg_pool_enable_reaper_thread' option), then this number is checked in background periodically.
 - `pg_pool_idle_timeout_millis` (`UBIGINT`, default: `60000`): maximum number of milliseconds the connection can be kept idle in the pool. This number is checked when the connection is taken from the pool. When the connection pool reaper thread is enabled ('pg_pool_enable_reaper_thread' option), then this number is checked in background periodically.
 - `pg_pool_enable_reaper_thread` (default: `TRUE`): whether to enable the connection pool reaper thread, that periodically scans the pool to check the 'max_lifetime_millis' and 'idle_timeout_millis' and closes the connection which exceed the specified values. Either 'max_lifetime_millis' or 'idle_timeout_millis' must be set to a non-zero value for this option to be effective.
 - `pg_pool_health_check_query` (`VARCHAR`, default: `SELECT 1`): the query that is used to check that the connection is healthy. Setting this option to an empty string disables the health check.
