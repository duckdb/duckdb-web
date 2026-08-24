---
layout: docu
redirect_from:
- /docs/clients/java/data_import
- /docs/preview/clients/java/data_import
- /docs/stable/clients/java/data_import
title: Import Data
---

## Overview

The JDBC driver offers two ways to load data into DuckDB in bulk: the high-performance [Appender](#appender) and a JDBC batch writer. This page describes both and when to use each.

## Appender

The [Appender]({% link docs/current/data/appender.md %}) is available in the DuckDB JDBC driver via the `org.duckdb.DuckDBAppender` class.
An appender is created from a `DuckDBConnection` with the `createAppender()` method, passing the table name and, optionally, the schema and catalog it is applied to.
The Appender is flushed when the `close()` method is called.

Example:

```java
import java.sql.DriverManager;
import org.duckdb.DuckDBConnection;

DuckDBConnection conn = (DuckDBConnection) DriverManager.getConnection("jdbc:duckdb:");
try (var stmt = conn.createStatement()) {
    stmt.execute("CREATE TABLE tbl (x INTEGER, y DOUBLE, s VARCHAR)");

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
}
```

An appender can also be created with `createAppender(tableName)` for the default schema, or with `createAppender(catalogName, schemaName, tableName)` to target a specific catalog. Buffered rows are written to the table when the appender is closed, or earlier by calling `flush()`. Within a row, `appendNull()` writes a `NULL` and `appendDefault()` writes the column's `DEFAULT` value.

Nested and collection types are appended within a row as well. For a `STRUCT` column, call `beginStruct()`, append each field value in declaration order, then `endStruct()`. For a `UNION` column, call `beginUnion(tag)` — where `tag` is the name of the target `UNION` member — append that member's value, then `endUnion()`. The following row targets a table declared as `CREATE TABLE nested_tbl (point STRUCT(x INTEGER, y INTEGER), value UNION(num INTEGER, str VARCHAR))`:

```java
try (var appender = conn.createAppender("nested_tbl")) {
    appender.beginRow();
    appender.beginStruct();      // enter the STRUCT column
    appender.append(1);          // field x
    appender.append(2);          // field y
    appender.endStruct();
    appender.beginUnion("str");  // select the UNION member named "str"
    appender.append("hello");    // its VARCHAR value
    appender.endUnion();
    appender.endRow();
}
```

For a `LIST` or `ARRAY` column, pass a Java array as a single value, optionally with a boolean null mask where `true` marks the corresponding element as `NULL`:

```java
try (var appender = conn.createAppender("list_tbl")) {
    appender.beginRow();
    appender.append(new int[] {1, 2, 3});               // a LIST value
    appender.append(new int[] {4, 5}, new boolean[] {false, true}); // second element is NULL
    appender.endRow();
}
```

For a `MAP` column, pass a Java `Map` as a single value; each entry is written as a key/value pair, and a `null` map is appended as SQL `NULL`. The following row targets a table declared as `CREATE TABLE map_tbl (m MAP(VARCHAR, INTEGER))`:

```java
try (var appender = conn.createAppender("map_tbl")) {
    appender.beginRow();
    appender.append(Map.of("a", 1, "b", 2));            // a MAP value
    appender.endRow();
}
```

### Maximizing Appender Performance

The Appender is already the fastest way to bulk-load data, but a few properties of how it works determine its throughput:

* **Row batching is fixed and internal.** The Appender writes rows in fixed-size batches of 2,048 rows, one DuckDB vector, and flushes a batch automatically as soon as it fills. There is no configurable flush count, so adding an application-level batch size on top of the Appender does not improve performance.
* **Prefer primitive columns over complex types.** Nested types such as `STRUCT`, `LIST`, and `UNION` cost more per value than flat, primitive columns. A schema built from primitive columns appends fastest.
* **Avoid allocating a Java object per row.** Boxing values or constructing a new object for every row adds allocation and garbage-collection pressure. Prefer the primitive `append()` overloads and reuse buffers where you can.
* **Keep strings short where possible.** DuckDB stores strings of up to 12 bytes inline; longer strings are stored out of line and add a small overhead per value.

### Single-Value Appender (Legacy)

An earlier appender, `org.duckdb.DuckDBSingleValueAppender`, created with `DuckDBConnection.createSingleValueAppender()`, writes one value at a time with typed `append()` overloads between `beginRow()` and `endRow()`. Both the class and the factory method are deprecated and retained only for backward compatibility.

> Warning New code should use the `DuckDBAppender` described above, which is faster and appends nested and collection types. `DuckDBSingleValueAppender` is kept only for existing applications.

## Batch Writer

The DuckDB JDBC driver offers batch write functionality.
The batch writer supports prepared statements to mitigate the overhead of query parsing.

> The preferred method for bulk inserts is to use the [Appender](#appender) due to its higher performance.
> However, when using the Appender is not possible, the batch writer is available as an alternative.

### Batch Writer with Prepared Statements

Prepared statements are the recommended way to use the batch writer, because the statement is parsed once and reused for every row. Bind each row's parameters, call `addBatch()` to queue the row, and call `executeBatch()` to write all queued rows in a single operation.

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

### Batch Writer with Vanilla Statements

The batch writer also accepts plain SQL statements that carry their values inline, without parameters. Queue each statement with `addBatch(String)` and submit them together with `executeBatch()`. This avoids parameter binding but does not benefit from the reuse that prepared statements provide.

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

## Further Reading

* [Appender]({% link docs/current/data/appender.md %}) — the engine-level Appender interface that the Java `DuckDBAppender` wraps.
* [Data Import]({% link docs/current/data/overview.md %}) — DuckDB's other bulk-loading options, including reading directly from CSV, Parquet, and JSON files.
* [Run Queries]({% link docs/current/clients/java/querying.md %}) — sending the [`INSERT`]({% link docs/current/sql/statements/insert.md %}) and [`CREATE TABLE`]({% link docs/current/sql/statements/create_table.md %}) statements the batch writer builds on.
* [Define Connections]({% link docs/current/clients/java/connecting.md %}) — obtaining the `DuckDBConnection` an Appender is created from.
