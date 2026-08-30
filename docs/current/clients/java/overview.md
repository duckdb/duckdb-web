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

The DuckDB Java (JDBC) client lets Java applications query DuckDB through the standard JDBC API, extended with DuckDB-specific features for bulk loading, [Apache Arrow](https://arrow.apache.org/) interchange, user-defined functions, and profiling, and can open a [DuckLake]({% link docs/current/core_extensions/ducklake.md %}) catalog directly from the JDBC URL. This page covers installation; the other pages in this section cover connecting and each feature in detail.

## Installation

The DuckDB Java JDBC API can be installed from [Maven Central](https://search.maven.org/artifact/org.duckdb/duckdb_jdbc). Please see the [installation page]({% link install/index.html %}?environment=java) for details.

> Tip To try features before they reach a stable release, preview (nightly) builds of the JDBC driver are published as `SNAPSHOT` versions to DuckDB's snapshot repository at `https://duckdb-staging.duckdb.org/duckdb/duckdb-java/maven`. This is an object storage repository with no browseable web page; it is consumed directly by Maven. Add the repository to your build and depend on a `duckdb_jdbc` `SNAPSHOT` version. See the [preview builds page]({% link install/preview.md %}) for a full Maven example.

## Basic API Usage

DuckDB's JDBC API implements the main parts of the standard Java Database Connectivity (JDBC) API, version 4.1. Describing JDBC is beyond the scope of this page, see the [official documentation](https://docs.oracle.com/javase/tutorial/jdbc/basics/index.html) for details. Below we focus on the DuckDB-specific parts.

Refer to the externally hosted [API Reference](https://javadoc.io/doc/org.duckdb/duckdb_jdbc) for more information about our extensions to the JDBC specification, or the [Arrow Methods]({% link docs/current/clients/java/result_handling.md %}#arrow-methods).

### Opening a Connection

In JDBC, database connections are created through the standard `java.sql.DriverManager` class, using the `jdbc:duckdb:` JDBC URL prefix:

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

Connection conn = DriverManager.getConnection("jdbc:duckdb:");
```

Used on its own, `jdbc:duckdb:` opens an in-memory database. Appending a file name, for example `jdbc:duckdb:/tmp/my_database`, opens a persistent database instead.

To confirm that the driver is on the classpath and a connection can be opened, run a trivial query:

```java
try (Statement stmt = conn.createStatement();
     ResultSet rs = stmt.executeQuery("SELECT 42")) {
    rs.next();
    System.out.println(rs.getInt(1)); // prints 42
}
```

[Define Connections]({% link docs/current/clients/java/connecting.md %}) covers the connection lifecycle in full: the URL forms the driver accepts, DuckDB and driver configuration options, read-only mode, instance caching, threading, and shutdown.

## Further Reading

* [Define Connections]({% link docs/current/clients/java/connecting.md %}) — the JDBC URL forms, configuration options, instance caching, threading, and connection shutdown.
* [Connect to a DuckLake]({% link docs/current/clients/java/connecting.md %}#connect-to-a-ducklake) — attach or open a DuckLake catalog from JDBC.
* [Run Queries]({% link docs/current/clients/java/querying.md %}) — sending queries with `Statement` and `PreparedStatement`, and reading DuckDB's nested types.
* [Import Data]({% link docs/current/clients/java/data_import.md %}) — bulk-loading data with the Appender and the JDBC batch writer.
* [Handle Results]({% link docs/current/clients/java/result_handling.md %}) — Apache Arrow interchange, result streaming, and chunked results.
* [Clients Overview]({% link docs/current/clients/overview.md %}) — the other client APIs DuckDB provides alongside JDBC.
