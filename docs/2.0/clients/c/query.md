---
layout: docu
redirect_from:
- /docs/api/c/query
- /docs/clients/c/query
- /docs/stable/clients/c/query
- /docs/current/clients/c/query
- /docs/lts/clients/c/query
- /docs/preview/clients/c/query
title: Query
---

<!-- markdownlint-disable MD001 -->

The `duckdb_query` method allows SQL queries to be run in DuckDB from C. This method takes two parameters, a (null-terminated) SQL query string and a `duckdb_result` result pointer. The result pointer may be `NULL` if the application is not interested in the result set or if the query produces no result. After the result is consumed, the `duckdb_destroy_result` method should be used to clean up the result.

Elements can be extracted from the `duckdb_result` object using a variety of methods. The `duckdb_column_count` can be used to extract the number of columns. `duckdb_column_name` and `duckdb_column_type` can be used to extract the names and types of individual columns.

## Example

```c
duckdb_state state;
duckdb_result result;

// create a table
state = duckdb_query(con, "CREATE TABLE integers (i INTEGER, j INTEGER);", NULL);
if (state == DuckDBError) {
    // handle error
}
// insert three rows into the table
state = duckdb_query(con, "INSERT INTO integers VALUES (3, 4), (5, 6), (7, NULL);", NULL);
if (state == DuckDBError) {
    // handle error
}
// query rows again
state = duckdb_query(con, "SELECT * FROM integers", &result);
if (state == DuckDBError) {
    // handle error
}
// handle the result
// ...

// destroy the result after we are done with it
duckdb_destroy_result(&result);
```

## Value Extraction

Values can be extracted using either the `duckdb_fetch_chunk` function, or using the `duckdb_value` convenience functions. The `duckdb_fetch_chunk` function directly hands you data chunks in DuckDB's native array format and can therefore be very fast. The `duckdb_value` functions perform bounds- and type-checking, and will automatically cast values to the desired type. This makes them more convenient and easier to use, at the expense of being slower.

See the [Types]({% link docs/2.0/clients/c/types.md %}) page for more information.

> For optimal performance, use `duckdb_fetch_chunk` to extract data from the query result.
> The `duckdb_value` functions perform internal type-checking, bounds-checking, and casting which makes them slower.

### Fetching Data Chunks

Below is an end-to-end example that prints the above result to CSV format using the `duckdb_fetch_chunk` function.
Note that the function is NOT generic: we do need to know exactly what the types of the result columns are.

```c
duckdb_database db;
duckdb_connection con;
duckdb_open(nullptr, &db);
duckdb_connect(db, &con);

duckdb_result res;
duckdb_query(con, "CREATE TABLE integers (i INTEGER, j INTEGER);", NULL);
duckdb_query(con, "INSERT INTO integers VALUES (3, 4), (5, 6), (7, NULL);", NULL);
duckdb_query(con, "SELECT * FROM integers;", &res);

// iterate until result is exhausted
while (true) {
    duckdb_data_chunk result = duckdb_fetch_chunk(res);
    if (!result) {
        // result is exhausted
        break;
    }
    // get the number of rows from the data chunk
    idx_t row_count = duckdb_data_chunk_get_size(result);
    // get the first column
    duckdb_vector col1 = duckdb_data_chunk_get_vector(result, 0);
    int32_t *col1_data = (int32_t *) duckdb_vector_get_data(col1);
    uint64_t *col1_validity = duckdb_vector_get_validity(col1);

    // get the second column
    duckdb_vector col2 = duckdb_data_chunk_get_vector(result, 1);
    int32_t *col2_data = (int32_t *) duckdb_vector_get_data(col2);
    uint64_t *col2_validity = duckdb_vector_get_validity(col2);

    // iterate over the rows
    for (idx_t row = 0; row < row_count; row++) {
        if (duckdb_validity_row_is_valid(col1_validity, row)) {
            printf("%d", col1_data[row]);
        } else {
            printf("NULL");
        }
        printf(",");
        if (duckdb_validity_row_is_valid(col2_validity, row)) {
            printf("%d", col2_data[row]);
        } else {
            printf("NULL");
        }
        printf("\n");
    }
    duckdb_destroy_data_chunk(&result);
}
// clean-up
duckdb_destroy_result(&res);
duckdb_disconnect(&con);
duckdb_close(&db);
```

This prints the following result:

```csv
3,4
5,6
7,NULL
```

### `duckdb_value`

> Deprecated The `duckdb_value` functions are deprecated and are scheduled for removal in a future release.

Below is an example that prints the above result to CSV format using the `duckdb_value_varchar` function.
Note that the function is generic: we do not need to know about the types of the individual result columns.

```c
// print the above result to CSV format using `duckdb_value_varchar`
idx_t row_count = duckdb_row_count(&result);
idx_t column_count = duckdb_column_count(&result);
for (idx_t row = 0; row < row_count; row++) {
    for (idx_t col = 0; col < column_count; col++) {
        if (col > 0) printf(",");
        auto str_val = duckdb_value_varchar(&result, col, row);
        printf("%s", str_val);
        duckdb_free(str_val);
   }
   printf("\n");
}
```

## API Reference Overview

<!-- This section is generated by scripts/generate_c_api_docs.py -->

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <a href="#duckdb_query"><span class="nf">duckdb_query</span></a>(<span class="kt">duckdb_connection</span> <span class="nv">connection</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">query</span>, <span class="kt">duckdb_result</span> *<span class="nv">out_result</span>);
<span class="kt">void</span> <a href="#duckdb_destroy_result"><span class="nf">duckdb_destroy_result</span></a>(<span class="kt">duckdb_result</span> *<span class="nv">result</span>);
<span class="kt">const</span> <span class="kt">char</span> *<a href="#duckdb_column_name"><span class="nf">duckdb_column_name</span></a>(<span class="kt">duckdb_result</span> *<span class="nv">result</span>, <span class="kt">idx_t</span> <span class="nv">col</span>);
<span class="kt">duckdb_type</span> <a href="#duckdb_column_type"><span class="nf">duckdb_column_type</span></a>(<span class="kt">duckdb_result</span> *<span class="nv">result</span>, <span class="kt">idx_t</span> <span class="nv">col</span>);
<span class="kt">duckdb_statement_type</span> <a href="#duckdb_result_statement_type"><span class="nf">duckdb_result_statement_type</span></a>(<span class="kt">duckdb_result</span> <span class="nv">result</span>);
<span class="kt">duckdb_logical_type</span> <a href="#duckdb_column_logical_type"><span class="nf">duckdb_column_logical_type</span></a>(<span class="kt">duckdb_result</span> *<span class="nv">result</span>, <span class="kt">idx_t</span> <span class="nv">col</span>);
<span class="kt">duckdb_arrow_options</span> <a href="#duckdb_result_get_arrow_options"><span class="nf">duckdb_result_get_arrow_options</span></a>(<span class="kt">duckdb_result</span> *<span class="nv">result</span>);
<span class="kt">idx_t</span> <a href="#duckdb_column_count"><span class="nf">duckdb_column_count</span></a>(<span class="kt">duckdb_result</span> *<span class="nv">result</span>);
<span class="kt">idx_t</span> <a href="#duckdb_rows_changed"><span class="nf">duckdb_rows_changed</span></a>(<span class="kt">duckdb_result</span> *<span class="nv">result</span>);
<span class="kt">const</span> <span class="kt">char</span> *<a href="#duckdb_result_error"><span class="nf">duckdb_result_error</span></a>(<span class="kt">duckdb_result</span> *<span class="nv">result</span>);
<span class="kt">duckdb_error_type</span> <a href="#duckdb_result_error_type"><span class="nf">duckdb_result_error_type</span></a>(<span class="kt">duckdb_result</span> *<span class="nv">result</span>);
<span class="kt">duckdb_result_type</span> <a href="#duckdb_result_return_type"><span class="nf">duckdb_result_return_type</span></a>(<span class="kt">duckdb_result</span> <span class="nv">result</span>);
<span class="kt">duckdb_data_chunk</span> <a href="#duckdb_fetch_chunk"><span class="nf">duckdb_fetch_chunk</span></a>(<span class="kt">duckdb_result</span> <span class="nv">result</span>);
<span class="kt">duckdb_error_data</span> <a href="#duckdb_create_error_data"><span class="nf">duckdb_create_error_data</span></a>(<span class="kt">duckdb_error_type</span> <span class="nv">type</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">message</span>);
<span class="kt">void</span> <a href="#duckdb_destroy_error_data"><span class="nf">duckdb_destroy_error_data</span></a>(<span class="kt">duckdb_error_data</span> *<span class="nv">error_data</span>);
<span class="kt">duckdb_error_type</span> <a href="#duckdb_error_data_error_type"><span class="nf">duckdb_error_data_error_type</span></a>(<span class="kt">duckdb_error_data</span> <span class="nv">error_data</span>);
<span class="kt">const</span> <span class="kt">char</span> *<a href="#duckdb_error_data_message"><span class="nf">duckdb_error_data_message</span></a>(<span class="kt">duckdb_error_data</span> <span class="nv">error_data</span>);
<span class="kt">bool</span> <a href="#duckdb_error_data_has_error"><span class="nf">duckdb_error_data_has_error</span></a>(<span class="kt">duckdb_error_data</span> <span class="nv">error_data</span>);
<span class="kt">void</span> *<a href="#duckdb_malloc"><span class="nf">duckdb_malloc</span></a>(<span class="kt">size_t</span> <span class="nv">size</span>);
<span class="kt">void</span> <a href="#duckdb_free"><span class="nf">duckdb_free</span></a>(<span class="kt">void</span> *<span class="nv">ptr</span>);
<span class="kt">idx_t</span> <a href="#duckdb_vector_size"><span class="nf">duckdb_vector_size</span></a>(<span class="kt">void</span>);
<span class="kt">bool</span> <a href="#duckdb_string_is_inlined"><span class="nf">duckdb_string_is_inlined</span></a>(<span class="kt">duckdb_string_t</span> <span class="nv">string</span>);
<span class="kt">uint32_t</span> <a href="#duckdb_string_t_length"><span class="nf">duckdb_string_t_length</span></a>(<span class="kt">duckdb_string_t</span> <span class="nv">string</span>);
<span class="kt">const</span> <span class="kt">char</span> *<a href="#duckdb_string_t_data"><span class="nf">duckdb_string_t_data</span></a>(<span class="kt">duckdb_string_t</span> *<span class="nv">string</span>);
<span class="kt">duckdb_error_data</span> <a href="#duckdb_valid_utf8_check"><span class="nf">duckdb_valid_utf8_check</span></a>(<span class="kt">const</span> <span class="kt">char</span> *<span class="nv">str</span>, <span class="kt">idx_t</span> <span class="nv">len</span>);
<span class="kt">idx_t</span> <a href="#duckdb_row_count"><span class="nf">duckdb_row_count</span></a>(<span class="kt">duckdb_result</span> *<span class="nv">result</span>);
<span class="kt">void</span> *<a href="#duckdb_column_data"><span class="nf">duckdb_column_data</span></a>(<span class="kt">duckdb_result</span> *<span class="nv">result</span>, <span class="kt">idx_t</span> <span class="nv">col</span>);
<span class="kt">bool</span> *<a href="#duckdb_nullmask_data"><span class="nf">duckdb_nullmask_data</span></a>(<span class="kt">duckdb_result</span> *<span class="nv">result</span>, <span class="kt">idx_t</span> <span class="nv">col</span>);
<span class="kt">duckdb_data_chunk</span> <a href="#duckdb_result_get_chunk"><span class="nf">duckdb_result_get_chunk</span></a>(<span class="kt">duckdb_result</span> <span class="nv">result</span>, <span class="kt">idx_t</span> <span class="nv">chunk_index</span>);
<span class="kt">bool</span> <a href="#duckdb_result_is_streaming"><span class="nf">duckdb_result_is_streaming</span></a>(<span class="kt">duckdb_result</span> <span class="nv">result</span>);
<span class="kt">idx_t</span> <a href="#duckdb_result_chunk_count"><span class="nf">duckdb_result_chunk_count</span></a>(<span class="kt">duckdb_result</span> <span class="nv">result</span>);
<span class="kt">duckdb_data_chunk</span> <a href="#duckdb_stream_fetch_chunk"><span class="nf">duckdb_stream_fetch_chunk</span></a>(<span class="kt">duckdb_result</span> <span class="nv">result</span>);
</code></pre></div></div>

#### `duckdb_query`

Stable since 0.1.0.

Executes a SQL query within a connection and stores the full (materialized) result in the out_result pointer.
If the query fails to execute, DuckDBError is returned and the error message can be retrieved by calling
`duckdb_result_error`.

Note that after running `duckdb_query`, `duckdb_destroy_result` must be called on the result object even if the
query fails, otherwise the error stored within the result will not be freed correctly.

##### Syntax

```c
duckdb_state duckdb_query(
  duckdb_connection connection,
  const char *query,
  duckdb_result *out_result
);
```

##### Parameters

* `connection`: The connection to perform the query in.
* `query`: The SQL query to run.
* `out_result`: The query result. (out)

##### Return Value

`DuckDBSuccess` on success or `DuckDBError` on failure.

<br>

#### `duckdb_destroy_result`

Stable since 0.1.0.

Closes the result and de-allocates all memory allocated for that result.

Destroying a streaming result whose statement has not completed aborts the statement. On autocommit, its writes
are rolled back. Inside a transaction, a statement that may write invalidates the transaction, and a read-only
statement just stops. Until the statement has completed, preparing or running another statement on the
connection fails with `DUCKDB_ERROR_RESOURCE_IN_USE` and leaves it untouched. To make sure the statement takes
effect, complete it by fetching until `duckdb_fetch_chunk` returns NULL before destroying the result. A NULL
chunk is also returned on an error, so check `duckdb_result_error` afterwards.

##### Syntax

```c
void duckdb_destroy_result(
  duckdb_result *result
);
```

##### Parameters

* `result`: The result to destroy.

<br>

#### `duckdb_column_name`

Stable since 0.2.1.

Returns the column name of the specified column. The result should not need to be freed; the column names will
automatically be destroyed when the result is destroyed.

Returns `NULL` if the column is out of range.

##### Syntax

```c
const char *duckdb_column_name(
  duckdb_result *result,
  idx_t col
);
```

##### Parameters

* `result`: The result object to fetch the column name from.
* `col`: The column index.

##### Return Value

The column name of the specified column.

<br>

#### `duckdb_column_type`

Stable since 0.2.9.

Returns the column type of the specified column.

Returns `DUCKDB_TYPE_INVALID` if the column is out of range.

##### Syntax

```c
duckdb_type duckdb_column_type(
  duckdb_result *result,
  idx_t col
);
```

##### Parameters

* `result`: The result object to fetch the column type from.
* `col`: The column index.

##### Return Value

The column type of the specified column.

<br>

#### `duckdb_result_statement_type`

Stable since 0.10.0.

Returns the statement type of the statement that was executed

##### Syntax

```c
duckdb_statement_type duckdb_result_statement_type(
  duckdb_result result
);
```

##### Parameters

* `result`: The result object to fetch the statement type from.

##### Return Value

duckdb_statement_type value or DUCKDB_STATEMENT_TYPE_INVALID

<br>

#### `duckdb_column_logical_type`

Stable since 0.3.3.

Returns the logical column type of the specified column.

The return type of this call should be destroyed with `duckdb_destroy_logical_type`.

Returns `NULL` if the column is out of range.

##### Syntax

```c
duckdb_logical_type duckdb_column_logical_type(
  duckdb_result *result,
  idx_t col
);
```

##### Parameters

* `result`: The result object to fetch the column type from.
* `col`: The column index.

##### Return Value

The logical column type of the specified column.

<br>

#### `duckdb_result_get_arrow_options`

Stable since 1.5.6.

Returns the arrow options associated with the given result. These options are definitions of how the arrow arrays/schema should be produced.

##### Syntax

```c
duckdb_arrow_options duckdb_result_get_arrow_options(
  duckdb_result *result
);
```

##### Parameters

* `result`: The result object to fetch arrow options from.

##### Return Value

The arrow options associated with the given result. This must be destroyed with `duckdb_destroy_arrow_options`.

<br>

#### `duckdb_column_count`

Stable since 0.2.9.

Returns the number of columns present in a the result object.

##### Syntax

```c
idx_t duckdb_column_count(
  duckdb_result *result
);
```

##### Parameters

* `result`: The result object.

##### Return Value

The number of columns present in the result object.

<br>

#### `duckdb_rows_changed`

Stable since 0.2.9.

Returns the number of rows changed by the query stored in the result. This is relevant only for INSERT/UPDATE/DELETE
queries. For other queries the rows_changed will be 0.

##### Syntax

```c
idx_t duckdb_rows_changed(
  duckdb_result *result
);
```

##### Parameters

* `result`: The result object.

##### Return Value

The number of rows changed.

<br>

#### `duckdb_result_error`

Stable since 0.2.9.

Returns the error message contained within the result. The error is only set if `duckdb_query` returns `DuckDBError`.

The result of this function must not be freed. It will be cleaned up when `duckdb_destroy_result` is called.

##### Syntax

```c
const char *duckdb_result_error(
  duckdb_result *result
);
```

##### Parameters

* `result`: The result object to fetch the error from.

##### Return Value

The error of the result.

<br>

#### `duckdb_result_error_type`

Stable since 1.1.0.

Returns the result error type contained within the result. The error is only set if `duckdb_query` returns
`DuckDBError`.

##### Syntax

```c
duckdb_error_type duckdb_result_error_type(
  duckdb_result *result
);
```

##### Parameters

* `result`: The result object to fetch the error from.

##### Return Value

The error type of the result.

<br>

#### `duckdb_result_return_type`

Stable since 0.10.0.

Returns the return_type of the given result, or DUCKDB_RETURN_TYPE_INVALID on error

##### Syntax

```c
duckdb_result_type duckdb_result_return_type(
  duckdb_result result
);
```

##### Parameters

* `result`: The result object

##### Return Value

The return_type

<br>

#### `duckdb_fetch_chunk`

Stable since 1.0.0.

Fetches a data chunk from a duckdb_result. This function should be called repeatedly until the result is exhausted.

The result must be destroyed with `duckdb_destroy_data_chunk`.

It is not known beforehand how many chunks will be returned by this result.

##### Syntax

```c
duckdb_data_chunk duckdb_fetch_chunk(
  duckdb_result result
);
```

##### Parameters

* `result`: The result object to fetch the data chunk from.

##### Return Value

The resulting data chunk. Returns `NULL` if the result has an error.

<br>

#### `duckdb_create_error_data`

Stable since 1.5.6.

Creates duckdb_error_data.
Must be destroyed with `duckdb_destroy_error_data`.

##### Syntax

```c
duckdb_error_data duckdb_create_error_data(
  duckdb_error_type type,
  const char *message
);
```

##### Parameters

* `type`: The error type.
* `message`: The error message.

##### Return Value

The error data.

<br>

#### `duckdb_destroy_error_data`

Stable since 1.5.6.

Destroys the error data and deallocates its memory.

##### Syntax

```c
void duckdb_destroy_error_data(
  duckdb_error_data *error_data
);
```

##### Parameters

* `error_data`: The error data to destroy.

<br>

#### `duckdb_error_data_error_type`

Stable since 1.5.6.

Returns the duckdb_error_type of the error data.

##### Syntax

```c
duckdb_error_type duckdb_error_data_error_type(
  duckdb_error_data error_data
);
```

##### Parameters

* `error_data`: The error data.

##### Return Value

The error type.

<br>

#### `duckdb_error_data_message`

Stable since 1.5.6.

Returns the error message of the error data. Must not be freed.

##### Syntax

```c
const char *duckdb_error_data_message(
  duckdb_error_data error_data
);
```

##### Parameters

* `error_data`: The error data.

##### Return Value

The error message.

<br>

#### `duckdb_error_data_has_error`

Stable since 1.5.6.

Returns whether the error data contains an error or not.

##### Syntax

```c
bool duckdb_error_data_has_error(
  duckdb_error_data error_data
);
```

##### Parameters

* `error_data`: The error data.

##### Return Value

True, if the error data contains an exception, else false.

<br>

#### `duckdb_malloc`

Stable since 0.2.7.

Allocate `size` bytes of memory using the duckdb internal malloc function. Any memory allocated in this manner
should be freed using `duckdb_free`.

##### Syntax

```c
void *duckdb_malloc(
  size_t size
);
```

##### Parameters

* `size`: The number of bytes to allocate.

##### Return Value

A pointer to the allocated memory region.

<br>

#### `duckdb_free`

Stable since 0.2.7.

Free a value returned from `duckdb_malloc`, `duckdb_value_varchar`, `duckdb_value_blob`, or
`duckdb_value_string`.

##### Syntax

```c
void duckdb_free(
  void *ptr
);
```

##### Parameters

* `ptr`: The memory region to de-allocate.

<br>

#### `duckdb_vector_size`

Stable since 0.3.3.

The internal vector size used by DuckDB.
This is the amount of tuples that will fit into a data chunk created by `duckdb_create_data_chunk`.

##### Syntax

```c
idx_t duckdb_vector_size(void);
```

##### Return Value

The vector size.

<br>

#### `duckdb_string_is_inlined`

Stable since 0.8.0.

Whether or not the duckdb_string_t value is inlined.
This means that the data of the string does not have a separate allocation.

##### Syntax

```c
bool duckdb_string_is_inlined(
  duckdb_string_t string
);
```

##### Return Value

`bool`

<br>

#### `duckdb_string_t_length`

Stable since 1.1.0.

Get the length of a string

##### Syntax

```c
uint32_t duckdb_string_t_length(
  duckdb_string_t string
);
```

##### Parameters

* `string`: The string to get the length of.

##### Return Value

The length.

<br>

#### `duckdb_string_t_data`

Stable since 1.1.0.

Get a pointer to the string data of a string

##### Syntax

```c
const char *duckdb_string_t_data(
  duckdb_string_t *string
);
```

##### Parameters

* `string`: The string to get the pointer to.

##### Return Value

The pointer.

<br>

#### `duckdb_valid_utf8_check`

Stable since 1.5.6.

Checks if a string is valid UTF-8.

##### Syntax

```c
duckdb_error_data duckdb_valid_utf8_check(
  const char *str,
  idx_t len
);
```

##### Parameters

* `str`: The string to check
* `len`: The length of the string (in bytes)

##### Return Value

nullptr if the string is valid UTF-8. Otherwise, a duckdb_error_data containing error information. Must be destroyed with `duckdb_destroy_error_data`.

<br>

#### `duckdb_row_count`

> Deprecated Deprecated since 1.0.0, stable since 0.2.9.

This method is scheduled for removal in a future release.

Returns the number of rows present in the result object.

##### Syntax

```c
idx_t duckdb_row_count(
  duckdb_result *result
);
```

##### Parameters

* `result`: The result object.

##### Return Value

The number of rows present in the result object.

<br>

#### `duckdb_column_data`

> Deprecated Deprecated since 1.0.0, stable since 0.2.9.

Prefer using `duckdb_result_get_chunk` instead.

Returns the data of a specific column of a result in columnar format.

The function returns a dense array which contains the result data. The exact type stored in the array depends on the
corresponding duckdb_type (as provided by `duckdb_column_type`). For the exact type by which the data should be
accessed, see the comments in [the types section]({% link docs/2.0/clients/c/types.md %}) or the `DUCKDB_TYPE` enum.

For example, for a column of type `DUCKDB_TYPE_INTEGER`, rows can be accessed in the following manner:
```c
int32_t *data = (int32_t *) duckdb_column_data(&result, 0);
printf("Data for row %d: %d\n", row, data[row]);
```

##### Syntax

```c
void *duckdb_column_data(
  duckdb_result *result,
  idx_t col
);
```

##### Parameters

* `result`: The result object to fetch the column data from.
* `col`: The column index.

##### Return Value

The column data of the specified column.

<br>

#### `duckdb_nullmask_data`

> Deprecated Deprecated since 1.0.0, stable since 0.2.9.

Prefer using `duckdb_result_get_chunk` instead.

Returns the nullmask of a specific column of a result in columnar format. The nullmask indicates for every row
whether or not the corresponding row is `NULL`. If a row is `NULL`, the values present in the array provided
by `duckdb_column_data` are undefined.

```c
int32_t *data = (int32_t *) duckdb_column_data(&result, 0);
bool *nullmask = duckdb_nullmask_data(&result, 0);
if (nullmask[row]) {
    printf("Data for row %d: NULL\n", row);
} else {
    printf("Data for row %d: %d\n", row, data[row]);
}
```

##### Syntax

```c
bool *duckdb_nullmask_data(
  duckdb_result *result,
  idx_t col
);
```

##### Parameters

* `result`: The result object to fetch the nullmask from.
* `col`: The column index.

##### Return Value

The nullmask of the specified column.

<br>

#### `duckdb_result_get_chunk`

> Deprecated Deprecated since 1.0.0, stable since 0.3.3.

This method is scheduled for removal in a future release.

Fetches a data chunk from the duckdb_result. This function should be called repeatedly until the result is exhausted.

The result must be destroyed with `duckdb_destroy_data_chunk`.

This function supersedes all `duckdb_value` functions, as well as the `duckdb_column_data` and `duckdb_nullmask_data`
functions. It results in significantly better performance, and should be preferred in newer code-bases.

If this function is used, none of the other result functions can be used and vice versa (i.e. this function cannot be
mixed with the legacy result functions).

Use `duckdb_result_chunk_count` to figure out how many chunks there are in the result.

##### Syntax

```c
duckdb_data_chunk duckdb_result_get_chunk(
  duckdb_result result,
  idx_t chunk_index
);
```

##### Parameters

* `result`: The result object to fetch the data chunk from.
* `chunk_index`: The chunk index to fetch from.

##### Return Value

The resulting data chunk. Returns `NULL` if the chunk index is out of bounds.

<br>

#### `duckdb_result_is_streaming`

> Deprecated Deprecated since 1.0.0, stable since 0.8.0.

This method is scheduled for removal in a future release.

Checks if the type of the internal result is StreamQueryResult.

##### Syntax

```c
bool duckdb_result_is_streaming(
  duckdb_result result
);
```

##### Parameters

* `result`: The result object to check.

##### Return Value

Whether or not the result object is of the type StreamQueryResult

<br>

#### `duckdb_result_chunk_count`

> Deprecated Deprecated since 1.0.0, stable since 0.3.3.

This method is scheduled for removal in a future release.

Returns the number of data chunks present in the result.

##### Syntax

```c
idx_t duckdb_result_chunk_count(
  duckdb_result result
);
```

##### Parameters

* `result`: The result object

##### Return Value

Number of data chunks present in the result.

<br>

#### `duckdb_stream_fetch_chunk`

> Deprecated Deprecated since 1.0.0, stable since 0.8.0.

This method is scheduled for removal in a future release.

Fetches a data chunk from the (streaming) duckdb_result. This function should be called repeatedly until the result is
exhausted.

The result must be destroyed with `duckdb_destroy_data_chunk`.

This function can only be used on duckdb_results created with 'duckdb_pending_prepared_streaming'

If this function is used, none of the other result functions can be used and vice versa (i.e. this function cannot be
mixed with the legacy result functions or the materialized result functions).

It is not known beforehand how many chunks will be returned by this result.

##### Syntax

```c
duckdb_data_chunk duckdb_stream_fetch_chunk(
  duckdb_result result
);
```

##### Parameters

* `result`: The result object to fetch the data chunk from.

##### Return Value

The resulting data chunk. Returns `NULL` if the result has an error.

<br>
