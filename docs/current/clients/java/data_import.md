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

An appender can also be created with `createAppender(tableName)` for the default schema, or with `createAppender(catalogName, schemaName, tableName)` to target a specific catalog. Buffered rows are written to the table when the appender is closed, or earlier by calling `flush()`. Within a row, `appendNull()` writes a `NULL` and `appendDefault()` writes the column's `DEFAULT` value.

Nested and collection types are appended within a row as well. Use `beginStruct()` and `endStruct()` for a `STRUCT` column, and `beginUnion(tag)` and `endUnion()` for a `UNION` column. For a `LIST` or `ARRAY` column, pass a Java array as a single value, optionally with a boolean null mask for its elements:

```java
try (var appender = conn.createAppender("list_tbl")) {
    appender.beginRow();
    appender.append(new int[] {1, 2, 3});               // a LIST value
    appender.append(new int[] {4, 5}, new boolean[] {false, true}); // second element is NULL
    appender.endRow();
}
```

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
