---
layout: docu
title: C API - Query
selected: Query
---

The `duckdb_query` method allows SQL queries to be run in DuckDB from C. This method takes two parameters, a (null-terminated) SQL query string and a `duckdb_result` result pointer. The result pointer may be `NULL` if the application is not interested in the result set or if the query produces no result. After the result is consumed, the `duckdb_destroy_result` method should be used to clean up the result.

Elements can be extracted from the `duckdb_result` object using a variety of methods. The `duckdb_column_count` and `duckdb_row_count` methods can be used to extract the number of columns and the number of rows, respectively. `duckdb_column_name` and `duckdb_column_type` can be used to extract the names and types of individual columns.

### **Example**
```c
duckdb_state state;
duckdb_result result;

// create a table
state = duckdb_query(con, "CREATE TABLE integers(i INTEGER, j INTEGER);", NULL);
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

### **Value Extraction**
Values can be extracted using either the `duckdb_column_data`/`duckdb_nullmask_data` functions, or using the `duckdb_value` convenience functions. The `duckdb_column_data`/`duckdb_nullmask_data` functions directly hand you
a pointer to the result arrays in columnar format, and can therefore be very fast. The `duckdb_value` functions perform bounds- and type-checking, and will automatically cast values to the desired type. This makes them more convenient and easier to use, at the expense of being slower.

See the [Types](types) page for more information.

> For optimal performance, use `duckdb_column_data` and `duckdb_nullmask_data` to extract data
from the query result. The `duckdb_value` functions perform internal type-checking, bounds-checking and casting
which makes them slower.

#### **duckdb_value**
Below is an example that prints the above result to CSV format using the `duckdb_value_varchar` function.
Note that the function is generic: we do not need to know about the types of the individual result columns.

```c
// print the above result to CSV format using `duckdb_value_varchar`
idx_t row_count = duckdb_row_count(&result);
idx_t column_count = duckdb_column_count(&result);
for(idx_t row = 0; row < row_count; row++) {
    for(idx_t col = 0; col < column_count; col++) {
        if (col > 0) printf(",");
        auto str_val = duckdb_value_varchar(&result, col, row);
        printf("%s", str_val);
        duckdb_free(str_val);
   }
   printf("\n");
}
```

#### **duckdb_column_data**
Below is an example that prints the above result to CSV format using the `duckdb_column_data` function.
Note that the function is NOT generic: we do need to know exactly what the types of the result columns are.

```c
int32_t *i_data = (int32_t *) duckdb_column_data(&result, 0);
int32_t *j_data = (int32_t *) duckdb_column_data(&result, 1);
bool    *i_mask = duckdb_nullmask_data(&result, 0);
bool    *j_mask = duckdb_nullmask_data(&result, 1);
idx_t row_count = duckdb_row_count(&result);
for(idx_t row = 0; row < row_count; row++) {
    if (i_mask[row]) {
        printf("NULL");
    } else {
        printf("%d", i_data[row]);
    }
    printf(",");
    if (j_mask[row]) {
        printf("NULL");
    } else {
        printf("%d", j_data[row]);
    }
    printf("\n");
}
```

> When using `duckdb_column_data`, be careful that the type matches exactly what you expect it to be. As the code
directly accesses an internal array, there is no type-checking. Accessing a `DUCKDB_TYPE_INTEGER` column as if it was
a `DUCKDB_TYPE_BIGINT` column will provide unpredictable results!


## **API Reference**
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_query">duckdb_query</a></span>(<span class="kt">duckdb_connection</span> <span class="k">connection</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="k">query</span>, <span class="kt">duckdb_result</span> *<span class="k">out_result</span>);
<span class="kt">void</span> <span class="nf"><a href="#duckdb_destroy_result">duckdb_destroy_result</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>);
<span class="kt">const</span> <span class="kt">char</span> *<span class="nf"><a href="#duckdb_column_name">duckdb_column_name</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>);
<span class="k">duckdb_type</span> <span class="nf"><a href="#duckdb_column_type">duckdb_column_type</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>);
<span class="kt">duckdb_logical_type</span> <span class="nf"><a href="#duckdb_column_logical_type">duckdb_column_logical_type</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>);
<span class="kt">idx_t</span> <span class="nf"><a href="#duckdb_column_count">duckdb_column_count</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>);
<span class="kt">idx_t</span> <span class="nf"><a href="#duckdb_row_count">duckdb_row_count</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>);
<span class="kt">idx_t</span> <span class="nf"><a href="#duckdb_rows_changed">duckdb_rows_changed</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>);
<span class="kt">void</span> *<span class="nf"><a href="#duckdb_column_data">duckdb_column_data</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>);
<span class="kt">bool</span> *<span class="nf"><a href="#duckdb_nullmask_data">duckdb_nullmask_data</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>);
<span class="kt">const</span> <span class="kt">char</span> *<span class="nf"><a href="#duckdb_result_error">duckdb_result_error</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>);
</code></pre></div></div>
### duckdb_query
---
Executes a SQL query within a connection and stores the full (materialized) result in the out_result pointer.
If the query fails to execute, DuckDBError is returned and the error message can be retrieved by calling
`duckdb_result_error`.

Note that after running `duckdb_query`, `duckdb_destroy_result` must be called on the result object even if the
query fails, otherwise the error stored within the result will not be freed correctly.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_query</span>(<span class="k">
</span>  <span class="kt">duckdb_connection</span> <span class="k">connection</span>,<span class="k">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="k">query</span>,<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">out_result
</span>);
</code></pre></div></div>
#### Parameters
---
* `connection`

The connection to perform the query in.
* `query`

The SQL query to run.
* `out_result`

The query result.
* `returns`

`DuckDBSuccess` on success or `DuckDBError` on failure.

<br>

### duckdb_destroy_result
---
Closes the result and de-allocates all memory allocated for that connection.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="k">duckdb_destroy_result</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result
</span>);
</code></pre></div></div>
#### Parameters
---
* `result`

The result to destroy.

<br>

### duckdb_column_name
---
Returns the column name of the specified column. The result should not need be freed; the column names will
automatically be destroyed when the result is destroyed.

Returns `NULL` if the column is out of range.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">const</span> <span class="kt">char</span> *<span class="k">duckdb_column_name</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col
</span>);
</code></pre></div></div>
#### Parameters
---
* `result`

The result object to fetch the column name from.
* `col`

The column index.
* `returns`

The column name of the specified column.

<br>

### duckdb_column_type
---
Returns the column type of the specified column.

Returns `DUCKDB_TYPE_INVALID` if the column is out of range.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">duckdb_type</span> <span class="k">duckdb_column_type</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col
</span>);
</code></pre></div></div>
#### Parameters
---
* `result`

The result object to fetch the column type from.
* `col`

The column index.
* `returns`

The column type of the specified column.

<br>

### duckdb_column_logical_type
---
Returns the logical column type of the specified column.

The return type of this call should be destroyed with `duckdb_destroy_logical_type`.

Returns `NULL` if the column is out of range.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="k">duckdb_column_logical_type</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col
</span>);
</code></pre></div></div>
#### Parameters
---
* `result`

The result object to fetch the column type from.
* `col`

The column index.
* `returns`

The logical column type of the specified column.

<br>

### duckdb_column_count
---
Returns the number of columns present in a the result object.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="k">duckdb_column_count</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result
</span>);
</code></pre></div></div>
#### Parameters
---
* `result`

The result object.
* `returns`

The number of columns present in the result object.

<br>

### duckdb_row_count
---
Returns the number of rows present in a the result object.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="k">duckdb_row_count</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result
</span>);
</code></pre></div></div>
#### Parameters
---
* `result`

The result object.
* `returns`

The number of rows present in the result object.

<br>

### duckdb_rows_changed
---
Returns the number of rows changed by the query stored in the result. This is relevant only for INSERT/UPDATE/DELETE
queries. For other queries the rows_changed will be 0.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="k">duckdb_rows_changed</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result
</span>);
</code></pre></div></div>
#### Parameters
---
* `result`

The result object.
* `returns`

The number of rows changed.

<br>

### duckdb_column_data
---
**DEPRECATED**: Prefer using `duckdb_result_get_chunk` instead.

Returns the data of a specific column of a result in columnar format.

The function returns a dense array which contains the result data. The exact type stored in the array depends on the
corresponding duckdb_type (as provided by `duckdb_column_type`). For the exact type by which the data should be
accessed, see the comments in [the types section](types) or the `DUCKDB_TYPE` enum.

For example, for a column of type `DUCKDB_TYPE_INTEGER`, rows can be accessed in the following manner:
```c
int32_t *data = (int32_t *) duckdb_column_data(&result, 0);
printf("Data for row %d: %d\n", row, data[row]);
```

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> *<span class="k">duckdb_column_data</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col
</span>);
</code></pre></div></div>
#### Parameters
---
* `result`

The result object to fetch the column data from.
* `col`

The column index.
* `returns`

The column data of the specified column.

<br>

### duckdb_nullmask_data
---
**DEPRECATED**: Prefer using `duckdb_result_get_chunk` instead.

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

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">bool</span> *<span class="k">duckdb_nullmask_data</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col
</span>);
</code></pre></div></div>
#### Parameters
---
* `result`

The result object to fetch the nullmask from.
* `col`

The column index.
* `returns`

The nullmask of the specified column.

<br>

### duckdb_result_error
---
Returns the error message contained within the result. The error is only set if `duckdb_query` returns `DuckDBError`.

The result of this function must not be freed. It will be cleaned up when `duckdb_destroy_result` is called.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">const</span> <span class="kt">char</span> *<span class="k">duckdb_result_error</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result
</span>);
</code></pre></div></div>
#### Parameters
---
* `result`

The result object to fetch the error from.
* `returns`

The error of the result.

<br>

