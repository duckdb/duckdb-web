---
layout: docu
redirect_from:
- /docs/api/cpp
- /docs/clients/cpp
- /docs/stable/clients/cpp
- /docs/current/clients/cpp
- /docs/lts/clients/cpp
- /docs/preview/clients/cpp
title: C++ API
---

> Installation To use the DuckDB C++ API, download the [`libduckdb` archive]({% link docs/2.0/installation.html %}?environment=c) for your platform.
>
> The latest stable version of the DuckDB C++ API is {{ site.latest_duckdb_version }}.

> Warning DuckDB's C++ API is internal.
> It is not guaranteed to be stable and can change without notice.
> If you would like to build an application on DuckDB, we recommend using the [C API]({% link docs/2.0/clients/c/overview.md %}).

## Installation

The DuckDB C++ API can be installed as part of the `libduckdb` packages. Please see the [installation page]({% link docs/2.0/installation.html %}?environment=c) for details. Starting with DuckDB 2.0, using the C++ API requires a [C++17 compiler]({% link docs/2.0/dev/building/overview.md %}#prerequisites).

## Basic API Usage

DuckDB implements a custom C++ API. This is built around the abstractions of a database instance (`DuckDB` class), multiple `Connection`s to the database instance, and `QueryResult` instances as the result of queries. The header file for the C++ API is `duckdb.hpp`.

### Startup & Shutdown

To use DuckDB, you must first initialize a `DuckDB` instance using its constructor. `DuckDB()` takes as parameter the database file to read and write from. The special value `nullptr` can be used to create an **in-memory database**. Note that for an in-memory database no data is persisted to disk (i.e., all data is lost when you exit the process). The second parameter to the `DuckDB` constructor is an optional `DBConfig` object. In `DBConfig`, you can set various database parameters, for example the read/write mode or memory limits. The `DuckDB` constructor may throw exceptions, for example if the database file is not usable.

With the `DuckDB` instance, you can create one or many `Connection` instances using the `Connection()` constructor. While connections should be thread-safe, they will be locked during querying. It is therefore recommended that each thread uses its own connection if you are in a multithreaded environment.

```cpp
DuckDB db(nullptr);
Connection con(db);
```

### Querying

Connections expose the `Query()` method to send a SQL query string to DuckDB from C++. `Query()` runs the query to completion and returns a `QueryResult` that retains the result in memory, so it can be read repeatedly. To submit a query without blocking, use `Submit()`.

```cpp
// create a table
con.Query("CREATE TABLE integers (i INTEGER, j INTEGER)");

// insert three rows into the table
con.Query("INSERT INTO integers VALUES (3, 4), (5, 6), (7, NULL)");

auto result = con.Query("SELECT * FROM integers");
if (result->HasError()) {
    cerr << result->GetError() << endl;
} else {
    cout << result->ToString() << endl;
}
```

`Query` will not throw exceptions under normal circumstances. Instead, invalid queries or other issues cause the `HasError()` method of the returned `QueryResult` to return `true`. In this case, the error message is available via `GetError()`. The methods `GetErrorType()` and `GetErrorObject()` are also available for any `QueryResult` instance which may aid in more explicit error handling.

```cpp
auto result = con.Query("INSERT INTO integers VALUES (1, 2)");
if (result->HasError()) {
    auto errorType = result->GetErrorType();
    switch (errorType) {
    case duckdb::ExceptionType::CONSTRAINT: {
        // Example handling
        auto errorObject = result->GetErrorObject();
        errorObject.ConvertErrorToJSON();
        std::cout << errorObject.Message() << std::endl;
        break;
    }
    // More handling
    }
} else {
    // Normal code
}
```

If successful, other fields are set: the type of statement that was just executed (e.g., `StatementType::INSERT_STATEMENT`) is returned by `GetStatementType()`. The high-level (“Logical type”/“SQL type”) types of the result set columns are returned by `GetTypes()`. The names of the result columns are returned by `GetNames()` as a vector of strings. In case multiple result sets are returned, for example because the result set contained multiple statements, the result set can be chained using the `next` field.

Because `Query()` retains the full result, the result set can be traversed directly by index. Use `ColumnCount()` and `RowCount()` for the dimensions, and `Collection().GetValue(column, row)` to retrieve an individual value as a `duckdb::Value`:

```cpp
auto result = con.Query("SELECT * FROM integers");
if (result->HasError()) {
    cerr << result->GetError() << endl;
} else {
    // Print the column names as a header row
    for (idx_t col_idx = 0; col_idx < result->ColumnCount(); col_idx++) {
        cout << result->GetNames()[col_idx];
        cout << (col_idx + 1 < result->ColumnCount() ? "\t" : "\n");
    }
    // Iterate over every row and column of the materialized result
    for (idx_t row_idx = 0; row_idx < result->RowCount(); row_idx++) {
        for (idx_t col_idx = 0; col_idx < result->ColumnCount(); col_idx++) {
            // GetValue returns a duckdb::Value; ToString renders it (NULL values become "NULL")
            cout << result->Collection().GetValue(col_idx, row_idx).ToString();
            cout << (col_idx + 1 < result->ColumnCount() ? "\t" : "\n");
        }
    }
}
```

DuckDB also supports prepared statements in the C++ API with the `Prepare()` method. This returns an instance of `PreparedStatement`. This instance can be used to execute the prepared statement with parameters. Below is an example:

```cpp
std::unique_ptr<PreparedStatement> prepare = con.Prepare("SELECT count(*) FROM a WHERE i = $1");
std::unique_ptr<QueryResult> result = prepare->Execute(12);
```

> Warning Do **not** use prepared statements to insert large amounts of data into DuckDB. See the [data import documentation]({% link docs/2.0/data/overview.md %}) for better options.

### UDF API

> Deprecated The `Connection` methods `CreateScalarFunction()`, `CreateVectorizedFunction()`, and `CreateAggregateFunction()` were removed in DuckDB 2.0. To define user-defined functions, use the [scalar function interface of the C API]({% link docs/2.0/clients/c/api.md %}#scalar-functions) or write an [extension]({% link docs/2.0/extensions/overview.md %}).
