---
layout: post
title: "DuckDB Table Functions in Java"
author: "Geertjan Wielenga, Alex Kasko"
excerpt: "The DuckDB Java client can register table functions written in pure Java, exposing any Java-accessible data source as a SQL table. That turns DuckDB into a single-node query engine for heterogeneous joins across remote systems and local files, with no export step."
tags: ["deep dive"]
thumb: "/images/blog/thumbs/java.svg"
image: "/images/blog/thumbs/java.png"
---

In a large organization, data is spread across many systems, including relational databases, document stores, message queues, data lakes, and cloud data warehouses. Some of these systems can be reached only through a vendor SDK, usually provided in Java, or a [SOAP](https://en.wikipedia.org/wiki/Service-oriented_architecture) endpoint, and many sit behind custom authentication or single sign-on that is awkward to satisfy from anything but a JVM client. The layer that ties these together is often a JVM-based distributed query engine, such as [Trino](https://trino.io/), that can run a single query joining across multiple data sources. The Java clients for those systems are mature and fast, with streaming APIs and, increasingly, virtual threads for asynchronous work. They are also already in production and cleared by corporate security.

Teams increasingly add DuckDB to these environments for fast single-node analytics. Because the surrounding infrastructure is Java, they use DuckDB through its [JDBC driver]({% link docs/current/clients/java/overview.md %}). But a query engine is only as useful as the data it can reach, and in these environments much of that data is accessible only through Java client libraries.

## Bringing External Data into DuckDB

In these environments, some data is best processed in SQL, which DuckDB handles in a performant, low-overhead way, while other data arrives from external Java-sourced systems and is often processed in application code on top of a DuckDB result set. It is frequently more convenient, and in many cases more performant, to bring that external data into DuckDB's SQL directly. *Table functions* are intended for exactly that.

DuckDB already reads almost everything. It reads Parquet and other files directly from data lakes. It connects to tightly integrated relational databases such as PostgreSQL, MySQL, and SQLite directly. The ODBC extension reaches proprietary databases such as Oracle, SQL Server, and DB2. JSON functions can query REST-like services by treating them as remote JSON files. And community extensions cover many more systems. For anything not covered, DuckDB has always supported *table functions* as a way to plug in a custom source, and those functions could be written in C++.

## Extending DuckDB in Pure Java

The DuckDB Java client can now register table functions written in [pure Java]({% link docs/current/clients/java/functions.md %}#table-functions). Any data source you can reach from Java can be exposed as a SQL table function, reusing the same streaming, asynchronous client libraries your infrastructure already runs and trusts. You can then query it alongside local Parquet and CSV files, wildcard globs included, joining and filtering across all of them in a single SQL statement.

Until now, adding a custom source in native code meant building and shipping a DuckDB extension. That involved a C++ toolchain, notoriously complex build systems, and the operational risk that a crash in native code is a segfault that takes down the whole JVM. A pure-Java table function is an ordinary Maven dependency that runs on the JVM alongside the rest of the application, with far less risk. And because it is just a Java API, any JVM language works, so the same function could be written in Kotlin, Scala, or Clojure.

This post walks through an [example project](https://github.com/staticlibs/duckdb_mongo_example/blob/master/README.md) that adds a `mongo_query()` function to DuckDB, and uses it to explain the mechanism.

> MongoDB is a document store with a robust Java API. The `mongo_query()` function below is a deliberately minimal, illustrative example, not a production connector. There are better ways to reach MongoDB in particular, including the [ODBC extension]({% link docs/current/core_extensions/odbc/overview.md %}) and the [MongoDB community extension]({% link community_extensions/extensions/mongo.md %}). We use MongoDB as an example because it is a popular system with a good Java client. The same pattern applies to any source reachable from the JVM, whether through a JDBC driver, one of the most common Java clients, a SOAP service, or a proprietary vendor SDK.

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

The first argument is a MongoDB collection name. The second is a MongoDB filter document, in native MongoDB query syntax, passed through unchanged. The named `columns` parameter specifies which fields to project and the shape of the result. Because the filter is a MongoDB BSON document rather than a full SQL query, the collection name and the desired result columns cannot be read out of the query itself and are passed as separate parameters instead. Run against a seeded collection, the function returns the documents that match the filter:

```text
┌─────────┬───────┬─────────┐
│  col1   │ col2  │  col3   │
│ varchar │ int32 │ varchar │
├─────────┼───────┼─────────┤
│ foo     │    10 │ match-a │
│ foo     │    41 │ match-b │
└─────────┴───────┴─────────┘
```

There is no export to Parquet step and no intermediate table. The rows are read from a MongoDB cursor during query execution. And because the result is an ordinary relation, it can be joined with anything else DuckDB can read. Here it joins a remote collection against a directory of local CSV files in one statement:

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

That is the heterogeneous join. A remote system reached through its Java driver is queried together with a glob of local files in one SQL statement on a single node.

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

> This example takes `username` and `password` parameters and opens a fresh connection on every call. In a real, non-toy implementation it is often preferable to open a connection to the remote server once and run several queries on it. That can be done with a set of scalar functions. A `mongo_connect()` opens a connection and returns its handle as a DuckDB value, a `mongo_query()` reads through that handle, and a `mongo_close()` closes it. That approach is outside the scope of this post and could be the subject of a follow-up. For a similar example, see [`odbc_connect`]({% link docs/current/core_extensions/odbc/functions.md %}#odbc_connect) in the ODBC extension.

The implementation is a class that implements `DuckDBTableFunction`, which follows DuckDB's native table-function lifecycle with three callbacks:

- **`bind`** runs at prepare time. It reads the parameters, determines the output schema, and declares each result column with `addResultColumn()`.
- **`init`** runs once before execution and sets up shared state, such as opening a cursor or issuing the remote request.
- **`apply`** is called repeatedly, each time filling a chunk of the output, until it returns `0`.

> The API also exposes an `initLocal` callback for per-thread local state used in multithreaded execution. This post keeps to single-threaded execution and does not use it, though it may be covered in a future post.

The example implements these in [`MongoQueryFunction.java`](https://github.com/staticlibs/duckdb_mongo_example/blob/master/src/main/java/org/duckdb/example/MongoQueryFunction.java), with named parameters defined in [`MongoQueryParameters.java`](https://github.com/staticlibs/duckdb_mongo_example/blob/master/src/main/java/org/duckdb/example/MongoQueryParameters.java).

### Bind: Declare the Output Schema

`bind` reads the call parameters and declares the output columns. Because MongoDB documents have no fixed schema, this example asks the caller to list the columns rather than inferring them from a prepared statement, and declares each one to DuckDB:

```java
public MongoQueryBindData bind(DuckDBTableFunctionBindInfo info)
    throws Exception {
    String collectionName = info.getParameter(0).getString();
    String queryJson      = info.getParameter(1).getString();
    String columnsJson    = info.getNamedParameter("columns").getString();
    // ... read hostname / port / database / credentials ...

    MongoClient client = MongoClients.create(settings.build());
    MongoCollection<Document> collection =
        client.getDatabase(database).getCollection(collectionName);

    List<String> columns = new ArrayList<>();
    for (BsonValue bv : BsonArray.parse(columnsJson)) {
        String name = bv.asString().getValue();
        columns.add(name);
        info.addResultColumn(name, String.class); // declare it to DuckDB
    }

    Document query = Document.parse(queryJson);
    return new MongoQueryBindData(client, collection, columns, query);
}
```

Two aspects here generalize beyond MongoDB. DuckDB never parses or interprets the source's query language. The filter is handed to the source's own driver essentially unchanged, apart from a JSON-to-BSON conversion, so the full source syntax stays available. The object returned from `bind`, here a [`MongoQueryBindData`](https://github.com/staticlibs/duckdb_mongo_example/blob/master/src/main/java/org/duckdb/example/MongoQueryBindData.java), then carries that state forward to the next callback. Note that `bind` also runs when a query is `EXPLAIN`ed, since DuckDB needs the output schema to plan the query.

### Init: Open the Cursor

`init` runs once and prepares the execution state that `apply` will consume. In the example it issues the query and stores the resulting cursor in a [`MongoQueryInitData`](https://github.com/staticlibs/duckdb_mongo_example/blob/master/src/main/java/org/duckdb/example/MongoQueryInitData.java). It also pins execution to a single thread with `setMaxThreads(1)`, because this post does not cover multithreaded execution:

```java
public MongoQueryInitData init(DuckDBTableFunctionInitInfo info)
    throws Exception {
    info.setMaxThreads(1);
    MongoQueryBindData bindData = info.getBindData();
    FindIterable<Document> iter = bindData.collection.find(bindData.query);
    return new MongoQueryInitData(iter.cursor());
}
```

### Apply: Stream Rows into Vectors

`apply` reflects DuckDB's vectorized execution model. Rather than returning rows, it writes them into the output data chunk column by column, up to the chunk's capacity of 2048 rows, and returns the number of rows produced:

```java
public long apply(DuckDBTableFunctionCallInfo info,
    DuckDBDataChunkWriter output) throws Exception {
    MongoCursor<Document> cursor = info.getInitData().getResultCursor();

    long row = 0;
    for (; row < output.capacity() && cursor.hasNext(); row++) {
        Document doc = cursor.next();
        for (long col = 0; col < output.columnCount(); col++) {
            copyValueFromResultSetToVector(
                doc,
                output.vector(col),
                row,
                columns.get((int) col)
            );
        }
    }
    return row; // 0 signals "no more data"
}
```

Values are written into typed vectors through the vector API, using `setString`, `setInt`, `setDouble`, `setNull`, and related methods. DuckDB calls `apply` repeatedly, draining the source one vector-sized batch of 2048 rows at a time, so the full result does not have to be materialized in memory on either side. In the example, the BSON-to-vector conversion lives in [`MongoTypes.java`](https://github.com/staticlibs/duckdb_mongo_example/blob/master/src/main/java/org/duckdb/example/MongoTypes.java).

## Implications

This example is a MongoDB connector, but the broader point is that DuckDB can now be extended in pure Java, putting the rich ecosystem of Java libraries within reach as a data source:

- **No native build.** The project contains no C++ code. It is a Maven project with two dependencies, the DuckDB JDBC driver and the MongoDB driver. Adding a new source is ordinary Java work, done with the tools a team already uses and without touching a native toolchain.
- **Reuse of the official client.** The example does not reimplement a wire protocol or query language. It uses the vendor's Java driver and passes filters through unchanged. The same applies to any system with a JDBC driver or a Java SDK, such as a REST API, a message queue, or a SOAP service.
- **In-process access.** The data is not exported and reloaded. It is read from a cursor during query execution. Because the result is an ordinary table function, it can be joined with Parquet files, CSV globs, or attached databases in a single SQL statement, so DuckDB acts as the query layer over the source rather than a copy of it.
- **Predicates run at the source.** The filter is written in the source's own query language and handed to its driver unchanged, so it executes at the source, against its indexes, and only matching rows cross the wire. The selective work happens remotely, and DuckDB streams back only what it needs.

## Current Limitations

These are limitations of the current Java table-function API:

- **A Java table function cannot yet be packaged as a DuckDB extension.** A DuckDB extension is a native shared library loaded into the DuckDB process, whereas a Java table function requires a JVM to run. As a result, the function can only be used from the DuckDB Java client. Packaging JVM code as a loadable extension is technically possible, for example through a JNI or [FFM](https://openjdk.org/jeps/454) shim that embeds the JVM, or by compiling to a GraalVM native image, but neither is supported today.
- **Bind and init objects are not managed automatically.** In the current release, the caller is responsible for the lifecycle of the objects returned from `bind` and `init`, for example closing the MongoDB client and cursor after the query completes. A [`DuckDBTableFunctionState`]({% link docs/current/clients/java/functions.md %}#cleaning-up-resources) mechanism ([contributed](https://github.com/duckdb/duckdb-java/pull/803) by a community member) manages that lifecycle for you. The init object then becomes:

  ```java
  public class MongoQueryInitData implements AutoCloseable
      /* DuckDBTableFunctionState */ {

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

For many analytical workloads, the data does not have to move to a cluster, and you do not need a distributed query engine to join across systems. With pure-Java table functions, the client libraries already running in your infrastructure expose remote data sources as SQL tables, and DuckDB joins them against each other and against local files in a single query on one node, using the Java client libraries you already have.

The table-function API is documented under [Defining Functions]({% link docs/current/clients/java/functions.md %}#table-functions). The complete example is available in the [`duckdb_mongo_example` repository](https://github.com/staticlibs/duckdb_mongo_example), and the DuckDB team is always happy to talk Java in the `#java` channel on the [DuckDB Discord](https://discord.duckdb.org).
