---
layout: docu
redirect_from:
- /docs/data/appender
- /docs/preview/data/appender
- /docs/stable/data/appender
title: Appender
---

The Appender can be used to load bulk data into a DuckDB database. It is available in the C, C++, Go, Java, Julia, Node.js, and Rust clients. This page describes how the Appender behaves across clients and shows a minimal example in each of them. For the full API of a given client, follow the links under [Client APIs](#client-apis).

## How It Works

An Appender is tied to a single connection and always appends to a single table in the database file, using that connection's transaction context.

Values added to the Appender are cached before being inserted into the database, for performance reasons. That means that, while appending, the rows might not be immediately visible in the system. The cache is flushed automatically when the Appender is closed or goes out of scope, and it can also be flushed manually. Once the Appender has been flushed or closed, all of its data has been written to the database.

Constraints such as `NOT NULL`, `PRIMARY KEY`, and `UNIQUE` are checked when the cache is flushed rather than as each row is added, so a row can be accepted but later fail at flush time. See [Handling Constraint Violations](#handling-constraint-violations).

## Creating an Appender

Each client creates an Appender from a connection and a target table, adds rows, and then flushes. The examples below insert into a table with an integer and a string column.

### C++

The `AppendRow` function is the easiest way of appending data. It uses recursive templates to allow you to put all the values of a single row within one function call:

```cpp
DuckDB db;
Connection con(db);
con.Query("CREATE TABLE people (id INTEGER, name VARCHAR)");
Appender appender(con, "people");
appender.AppendRow(1, "Mark");
```

Rows can also be individually constructed using the `BeginRow`, `EndRow`, and `Append` methods. This is done internally by `AppendRow`, and hence has the same performance characteristics:

```cpp
appender.BeginRow();
appender.Append<int32_t>(2);
appender.Append<string>("Hannes");
appender.EndRow();
```

For more information, see the [C++ client]({% link docs/current/clients/cpp.md %}).

### Java (JDBC)

An appender is created from a `DuckDBConnection` with `createAppender()`, and rows are built with `beginRow()`, `append()`, and `endRow()`. Using try-with-resources flushes and closes it at the end of the scope:

```java
try (var appender = conn.createAppender(DuckDBConnection.DEFAULT_SCHEMA, "tbl")) {
    appender.beginRow();
    appender.append(10);
    appender.append("hello");
    appender.endRow();
}
```

For more information, see the [Java Appender API]({% link docs/current/clients/java/data_import.md %}#appender).

### Go

Obtain an appender by supplying a connection to `NewAppenderFromConn()`, then add rows with `AppendRow()`:

```go
appender, err := NewAppenderFromConn(conn, "", "test")
defer appender.Close()

err = appender.AppendRow(1, "hello")

// Optional, if you want to access the appended rows immediately.
err = appender.Flush()
```

For more information, see the [Go Appender API]({% link docs/current/clients/go/data_import.md %}#appender).

### Rust

Create an appender from a `Connection` with `appender()`, then push rows built with the `params!` macro:

```rust
let mut app = conn.appender("foo")?;
app.append_row(params![1, "hello"])?;
app.flush()?;
```

For more information, see the [Rust Appender API]({% link docs/current/clients/rust/data_import.md %}#appender).

### C

For more information, see the [C Appender API]({% link docs/current/clients/c/appender.md %}).

## Date, Time and Timestamps

While numbers and strings are rather self-explanatory, dates, times, and timestamps require some explanation. In the C++ API, they can be directly appended using the methods provided by `duckdb::Date`, `duckdb::Time` or `duckdb::Timestamp`. They can also be appended using the internal `duckdb::Value` type, however, this adds some additional overheads and should be avoided if possible.

Below is a short example:

```cpp
con.Query("CREATE TABLE dates (d DATE, t TIME, ts TIMESTAMP)");
Appender appender(con, "dates");

// construct the values using the Date/Time/Timestamp types
// (this is the most efficient approach)
appender.AppendRow(
    Date::FromDate(1992, 1, 1),
    Time::FromTime(1, 1, 1, 0),
    Timestamp::FromDatetime(Date::FromDate(1992, 1, 1), Time::FromTime(1, 1, 1, 0))
);
// construct duckdb::Value objects
appender.AppendRow(
    Value::DATE(1992, 1, 1),
    Value::TIME(1, 1, 1, 0),
    Value::TIMESTAMP(1992, 1, 1, 1, 1, 1, 0)
);
```

## Commit Frequency

By default, the appender performs commits every 204,800 rows.
You can change this by explicitly using [transactions]({% link docs/current/sql/statements/transactions.md %}) and surrounding your batches of appended rows by `BEGIN TRANSACTION` and `COMMIT` statements.

## Handling Constraint Violations

If the Appender encounters a `PRIMARY KEY` conflict or a `UNIQUE` constraint violation, it fails and returns the following error:

```console
Constraint Error:
PRIMARY KEY or UNIQUE constraint violated: duplicate key "..."
```

In this case, the entire append operation fails and no rows are inserted.

## Client APIs

Each client's documentation covers its full Appender API, including constructors for non-default schemas and catalogs and any client-specific features:

* [C]({% link docs/current/clients/c/appender.md %})
* [Go]({% link docs/current/clients/go/data_import.md %}#appender)
* [Java (JDBC)]({% link docs/current/clients/java/data_import.md %}#appender)
* [Julia]({% link docs/current/clients/tertiary_clients/julia.md %}#appender-api)
* [Rust]({% link docs/current/clients/rust/data_import.md %}#appender)
* [Node.js]({% link docs/current/clients/node_neo/overview.md %}#append-to-table)
