---
layout: docu
title: C API
selected: Client APIs
---
## Installation
The DuckDB C API can be installed as part of the `libduckdb` packages. Please see the [installation page](../installation?environment=cplusplus) for details.

## Basic API Usage
DuckDB implements a custom C API modelled somewhat following the SQLite C API. See [duckdb.h](https://github.com/cwida/duckdb/blob/master/src/include/duckdb.h) for the full API definition.

### Startup & Shutdown

To use DuckDB, you must first initialize a `duckdb_database` handle using `duckdb_open()`. `duckdb_open()` takes as parameter the database file to read and write from. The special value `NULL` (`0`) can be used to create an **in-memory database**. Note that for an in-memory database no data is persisted to disk (i.e. all data is lost when you exit the process). With the `duckdb_database` handle, you can create one or many `duckdb_connection` using `duckdb_connect()`. While connections should be thread-safe, they will be locked during querying. It is therefore recommended that each thread uses its own connection.


```c
duckdb_database db;
duckdb_connection con;

if (duckdb_open(NULL, &db) == DuckDBError) {
	// handle error
}
if (duckdb_connect(db, &con) == DuckDBError) {
	// handle error
}
```

All `duckdb_connection`s have to explicitly be disconnected with `duckdb_disconnect()` and the `duckdb_database` has to be explicitly closed with `duckdb_close()` to avoid memory and file handle leaking:

```c
duckdb_disconnect(&con);
duckdb_close(&db);
```

### Querying

The `duckdb_query()` method allows queries to be sent to DuckDB from C. This method takes two parameters, a SQL query string and a `duckdb_result` result pointer. The result pointer may be `NULL` if the application is not interested in the result set or if the query produces no result. Below an example:

```c
// create a table
if (duckdb_query(con, "CREATE TABLE integers(i INTEGER, j INTEGER);", NULL) == DuckDBError) {
	// handle error
}
// insert three rows into the table
if (duckdb_query(con, "INSERT INTO integers VALUES (3, 4), (5, 6), (7, NULL);", NULL) == DuckDBError) {
	// handle error
}
// query rows again
if (duckdb_query(con, "SELECT * FROM integers", &result) == DuckDBError) {
	// handle error
}
```

The `duckdb_result` struct contains the dimensions of the result set (`column_count` & `row_count`) and a list of result columns with a name, a type, a nullmask and `void *` data pointer. While it is possible to cast the data pointer manually based on the type, it is not recommended. Instead, the C API provides safe(r) accessor functions for column values: `duckdb_value_<type>()`, for example `duckdb_value_int32()` or `duckdb_value_varchar()`. These functions take a `duckdb_result` pointer and a column and row index and return the corresponding value from the result set. The functions attempt to cast the value to the target type if required. Finally, the result set needs to be cleaned up `duckdb_destroy_result()` when finished to avoid memory leaks. Below an example:

```c

for (size_t row_idx = 0; row_idx < result.row_count; row_idx++) {
	for (size_t col_idx = 0; col_idx < result.column_count; col_idx++) {
		char *val = duckdb_value_varchar(&result, col_idx, row_idx);
		printf("%s ", val);
		free(val);
	}
	printf("\n");
}
duckdb_destroy_result(&result);
```

DuckDB also supports prepared statements in the C API with the `duckdb_prepare()` method. The `duckdb_bind_<type>()` family of functions is used to supply values for subsequent execution of the prepared statement using `duckdb_execute_prepared()`. Again, it is important to clear up the prepared statement after being done with it using `duckdb_destroy_prepare()` to avoid memory and reference leakage. Below is an example:

```c
duckdb_prepared_statement stmt;
if (duckdb_prepare(con, "INSERT INTO integers VALUES (?, ?)", &stmt) == DuckDBError) {
	// handle error
}

duckdb_bind_int32(stmt, 1, 42); // the parameter index starts counting at 1!
duckdb_bind_int32(stmt, 2, 43);
// NULL as second parameter means no result set is requested
duckdb_execute_prepared(stmt, NULL);
duckdb_destroy_prepare(&stmt);

// we can also query result sets using prepared statements
if (duckdb_prepare(con, "SELECT * FROM integers WHERE i = ?", &stmt) == DuckDBError) {
	// handle error
}
duckdb_bind_int32(stmt, 1, 42);
duckdb_execute_prepared(stmt, &result);

// do something with result

// clean up
duckdb_destroy_result(&result);
duckdb_destroy_prepare(&stmt);
```

> Do **not** use prepared statements to insert large amounts of data into DuckDB. See [the data import documentation](../../data/import) for better options.



