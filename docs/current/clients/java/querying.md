---
layout: docu
redirect_from:
- /docs/clients/java/querying
- /docs/preview/clients/java/querying
- /docs/stable/clients/java/querying
title: Run Queries
---

## Overview

Java applications send queries and read result sets through the familiar `Statement`, `PreparedStatement`, and `ResultSet` interfaces. This page covers sending queries and reading DuckDB's nested and composite types. For opening the `Connection` these run on, see [Define Connections]({% link docs/current/clients/java/connecting.md %}).

## Sending Queries

DuckDB supports the standard JDBC methods to send queries and retrieve result sets. First a `Statement` object has to be created from the `Connection`, this object can then be used to send queries using `execute()` and `executeQuery()`. `execute()` is meant for queries where no results are expected like [`CREATE TABLE`]({% link docs/current/sql/statements/create_table.md %}) or [`UPDATE`]({% link docs/current/sql/statements/update.md %}) etc. and `executeQuery()` is meant to be used for queries that produce results (e.g., [`SELECT`]({% link docs/current/sql/statements/select.md %})). Below are two examples. See also the JDBC [`Statement`](https://docs.oracle.com/javase/7/docs/api/java/sql/Statement.html) and [`ResultSet`](https://docs.oracle.com/javase/7/docs/api/java/sql/ResultSet.html) documentations.

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
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

## Reading Nested and Composite Types

DuckDB supports nested and composite column types such as `LIST`, `STRUCT`, `MAP`, `UNION`, and `ENUM`. The JDBC driver maps each of these to an idiomatic Java object. Read the values from a `ResultSet` with `getObject`, which returns the following types:

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

## Further Reading

* [Handle Results]({% link docs/current/clients/java/result_handling.md %}) — Apache Arrow interchange, result streaming, and chunked results beyond the standard `ResultSet`.
* [Import Data]({% link docs/current/clients/java/data_import.md %}) — the Appender and batch writer, the recommended alternatives to prepared statements for bulk inserts.
* [Prepared Statements]({% link docs/current/sql/query_syntax/prepared_statements.md %}) — DuckDB's SQL-level support for the parameterized queries used here.
* [Define Connections]({% link docs/current/clients/java/connecting.md %}) — opening the `Connection` that these statements run on.
