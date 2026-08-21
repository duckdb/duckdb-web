---
layout: docu
redirect_from:
- /docs/clients/java/connecting
- /docs/preview/clients/java/connecting
- /docs/stable/clients/java/connecting
title: Define Connections
---

## Overview

Every DuckDB feature reachable from Java starts with a `Connection`. This page covers the JDBC URL forms the driver accepts, how DuckDB and driver options are passed and which of them win, how connections come to share (or not share) an underlying database instance, how DuckDB's threads relate to that instance, and how to reach a remote DuckDB server over [Quack]({% link docs/current/quack/overview.md %}).

## Opening a Connection

In JDBC, database connections are created through the standard `java.sql.DriverManager` class.
The driver should auto-register in the `DriverManager`. If that does not work for some reason, you can enforce registration using the following statement:

```java
Class.forName("org.duckdb.DuckDBDriver");
```

To create a DuckDB connection, call `DriverManager` with the `jdbc:duckdb:` JDBC URL prefix, like so:

```java
import java.sql.Connection;
import java.sql.DriverManager;

Connection conn = DriverManager.getConnection("jdbc:duckdb:");
```

To use DuckDB-specific features such as the [Appender]({% link docs/current/clients/java/data_import.md %}#appender), cast the object to a `DuckDBConnection`:

```java
import java.sql.DriverManager;
import org.duckdb.DuckDBConnection;

DuckDBConnection conn = (DuckDBConnection) DriverManager.getConnection("jdbc:duckdb:");
```

Additional connections can be created using the `DriverManager`. The `DuckDBConnection#duplicate()` method opens another connection to the same database instance without re-reading the configuration:

```java
Connection conn2 = ((DuckDBConnection) conn).duplicate();
```

Its main purpose is to reach a **connection-private in-memory** database instance — the one created by the plain `jdbc:duckdb:` URL — which no other URL can address. On a named in-memory or a file-backed connection, `duplicate()` is effectively the same as opening a new connection on the same URL, because those instances are shared through the [instance cache](#database-instances-and-instance-caching) anyway.

Multiple connections to the same instance are allowed, but they must all be opened with the same options. Options are applied when the instance starts, as the first connection is opened, so a later connection that requests different options — a different `access_mode`, for example — is rejected. See [Database Instances and Instance Caching](#database-instances-and-instance-caching).

## JDBC URL Syntax

A DuckDB JDBC URL consists of the `jdbc:duckdb:` prefix, an optional database name, and an optional list of options separated by semicolons:

```text
jdbc:duckdb:⟨database⟩;⟨key⟩=⟨value⟩;⟨key⟩=⟨value⟩
```

The database part determines what the connection opens:

<div class="monospace_table"></div>

| JDBC URL | Opens |
|--|--|
| `jdbc:duckdb:` | A connection-private in-memory database. |
| `jdbc:duckdb:memory:` | The same as above, written explicitly. |
| `jdbc:duckdb:memory:⟨label⟩` | A named in-memory database that other connections can share. |
| `jdbc:duckdb:⟨path⟩` | A database file on disk, for example `jdbc:duckdb:/tmp/my_database`. |
| `jdbc:duckdb:ducklake:⟨metadata_path⟩` | A [DuckLake]({% link docs/current/core_extensions/ducklake.md %}) catalog. |

When using the `jdbc:duckdb:` URL alone, a **connection-private in-memory database** is created: the instance belongs to that single connection and cannot be shared, other than through `duplicate()`. Note that for an in-memory database no data is persisted to disk (i.e., all data is lost when you exit the Java program). If you would like to access or create a persistent database, append its file name after the path.

## Read-Only Connections

It is possible to open a DuckDB database file in **read-only** mode. This is for example useful if multiple Java processes want to read the same database file at the same time. To open an existing database file in read-only mode, set the connection property `duckdb.read_only` like so:

```java
Properties readOnlyProperty = new Properties();
readOnlyProperty.setProperty("duckdb.read_only", "true");
Connection conn = DriverManager.getConnection("jdbc:duckdb:/tmp/my_database", readOnlyProperty);
```

Read-only mode can also be set through DuckDB's standard `access_mode` property, for example `access_mode=READ_ONLY`. If both `duckdb.read_only` and `access_mode` are supplied and disagree, the driver throws an error.

## Configuration Options

### DuckDB Settings

Any DuckDB configuration option can be supplied when a connection is opened: the driver hands every option it does not recognize as its own to DuckDB. Note that many of these settings can also be changed later on with a [`SET` (or `SET GLOBAL`) statement]({% link docs/current/sql/statements/set.md %}), or the equivalent [`PRAGMA`]({% link docs/current/configuration/pragmas.md %}).

```java
Properties connectionProperties = new Properties();
connectionProperties.setProperty("temp_directory", "/path/to/temp/dir/");
connectionProperties.setProperty("memory_limit", "4GB");
Connection conn = DriverManager.getConnection("jdbc:duckdb:/tmp/my_database", connectionProperties);
```

The available options are listed on the [Configuration page]({% link docs/current/configuration/overview.md %}) and can also be queried at runtime with `duckdb_settings()`. The driver exposes the same list through the standard `Driver.getPropertyInfo()` call, which returns one `DriverPropertyInfo` per DuckDB setting alongside the driver's own options.

> Note Options passed at connection time are applied as **global** settings on the database instance. A setting that only has session scope has to be applied with a `SET` statement after connecting; setting it at connection time fails with `Could not set option "⟨name⟩" as a global option`.

### Setting Options in the URL

The same options can be appended to the JDBC URL, separated by semicolons. This is the only way to configure DuckDB in tools that accept a connection string but no `Properties` object:

```text
jdbc:duckdb:/tmp/my_database;threads=4;memory_limit=4GB;jdbc_stream_results=true
```

Each entry is a `key=value` pair and surrounding whitespace is trimmed. The driver splits the URL on `;` and each entry on `=`, so a value that itself contains a semicolon or an equals sign has to be passed in a `Properties` object instead.

### Option Precedence

When the same option appears in both places, the value in the URL wins:

```java
Properties props = new Properties();
props.setProperty("threads", "8");
// The connection is opened with threads = 4.
Connection conn = DriverManager.getConnection("jdbc:duckdb:/tmp/my_database;threads=4", props);
```

### Unsupported Options

An option name that is neither a DuckDB setting nor a driver option makes the connection fail. Set `jdbc_ignore_unsupported_options` to `true` to have the driver drop such names silently, which is useful for frameworks and BI tools that add JDBC properties of their own. The driver already discards two options that are known to be passed by mistake: Apache Spark's `path` and LibreOffice Base's `Type`.

### JDBC-Specific Options

Alongside DuckDB's own settings, the driver recognizes a number of DuckDB-specific JDBC connection properties:

<div class="monospace_table"></div>

| Property | Description |
|--|--|
| `duckdb.read_only` | Open the database in read-only mode. |
| `access_mode` | Standard DuckDB access mode: `READ_ONLY`, `READ_WRITE`, or `AUTOMATIC`. |
| `custom_user_agent` | Append a custom string to the user agent reported to DuckDB. |
| `jdbc_stream_results` | Stream result sets instead of materializing them. See [Streaming Results]({% link docs/current/clients/java/result_handling.md %}#streaming-results). |
| `jdbc_auto_commit` | Set the default auto-commit mode for new connections. |
| `jdbc_pin_db` | Keep the database instance alive after its last connection closes. Disabled by default. Enabled by default, together with `jdbc_stream_results`, for `ducklake:` URLs, so that BI tools such as Metabase do not repeatedly close and re-create the instance or accidentally materialize large DuckLake datasets. |
| `jdbc_instance_cache` | Reuse the process-wide database instance for the same database. Enabled by default. See [Database Instances and Instance Caching](#database-instances-and-instance-caching). |
| `jdbc_ignore_unsupported_options` | Silently ignore unsupported connection options instead of throwing an error. |
| `jdbc_jfr_memory_monitor` | Enable JFR memory monitoring for the connection's database instance. See [Memory Monitoring with JFR]({% link docs/current/clients/java/profiling.md %}#memory-monitoring-with-jfr). |
| `session_init_sql_file` | Run the SQL in the given file before handing over the connection. URL-only, see [Running SQL at Connection Startup](#running-sql-at-connection-startup). |
| `session_init_sql_file_sha256` | Expected SHA-256 digest of the session init SQL file. URL-only. |

## Running SQL at Connection Startup

The `session_init_sql_file` option points the driver at a SQL file on the local file system that is executed before the connection is returned to the caller. It is intended for environments where you control the connection string but not the code that opens the connection, for example a BI tool that only offers a JDBC URL field:

```text
jdbc:duckdb:/tmp/my_database;session_init_sql_file=/path/to/init.sql
```

The file can be split into a database part and a connection part with a marker comment:

```sql
-- Runs once, when the database instance is created.
SET memory_limit = '4GB';
CREATE OR REPLACE VIEW recent_events AS
    SELECT *
    FROM events
    WHERE ts > now() - INTERVAL 7 DAYS;

/* DUCKDB_CONNECTION_INIT_BELOW_MARKER */

-- Runs for every connection.
SET search_path = 'analytics';
```

Everything above the marker runs the first time the database is opened in the JVM process, and everything below it runs for every connection. A file without a marker is treated entirely as database initialization. For the unnamed in-memory database the database part runs for every connection, because each connection gets its own instance.

Because the option makes the connection string execute arbitrary SQL, the driver constrains it:

* It is read from the JDBC URL only and is not picked up from a `Properties` object.
* It has to be the first option in the connection string, and `session_init_sql_file_sha256`, if present, has to be the second. Neither may appear more than once.
* The file may not be larger than 1 MB.
* If `session_init_sql_file_sha256` is given and does not match the file's digest, opening the connection fails. Use it to detect a file that was modified after deployment.
* `DuckDBConnection.getSessionInitSQL()` returns the text that was executed, so an application can log or audit it.

> Warning The SQL in the file runs with the full privileges of the connection. Treat the connection string and the file it points at as trusted input.

## Database Instances and Instance Caching

The JDBC URL determines whether connections share a single underlying database instance or each get their own. By default, the driver caches the database instance so that connections addressing the same database reuse it.

The behavior depends on the form of the URL:

<div class="monospace_table"></div>

| JDBC URL | Behavior |
|--|--|
| `jdbc:duckdb:` or `jdbc:duckdb:memory:` | A connection-private, uncached in-memory database. Each connection gets its own separate instance, and its data is not shared with any other connection. |
| `jdbc:duckdb:memory:⟨label⟩` | A named in-memory database. Connections using the same label share one cached instance, keyed by `:memory:⟨label⟩`. |
| `jdbc:duckdb:⟨path⟩` | A file-backed database. The instance is cached using the absolute path to the database file as the cache key, so connections that open the same file share one instance. On Windows and macOS the key is case-insensitive. |

```java
// Two connections to the same named in-memory database point to the same database instance.
Connection conn1 = DriverManager.getConnection("jdbc:duckdb:memory:shared_db");
Connection conn2 = DriverManager.getConnection("jdbc:duckdb:memory:shared_db");
```

Instance caching is controlled by the `jdbc_instance_cache` connection property, which is enabled by default. Setting it to `false` creates an isolated instance per connection. Disabling the cache for a file-backed database may cause local file lock conflicts if another connection has the same file open, and pinning an uncached instance with `jdbc_pin_db` does not make it reusable.

Because configuration options apply to the instance rather than to the connection, only the connection that creates the instance can set them. A later connection that reaches a cached instance and asks for a different configuration fails with:

```console
Connection Error:
Can't open a connection to same database file with a different configuration than existing connections
```

Pass the same options on every connection to a given database, or open the first connection with the intended configuration and create the rest with `duplicate()`.

## Threads and Thread Pools

DuckDB runs queries on its own pool of native threads. This pool is independent of the JVM's threads: a single `Statement.executeQuery()` call can occupy every thread in the pool, and blocking JDBC calls from many application threads do not increase DuckDB's parallelism.

The pool belongs to the **database instance**, not to the `Connection`. Every connection to the same instance, whether created through `DriverManager` or `duplicate()`, submits work to the same pool. Two connections that resolve to different instances, as described in [Database Instances and Instance Caching](#database-instances-and-instance-caching), each get a pool of their own.

The size of the pool is set by DuckDB's `threads` option, which defaults to the number of CPU cores. DuckDB reserves `external_threads` of that budget, one by default, for the thread that calls into the library, and starts `threads - external_threads` background threads. On a 16-core machine, that is 15 native threads per database instance.

To bound the thread count, set `threads` when the instance is created:

```text
jdbc:duckdb:/tmp/my_database;threads=4
```

An already-running instance can be resized with a `SET` statement, which affects every connection to that instance:

```sql
SET threads = 4;
```

Two consequences are worth calling out for Java applications:

* **Attached databases do not add threads.** [`ATTACH`]({% link docs/current/sql/statements/attach.md %}) adds a catalog to the database instance the connection already belongs to. All attached databases share that instance's thread pool, memory limit, and temporary directory. Only opening a *new* JDBC connection to a different database name creates a second instance, and with it a second pool.
* **Multiple instances multiply the thread count.** An application that opens a dozen private in-memory databases with `jdbc:duckdb:` on a 16-core machine starts about 180 native threads, each with its own stack and its own share of the memory limit.

> Warning Each private (uncached) in-memory database creates its own instance with an independent thread pool. An application that opens many connections with the default `jdbc:duckdb:` URL can therefore create a large number of operating system threads. Use a named in-memory database, share one instance through the [instance cache](#database-instances-and-instance-caching), or set the `threads` option to bound the thread count.

> Note Upcoming DuckDB v2.0 adds a second pool of `ASYNC` threads dedicated to blocking I/O, sized at four times the number of system threads and capped at 256. On a 16-core machine, this raises the default per-instance thread count from roughly 15 to roughly 80, which makes bounding the number of instances and setting `threads` explicitly more important. See the [asynchronous I/O blog post]({% post_url 2026-07-31-asynchronous-io %}) for details.

Separately from DuckDB's pools, the driver starts a single daemon thread named `duckdb-query-cancel-scheduler-thread` in the JVM the first time it is loaded. It is shared by the whole process and is used to fire `Statement.setQueryTimeout()` cancellations. Applications that unload the driver, for example in an application server, can stop it with `DuckDBDriver.shutdownQueryCancelScheduler()`.

## Connecting to a Quack Server

The [Quack remote protocol]({% link docs/current/quack/overview.md %}) turns a DuckDB instance into a server that other DuckDB instances can query over HTTP. The JDBC driver has no dedicated URL scheme for it: open a local, usually in-memory, DuckDB connection in the normal way and attach the remote server as a catalog.

```java
try (Connection conn = DriverManager.getConnection("jdbc:duckdb:");
     Statement stmt = conn.createStatement()) {
    stmt.execute("ATTACH 'quack:⟨hostname⟩' AS remote_db (TOKEN '⟨MY_QUACK_TOKEN⟩')");

    try (ResultSet rs = stmt.executeQuery("SELECT count(*) FROM remote_db.events")) {
        rs.next();
        System.out.println(rs.getLong(1));
    }
}
```

The token can also be stored in a secret, which keeps it out of the `ATTACH` statement:

```java
stmt.execute("CREATE SECRET (TYPE quack, TOKEN '⟨MY_QUACK_TOKEN⟩')");
stmt.execute("ATTACH 'quack:⟨hostname⟩' AS remote_db");
```

Once attached, remote tables behave like local ones, so the whole JDBC API applies to them. Run `USE remote_db` to make the remote catalog the default, so that unqualified table names resolve against the server. The local instance still holds its own thread pool and memory limit, and the connection is subject to the same instance rules as any other JDBC connection, so a client that only forwards queries to a server can be opened with a small `threads` value.

> Warning Quack is under active development and its protocol, function names, settings, and defaults are still subject to change. See the [Quack documentation]({% link docs/current/quack/overview.md %}) for the current state.

## Closing Connections

DuckDB shuts down a database when its last open connection is closed. Closing the final connection checkpoints the database, which merges the write-ahead log (the `.wal` file) into the database file and then removes it. See [Files Created by DuckDB]({% link docs/current/operations_manual/footprint_of_duckdb/files_created_by_duckdb.md %}) for details on these files.

For the JDBC driver, “exiting normally” means that every `Connection` to the database has been closed with `Connection.close()` before the Java program ends. There is no separate shutdown method to call: closing all connections is sufficient. Use a try-with-resources block so that connections are closed even when an exception is thrown:

```java
try (Connection conn = DriverManager.getConnection("jdbc:duckdb:/tmp/my_database")) {
    // work with the connection
}
```

If the process is terminated without closing its connections, the write-ahead log is left in place. It is replayed the next time the database file is opened, so no committed data is lost, but the file is only compacted once the database is checkpointed on a clean shutdown. To force a checkpoint without closing the connection, run the [`CHECKPOINT` statement]({% link docs/current/sql/statements/checkpoint.md %}).

Repeatedly opening and closing the last connection to a database means starting and shutting down the instance each time, including its thread pool. Applications that do this in a loop can keep the instance alive between connections with the `jdbc_pin_db` option and release it later with `DuckDBDriver.releaseDB(url)`.

## Further Reading

* [Run Queries]({% link docs/current/clients/java/querying.md %}) — using the `Connection` to send queries and read result sets.
* [Handle Results]({% link docs/current/clients/java/result_handling.md %}) — the `jdbc_stream_results` option and other result-handling choices set at connection time.
* [Configuration]({% link docs/current/configuration/overview.md %}) — the full list of DuckDB settings that can be passed as connection options.
* [Files Created by DuckDB]({% link docs/current/operations_manual/footprint_of_duckdb/files_created_by_duckdb.md %}) — the database, WAL, and temporary files that connection shutdown checkpoints and cleans up.
* [Troubleshoot]({% link docs/current/clients/java/known_issues.md %}) — workarounds for common connection and driver problems.
