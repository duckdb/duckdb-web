---
layout: docu
redirect_from:
- /docs/api/c/query
- /docs/clients/c/query
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

See the [Types]({% link docs/stable/clients/c/types.md %}) page for more information.

> For optimal performance, use `duckdb_fetch_chunk` to extract data from the query result.
> The `duckdb_value` functions perform internal type-checking, bounds-checking and casting which makes them slower.

### `duckdb_fetch_chunk`

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
<span class="kt">idx_t</span> <a href="#duckdb_row_count"><span class="nf">duckdb_row_count</span></a>(<span class="kt">duckdb_result</span> *<span class="nv">result</span>);
<span class="kt">idx_t</span> <a href="#duckdb_rows_changed"><span class="nf">duckdb_rows_changed</span></a>(<span class="kt">duckdb_result</span> *<span class="nv">result</span>);
<span class="kt">void</span> *<a href="#duckdb_column_data"><span class="nf">duckdb_column_data</span></a>(<span class="kt">duckdb_result</span> *<span class="nv">result</span>, <span class="kt">idx_t</span> <span class="nv">col</span>);
<span class="kt">bool</span> *<a href="#duckdb_nullmask_data"><span class="nf">duckdb_nullmask_data</span></a>(<span class="kt">duckdb_result</span> *<span class="nv">result</span>, <span class="kt">idx_t</span> <span class="nv">col</span>);
<span class="kt">const</span> <span class="kt">char</span> *<a href="#duckdb_result_error"><span class="nf">duckdb_result_error</span></a>(<span class="kt">duckdb_result</span> *<span class="nv">result</span>);
<span class="kt">duckdb_error_type</span> <a href="#duckdb_result_error_type"><span class="nf">duckdb_result_error_type</span></a>(<span class="kt">duckdb_result</span> *<span class="nv">result</span>);
</code></pre></div></div>

#### `duckdb_query`

Executes a SQL query within a connection and stores the full (materialized) result in the out_result pointer.
If the query fails to execute, DuckDBError is returned and the error message can be retrieved by calling
`duckdb_result_error`.

Note that after running `duckdb_query`, `duckdb_destroy_result` must be called on the result object even if the
query fails, otherwise the error stored within the result will not be freed correctly.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_query</span>(<span class="nv">
</span>  <span class="kt">duckdb_connection</span> <span class="nv">connection</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">query</span>,<span class="nv">
</span>  <span class="kt">duckdb_result</span> *<span class="nv">out_result
</span>);
</code></pre></div></div>

##### Parameters

* `connection`: The connection to perform the query in.
* `query`: The SQL query to run.
* `out_result`: The query result.

##### Return Value

`DuckDBSuccess` on success or `DuckDBError` on failure.

<br>

#### `duckdb_destroy_result`

Closes the result and de-allocates all memory allocated for that result.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nv">duckdb_destroy_result</span>(<span class="nv">
</span>  <span class="kt">duckdb_result</span> *<span class="nv">result
</span>);
</code></pre></div></div>

##### Parameters

* `result`: The result to destroy.

<br>

#### `duckdb_column_name`

Returns the column name of the specified column. The result should not need to be freed; the column names will
automatically be destroyed when the result is destroyed.

Returns `NULL` if the column is out of range.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">const</span> <span class="kt">char</span> *<span class="nv">duckdb_column_name</span>(<span class="nv">
</span>  <span class="kt">duckdb_result</span> *<span class="nv">result</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">col
</span>);
</code></pre></div></div>

##### Parameters

* `result`: The result object to fetch the column name from.
* `col`: The column index.

##### Return Value

The column name of the specified column.

<br>

#### `duckdb_column_type`

Returns the column type of the specified column.

Returns `DUCKDB_TYPE_INVALID` if the column is out of range.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_type</span> <span class="nv">duckdb_column_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_result</span> *<span class="nv">result</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">col
</span>);
</code></pre></div></div>

##### Parameters

* `result`: The result object to fetch the column type from.
* `col`: The column index.

##### Return Value

The column type of the specified column.

<br>

#### `duckdb_result_statement_type`

Returns the statement type of the statement that was executed

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_statement_type</span> <span class="nv">duckdb_result_statement_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_result</span> <span class="nv">result
</span>);
</code></pre></div></div>

##### Parameters

* `result`: The result object to fetch the statement type from.

##### Return Value

duckdb_statement_type value or DUCKDB_STATEMENT_TYPE_INVALID

<br>

#### `duckdb_column_logical_type`

Returns the logical column type of the specified column.

The return type of this call should be destroyed with `duckdb_destroy_logical_type`.

Returns `NULL` if the column is out of range.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="nv">duckdb_column_logical_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_result</span> *<span class="nv">result</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">col
</span>);
</code></pre></div></div>

##### Parameters

* `result`: The result object to fetch the column type from.
* `col`: The column index.

##### Return Value

The logical column type of the specified column.

<br>

#### `duckdb_result_get_arrow_options`

Returns the arrow options associated with the given result. These options are definitions of how the arrow arrays/schema
should be produced.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_arrow_options</span> <span class="nv">duckdb_result_get_arrow_options</span>(<span class="nv">
</span>  <span class="kt">duckdb_result</span> *<span class="nv">result
</span>);
</code></pre></div></div>

##### Parameters

* `result`: The result object to fetch arrow options from.

##### Return Value

The arrow options associated with the given result. This must be destroyed with
`duckdb_destroy_arrow_options`.

<br>

#### `duckdb_column_count`

Returns the number of columns present in the result object.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="nv">duckdb_column_count</span>(<span class="nv">
</span>  <span class="kt">duckdb_result</span> *<span class="nv">result
</span>);
</code></pre></div></div>

##### Parameters

* `result`: The result object.

##### Return Value

The number of columns present in the result object.

<br>

#### `duckdb_row_count`

> Warning Deprecation notice. This method is scheduled for removal in a future release.

Returns the number of rows present in the result object.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="nv">duckdb_row_count</span>(<span class="nv">
</span>  <span class="kt">duckdb_result</span> *<span class="nv">result
</span>);
</code></pre></div></div>

##### Parameters

* `result`: The result object.

##### Return Value

The number of rows present in the result object.

<br>

#### `duckdb_rows_changed`

Returns the number of rows changed by the query stored in the result. This is relevant only for INSERT/UPDATE/DELETE
queries. For other queries the rows_changed will be 0.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="nv">duckdb_rows_changed</span>(<span class="nv">
</span>  <span class="kt">duckdb_result</span> *<span class="nv">result
</span>);
</code></pre></div></div>

##### Parameters

* `result`: The result object.

##### Return Value

The number of rows changed.

<br>

#### `duckdb_column_data`

> Deprecated This method has been deprecated. Prefer using `duckdb_result_get_chunk` instead.

Returns the data of a specific column of a result in columnar format.

The function returns a dense array which contains the result data. The exact type stored in the array depends on the
corresponding duckdb_type (as provided by `duckdb_column_type`). For the exact type by which the data should be
accessed, see the comments in [the types section](types) or the `DUCKDB_TYPE` enum.

For example, for a column of type `DUCKDB_TYPE_INTEGER`, rows can be accessed in the following manner:
```c
int32_t *data = (int32_t *) duckdb_column_data(&result, 0);
printf("Data for row %d: %d\n", row, data[row]);
```

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> *<span class="nv">duckdb_column_data</span>(<span class="nv">
</span>  <span class="kt">duckdb_result</span> *<span class="nv">result</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">col
</span>);
</code></pre></div></div>

##### Parameters

* `result`: The result object to fetch the column data from.
* `col`: The column index.

##### Return Value

The column data of the specified column.

<br>

#### `duckdb_nullmask_data`

> Deprecated This method has been deprecated. Prefer using `duckdb_result_get_chunk` instead.

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

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">bool</span> *<span class="nv">duckdb_nullmask_data</span>(<span class="nv">
</span>  <span class="kt">duckdb_result</span> *<span class="nv">result</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">col
</span>);
</code></pre></div></div>

##### Parameters

* `result`: The result object to fetch the nullmask from.
* `col`: The column index.

##### Return Value

The nullmask of the specified column.

<br>

#### `duckdb_result_error`

Returns the error message contained within the result. The error is only set if `duckdb_query` returns `DuckDBError`.

The result of this function must not be freed. It will be cleaned up when `duckdb_destroy_result` is called.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">const</span> <span class="kt">char</span> *<span class="nv">duckdb_result_error</span>(<span class="nv">
</span>  <span class="kt">duckdb_result</span> *<span class="nv">result
</span>);
</code></pre></div></div>

##### Parameters

* `result`: The result object to fetch the error from.

##### Return Value

The error of the result.

<br>

#### `duckdb_result_error_type`

Returns the result error type contained within the result. The error is only set if `duckdb_query` returns
`DuckDBError`.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_error_type</span> <span class="nv">duckdb_result_error_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_result</span> *<span class="nv">result
</span>);
</code></pre></div></div>

##### Parameters

* `result`: The result object to fetch the error from.

##### Return Value

The error type of the result.

<br>
