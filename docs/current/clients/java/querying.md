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

The DuckDB result set also exposes typed accessors as extensions to the JDBC API, including `getArray(int)`, `getStruct(int)`, `getUuid(int)`, `getHugeint(int)`, and `getJsonObject(int)`. `DuckDBStruct.getMap()` returns the struct fields keyed by name.

`DuckDBArray.getResultSet()` exposes the list elements as an `org.duckdb.DuckDBArrayResultSet`, a read-only `ResultSet` with two columns: `INDEX`, the 1-based position of the element, and `VALUE`, the element itself. Iterate it like any other result set:

```java
try (ResultSet rs = stmt.executeQuery("SELECT [10, 20, 30] AS l")) {
    rs.next();
    DuckDBArray list = (DuckDBArray) rs.getObject(1);
    try (ResultSet elements = list.getResultSet()) {
        while (elements.next()) {
            int index = elements.getInt("INDEX"); // 1-based position
            int value = elements.getInt("VALUE"); // the element
            System.out.println(index + " -> " + value);
        }
    }
}
```

A `JSON` column is returned by `getObject(int)` (and `getJsonObject(int)`) as an `org.duckdb.JsonNode`, a lightweight wrapper over the raw JSON text. Test its type with `isArray()`, `isObject()`, `isString()`, `isNumber()`, `isBoolean()`, and `isNull()`, and recover the JSON source with `toString()`:

```java
try (ResultSet rs = stmt.executeQuery("SELECT '[1, 2, 3]'::JSON AS j")) {
    rs.next();
    JsonNode json = (JsonNode) rs.getObject(1);
    if (json.isArray()) {
        System.out.println(json); // [1, 2, 3]
    }
}
```

## Binding Nested and Composite Parameters

To bind a `LIST`/`ARRAY`, `STRUCT`, or `MAP` value as a prepared-statement parameter, build it from the `Connection` and pass it to `setObject()`. Each factory method attaches the SQL type name the driver needs to marshal the value.

* `createArrayOf(typeName, elements)` — the standard JDBC method — returns an `org.duckdb.DuckDBUserArray` (a `java.sql.Array`) for a `LIST` or `ARRAY`, where `typeName` is the element type.
* `createStruct(typeName, attributes)` — the standard JDBC method — returns an `org.duckdb.DuckDBUserStruct` (a `java.sql.Struct`), where `typeName` is the `STRUCT` type and `attributes` are the field values in declaration order.
* `createMap(typeName, map)` — a DuckDB extension on `DuckDBConnection` — returns an `org.duckdb.DuckDBMap` (a `java.util.Map`) for a `MAP`, where `typeName` is the full map type such as `MAP(VARCHAR, INTEGER)`.

```java
import java.sql.Array;
import java.sql.Struct;
import java.util.Map;
import org.duckdb.DuckDBConnection;

DuckDBConnection conn = (DuckDBConnection) DriverManager.getConnection("jdbc:duckdb:");

// LIST / ARRAY
Array list = conn.createArrayOf("INTEGER", new Object[] {1, 2, 3});
try (PreparedStatement stmt = conn.prepareStatement("SELECT ?::INTEGER[]")) {
    stmt.setObject(1, list);
    stmt.execute();
}

// STRUCT
Struct point = conn.createStruct("STRUCT(x DOUBLE, y DOUBLE)", new Object[] {1.0, 2.0});

// MAP
Map<String, Integer> counts = conn.createMap("MAP(VARCHAR, INTEGER)", Map.of("a", 1, "b", 2));
```

### Binding Spatial Values

The [`spatial` extension]({% link docs/current/core_extensions/spatial/overview.md %}) builds its geometry types from `STRUCT` and `LIST` types, so they are bound with the same factory methods. A `POINT_2D` is a struct of two `DOUBLE` fields, and a `LINESTRING` is a list of such points. After loading the extension, build the value with `createStruct()` (or `createArrayOf()`) and cast the parameter to `GEOMETRY`; a `GEOMETRY` result comes back as Well-Known Binary through `getBlob()`:

```java
try (Statement stmt = conn.createStatement()) {
    stmt.execute("INSTALL spatial");
    stmt.execute("LOAD spatial");
}

// POINT_2D is a STRUCT(x DOUBLE, y DOUBLE)
Struct point = conn.createStruct("POINT_2D", new Object[] {41.1, 42.2});
try (PreparedStatement stmt = conn.prepareStatement("SELECT ?::POINT_2D::GEOMETRY")) {
    stmt.setObject(1, point);
    try (ResultSet rs = stmt.executeQuery()) {
        rs.next();
        Blob wkb = rs.getBlob(1); // the geometry as Well-Known Binary
    }
}

// A LINESTRING is a LIST of POINT_2D structs
Struct p1 = conn.createStruct("POINT_2D", new Object[] {0.0, 0.0});
Struct p2 = conn.createStruct("POINT_2D", new Object[] {1.0, 1.0});
Array line = conn.createArrayOf("POINT_2D", new Object[] {p1, p2});
```

## Binding Temporal Parameters

Date and time parameters follow the same `setObject()` path. When you bind a `java.time` or `java.sql` temporal value, the driver wraps it in the matching internal holder — `java.sql.Date`/`LocalDate` become an `org.duckdb.DuckDBDate`, `Timestamp`/`LocalDateTime` become a `DuckDBTimestamp`, `OffsetDateTime` becomes a `DuckDBTimestampTZ`, and `Time`/`LocalTime` become a `DuckDBTime` — and marshals it to the corresponding DuckDB type:

```java
import java.time.LocalDate;
import java.time.LocalDateTime;

try (PreparedStatement stmt = conn.prepareStatement("SELECT ?, ?")) {
    stmt.setObject(1, LocalDate.of(2024, 1, 15));
    stmt.setObject(2, LocalDateTime.of(2024, 1, 15, 12, 30));
    stmt.execute();
}
```

Each holder keeps its value relative to the Unix epoch (`1970-01-01`): `DuckDBDate` counts whole days through `getDaysSinceEpoch()`, while `DuckDBTimestamp`, `DuckDBTimestampTZ`, and `DuckDBTime` report microseconds through `getMicrosEpoch()` (for `DuckDBTime`, microseconds since midnight):

```java
import java.sql.Date;
import java.sql.Time;
import java.sql.Timestamp;
import java.time.OffsetDateTime;
import org.duckdb.DuckDBDate;
import org.duckdb.DuckDBTime;
import org.duckdb.DuckDBTimestamp;
import org.duckdb.DuckDBTimestampTZ;

long days = new DuckDBDate(Date.valueOf("2024-01-15")).getDaysSinceEpoch();                     // 19737
long micros = new DuckDBTimestamp(Timestamp.valueOf("2024-01-15 12:30:00")).getMicrosEpoch();
long zonedMicros = new DuckDBTimestampTZ(OffsetDateTime.parse("2024-01-15T12:30:00Z")).getMicrosEpoch();
long timeMicros = new DuckDBTime(Time.valueOf("12:30:00")).getMicrosEpoch();
```

## Inspecting Metadata

The driver implements the standard JDBC metadata interfaces, so an application can introspect the database, a result set, or a prepared statement's parameters without running catalog queries by hand.

* `Connection.getMetaData()` returns an `org.duckdb.DuckDBDatabaseMetaData`, a `java.sql.DatabaseMetaData` that reports database-wide capabilities and exposes catalog objects such as `getTables()`, `getColumns()`, and `getSchemas()` as result sets built from DuckDB's system tables.
* `ResultSet.getMetaData()` returns an `org.duckdb.DuckDBResultSetMetaData` describing the result columns — `getColumnCount()`, `getColumnName(int)`, `getColumnType(int)`, `getColumnTypeName(int)`, `getPrecision(int)`, and `getScale(int)`.
* `PreparedStatement.getParameterMetaData()` returns an `org.duckdb.DuckDBParameterMetaData` describing the statement's parameters (1-based), including `getParameterCount()`, `getParameterType(int)`, and `getParameterTypeName(int)`.

```java
try (PreparedStatement stmt = conn.prepareStatement("SELECT * FROM items WHERE value > ?")) {
    stmt.setDouble(1, 10.0);
    ResultSetMetaData rsMeta = stmt.getMetaData();
    for (int i = 1; i <= rsMeta.getColumnCount(); i++) {
        System.out.println(rsMeta.getColumnName(i) + " : " + rsMeta.getColumnTypeName(i));
    }
    System.out.println("parameters: " + stmt.getParameterMetaData().getParameterCount());
}
```

As a DuckDB extension, `DuckDBResultSetMetaData.getReturnType()` reports what a statement returns as an `org.duckdb.StatementReturnType` — `QUERY_RESULT`, `CHANGED_ROWS`, or `NOTHING`:

```java
import org.duckdb.DuckDBResultSetMetaData;
import org.duckdb.StatementReturnType;

DuckDBResultSetMetaData meta = (DuckDBResultSetMetaData) rs.getMetaData();
StatementReturnType returnType = meta.getReturnType(); // QUERY_RESULT
```

For a `DECIMAL` column, `getPrecision(int)` and `getScale(int)` report the width and scale that DuckDB records for the type in a `DuckDBColumnTypeMetaData`. For the `value DECIMAL(10, 2)` column of the `items` table, they return `10` and `2`:

```java
try (ResultSet rs = stmt.executeQuery("SELECT value FROM items")) {
    ResultSetMetaData rsMeta = rs.getMetaData();
    int precision = rsMeta.getPrecision(1); // 10
    int scale = rsMeta.getScale(1);         // 2
    System.out.println("DECIMAL(" + precision + ", " + scale + ")");
}
```

## Further Reading

* [Handle Results]({% link docs/current/clients/java/result_handling.md %}) — Apache Arrow interchange, result streaming, and chunked results beyond the standard `ResultSet`.
* [Import Data]({% link docs/current/clients/java/data_import.md %}) — the Appender and batch writer, the recommended alternatives to prepared statements for bulk inserts.
* [Prepared Statements]({% link docs/current/sql/query_syntax/prepared_statements.md %}) — DuckDB's SQL-level support for the parameterized queries used here.
* [Define Connections]({% link docs/current/clients/java/connecting.md %}) — opening the `Connection` that these statements run on.
