---
layout: post
title: "Querying MongoDB from DuckDB with Java Table Functions"
author: "Geertjan Wielenga, Alex Kasko"
excerpt: "DuckDB's Java client can register table functions written in Java. This post uses that capability to implement a `mongo_query()` function that reads a MongoDB collection directly into SQL, without native compilation or an intermediate export."
tags: ["deep dive"]
thumb: "/images/blog/thumbs/java.svg"
image: "/images/blog/thumbs/java.png"
---

Operational data often lives in a system that is not designed for analytics. A common example is MongoDB, a document store used for application state. Answering analytical questions of that data, such as aggregations, joins against a Parquet file, or input to a dashboard, usually means exporting a collection to JSON or CSV and loading it into an analytical engine, and repeating the export whenever the data changes.

DuckDB reads several systems directly, including PostgreSQL, MySQL, SQLite, and any source that produces Arrow. MongoDB is a document store rather than a relational database and is not among them. It does not need to be. The DuckDB Java client can register [table functions written in Java]({% link docs/current/clients/java/functions.md %}), and a table function is a suitable place to connect to MongoDB. This post describes an [example project](https://github.com/staticlibs/duckdb_mongo_example/blob/master/README.md) that adds a `mongo_query()` function to DuckDB and explains the mechanism behind it.

## The Goal

The function should be callable from ordinary SQL:

```sql
FROM mongo_query(
    'tab1',
    '{ "col1": "foo", "col2": { "$lt": 42 } }',
    columns = '["col1", "col2", "col3"]',
    hostname = 'localhost',
    port = 27017,
    database = 'db1'
);
```

The first argument is a MongoDB collection name. The second is a MongoDB filter document, in native MongoDB query syntax, passed through unchanged. The named `columns` parameter specifies which fields to project and the shape of the result. Run against a seeded collection, the function returns the documents that match the filter:

```text
┌─────────┬───────┬─────────┐
│  col1   │ col2  │  col3   │
│ varchar │ int32 │ varchar │
├─────────┼───────┼─────────┤
│ foo     │    10 │ match-a │
│ foo     │    41 │ match-b │
└─────────┴───────┴─────────┘
```

No export step or intermediate table is involved. The rows are read from a MongoDB cursor during query execution.

## Table Functions in Java

Adding support for a new data source in DuckDB has typically required a C++ extension, which involves a native toolchain and a separate build. The Java client offers an alternative: through the JDBC driver, a table function can be registered entirely in Java using the `DuckDBFunctions.tableFunction()` builder. Registration is done in [`MongoExample.java`](https://github.com/staticlibs/duckdb_mongo_example/blob/master/src/main/java/org/duckdb/example/MongoExample.java):

```java
DuckDBFunctions.tableFunction()
        .withName("mongo_query")
        .withParameter(String.class)   // collection name
        .withParameter(String.class)   // Mongo filter (JSON)
        .withNamedParameter("columns", String.class)
        .withNamedParameter("hostname", String.class)
        .withNamedParameter("port", Integer.class)
        .withNamedParameter("database", String.class)
        .withNamedParameter("username", String.class)
        .withNamedParameter("password", String.class)
        .withFunction(new MongoQueryFunction())
        .register(connection);
```

This completes registration. `mongo_query(...)` is then available as a table function on that DuckDB connection and can be used in `FROM` clauses, joins, CTEs, and subqueries like any built-in function.

The named parameters are defined in [`MongoQueryParameters.java`](https://github.com/staticlibs/duckdb_mongo_example/blob/master/src/main/java/org/duckdb/example/MongoQueryParameters.java). The behavior is implemented in [`MongoQueryFunction.java`](https://github.com/staticlibs/duckdb_mongo_example/blob/master/src/main/java/org/duckdb/example/MongoQueryFunction.java), a class implementing `DuckDBTableFunction`, which follows DuckDB's native table-function lifecycle with three callbacks:

- **`bind`** runs at prepare time. It reads the parameters, determines the output schema, and declares each result column with `addResultColumn()`.
- **`init`** runs once before execution and sets up shared state. Here it opens the MongoDB cursor.
- **`apply`** is called repeatedly, each time filling a chunk of the output, until it returns `0`.

### Bind: Parameters in, Schema out

MongoDB documents have no fixed schema, so the function does not infer one. The caller lists the required columns, and `bind` declares each as a `VARCHAR` result column and opens the connection:

```java
public MongoQueryBindData bind(DuckDBTableFunctionBindInfo info) throws Exception {
    String collectionName = info.getParameter(0).getString();
    String queryJson       = info.getParameter(1).getString();
    String columnsJson     = info.getNamedParameter("columns").getString();
    // ... read hostname / port / database / credentials ...

    MongoClient client = MongoClients.create(settings.build());
    MongoCollection<Document> collection =
        client.getDatabase(database).getCollection(collectionName);

    List<String> columns = new ArrayList<>();
    for (BsonValue bv : BsonArray.parse(columnsJson)) {
        String name = bv.asString().getValue();
        columns.add(name);
        info.addResultColumn(name, String.class);   // declare it to DuckDB
    }

    Document query = Document.parse(queryJson);
    return new MongoQueryBindData(client, collection, columns, query);
}
```

Two points are worth noting. The MongoDB filter is parsed with `Document.parse()` and passed to the driver unchanged, so DuckDB does not need to interpret MongoDB's query language and the full filter syntax remains available. The object returned from `bind`, a [`MongoQueryBindData`](https://github.com/staticlibs/duckdb_mongo_example/blob/master/src/main/java/org/duckdb/example/MongoQueryBindData.java) holding the client, collection, columns, and parsed query, carries state to the next callback.

### Init: Open the Cursor

`init` runs the query and stores the resulting cursor in a [`MongoQueryInitData`](https://github.com/staticlibs/duckdb_mongo_example/blob/master/src/main/java/org/duckdb/example/MongoQueryInitData.java). It also sets the thread count to one, because a MongoDB cursor is stateful and should not be read by multiple DuckDB workers concurrently:

```java
public MongoQueryInitData init(DuckDBTableFunctionInitInfo info) throws Exception {
    info.setMaxThreads(1);
    MongoQueryBindData bindData = info.getBindData();
    FindIterable<Document> iter = bindData.collection.find(bindData.query);
    return new MongoQueryInitData(iter.cursor());
}
```

### Apply: Stream Documents into Vectors

`apply` reflects DuckDB's vectorized execution model. Rather than returning rows, it writes them into the output data chunk column by column, up to the chunk's capacity, and returns the number of rows produced:

```java
public long apply(DuckDBTableFunctionCallInfo info, DuckDBDataChunkWriter output) throws Exception {
    MongoCursor<Document> cursor = info.getInitData().getResultCursor();

    long row = 0;
    for (; row < output.capacity() && cursor.hasNext(); row++) {
        Document doc = cursor.next();
        for (long col = 0; col < output.columnCount(); col++) {
            copyValueFromResultSetToVector(doc, output.vector(col), row, columns.get((int) col));
        }
    }
    return row;   // 0 signals "no more data"
}
```

Values are written into typed vectors by a conversion helper in [`MongoTypes.java`](https://github.com/staticlibs/duckdb_mongo_example/blob/master/src/main/java/org/duckdb/example/MongoTypes.java), which maps BSON values to DuckDB vector types using `setString`, `setInt`, `setDouble`, `setNull`, and related methods. DuckDB calls `apply` repeatedly, draining the cursor one vector-sized batch at a time, so the full collection is not materialized in memory on either side.

## Implications

This example is a MongoDB connector, but the more general result is that DuckDB can be extended in Java, which makes the JVM ecosystem available as a source of data. The approach has several properties:

- **No native build.** The project contains no C++ and no platform-specific binary. It is a Maven project with two dependencies, the DuckDB JDBC driver and the MongoDB driver, built and run with `mvn test`. A developer familiar with Java can add a new source.
- **Reuse of the official driver.** The example does not reimplement the MongoDB wire protocol or query language. It uses the vendor's Java driver and passes filters through unchanged. The same approach applies to any system with a JDBC driver or a Java SDK, such as a REST API or a message queue.
- **In-process access.** The data is not exported and reloaded; it is read from a cursor during query execution. Because the result is an ordinary table function, it can be joined with Parquet files, CSV files, or attached databases in a single SQL statement, so DuckDB acts as the query layer over MongoDB rather than a copy of it.
- **Filter pushdown.** The filter runs inside MongoDB and uses its indexes, so only matching documents are transferred. The `apply` loop then reads them in batches.

The `mongo_query()` function is roughly 150 lines of code, most of which is connection setup and type conversion.

## Current Limitations

The example is intended to demonstrate the mechanism, not to serve as a production connector. It has the following limitations:

- **Schema is supplied by the caller.** Because documents have no fixed schema, the caller lists the columns, and they are returned as `VARCHAR` unless the conversion helper is extended. There is no schema inference.
- **Single-threaded execution.** The cursor is read on one thread. DuckDB table functions support parallelism through `setMaxThreads` and projection pushdown through `withProjectionPushdown`; using them here would require partitioning the query across multiple cursors.
- **Scalar types only.** The type mapping covers `VARCHAR`, `BOOLEAN`, `INTEGER`, `BIGINT`, and `DOUBLE`. Nested documents and arrays would require mapping to DuckDB's `STRUCT` and `LIST` types, which UDFs do not yet fully support.

These are extension points rather than fundamental constraints.

## Conclusion

Java table functions allow DuckDB to be extended within the JVM. Using the builder API and three lifecycle callbacks, the example exposes a MongoDB collection as a SQL table: it sends the filter to MongoDB, reads the results through DuckDB's vectorized executor, and does so in-process without an intermediate file.

The same structure, `bind` to declare the schema and open a connection, `init` to run the request, and `apply` to stream results into vectors, applies to other sources reachable from Java, such as message queues, HTTP APIs, or systems that provide only a Java SDK. Any source with a Java library can be exposed to DuckDB as a table function and queried with SQL.

The table-function API is documented under [Defining Functions]({% link docs/current/clients/java/functions.md %}). The complete example is available in the [`duckdb_mongo_example` repository](https://github.com/staticlibs/duckdb_mongo_example), and the DuckDB team is always happy to talk Java in the `#java` channel on the [DuckDB Discord](https://discord.duckdb.org).
