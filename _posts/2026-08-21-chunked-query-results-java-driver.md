---
layout: post
title: "Chunked Query Results in the DuckDB Java Driver"
author: "Geertjan Wielenga, Alex Kasko"
excerpt: "The DuckDB Java driver can now return query results as a lazily fetched sequence of columnar data chunks, avoiding JDBC's row-at-a-time ResultSet and its per-value overhead."
tags: ["deep dive"]
thumb: "/images/blog/thumbs/java.svg"
image: "/images/blog/thumbs/java.png"
---

DuckDB is a columnar, vectorized database. Every operator inside the engine works on [*data chunks:*]({% link docs/current/clients/c/data_chunk.md %}) batches of column vectors, 2,048 rows at a time. That is a big part of why DuckDB is fast: the engine amortizes interpretation overhead over thousands of values instead of paying it once per value.

JDBC, on the other hand, was designed in 1997 around a very different idea. The `ResultSet` API hands you one row at a time (`next()`) and one value at a time (`getInt(1)`, `getString(2)` and so on). It is a solid, familiar API, supported across the Java ecosystem, but it forces the data into a form that DuckDB never used internally.

The DuckDB Java driver has to bridge the two. It embeds the native DuckDB library and talks to it over JNI. When the engine has already produced a columnar chunk of 2,048 rows, the JDBC specification requires the driver to slice it back into rows and cells before you can read it. If your application is going to put those values right back into columnar form, such as arrays, Arrow buffers or a machine learning feature matrix, the data is split into rows only to be reassembled into columns, wasting work on both sides.

Version 1.5.3.0 of the Java driver adds an alternative.

> Tip We have thoroughly updated the [Java client documentation]({% link docs/current/clients/java/overview.md %}), which now covers the driver's full API surface across dedicated pages: [defining connections]({% link docs/current/clients/java/connecting.md %}), [running queries]({% link docs/current/clients/java/querying.md %}), [handling results]({% link docs/current/clients/java/result_handling.md %}) (including [Arrow methods]({% link docs/current/clients/java/result_handling.md %}#arrow-methods) and [streaming results]({% link docs/current/clients/java/result_handling.md %}#streaming-results)), [importing data]({% link docs/current/clients/java/data_import.md %}) with the [appender]({% link docs/current/clients/java/data_import.md %}#appender) and [batch writer]({% link docs/current/clients/java/data_import.md %}#batch-writer), and [defining functions]({% link docs/current/clients/java/functions.md %}). The chunked query results discussed in this post are documented under [Chunked Results]({% link docs/current/clients/java/result_handling.md %}#chunked-results).

## Reading Results Row by Row

A typical JDBC read loop looks like this:

```java
try (ResultSet rs = stmt.executeQuery("SELECT a, b FROM measurements")) {
    while (rs.next()) {
        long a = rs.getLong(1);
        double b = rs.getDouble(2);
        // ...
    }
}
```

Calling `next()` advances the cursor, and a `get*` call then locates the value inside the current native chunk and converts it to a Java representation. For some non-primitive types that conversion has to cross the JNI boundary on every value, and a few conversions are more involved, such as fetching a timestamp against a caller-supplied `java.util.Calendar` (the pre-`java.time` class the JDBC specification still mandates here). None of these steps is expensive on its own, but multiplied by millions of rows times a handful of columns, they add up. This is exactly the per-value interpretation overhead that vectorized execution is designed to avoid.

The loop also carries fixed overhead. So that a single connection can keep several result sets open at once, [result streaming]({% link docs/current/clients/java/result_handling.md %}#streaming-results) is off by default, which means a query's entire result is read into memory unless you set `jdbc_stream_results`, an option most users never set. The driver also assembles a full set of result metadata. That happens once per result rather than once per row, so it is cheap next to the row loop, but it is not free, and most queries never look at it.

The `ResultSet` path is the standard your ORM and the rest of the ecosystem already use, and for the vast majority of queries, the ones returning hundreds or thousands of rows, it is the right choice. The chunked API is for the other case: a query returns *a lot* of data, you control both ends of the pipe, and reading it row by row provides no advantage.

## Reading Chunks with `DuckDBChunkedResult`

The Java driver now exposes the engine's native chunk stream directly, via the same mechanism the [C API]({% link docs/current/clients/c/overview.md %}) offers as `duckdb_fetch_chunk`. A query result becomes a lazily fetched sequence of data chunks, and you read column vectors out of each chunk in batches, the way the engine produced them, avoiding the per-row overhead required by the JDBC specification.

Putting that together:

```java
try (DuckDBConnection conn = DriverManager
        .getConnection("jdbc:duckdb:")
        .unwrap(DuckDBConnection.class);
     DuckDBPreparedStatement ps = conn.prepare(
         "SELECT l_orderkey, l_linenumber, l_shipmode "
             + "FROM 's3://my-bucket-name/lineitems.parquet'")) {

    try (DuckDBChunkedResult res = ps.query()) {

        // advance to the next chunk, returns true on success
        while (res.nextChunk()) {

            // get the current chunk from the result
            DuckDBDataChunkReader chunk = res.chunk();

            // vectors are addressed by 0-based column index
            DuckDBReadableVector orderKeys = chunk.vector(0);
            DuckDBReadableVector lineNumbers = chunk.vector(1);
            DuckDBReadableVector shipModes = chunk.vector(2);

            // read each column with the getter for its type
            for (long row = 0; row < chunk.rowCount(); row++) {
                long orderKey = orderKeys.getLong(row);
                int lineNumber = lineNumbers.getInt(row);
                String shipMode = shipModes.getString(row);
                System.out.println(orderKey + " " + lineNumber + " " + shipMode);
            }
        }
    }
}
```

This approach has a few notable properties:

* **Laziness.** `nextChunk()` pulls one chunk at a time from the engine. The full result is never materialized on the native side or the Java side, so you can stream through results far larger than your heap, the same way the engine itself produces them.

* **Columnar access.** Inside a chunk you work vector by vector. If your destination is columnar too, such as a `long[]`, an Arrow `VectorSchemaRoot` or a Parquet writer, you copy values in tight, monomorphic loops instead of switching columns on every row.

* **Enough metadata to dispatch.** Each result still reports its column count and column types, so you can pick the right `get*` call per vector without carrying a separate schema description alongside the data.

* **A familiar API if you have written a UDF.** Chunk contents are accessed through the same `DuckDBDataChunkReader` API that the driver's [user-defined functions]({% link docs/current/clients/java/functions.md %}) use to read their input vectors. So the same code that reads a function's arguments inside a UDF also reads query results outside one.

* **Zero-based indexing.** Chunk *columns and rows* are 0-based, matching the C API and the UDF interfaces.

Inside a vector you are free to iterate however suits your code, a Java `Stream` included. A *parallel* stream over a single chunk rarely helps, though: 2,048 values is small enough that fork/join coordination usually costs more than it saves. If you want parallelism, apply it across chunks rather than within a single one.

## Current Limitations

This is the first iteration of the API, and there are a few limitations you should know about before adopting it:

* **Basic data types only, for now.** The scalar types are supported. Composite types (`LIST`, `STRUCT`) are not yet readable through the chunked interface. Support for them is planned for a future release.

* **Prepared statements only.** `query()` currently exists on `DuckDBPreparedStatement`, and there is no `query(String)` convenience overload yet. Preparing the statement first adds one line.

* **A small reader surface, for now.** The reader covers the essential types today, with more coverage planned for future releases. One addition already planned is reading `VARCHAR` values directly as UTF-8 `byte[]`, so text-heavy workloads can skip materializing a Java `String` per value.

If any of these blocks a use case you care about, please [open an issue](https://github.com/duckdb/duckdb-java/issues). Your feedback is what drives the priorities for the next iteration.

## Conclusion

The JDBC `ResultSet` remains the right default for most applications. But the engine produces its results in columnar chunks, and `DuckDBChunkedResult` lets your Java code read them in that same form: directly and lazily, with little overhead at the JNI boundary.

The feature is provided by [duckdb-java#682](https://github.com/duckdb/duckdb-java/pull/682) and is available in the current [`duckdb_jdbc` releases on Maven Central](https://central.sonatype.com/artifact/org.duckdb/duckdb_jdbc). Try it on your largest result set and let us know how it performs. Issues and [pull requests](https://github.com/duckdb/duckdb-java/pulls) are welcome, and the DuckDB team is always happy to talk Java in the `#java` channel on the [DuckDB Discord](https://discord.duckdb.org).
