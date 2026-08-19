---
layout: docu
redirect_from:
- /docs/clients/java/functions
- /docs/preview/clients/java/functions
- /docs/stable/clients/java/functions
title: Define Functions
---

## Overview

The JDBC driver can register user-defined functions (UDFs) written in Java, including scalar functions and table functions. This page covers the common cases.

> Note For the full API, including the vectorized interface and the function registry, see the [`UDF.MD` guide](https://github.com/duckdb/duckdb-java/blob/main/UDF.MD).

## Scalar Functions

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

### Vectorized Scalar Functions

The examples above process one value per call. To process a whole batch of rows at once, register a `DuckDBScalarFunction` with `withVectorizedFunction()`. The callback receives the input as a `DuckDBDataChunkReader` (up to 2,048 rows) and writes results into a `DuckDBWritableVector`. Read each input column with `input.vector(columnIndex)`, iterate the row indices with `input.stream()`, and write each result at the same row index. This is the scalar-function counterpart to reading query results with [chunked results]({% link docs/current/clients/java/result_handling.md %}#chunked-results).

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

## Table Functions

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

Rows are written through a `DuckDBDataChunkWriter`, the write-side counterpart to the [`DuckDBDataChunkReader`]({% link docs/current/clients/java/result_handling.md %}#chunked-results) used for reading results. Each output vector is addressed by column index, and values are set by row index with methods such as `setInt()`, `setString()`, and `setNull()`.

### Cleaning up Resources

A table function may hold open resources such as files, sockets, or iterators that have to be released when the scan finishes. A state that owns such a resource can implement `DuckDBTableFunctionState` to receive a deterministic `close()` call once DuckDB no longer needs it:

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

### Parallel Execution

To run a table function on multiple threads, set the thread count with `info.setMaxThreads()` in the `init` callback. Parallel output may also require `preserve_insertion_order = false`, set in the connection string or the connection properties.

## Type Mapping

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
