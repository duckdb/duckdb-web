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

### Chunked Results

The JDBC driver can return a query result as a lazily fetched sequence of columnar data chunks via the `org.duckdb.DuckDBChunkedResult` class.
This exposes the C API's `duckdb_fetch_chunk` function to Java and avoids the per-row overhead required by the JDBC `ResultSet` interface.
Chunk contents are read through the same `DuckDBDataChunkReader` API that is used by [user-defined functions](https://github.com/duckdb/duckdb-java/blob/main/UDF.MD).

Call `query()` on a `DuckDBPreparedStatement` to obtain a `DuckDBChunkedResult`, then advance through the chunks with `nextChunk()` and read each column vector by index.

Example:

```java
import java.sql.DriverManager;
import org.duckdb.DuckDBConnection;
import org.duckdb.DuckDBPreparedStatement;
import org.duckdb.DuckDBChunkedResult;
import org.duckdb.DuckDBDataChunkReader;
import org.duckdb.DuckDBReadableVector;

try (DuckDBConnection conn = DriverManager
        .getConnection("jdbc:duckdb:")
        .unwrap(DuckDBConnection.class);
     DuckDBPreparedStatement ps = conn.prepare("SELECT ? AS col1")) {

    // statement parameters are 1-based
    ps.setInt(1, 42);

    try (DuckDBChunkedResult res = ps.query()) {

        // advance to the next chunk, returns true on success
        while (res.nextChunk()) {

            // get the current chunk from the result
            DuckDBDataChunkReader chunk = res.chunk();

            // iterate over the chunk columns, all indices are 0-based
            for (long col = 0; col < chunk.columnCount(); col++) {

                // get a vector for the specified column
                DuckDBReadableVector vector = chunk.vector(col);

                // iterate over the vector rows
                for (long row = 0; row < chunk.rowCount(); row++) {
                    int val = vector.getInt(row);
                    System.out.println(val);
                }
            }
        }
    }
}
```

Statement parameters remain 1-based, following the JDBC convention, while chunk columns and rows are 0-based, matching the C API and the user-defined function interfaces.

> The chunked result API currently supports basic data types only. Composite types such as `LIST` and `STRUCT` are not yet readable through this interface. The `query()` method is available on prepared statements only; there is no `query(String)` overload.

### Appender

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

## User-Defined Functions

The JDBC driver can register user-defined functions (UDFs) written in Java, including scalar functions and table functions. This section covers the common cases. For the full API, including the vectorized interface and the function registry, see the [`UDF.MD` guide](https://github.com/duckdb/duckdb-java/blob/main/UDF.MD).

### Scalar Functions

Build a scalar function with the `DuckDBFunctions.scalarFunction()` builder and register it on a connection with `register()`. Once registered, the function can be called from SQL by the name passed to `withName()`.

```java
import java.sql.Connection;
import java.sql.DriverManager;
import org.duckdb.DuckDBColumnType;
import org.duckdb.DuckDBFunctions;
import org.duckdb.DuckDBLogicalType;

try (Connection conn = DriverManager.getConnection("jdbc:duckdb:");
     DuckDBLogicalType intType = DuckDBLogicalType.of(DuckDBColumnType.INTEGER)) {
    DuckDBFunctions.scalarFunction()
        .withName("java_sum_varargs")
        .withParameter(Integer.class) // fixed argument
        .withVarArgs(intType)         // variadic argument type
        .withReturnType(Integer.class)
        .withVarArgsFunction(args -> {
            int sum = 0;
            for (Object arg : args) {
                sum += (Integer) arg;
            }
            return sum;
        })
        .register(conn);
}
```

The registered function is then available in SQL:

```sql
SELECT java_sum_varargs(1, 2, 3, 4);
```

For a fixed number of arguments, use `withParameter()` (or `withParameters()`) together with `withFunction()`. For variable arguments, call `withVarArgs()` to declare the element type and `withVarArgsFunction()` to supply the implementation. Callbacks that take object arguments receive `null` for SQL `NULL` inputs.

#### Vectorized Scalar Functions

The examples above process one value per call. To process a whole batch of rows at once, register a `DuckDBScalarFunction` with `withVectorizedFunction()`. The callback receives the input as a `DuckDBDataChunkReader` (up to 2,048 rows) and writes results into a `DuckDBWritableVector`. Read each input column with `input.vector(columnIndex)`, iterate the row indices with `input.stream()`, and write each result at the same row index. This is the scalar-function counterpart to reading query results with [chunked results](#chunked-results).

```java
try (Connection conn = DriverManager.getConnection("jdbc:duckdb:");
     DuckDBLogicalType tsType = DuckDBLogicalType.of(DuckDBColumnType.TIMESTAMP);
     DuckDBLogicalType strType = DuckDBLogicalType.of(DuckDBColumnType.VARCHAR);
     DuckDBLogicalType dblType = DuckDBLogicalType.of(DuckDBColumnType.DOUBLE)) {
    DuckDBFunctions.scalarFunction()
        .withName("java_event_label")
        .withParameters(tsType, strType, dblType)
        .withReturnType(strType)
        .withVectorizedFunction((input, output) -> {
            input.stream().forEach(row -> {
                String value = input.vector(0).getLocalDateTime(row) + " | " +
                               String.valueOf(input.vector(1).getString(row)).trim().toUpperCase() + " | " +
                               input.vector(2).getDouble(row, 0.0d);
                output.setString(row, value);
            });
        })
        .register(conn);
}
```

```sql
SELECT java_event_label(TIMESTAMP '2026-04-04 12:00:00', 'launch', 4.5);
```

The reader, vector, and writer objects are valid only during callback execution and must not be retained.

### Table Functions

Build a table function with the `DuckDBFunctions.tableFunction()` builder. The implementation is a `DuckDBTableFunction` with three main callbacks:

* `bind` runs when the statement is prepared. It registers the output columns with `addResultColumn()` and reads the call parameters. It may return bind data that is passed to the later callbacks.
* `init` runs once before execution and returns the global state.
* `apply` writes rows into the output vectors and returns the number of rows written. The engine calls it repeatedly until it returns `0`.

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.util.concurrent.atomic.AtomicBoolean;
import org.duckdb.DuckDBFunctions;
import org.duckdb.DuckDBTableFunction;
import org.duckdb.DuckDBTableFunctionBindInfo;
import org.duckdb.DuckDBTableFunctionInitInfo;
import org.duckdb.DuckDBTableFunctionCallInfo;
import org.duckdb.DuckDBDataChunkWriter;
import org.duckdb.DuckDBValue;

try (Connection conn = DriverManager.getConnection("jdbc:duckdb:")) {
    DuckDBFunctions.tableFunction()
        .withName("java_table_basic")
        .withParameter(int.class)
        .withNamedParameter("param1", String.class)
        .withFunction(new DuckDBTableFunction<Integer, AtomicBoolean, Object>() {
            @Override
            public Integer bind(DuckDBTableFunctionBindInfo info) throws Exception {
                info.addResultColumn("col1", Integer.TYPE)
                    .addResultColumn("col2", String.class);
                DuckDBValue param = info.getParameter(0);
                return param.getInt();
            }

            @Override
            public AtomicBoolean init(DuckDBTableFunctionInitInfo info) throws Exception {
                return new AtomicBoolean(false);
            }

            @Override
            public long apply(DuckDBTableFunctionCallInfo info, DuckDBDataChunkWriter output) throws Exception {
                Integer bindData = info.getBindData();
                AtomicBoolean done = info.getInitData();
                if (done.get()) {
                    return 0;
                }
                output.vector(0).setInt(0, bindData);
                output.vector(1).setString(0, "foo");
                output.vector(0).setNull(1);
                output.vector(1).setString(1, "bar");
                done.set(true);
                return 2;
            }
        })
        .register(conn);
}
```

The generic type parameters of `DuckDBTableFunction` are, in order, the bind data, the global init data, and the local init data. Call the function from SQL:

```sql
FROM java_table_basic(42, param1 = 'foobar');
```

Rows are written through a `DuckDBDataChunkWriter`, the write-side counterpart to the [`DuckDBDataChunkReader`](#chunked-results) used for reading results. Each output vector is addressed by column index, and values are set by row index with methods such as `setInt()`, `setString()`, and `setNull()`.

#### Cleaning up Resources

A state that owns a resource can implement `DuckDBTableFunctionState` to receive a deterministic `close()` call once DuckDB no longer needs it:

```java
final class SourceState implements DuckDBTableFunctionState {
    private final AutoCloseable resource;

    SourceState(AutoCloseable resource) {
        this.resource = resource;
    }

    @Override
    public void close() throws Exception {
        resource.close();
    }
}
```

DuckDB calls `close()` after the function is exhausted, after a `LIMIT`, or on an error, cancellation, or early JDBC close. Cleanup may run on native worker threads with no ordering guarantees, so `close()` should be fast, idempotent, and thread-safe. It must not run SQL or reuse the same connection, and any exception it throws is not propagated to the query. A state that only implements `AutoCloseable`, or a `null` state, is left untouched.

#### Parallel Execution

To run a table function on multiple threads, set the thread count with `info.setMaxThreads()` in the `init` callback. Parallel output may also require `preserve_insertion_order = false`, set in the connection string or the connection properties.

### Type Mapping

When a UDF declares parameters or a return type using a Java `Class`, the driver maps it to a DuckDB type as follows:

<div class="monospace_table"></div>

| Java type | DuckDB type |
|--|--|
| `int` | `INTEGER` |
| `long` | `BIGINT` |
| `float` | `FLOAT` |
| `double` | `DOUBLE` |
| `String` | `VARCHAR` |
| `BigDecimal` | `DECIMAL` |
| `BigInteger` | `HUGEINT` |
| `LocalDate`, `java.sql.Date` | `DATE` |
| `LocalDateTime`, `java.sql.Timestamp`, `java.util.Date` | `TIMESTAMP` |

For types without a direct Java mapping, declare the type explicitly with `DuckDBColumnType` or `DuckDBLogicalType`. For example, `UHUGEINT` requires an explicit `DuckDBColumnType.UHUGEINT` declaration, and `DuckDBLogicalType.decimal(width, scale)` sets an explicit `DECIMAL` precision and scale.

Composite types such as `LIST` and `STRUCT` are not currently supported in UDFs. Support for them is planned for a future release.

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
