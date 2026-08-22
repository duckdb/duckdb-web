---
layout: post
title: "Heterogeneous Joins in DuckDB with Java Table Functions"
author: "Geertjan Wielenga, Alex Kasko"
excerpt: "The DuckDB Java client can register table functions written in pure Java, exposing any Java-accessible data source as a SQL table. That turns DuckDB into a single-node query engine for heterogeneous joins across remote systems and local files, with no native extension and no export step."
tags: ["deep dive"]
thumb: "/images/blog/thumbs/java.svg"
image: "/images/blog/thumbs/java.png"
---

In a large organization, data is spread across many systems: relational databases, document stores such as MongoDB, message queues, and older services reached only through a vendor SDK or a SOAP endpoint. The layer that ties these together is often a JVM-based distributed query engine, such as Trino, that can run a single query joining across all of them. The Java clients for those systems are mature and fast, with streaming and asynchronous APIs. They are also already in production and cleared by corporate security.

Teams increasingly add DuckDB to these environments for fast single-node analytics. Because the surrounding infrastructure is Java, they use it through its [JDBC driver]({% link docs/current/clients/java/overview.md %}). But DuckDB needs data, and much of that data sits behind those Java clients.

DuckDB already reads almost everything. It connects to PostgreSQL, MySQL, and SQLite directly; community extensions cover many more systems; JSON functions can query REST APIs from SQL; and the ODBC extension reaches Oracle, SQL Server, DB2, and other proprietary databases. For anything not covered, DuckDB has always supported *table functions* as a way to plug in a custom source, and those functions could be written in C++ or Rust.

The DuckDB Java client can now register table functions written in [pure Java]({% link docs/current/clients/java/functions.md %}#table-functions). Any data source you can reach from Java can be exposed as a SQL table function, reusing the same streaming, asynchronous client libraries your infrastructure already runs and trusts. You can then query it alongside local Parquet and CSV files, wildcard globs included, joining and filtering across all of them in a single SQL statement.

Until now, adding a custom source in native code meant building and shipping a DuckDB extension: a C++ or Rust toolchain, a build system that Java developers find complex and brittle (CMake plus vcpkg), and the operational risk that a crash in native code is a segfault that takes down the whole JVM, and with it the node. A pure-Java table function is an ordinary Maven dependency that runs on the JVM alongside the rest of the application, with far less risk.

This post walks through an [example project](https://github.com/staticlibs/duckdb_mongo_example/blob/master/README.md) that adds a `mongo_query()` function to DuckDB, and uses it to explain the mechanism.

> The `mongo_query()` function below is a deliberately minimal, illustrative example, not a production connector. There are better ways to reach MongoDB in particular, including the [MongoDB community extension]({% link community_extensions/extensions/mongo.md %}) and the [ODBC extension]({% link docs/current/core_extensions/odbc/overview.md %}). MongoDB is used here only because it is a familiar system with a good Java client. The same pattern applies to any source that has one, such as a SOAP service or a proprietary vendor SDK.

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

There is no export step and no intermediate table. The rows are read from a MongoDB cursor during query execution. And because the result is an ordinary table function, it can be joined with anything else DuckDB can read. Here it joins a remote collection against a directory of local CSV files in one statement:

```sql
SELECT
    c.region,
    count(*)                     AS orders,
    sum(o.amount::DECIMAL(10,2)) AS revenue
FROM mongo_query(
         'orders',
         '{ "status": "shipped" }',
         columns = '["customer_id", "amount"]',
         database = 'app'
     ) AS o
JOIN 'customers/*.csv' AS c
    ON c.customer_id = o.customer_id
GROUP BY c.region;
```

That is the heterogeneous join: a remote system reached through its Java driver, queried together with a glob of local files in one SQL statement on a single node.

## Table Functions in Java

Adding a new data source no longer requires a native extension. Through the JDBC driver, a table function is registered entirely in Java using the `DuckDBFunctions.tableFunction()` builder. The builder declares the function name, its positional and named parameters and their types, and the implementation class. Registration in the example is done in [`MongoExample.java`](https://github.com/staticlibs/duckdb_mongo_example/blob/master/src/main/java/org/duckdb/example/MongoExample.java):

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

The implementation is a class that implements `DuckDBTableFunction`, which follows DuckDB's native table-function lifecycle with three callbacks:

- **`bind`** runs at prepare time. It reads the parameters, determines the output schema, and declares each result column with `addResultColumn()`.
- **`init`** runs once before execution and sets up shared state, such as opening a cursor or issuing the remote request.
- **`apply`** is called repeatedly, each time filling a chunk of the output, until it returns `0`.

The example implements these in [`MongoQueryFunction.java`](https://github.com/staticlibs/duckdb_mongo_example/blob/master/src/main/java/org/duckdb/example/MongoQueryFunction.java), with named parameters defined in [`MongoQueryParameters.java`](https://github.com/staticlibs/duckdb_mongo_example/blob/master/src/main/java/org/duckdb/example/MongoQueryParameters.java).

### Bind: Declare the Output Schema

`bind` reads the call parameters and declares the output columns. Because MongoDB documents have no fixed schema, this example asks the caller to list the columns rather than inferring them, and declares each one to DuckDB:

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

Two aspects here generalize beyond MongoDB. The source's own query is parsed and passed to its driver unchanged, so DuckDB never interprets the source's query language and the full syntax stays available. The object returned from `bind`, here a [`MongoQueryBindData`](https://github.com/staticlibs/duckdb_mongo_example/blob/master/src/main/java/org/duckdb/example/MongoQueryBindData.java), then carries that state forward to the next callback.

### Init: Open the Cursor

`init` runs once and prepares the shared state that `apply` will consume. In the example it issues the query and stores the resulting cursor in a [`MongoQueryInitData`](https://github.com/staticlibs/duckdb_mongo_example/blob/master/src/main/java/org/duckdb/example/MongoQueryInitData.java). It also pins execution to a single thread with `setMaxThreads(1)`, because a single cursor is stateful and cannot be read by multiple DuckDB workers concurrently:

```java
public MongoQueryInitData init(DuckDBTableFunctionInitInfo info) throws Exception {
    info.setMaxThreads(1);
    MongoQueryBindData bindData = info.getBindData();
    FindIterable<Document> iter = bindData.collection.find(bindData.query);
    return new MongoQueryInitData(iter.cursor());
}
```

### Apply: Stream Rows into Vectors

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

Values are written into typed vectors through the vector API, using `setString`, `setInt`, `setDouble`, `setNull`, and related methods. DuckDB calls `apply` repeatedly, draining the source one vector-sized batch at a time, so the full result is never materialized in memory on either side. In the example, the BSON-to-vector conversion lives in [`MongoTypes.java`](https://github.com/staticlibs/duckdb_mongo_example/blob/master/src/main/java/org/duckdb/example/MongoTypes.java).

## Implications

This example is a MongoDB connector, but the broader point is that DuckDB can now be extended in pure Java, putting the JVM ecosystem within reach as a data source:

- **No native build.** The project contains no C++ and no platform-specific binary. It is a Maven project with two dependencies, the DuckDB JDBC driver and the MongoDB driver, built and run with `mvn test`. Any Java developer can add a new source.
- **Reuse of the official client.** The example does not reimplement a wire protocol or query language. It uses the vendor's Java driver and passes filters through unchanged. The same applies to any system with a JDBC driver or a Java SDK, such as a REST API, a message queue, or a SOAP service.
- **In-process access.** The data is not exported and reloaded. It is read from a cursor during query execution. Because the result is an ordinary table function, it can be joined with Parquet files, CSV globs, or attached databases in a single SQL statement, so DuckDB acts as the query layer over the source rather than a copy of it.
- **Predicates run at the source.** The filter is written in the source's own query language and handed to its driver unchanged, so it executes at the source, against its indexes, and only matching rows cross the wire. This is not DuckDB filter pushdown: the C API that Java table functions build on supports projection pushdown but not filter pushdown. It does not need to be, because the caller expresses the filter directly in the function call, which in practice is often remote SQL. The selective work happens remotely, and DuckDB streams back only what it needs.

## Current Limitations

These are limitations of the current Java table-function API, not of the toy example:

- **A Java table function cannot yet be packaged as a DuckDB extension.** A DuckDB extension is a native shared library loaded into the DuckDB process, whereas a Java table function lives in the JVM, on the other side of the JDBC boundary, and is registered on a live connection through the driver. There is no way to package JVM code as a loadable native extension, so the function is available only to the JVM process that registered it, not to other clients or the CLI, and not to a database opened without the Java driver. <!-- TODO(Alex): confirm/expand the technical detail here. --> This may or may not change in a future release.
- **Bind and init objects are not managed automatically.** In the current release, the caller is responsible for the lifecycle of the objects returned from `bind` and `init`, for example closing the MongoDB client and cursor after the query completes. An upcoming release manages that lifecycle for you: the returned objects implement `AutoCloseable`, and DuckDB calls `close()` when the function is done. <!-- TODO(Alex): replace with the real example from the upcoming release. --> The init object then becomes:

  ```java
  public class MongoQueryInitData implements AutoCloseable {
      final MongoCursor<Document> cursor;
      // ...
      @Override
      public void close() {
          cursor.close();
      }
  }
  ```

- **Composite DuckDB types are not yet supported.** The vector API currently covers scalar types, but `STRUCT`, `LIST`, and other nested types are planned for the future. Until then, nested source data has to be flattened or serialized to a scalar column.

## Conclusion

For many analytical workloads, the data does not have to move to a cluster, and you do not need a distributed query engine to join across systems. With pure-Java table functions, the client libraries already running in your infrastructure become SQL tables, and DuckDB joins them against each other and against local files in a single query on one node, using the JDBC driver you already have.

The table-function API is documented under [Defining Functions]({% link docs/current/clients/java/functions.md %}#table-functions). The complete example is available in the [`duckdb_mongo_example` repository](https://github.com/staticlibs/duckdb_mongo_example), and the DuckDB team is always happy to talk Java in the `#java` channel on the [DuckDB Discord](https://discord.duckdb.org).
