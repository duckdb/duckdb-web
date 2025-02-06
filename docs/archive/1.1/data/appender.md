---
layout: docu
title: Appender
---

The Appender can be used to load bulk data into a DuckDB database. It is currently available in the [C, C++, Go, Java, and Rust APIs](#appender-support-in-other-clients). The Appender is tied to a connection, and will use the transaction context of that connection when appending. An Appender always appends to a single table in the database file.

In the [C++ API]({% link docs/archive/1.1/api/cpp.md %}), the Appender works as follows:

```cpp
DuckDB db;
Connection con(db);
// create the table
con.Query("CREATE TABLE people (id INTEGER, name VARCHAR)");
// initialize the appender
Appender appender(con, "people");
```

The `AppendRow` function is the easiest way of appending data. It uses recursive templates to allow you to put all the values of a single row within one function call, as follows:

```cpp
appender.AppendRow(1, "Mark");
```

Rows can also be individually constructed using the `BeginRow`, `EndRow` and `Append` methods. This is done internally by `AppendRow`, and hence has the same performance characteristics.

```cpp
appender.BeginRow();
appender.Append<int32_t>(2);
appender.Append<string>("Hannes");
appender.EndRow();
```

Any values added to the Appender are cached prior to being inserted into the database system
for performance reasons. That means that, while appending, the rows might not be immediately visible in the system. The cache is automatically flushed when the Appender goes out of scope or when `appender.Close()` is called. The cache can also be manually flushed using the `appender.Flush()` method. After either `Flush` or `Close` is called, all the data has been written to the database system.

## Date, Time and Timestamps

While numbers and strings are rather self-explanatory, dates, times and timestamps require some explanation. They can be directly appended using the methods provided by `duckdb::Date`, `duckdb::Time` or `duckdb::Timestamp`. They can also be appended using the internal `duckdb::Value` type, however, this adds some additional overheads and should be avoided if possible.

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

By default, the appender performs a commits every 204,800 rows.
You can change this by explicitly using [transactions]({% link docs/archive/1.1/sql/statements/transactions.md %}) and surrounding your batches of `AppendRow` calls by `BEGIN TRANSACTION` and `COMMIT` statements.

## Handling Constraint Violations

If the Appender encounters a `PRIMARY KEY` conflict or a `UNIQUE` constraint violation, it fails and returns the following error:

```console
Constraint Error: PRIMARY KEY or UNIQUE constraint violated: duplicate key "..."
```

In this case, the entire append operation fails and no rows are inserted.

## Appender Support in Other Clients

The Appender is also available in the following client APIs:

* [C]({% link docs/archive/1.1/api/c/appender.md %})
* [Go]({% link docs/archive/1.1/api/go.md %}#appender)
* [Java (JDBC)]({% link docs/archive/1.1/api/java.md %}#appender)
* [Julia]({% link docs/archive/1.1/api/julia.md %}#appender-api)
* [Rust]({% link docs/archive/1.1/api/rust.md %}#appender)