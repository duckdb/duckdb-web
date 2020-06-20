---
layout: docu
title: C++ API
selected: C++
---
## Installation
The DuckDB C++ API can be installed as part of the `libduckdb` packages. Please see the [installation page](../../installation#ENV_C) for details.

## Basic API Usage
DuckDB implements a custom C++ API. This is built around the abstractions of a database instance (`DuckDB` class), multiple `Connection`s to the database instance and `QueryResult` instances as the result of queries. The header file for the C++ API is `duckdb.hpp`. 

> The standard source distribution of `libduckdb` contains an "amalgamation" of the DuckDB sources, which combine all sources into two files `duckdb.hpp` and `duckdb.cpp`. The `duckdb.hpp` header is much larger in this case. Regardless of whether you are using the amalgamation or not, just include `duckdb.hpp`.

### Startup & Shutdown

To use DuckDB, you must first initialize a `DuckDB` instance using its constructor. `DuckDB()` takes as parameter the database file to read and write from. The special value `nullptr` can be used to create an **in-memory database**. Note that for an in-memory database no data is persisted to disk (i.e. all data is lost when you exit the process). The second parameter to the `DuckDB` constructor is an optional `DBConfig` object. In `DBConfig`, you can set various database parameters, for example the read/write mode or memory limits. The `DuckDB` constructor may throw exceptions, for example if the database file is not usable.

With the `DuckDB` instance, you can create one or many `Connection` instances using the `Connection()` constructor. While connections should be thread-safe, they will be locked during querying. It is therefore recommended that each thread uses its own connection if you are in a multithreaded environment.


```c++
DuckDB db(nullptr);
Connection con(db);
```

### Querying
Connections expose the `Query()` method to send a SQL query string to DuckDB from C++. `Query()` fully materializes the query result as a `MaterializedQueryResult` in memory before returning at which point the query result can be consumed. There is also a streaming API for queries, see further below.

```c++
// create a table
con.Query("CREATE TABLE integers(i INTEGER, j INTEGER)");

// insert three rows into the table
con.Query("INSERT INTO integers VALUES (3, 4), (5, 6), (7, NULL)";

MaterializedQueryResult result = con.Query("SELECT * FROM integers");
if (!result->success) {
	cerr << result->error;
}
```

The `MaterializedQueryResult` instance contains firstly two fields that indicate whether the query was successful. `Query` will not throw exceptions under normal circumstances. Instead, invalid queries or other issues will lead to the `success` boolean field in the query result instance to be set to `false`. In this case an error message may be available in `error` as a string. If successful, other fields are set: The type of statement that was just executed (e.g. `StatementType::INSERT_STATEMENT`) is contained in `statement_type`. The high-level ("SQL type") types of the result set columns are in `sql_types` and the low-level data representation types are in `types`. The names of the result columns are in the `names` string vector. In case multiple result sets are returned, for example because the result set contained multiple statements, the result set can be chained using the `next` field. 

```c++
// TODO
```

DuckDB also supports prepared statements in the C++ API with the `Prepare()` method. This returns an instance of `PreparedStatement`. This instance can be used to execute the prepared statement with parameters. Below is an example:

```c++
// TODO
```

> Do **not** use prepared statements to insert large amounts of data into DuckDB. See [the data import documentation](/docs/data/import) for better options.



### Streaming Queries
