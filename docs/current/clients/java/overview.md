---
github_repository: https://github.com/duckdb/duckdb-java
layout: docu
redirect_from:
- /docs/api/java
- /docs/api/scala
- /docs/clients/java
- /docs/clients/java/overview
- /docs/current/clients/java
- /docs/preview/clients/java
- /docs/preview/clients/java/overview
- /docs/stable/clients/java
- /docs/stable/clients/java/overview
title: Java (JDBC) Client
---

> Installation To use the DuckDB Java (JDBC) client, visit the [Java installation page]({% link install/index.html %}?environment=java).
>
> The latest stable version of the DuckDB Java (JDBC) client is {% if site.current_duckdb_java_short_version != "" %}{{ site.current_duckdb_java_short_version }}{% else %}{{ site.lts_duckdb_java_short_version }}{% endif %}.

The DuckDB Java (JDBC) client lets Java applications query DuckDB through the standard JDBC API, extended with DuckDB-specific features for bulk loading, [Apache Arrow](https://arrow.apache.org/) interchange, user-defined functions, and profiling. This page covers installation and the connection lifecycle; the other pages in this section cover each feature in detail.

## Installation

The DuckDB Java JDBC API can be installed from [Maven Central](https://search.maven.org/artifact/org.duckdb/duckdb_jdbc). Please see the [installation page]({% link install/index.html %}?environment=java) for details.

> Tip To try features before they reach a stable release, preview (nightly) builds of the JDBC driver are published as `SNAPSHOT` versions to DuckDB's snapshot repository at `https://duckdb-staging.duckdb.org/duckdb/duckdb-java/maven`. This is an object storage repository with no browseable web page; it is consumed directly by Maven. Add the repository to your build and depend on a `duckdb_jdbc` `SNAPSHOT` version. See the [preview builds page]({% link install/preview.md %}) for a full Maven example.

## Basic API Usage

DuckDB's JDBC API implements the main parts of the standard Java Database Connectivity (JDBC) API, version 4.1. Describing JDBC is beyond the scope of this page, see the [official documentation](https://docs.oracle.com/javase/tutorial/jdbc/basics/index.html) for details. Below we focus on the DuckDB-specific parts.

Refer to the externally hosted [API Reference](https://javadoc.io/doc/org.duckdb/duckdb_jdbc) for more information about our extensions to the JDBC specification, or the [Arrow Methods]({% link docs/current/clients/java/result_handling.md %}#arrow-methods).

### Startup & Shutdown

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

When using the `jdbc:duckdb:` URL alone, an **in-memory database** is created. Note that for an in-memory database no data is persisted to disk (i.e., all data is lost when you exit the Java program). If you would like to access or create a persistent database, append its file name after the path. For example, if your database is stored in `/tmp/my_database`, use the JDBC URL `jdbc:duckdb:/tmp/my_database` to create a connection to it.

It is possible to open a DuckDB database file in **read-only** mode. This is for example useful if multiple Java processes want to read the same database file at the same time. To open an existing database file in read-only mode, set the connection property `duckdb.read_only` like so:

```java
Properties readOnlyProperty = new Properties();
readOnlyProperty.setProperty("duckdb.read_only", "true");
Connection conn = DriverManager.getConnection("jdbc:duckdb:/tmp/my_database", readOnlyProperty);
```

Read-only mode can also be set through DuckDB's standard `access_mode` property, for example `access_mode=READ_ONLY`. If both `duckdb.read_only` and `access_mode` are supplied and disagree, the driver throws an error.

Additional connections can be created using the `DriverManager`. A more efficient mechanism is to call the `DuckDBConnection#duplicate()` method:

```java
Connection conn2 = ((DuckDBConnection) conn).duplicate();
```

Multiple connections are allowed, but mixing read-write and read-only connections is unsupported.

DuckDB shuts down a database when its last open connection is closed. Closing the final connection checkpoints the database, which merges the write-ahead log (the `.wal` file) into the database file and then removes it. See [Files Created by DuckDB]({% link docs/current/operations_manual/footprint_of_duckdb/files_created_by_duckdb.md %}) for details on these files.

For the JDBC driver, "exiting normally" means that every `Connection` to the database has been closed with `Connection.close()` before the Java program ends. There is no separate shutdown method to call: closing all connections is sufficient. Use a try-with-resources block so that connections are closed even when an exception is thrown:

```java
try (Connection conn = DriverManager.getConnection("jdbc:duckdb:/tmp/my_database")) {
    // work with the connection
}
```

If the process is terminated without closing its connections, the write-ahead log is left in place. It is replayed the next time the database file is opened, so no committed data is lost, but the file is only compacted once the database is checkpointed on a clean shutdown. To force a checkpoint without closing the connection, run the [`CHECKPOINT` statement]({% link docs/current/sql/statements/checkpoint.md %}).

### Configuring Connections

Configuration options can be provided to change different settings of the database system. Note that many of these settings can be changed later on using [`PRAGMA` statements]({% link docs/current/configuration/pragmas.md %}) as well.

```java
Properties connectionProperties = new Properties();
connectionProperties.setProperty("temp_directory", "/path/to/temp/dir/");
Connection conn = DriverManager.getConnection("jdbc:duckdb:/tmp/my_database", connectionProperties);
```

Alongside DuckDB's own settings, the driver recognizes a number of DuckDB-specific JDBC connection properties:

<div class="monospace_table"></div>

| Property | Description |
|--|--|
| `duckdb.read_only` | Open the database in read-only mode. |
| `access_mode` | Standard DuckDB access mode: `READ_ONLY`, `READ_WRITE`, or `AUTOMATIC`. |
| `custom_user_agent` | Append a custom string to the user agent reported to DuckDB. |
| `jdbc_stream_results` | Stream result sets instead of materializing them. See [Streaming Results]({% link docs/current/clients/java/result_handling.md %}#streaming-results). |
| `jdbc_auto_commit` | Set the default auto-commit mode for new connections. |
| `jdbc_pin_db` | Keep the database instance alive after its last connection closes. Disabled by default; enabled by default for DuckLake connections. |
| `jdbc_instance_cache` | Reuse the process-wide database instance for the same database. Enabled by default. See [In-Memory Databases and Instance Caching](#in-memory-databases-and-instance-caching). |
| `jdbc_ignore_unsupported_options` | Silently ignore unsupported connection options instead of throwing an error. |
| `jdbc_jfr_memory_monitor` | Enable JFR memory monitoring for the connection's database instance. See [Memory Monitoring with JFR]({% link docs/current/clients/java/profiling.md %}#memory-monitoring-with-jfr). |

These properties can be passed in the `Properties` object or appended to the JDBC URL after a semicolon, for example `jdbc:duckdb:/tmp/my_database;jdbc_stream_results=true`.

### In-Memory Databases and Instance Caching

The JDBC URL determines whether connections share a single underlying database instance or each get their own. By default, the driver caches the database instance so that connections addressing the same database reuse it.

The behavior depends on the form of the URL:

<div class="monospace_table"></div>

| JDBC URL | Behavior |
|--|--|
| `jdbc:duckdb:` or `jdbc:duckdb::memory:` | A private, uncached in-memory database. Each connection gets its own separate instance, and its data is not shared with any other connection. |
| `jdbc:duckdb::memory:⟨label⟩` | A named in-memory database. Connections using the same label share one cached instance, keyed by `:memory:⟨label⟩`. |
| `jdbc:duckdb:⟨path⟩` | A file-backed database. The instance is cached using the absolute path to the database file as the cache key, so connections that open the same file share one instance. |

```java
// Two connections to the same named in-memory database share their data.
Connection conn1 = DriverManager.getConnection("jdbc:duckdb::memory:shared_db");
Connection conn2 = DriverManager.getConnection("jdbc:duckdb::memory:shared_db");
```

Instance caching is controlled by the `jdbc_instance_cache` connection property, which is enabled by default. Setting it to `false` creates an isolated instance per connection. Disabling the cache for a file-backed database may cause local file lock conflicts if another connection has the same file open, and pinning an uncached instance with `jdbc_pin_db` does not make it reusable.

> Warning Each private (uncached) in-memory database creates its own instance with an independent thread pool. Unless the `threads` option is set, that pool is initialized with `cpu_count - 1` worker threads. An application that opens many connections with the default `jdbc:duckdb:` URL can therefore create a large number of operating system threads. Use a named in-memory database or set the `threads` option to bound the thread count.
