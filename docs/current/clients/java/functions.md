---
layout: docu
redirect_from:
- /docs/clients/java/functions
- /docs/preview/clients/java/functions
- /docs/stable/clients/java/functions
title: Define Functions
---

## Overview

The JDBC driver can register user-defined functions (UDFs) written in Java, including scalar functions and table functions. This page covers building and registering both, from the simple functional-interface overloads to the vectorized interface, along with type mapping and the function registry.

## Scalar Functions

Build a scalar function with the `DuckDBFunctions.scalarFunction()` builder — which returns an `org.duckdb.DuckDBScalarFunctionBuilder` — and register it on a connection with `register()`. Once registered, the function can be called from SQL by the name passed to `withName()`. The builder is single-use: it is finalized once `register()` (or `close()`) is called.

The simplest functions map directly to a Java functional interface. Pick the overload that matches the number of arguments and, for primitives, their type:

* `withFunction(Supplier)`, `withFunction(Function)`, and `withFunction(BiFunction)` take zero, one, or two boxed (`Object`) arguments.
* `withIntFunction()`, `withLongFunction()`, and `withDoubleFunction()` take a unary or binary operator over `INTEGER`, `BIGINT`, or `DOUBLE` and avoid boxing.

```java
import java.sql.Connection;
import java.sql.DriverManager;
import org.duckdb.DuckDBFunctions;

try (Connection conn = DriverManager.getConnection("jdbc:duckdb:")) {
    DuckDBFunctions.scalarFunction()
        .withName("java_add_one")
        .withParameter(int.class)
        .withReturnType(int.class)
        .withIntFunction(x -> x + 1)
        .register(conn);
}
```

```sql
SELECT java_add_one(41);
```

The binary overloads take two arguments of the same type, declared with `withParameters()`:

```java
DuckDBFunctions.scalarFunction()
    .withName("java_weighted_sum")
    .withParameters(double.class, double.class)
    .withReturnType(double.class)
    .withDoubleFunction((x, w) -> x * w + 10.0)
    .register(conn);
```

```sql
SELECT java_weighted_sum(2.5, 4.0);
```

### Variadic Arguments

For a variable number of arguments, call `withVarArgs()` to declare the element type and `withVarArgsFunction()` to supply the implementation. The callback receives the variadic arguments as an `Object[]`. `withVarArgs()` has to be set before `withVarArgsFunction()`, and the object-argument `withFunction()` overloads cannot be combined with varargs.

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

```sql
SELECT java_sum_varargs(1, 2, 3, 4);
```

### NULL Handling

By default, a scalar function is called for every input row, including rows that contain SQL `NULL`:

* Callbacks that take `Object` arguments (`Function`, `BiFunction`, and the varargs form) receive `null` for a `NULL` input and may return `null` to produce a `NULL` result.
* The primitive callbacks (`withIntFunction()`, `withLongFunction()`, and `withDoubleFunction()`) are never handed a `null`. When DuckDB passes a `NULL`, the driver skips the Java call and writes `NULL` to the output automatically.

Call `withNullInNullOut()` to let the engine short-circuit *NULL in, NULL out*: it may skip the call and return `NULL` whenever an argument is `NULL`. The engine does not always take this shortcut, so an object callback should still check its arguments for `null`.

### Volatile Functions

DuckDB may treat a scalar function as deterministic and cache or constant-fold its result for repeated inputs. Call `withVolatile()` for a function whose output can change between calls with the same arguments — for example one that reads external state — so the engine evaluates it for every row.

### Error Handling

* Type and value errors raised while a callback reads its inputs or writes its result throw `DuckDBFunctions.FunctionException`, an unchecked `RuntimeException`.
* An out-of-range row or column index throws `IndexOutOfBoundsException`.
* Registration-time problems, such as an undefined return type or an invalid type declaration, throw `SQLException`.

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

The `DuckDBDataChunkReader`, its `DuckDBReadableVector` columns, and the `DuckDBWritableVector` are valid only during callback execution and must not be retained.

### Scalar Function Builder Methods

The `scalarFunction()` builder exposes the following methods:

* `withName(String)`
* `withParameter(Class<?> | DuckDBColumnType | DuckDBLogicalType)`
* `withParameters(Class<?>... | DuckDBColumnType... | DuckDBLogicalType...)`
* `withReturnType(Class<?> | DuckDBColumnType | DuckDBLogicalType)`
* `withFunction(Supplier | Function | BiFunction)`
* `withIntFunction(IntUnaryOperator | IntBinaryOperator)`
* `withLongFunction(LongUnaryOperator | LongBinaryOperator)`
* `withDoubleFunction(DoubleUnaryOperator | DoubleBinaryOperator)`
* `withVarArgs(DuckDBLogicalType)`
* `withVarArgsFunction(Function<Object[], ?>)`
* `withVectorizedFunction(DuckDBScalarFunction)`
* `withVolatile()`
* `withNullInNullOut()`
* `register(java.sql.Connection)`

## Table Functions

Build a table function with the `DuckDBFunctions.tableFunction()` builder, which returns an `org.duckdb.DuckDBTableFunctionBuilder`. Like the scalar builder, it is single-use and finalized on `register()` (or `close()`). The implementation is a `DuckDBTableFunction` with the following callbacks:

* `bind` runs when the statement is prepared. It registers the output columns with `addResultColumn()` and reads positional and named call parameters with `getParameter()` and `getNamedParameter()`. It may return bind data that is passed to the later callbacks.
* `init` runs once before execution and returns the global state.
* `localInit` (optional) runs once per execution thread and returns thread-local state. Override it when a [parallel scan](#parallel-execution) needs per-thread state; the default returns `null`.
* `apply` writes rows into the output vectors and returns the number of rows written, with access to the bind, global-init, and local-init data. The engine calls it repeatedly until it returns `0`.

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

All callback arguments, including the parameter and info objects, are valid only during callback execution and must not be retained. The Java table function interface mirrors DuckDB's [C API table functions]({% link docs/current/clients/c/api.md %}) as closely as possible.

### Producing Rows in Chunks

The example above writes every row in a single `apply` call, but a table function is not expected to. DuckDB calls `apply` repeatedly, each time passing a fresh output chunk that holds up to `output.capacity()` rows (2,048 by default). Fill up to that many rows, return how many you wrote, and DuckDB calls `apply` again for the next chunk until you return `0`. A cursor into the source therefore has to live in the init (or local-init) state so it survives across calls, rather than in a local variable.

The `apply` below streams a bounded integer series in chunks. It also dispatches on each column's declared type with `DuckDBWritableVector.getType()`, which is convenient when the same routine populates columns of different types:

```java
// Held in the init state so the position survives across apply() calls.
final class Series {
    long next;
    final long end;
    Series(long end) { this.end = end; }
}

DuckDBFunctions.tableFunction()
    .withName("java_series")
    .withParameter(long.class)
    .withFunction(new DuckDBTableFunction<Long, Series, Object>() {
        @Override
        public Long bind(DuckDBTableFunctionBindInfo info) throws Exception {
            info.addResultColumn("n", Long.TYPE)
                .addResultColumn("label", String.class);
            return info.getParameter(0).getLong();
        }

        @Override
        public Series init(DuckDBTableFunctionInitInfo info) throws Exception {
            return new Series(info.getBindData());
        }

        @Override
        public long apply(DuckDBTableFunctionCallInfo info, DuckDBDataChunkWriter output) throws Exception {
            Series cursor = info.getInitData();
            long row = 0;
            // Fill at most one chunk; DuckDB calls apply() again for the rest.
            for (; row < output.capacity() && cursor.next < cursor.end; row++, cursor.next++) {
                for (long col = 0; col < output.columnCount(); col++) {
                    DuckDBWritableVector vector = output.vector(col);
                    switch (vector.getType()) {
                        case BIGINT:  vector.setLong(row, cursor.next); break;
                        case VARCHAR: vector.setString(row, "row-" + cursor.next); break;
                        default:      vector.setNull(row);
                    }
                }
            }
            return row; // returning 0 tells DuckDB the scan is finished
        }
    })
    .register(conn);
```

Calling `FROM java_series(5000)` drives `apply` three times — two full 2,048-row chunks and a final partial one — before the fourth call returns `0`.

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

To run a table function on multiple threads, set the thread count with `info.setMaxThreads()` in the `init` callback. Parallel output may also require the [`preserve_insertion_order`]({% link docs/current/configuration/overview.md %}) option set to `false`, in the connection string or the connection properties.

### Projection Pushdown

By default a table function is asked to produce every column it declared in `bind`, even when the query selects only a few of them. Call `withProjectionPushdown()` on the builder to let DuckDB tell the function which columns are actually needed, so that `apply` can skip the work of filling the rest.

When pushdown is enabled, the `init` callback learns the projected columns from its `DuckDBTableFunctionInitInfo`: `getColumnCount()` returns the number of columns the query requires, and `getColumnIndex(position)` maps each projected position back to the column index used in `bind` and in the output vectors. Store this mapping in the init state and consult it in `apply`.

```java
.withProjectionPushdown()
.withFunction(new DuckDBTableFunction<Void, long[], Object>() {
    // ... bind() registers the full set of output columns ...

    @Override
    public long[] init(DuckDBTableFunctionInitInfo info) throws Exception {
        // Record which declared columns the query actually needs.
        long[] projected = new long[(int) info.getColumnCount()];
        for (int i = 0; i < projected.length; i++) {
            projected[i] = info.getColumnIndex(i);
        }
        return projected;
    }
    // ... apply() writes only the columns listed in the projected mapping ...
})
```

Without `withProjectionPushdown()`, `getColumnCount()` reports every declared column and the function must populate all of them.

## Inspecting Registered Functions

Every successful `register()` call returns a `DuckDBFunctions.RegisteredFunction` and records the registration in a process-wide, Java-side registry. This registry is bookkeeping for functions registered through the JDBC API; it is not an authoritative view of the DuckDB catalog.

```java
List<DuckDBFunctions.RegisteredFunction> functions = DuckDBDriver.registeredFunctions();
```

`registeredFunctions()` returns a read-only snapshot, and each `RegisteredFunction` exposes `name()` and `functionKind()` (`SCALAR` or `TABLE`). Duplicate names may appear if the same name is registered more than once. `DuckDBDriver.clearFunctionsRegistry()` clears the Java-side registry only; it does not de-register the functions from DuckDB.

## Type Mapping

`withParameter()`, `withParameters()`, and `withReturnType()` accept three forms of type declaration:

* a Java `Class<?>`, including primitive class literals such as `int.class` or `Integer.TYPE`
* a `DuckDBColumnType` enum value
* a `DuckDBLogicalType` instance

When a type is declared with a Java `Class`, the driver maps it to a DuckDB type as follows:

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

## Further Reading

* [Handle Results]({% link docs/current/clients/java/result_handling.md %}) — the `DuckDBDataChunkReader` API used to read a vectorized function's inputs is shared with chunked results.
* [C API]({% link docs/current/clients/c/api.md %}) — the table function interface that the Java table function API mirrors.
* [Run Queries]({% link docs/current/clients/java/querying.md %}) — calling registered functions from SQL.
* [Configuration]({% link docs/current/configuration/overview.md %}) — the `preserve_insertion_order` option that parallel table functions may require.
