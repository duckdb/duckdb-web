---
layout: post
title: "Chunked Query Results in the DuckDB Java Driver"
author: "Geertjan Wielenga, Alex Kasko"
excerpt: "The DuckDB Java driver can now return query results as a lazily fetched sequence of columnar data chunks, avoiding JDBC's row-at-a-time ResultSet and its per-value overhead."
tags: ["deep dive"]
thumb: "/images/blog/thumbs/java.svg"
image: "/images/blog/thumbs/java.png"
---

DuckDB is a columnar, vectorized database. Every operator inside the engine works on [*data chunks*]({% link docs/current/clients/c/data_chunk.md %}): batches of column vectors, 2,048 rows at a time. That is a big part of why DuckDB is fast: the engine amortizes interpretation overhead over thousands of values instead of paying it once per value.

JDBC, on the other hand, was designed in 1997 around a very different idea. The `ResultSet` API hands you one row at a time (`next()`) and one value at a time (`getInt(1)`, `getString(2)`, and so on). It is a solid API, familiar to every Java developer and supported by every tool in the ecosystem, but it forces the data into a form that DuckDB never used internally.

The DuckDB Java driver has to bridge the two. It embeds the native DuckDB library and talks to it over JNI. When the engine has already produced a columnar chunk of 2,048 rows, the JDBC specification requires the driver to slice it back into rows and cells before you can read it. If your application is going to put those values right back into columnar form, such as arrays, Arrow buffers, or a machine learning feature matrix, the data is split into rows only to be reassembled into columns, wasting work on both sides.

Starting with version 1.5.3.0 of the Java driver, there is an alternative.

## The Cost of Row-at-a-Time Access

Consider the classic loop:

```java
try (ResultSet rs = stmt.executeQuery("SELECT a, b FROM measurements")) {
    while (rs.next()) {
        long a = rs.getLong(1);
        double b = rs.getDouble(2);
        // ...
    }
}
```

For every row, the driver tracks a cursor position. For every cell, it locates the value inside the current native chunk and converts it to a Java representation. For some non-primitive types that conversion has to cross the JNI boundary for every value, and a few conversions take extra work to get right, such as fetching a timestamp against a caller-supplied `java.util.Calendar` (the pre-`java.time` class the JDBC specification still mandates here). None of these steps is expensive on its own. Multiplied by millions of rows times a handful of columns, they add up, and this is exactly the per-value interpretation overhead that vectorized execution is designed to avoid.

There is fixed overhead around the loop, too. So that a single connection can keep several result sets open at once, [result streaming]({% link docs/current/clients/java.md %}#streaming-results) is off by default, which means a query's entire result is read into memory unless you set `jdbc_stream_results`, an option most users never set. The driver also assembles a full set of result metadata. That happens once per result rather than once per row, so it is cheap next to the row loop, but it is not free, and most queries never look at it.

The `ResultSet` path is not going anywhere. It is the standard your ORM and the rest of the ecosystem already use, and for the vast majority of queries, the ones returning hundreds or thousands of rows, it is the right choice. The chunked API is for the other case: a query returns *a lot* of data, you control both ends of the pipe, and reading it row by row gains you nothing.

## Meet `DuckDBChunkedResult`

The Java driver now exposes the engine's native chunk stream directly, via the same mechanism the [C API]({% link docs/current/clients/c/overview.md %}) offers as `duckdb_fetch_chunk`. A query result becomes a lazily fetched sequence of data chunks, and you read column vectors out of each chunk in batches, the way the engine produced them, avoiding the per-row overhead required by the JDBC specification.

Here is the whole flow:

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

A few properties to note:

* **Laziness.** `nextChunk()` pulls one chunk at a time from the engine. The full result is never materialized, neither on the native side nor on the Java side, so you can stream through results far larger than your heap, the same way the engine itself produces them.

* **Columnar access.** Inside a chunk you work vector by vector. If your destination is columnar too, such as a `long[]`, an Arrow `VectorSchemaRoot`, or a Parquet writer, you copy values in tight, monomorphic loops instead of bouncing between columns on every row.

* **Enough metadata to dispatch.** Each result still reports its column count and column types, so you can pick the right `get*` call per vector without carrying a separate schema description alongside the data.

* **A familiar API if you have written a UDF.** Chunk contents are accessed through the same `DuckDBDataChunkReader` API that the driver's [user-defined functions]({% link docs/current/clients/java.md %}#user-defined-functions) use to read their input vectors. Learn the API once and use it on both sides: reading function arguments inside a UDF, and reading query results outside of one.

* **Zero-based indexing.** Chunk *columns and rows* are 0-based, matching the C API and the UDF interfaces.

Inside a vector you are free to iterate however suits your code, a Java `Stream` included. Reaching for a *parallel* stream over a single chunk rarely pays off, though: 2,048 values is small enough that fork/join coordination usually costs more than it saves. Parallelism belongs across chunks, not inside one.

## Current Limitations

This is the first iteration of the API, and there are a few limitations you should know about before adopting it:

* **Basic data types only, for now.** The scalar types are supported. Composite types (`LIST`, `STRUCT`) are not yet readable through the chunked interface. Support for them is planned for a future release.

* **Prepared statements only.** `query()` currently exists on `DuckDBPreparedStatement`, and there is no `query(String)` convenience overload yet. Preparing the statement first adds one line.

* **A small reader surface, for now.** The reader covers the essentials today and will grow. One addition already on the list is reading `VARCHAR` values directly as UTF-8 `byte[]`, so text-heavy workloads can skip materializing a Java `String` per value.

If any of these blocks a use case you care about, please [open an issue](https://github.com/duckdb/duckdb-java/issues). Knowing what people actually need is the best way to prioritize.

## Conclusion

The JDBC `ResultSet` will remain the right default for most applications, and the driver will always support it. But DuckDB thinks in chunks, and now your Java code can too. `DuckDBChunkedResult` gives you the engine's columnar batches directly and lazily, with little overhead at the JNI boundary.

The feature is provided by [duckdb-java#682](https://github.com/duckdb/duckdb-java/pull/682) and is available in the current [`duckdb_jdbc` releases on Maven Central](https://central.sonatype.com/artifact/org.duckdb/duckdb_jdbc). Try it on your biggest result set and share how it goes. Issues and [pull requests](https://github.com/duckdb/duckdb-java/pulls) are welcome, and the DuckDB team is always happy to talk Java in the `#java` channel on the [DuckDB Discord](https://discord.duckdb.org).
