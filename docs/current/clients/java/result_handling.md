---
layout: docu
redirect_from:
- /docs/clients/java/result_handling
- /docs/preview/clients/java/result_handling
- /docs/stable/clients/java/result_handling
title: Handle Results
---

## Overview

Beyond the standard JDBC `ResultSet`, the DuckDB driver can hand results to [Apache Arrow](https://arrow.apache.org/), stream large results instead of materializing them, and expose raw columnar data chunks. This page covers each of these result-handling options.

## Arrow Methods

The DuckDB result set integrates with [Apache Arrow](https://arrow.apache.org/) through the [Java Arrow bindings](https://arrow.apache.org/docs/java/). A `DuckDBResultSet` can export its rows as an Arrow stream for consumption by Arrow-based tools, and an Arrow stream produced elsewhere can be registered on a connection and queried as a DuckDB table. Refer to the [API Reference](https://javadoc.io/doc/org.duckdb/duckdb_jdbc/latest/org/duckdb/DuckDBResultSet.html#arrowExportStream(java.lang.Object,long)) for the type signatures.

### Arrow Export

The following example exports an Arrow stream from a query result and consumes it using the Java Arrow bindings. Each batch is loaded in turn, and its vectors are read from the `VectorSchemaRoot`.

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

### Arrow Import

The following example consumes an Arrow stream produced by the Java Arrow bindings and registers it on a DuckDB connection with `registerArrowStream()`. Once registered, the stream is addressed by the name passed to that method and can be queried like any other table.

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

## Streaming Results

Result streaming is opt-in in the JDBC driver. Enable it by setting the `jdbc_stream_results` config to `true` before running a query. The easiest way to do that is to pass it in the `Properties` object.

```java
Properties props = new Properties();
props.setProperty(DuckDBDriver.JDBC_STREAM_RESULTS, String.valueOf(true));

Connection conn = DriverManager.getConnection("jdbc:duckdb:", props);
```

## Chunked Results

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
