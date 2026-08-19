---
github_repository: https://github.com/duckdb/duckdb-java
layout: docu
redirect_from:
- /docs/api/java
- /docs/api/scala
- /docs/clients/java
- /docs/preview/clients/java
- /docs/stable/clients/java
title: Java (JDBC) Client
---

> Installation To use the DuckDB Java (JDBC) client, visit the [Java installation page]({% link install/index.html %}?environment=java).
>
> The latest stable version of the DuckDB Java (JDBC) client is {% if site.current_duckdb_java_short_version != "" %}{{ site.current_duckdb_java_short_version }}{% else %}{{ site.lts_duckdb_java_short_version }}{% endif %}.

## Installation

The DuckDB Java JDBC API can be installed from [Maven Central](https://search.maven.org/artifact/org.duckdb/duckdb_jdbc). Please see the [installation page]({% link install/index.html %}?environment=java) for details.

To try features before they reach a stable release, preview (nightly) builds of the JDBC driver are published as `SNAPSHOT` versions to the Sonatype Central snapshots repository at `https://central.sonatype.com/repository/maven-snapshots/`. Add this repository to your build and depend on a `duckdb_jdbc` `SNAPSHOT` version. See the [preview builds page]({% link install/preview.md %}) for a full Maven example.

## Basic API Usage

DuckDB's JDBC API implements the main parts of the standard Java Database Connectivity (JDBC) API, version 4.1. Describing JDBC is beyond the scope of this page, see the [official documentation](https://docs.oracle.com/javase/tutorial/jdbc/basics/index.html) for details. Below we focus on the DuckDB-specific parts.

Refer to the externally hosted [API Reference](https://javadoc.io/doc/org.duckdb/duckdb_jdbc) for more information about our extensions to the JDBC specification, or the below [Arrow Methods](#arrow-methods).

### Startup & Shutdown

In JDBC, database connections are created through the standard `java.sql.DriverManager` class.
The driver should auto-register in the `DriverManager`, if that does not work for some reason, you can enforce registration using the following statement:

```java
Class.forName("org.duckdb.DuckDBDriver");
```

To create a DuckDB connection, call `DriverManager` with the `jdbc:duckdb:` JDBC URL prefix, like so:

```java
import java.sql.Connection;
import java.sql.DriverManager;

Connection conn = DriverManager.getConnection("jdbc:duckdb:");
```

To use DuckDB-specific features such as the [Appender](#appender), cast the object to a `DuckDBConnection`:

```java
import java.sql.DriverManager;
import org.duckdb.DuckDBConnection;

DuckDBConnection conn = (DuckDBConnection) DriverManager.getConnection("jdbc:duckdb:");
```

When using the `jdbc:duckdb:`  URL alone, an **in-memory database** is created. Note that for an in-memory database no data is persisted to disk (i.e., all data is lost when you exit the Java program). If you would like to access or create a persistent database, append its file name after the path. For example, if your database is stored in `/tmp/my_database`, use the JDBC URL `jdbc:duckdb:/tmp/my_database` to create a connection to it.

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

Configuration options can be provided to change different settings of the database system. Note that many of these
settings can be changed later on using [`PRAGMA` statements]({% link docs/current/configuration/pragmas.md %}) as well.

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
| `jdbc_stream_results` | Stream result sets instead of materializing them. See [Streaming Results](#streaming-results). |
| `jdbc_auto_commit` | Set the default auto-commit mode for new connections. |
| `jdbc_pin_db` | Keep the database instance alive after its last connection closes. Defaults to `true` for in-memory databases. |
| `jdbc_instance_cache` | Reuse a single database instance across connections that open the same file. |
| `jdbc_ignore_unsupported_options` | Silently ignore unsupported connection options instead of throwing an error. |
| `jdbc_jfr_memory_monitor` | Enable JFR memory monitoring for the connection's database instance. See [Memory Monitoring with JFR](#memory-monitoring-with-jfr). |

These properties can be passed in the `Properties` object or appended to the JDBC URL after a semicolon, for example `jdbc:duckdb:/tmp/my_database;jdbc_stream_results=true`.

### Querying

DuckDB supports the standard JDBC methods to send queries and retrieve result sets. First a `Statement` object has to be created from the `Connection`, this object can then be used to send queries using `execute` and `executeQuery`. `execute()` is meant for queries where no results are expected like `CREATE TABLE` or `UPDATE` etc. and `executeQuery()` is meant to be used for queries that produce results (e.g., `SELECT`). Below two examples. See also the JDBC [`Statement`](https://docs.oracle.com/javase/7/docs/api/java/sql/Statement.html) and [`ResultSet`](https://docs.oracle.com/javase/7/docs/api/java/sql/ResultSet.html) documentations.

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

Connection conn = DriverManager.getConnection("jdbc:duckdb:");

// create a table
Statement stmt = conn.createStatement();
stmt.execute("CREATE TABLE items (item VARCHAR, value DECIMAL(10, 2), count INTEGER)");
// insert two items into the table
stmt.execute("INSERT INTO items VALUES ('jeans', 20.0, 1), ('hammer', 42.2, 2)");

try (ResultSet rs = stmt.executeQuery("SELECT * FROM items")) {
    while (rs.next()) {
        System.out.println(rs.getString(1));
        System.out.println(rs.getInt(3));
    }
}
stmt.close();
```

```text
jeans
1
hammer
2
```

DuckDB also supports prepared statements as per the JDBC API:

```java
import java.sql.PreparedStatement;

try (PreparedStatement stmt = conn.prepareStatement("INSERT INTO items VALUES (?, ?, ?);")) {
    stmt.setString(1, "chainsaw");
    stmt.setDouble(2, 500.0);
    stmt.setInt(3, 42);
    stmt.execute();
    // more calls to execute() possible
}
```

> Warning Do *not* use prepared statements to insert large amounts of data into DuckDB. See the [data import documentation]({% link docs/current/data/overview.md %}) for better options.

### Reading Nested and Composite Types

DuckDB's nested and composite types are read from a `ResultSet` with `getObject`, which returns an idiomatic Java object for each type:

<div class="monospace_table"></div>

| DuckDB type | Java type returned by `getObject` |
|--|--|
| `LIST`, `ARRAY` | `org.duckdb.DuckDBArray` (implements `java.sql.Array`) |
| `STRUCT` | `org.duckdb.DuckDBStruct` (implements `java.sql.Struct`) |
| `MAP` | `java.util.LinkedHashMap` |
| `UNION` | the resolved member value |
| `ENUM` | `String` |

```java
try (ResultSet rs = stmt.executeQuery("SELECT [1, 2, 3] AS l, {'a': 1, 'b': 2} AS s")) {
    while (rs.next()) {
        DuckDBArray list = (DuckDBArray) rs.getObject(1);
        Object[] values = (Object[]) list.getArray();

        DuckDBStruct struct = (DuckDBStruct) rs.getObject(2);
        Map<String, Object> fields = struct.getMap();
    }
}
```

The DuckDB result set also exposes typed accessors as extensions to the JDBC API, including `getArray(int)`, `getStruct(int)`, `getUuid(int)`, `getHugeint(int)`, and `getJsonObject(int)`. `DuckDBStruct.getMap()` returns the struct fields keyed by name, and `DuckDBArray.getResultSet()` exposes the list elements as an index and value result set.

### Arrow Methods

Refer to the [API Reference](https://javadoc.io/doc/org.duckdb/duckdb_jdbc/latest/org/duckdb/DuckDBResultSet.html#arrowExportStream(java.lang.Object,long)) for type signatures

#### Arrow Export

The following demonstrates exporting an arrow stream and consuming it using the java arrow bindings

```java
import org.apache.arrow.memory.RootAllocator;
import org.apache.arrow.vector.ipc.ArrowReader;
import org.duckdb.DuckDBResultSet;

try (var conn = DriverManager.getConnection("jdbc:duckdb:");
    var stmt = conn.prepareStatement("SELECT * FROM generate_series(2000)");
    var resultset = (DuckDBResultSet) stmt.executeQuery();
    var allocator = new RootAllocator()) {
    try (var reader = (ArrowReader) resultset.arrowExportStream(allocator, 256)) {
        while (reader.loadNextBatch()) {
            System.out.println(reader.getVectorSchemaRoot().getVector("generate_series"));
        }
    }
    stmt.close();
}
```

#### Arrow Import

The following demonstrates consuming an Arrow stream from the Java Arrow bindings.

```java
import org.apache.arrow.memory.RootAllocator;
import org.apache.arrow.vector.ipc.ArrowReader;
import org.duckdb.DuckDBConnection;

// Arrow binding
try (var allocator = new RootAllocator();
     ArrowStreamReader reader = null; // should not be null of course
     var arrow_array_stream = ArrowArrayStream.allocateNew(allocator)) {
    Data.exportArrayStream(allocator, reader, arrow_array_stream);

    // DuckDB setup
    try (var conn = (DuckDBConnection) DriverManager.getConnection("jdbc:duckdb:")) {
        conn.registerArrowStream("asdf", arrow_array_stream);

        // run a query
        try (var stmt = conn.createStatement();
             var rs = (DuckDBResultSet) stmt.executeQuery("SELECT count(*) FROM asdf")) {
            while (rs.next()) {
                System.out.println(rs.getInt(1));
            }
        }
    }
}
```

### Streaming Results

Result streaming is opt-in in the JDBC driver. Enable it by setting the `jdbc_stream_results` config to `true` before running a query. The easiest way to do that is to pass it in the `Properties` object.

```java
Properties props = new Properties();
props.setProperty(DuckDBDriver.JDBC_STREAM_RESULTS, String.valueOf(true));

Connection conn = DriverManager.getConnection("jdbc:duckdb:", props);
```

### Appender

The [Appender]({% link docs/current/data/appender.md %}) is available in the DuckDB JDBC driver via the `org.duckdb.DuckDBAppender` class.
The constructor of the class requires the schema name and the table name it is applied to.
The Appender is flushed when the `close()` method is called.

Example:

```java
import java.sql.DriverManager;
import java.sql.Statement;
import org.duckdb.DuckDBConnection;

DuckDBConnection conn = (DuckDBConnection) DriverManager.getConnection("jdbc:duckdb:");
try (var stmt = conn.createStatement()) {
    stmt.execute("CREATE TABLE tbl (x BIGINT, y FLOAT, s VARCHAR)"
);

// using try-with-resources to automatically close the appender at the end of the scope
try (var appender = conn.createAppender(DuckDBConnection.DEFAULT_SCHEMA, "tbl")) {
    appender.beginRow();
    appender.append(10);
    appender.append(3.2);
    appender.append("hello");
    appender.endRow();
    appender.beginRow();
    appender.append(20);
    appender.append(-8.1);
    appender.append("world");
    appender.endRow();
}
```

### Batch Writer

The DuckDB JDBC driver offers batch write functionality.
The batch writer supports prepared statements to mitigate the overhead of query parsing.

> The preferred method for bulk inserts is to use the [Appender](#appender) due to its higher performance.
> However, when using the Appender is not possible, the batch writer is available as alternative.

#### Batch Writer with Prepared Statements

```java
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import org.duckdb.DuckDBConnection;

DuckDBConnection conn = (DuckDBConnection) DriverManager.getConnection("jdbc:duckdb:");
PreparedStatement stmt = conn.prepareStatement("INSERT INTO test (x, y, z) VALUES (?, ?, ?);");

stmt.setObject(1, 1);
stmt.setObject(2, 2);
stmt.setObject(3, 3);
stmt.addBatch();

stmt.setObject(1, 4);
stmt.setObject(2, 5);
stmt.setObject(3, 6);
stmt.addBatch();

stmt.executeBatch();
stmt.close();
```

#### Batch Writer with Vanilla Statements

The batch writer also supports vanilla SQL statements:

```java
import java.sql.DriverManager;
import java.sql.Statement;
import org.duckdb.DuckDBConnection;

DuckDBConnection conn = (DuckDBConnection) DriverManager.getConnection("jdbc:duckdb:");
Statement stmt = conn.createStatement();

stmt.execute("CREATE TABLE test (x INTEGER, y INTEGER, z INTEGER)");

stmt.addBatch("INSERT INTO test (x, y, z) VALUES (1, 2, 3);");
stmt.addBatch("INSERT INTO test (x, y, z) VALUES (4, 5, 6);");

stmt.executeBatch();
stmt.close();
```

## Troubleshooting

### Driver Class Not Found

If the Java application is unable to find the DuckDB driver, it may throw the following error:

```console
Exception in thread "main" java.sql.SQLException: No suitable driver found for jdbc:duckdb:
    at java.sql/java.sql.DriverManager.getConnection(DriverManager.java:706)
    at java.sql/java.sql.DriverManager.getConnection(DriverManager.java:252)
    ...
```

And when trying to load the class manually, it may result in this error:

```console
Exception in thread "main" java.lang.ClassNotFoundException: org.duckdb.DuckDBDriver
    at java.base/jdk.internal.loader.BuiltinClassLoader.loadClass(BuiltinClassLoader.java:641)
    at java.base/jdk.internal.loader.ClassLoaders$AppClassLoader.loadClass(ClassLoaders.java:188)
    at java.base/java.lang.ClassLoader.loadClass(ClassLoader.java:520)
    at java.base/java.lang.Class.forName0(Native Method)
    at java.base/java.lang.Class.forName(Class.java:375)
    ...
```

These errors stem from the DuckDB Maven/Gradle dependency not being detected. To ensure that it is detected, force refresh the Maven configuration in your IDE.
