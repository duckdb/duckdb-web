---
layout: post
title: "Chunked Query Results in the DuckDB Java Driver"
author: "Alex Kasko, Geertjan Wielenga"
excerpt: "The DuckDB Java driver can now return query results as a lazily fetched sequence of columnar data chunks, sidestepping JDBC's row-at-a-time ResultSet and its per-value overhead."
tags: ["deep dive"]
thumb: "/images/blog/thumbs/java.svg"
image: "/images/blog/thumbs/java.png"
---

DuckDB is a columnar, vectorized database. Every operator inside the engine works on *data chunks:* batches of column vectors, up to 2,048 rows at a time. This is a big part of why DuckDB is fast, because the engine amortizes interpretation overhead over thousands of values instead of paying it once per value.

JDBC, on the other hand, was designed in 1997 around a very different idea. The `ResultSet` API hands you one row at a time (`next()`) and one value at a time (`getInt(1)`, `getString(2)`, and so on). It is a solid API, familiar to every Java developer and supported by every tool in the ecosystem, but it forces a shape onto the data that DuckDB never had on the inside.

For the DuckDB Java driver, that mismatch has a concrete cost. The driver embeds the native DuckDB library and talks to it over JNI. When the engine has already produced a columnar chunk of 2,048 rows, the JDBC specification requires the driver to slice it back into rows and cells before you can read it. If your application is going to put those values right back into columnar form, such as arrays, Arrow buffers, or a machine learning feature matrix, everyone involved is doing work that nobody asked for.

Starting with version 1.5.3.0 of the [Java driver](https://github.com/duckdb/duckdb-java/pull/682), there is a way out.

## The Row-at-a-Time Tax

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

For every row, the driver needs to track a cursor position. For every cell, it needs to locate the value inside the current native chunk, convert it, and hand it across the JNI boundary in a form the JDBC interface allows. None of these steps is expensive on its own. All of them together, multiplied by millions of rows times a handful of columns, add up to real time, and the profile of that time is exactly the per-value interpretation overhead that vectorized execution was invented to eliminate.

To be clear, the `ResultSet` path is not going anywhere. It is the standard, it is what your ORM speaks, and for the vast majority of queries, the ones returning hundreds or thousands of rows, it is perfectly fine. But when a query returns *a lot* of data and you control both ends of the pipe, you should not have to pay the row-at-a-time tax.

## Meet `DuckDBChunkedResult`

The Java driver now exposes the engine's native chunk stream directly, via the same mechanism the [C API]({% link docs/current/clients/c/overview.md %}) offers as `duckdb_fetch_chunk`. A query result becomes a lazily fetched sequence of data chunks, and you read column vectors out of each chunk in batches, the way the engine produced them, avoiding the per-row overhead mandated by the JDBC specification.

Here is the whole flow:

```java
try (DuckDBConnection conn = DriverManager
        .getConnection("jdbc:duckdb:")
        .unwrap(DuckDBConnection.class);
     DuckDBPreparedStatement ps = conn.prepare("SELECT ? AS col1")) {

    ps.setInt(1, 42); // statement parameters are still 1-based

    try (DuckDBChunkedResult res = ps.query()) {

        // advance to the next chunk, returns true on success
        while (res.nextChunk()) {

            // get the current chunk from the result
            DuckDBDataChunkReader chunk = res.chunk();

            // iterate over the chunk columns, all indexes are 0-based
            for (long col = 0; col < chunk.columnCount(); col++) {

                // get a vector for the specified column
                DuckDBReadableVector vector = chunk.vector(col);

                // iterate over vector rows
                for (long row = 0; row < chunk.rowCount(); row++) {
                    int val = vector.getInt(row);
                    System.out.println(val);
                }
            }
        }
    }
}
```

A few things to point out:

* **It is lazy.** `nextChunk()` pulls one chunk at a time from the engine. The full result is never materialized on the Java side, so you can stream through results far larger than your heap, the same property that makes the engine itself happy to produce them.

* **It is columnar.** Inside a chunk you work vector by vector. If your destination is columnar too, such as a `long[]`, an Arrow `VectorSchemaRoot`, or a Parquet writer, you copy values in tight, monomorphic loops instead of bouncing between columns on every row.

* **It is familiar if you have written a UDF.** Chunk contents are accessed through the same `DuckDBDataChunkReader` API that the driver's [user-defined functions](https://github.com/duckdb/duckdb-java/blob/main/UDF.MD) use to read their input vectors. Learn the API once and use it on both sides: reading function arguments inside a UDF, and reading query results outside of one.

* **Watch your indexes.** In keeping with JDBC tradition, statement *parameters* remain 1-based. Chunk *columns and rows* are 0-based, matching the C API and the UDF interfaces. This is a difference to keep in mind in both directions.

## Current Limitations

This is the first iteration of the API, and there are two limitations you should know about before adopting it:

* **Basic data types only, for now.** The scalar types are supported. Composite types (`LIST`, `STRUCT`) are not yet readable through the chunked interface. Support for them is planned for a future release.
* **Prepared statements only.** `query()` currently exists on `DuckDBPreparedStatement`, and there is no `query(String)` convenience overload yet. Preparing the statement first is a one-line detour.

If either of these blocks a use case you care about, please [open an issue](https://github.com/duckdb/duckdb-java/issues). Knowing what people actually need is the best way to prioritize.

## Conclusion

The JDBC `ResultSet` will remain the right default for most applications, and the driver will always support it. But DuckDB thinks in chunks, and now your Java code can too. `DuckDBChunkedResult` gives you the engine's columnar batches directly, lazily, with minimal ceremony at the JNI border.

The feature is provided by [duckdb-java#682](https://github.com/duckdb/duckdb-java/pull/682) and is available in the current [`duckdb_jdbc` releases on Maven Central](https://central.sonatype.com/artifact/org.duckdb/duckdb_jdbc). Try it on your biggest result set and share how it goes. Issues and [pull requests](https://github.com/duckdb/duckdb-java/pulls) are welcome, and the DuckDB team is always happy to talk Java in the `#java` channel on the [DuckDB Discord](https://discord.duckdb.org).
