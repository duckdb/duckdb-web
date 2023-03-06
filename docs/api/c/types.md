---
layout: docu
title: C API - Types
selected: Types
---

DuckDB is a strongly typed database system. As such, every column has a single type specified. This type is constant
over the entire column. That is to say, a column that is labeled as an `INTEGER` column will only contain `INTEGER`
values.

DuckDB also supports columns of composite types. For example, it is possible to define an array of integers (`INT[]`). It is also possible to define types as arbitrary structs (`ROW(i INTEGER, j VARCHAR)`). For that reason, native DuckDB type objects are not mere enums, but a class that can potentially be nested.

Types in the C API are modeled using an enum (`duckdb_type`) and a complex class (`duckdb_logical_type`). For most primitive types, e.g. integers or varchars, the enum is sufficient. For more complex types, such as lists, structs or decimals, the logical type must be used.



```c
typedef enum DUCKDB_TYPE {
  DUCKDB_TYPE_INVALID,
  DUCKDB_TYPE_BOOLEAN,
  DUCKDB_TYPE_TINYINT,
  DUCKDB_TYPE_SMALLINT,
  DUCKDB_TYPE_INTEGER,
  DUCKDB_TYPE_BIGINT,
  DUCKDB_TYPE_UTINYINT,
  DUCKDB_TYPE_USMALLINT,
  DUCKDB_TYPE_UINTEGER,
  DUCKDB_TYPE_UBIGINT,
  DUCKDB_TYPE_FLOAT,
  DUCKDB_TYPE_DOUBLE,
  DUCKDB_TYPE_TIMESTAMP,
  DUCKDB_TYPE_DATE,
  DUCKDB_TYPE_TIME,
  DUCKDB_TYPE_INTERVAL,
  DUCKDB_TYPE_HUGEINT,
  DUCKDB_TYPE_VARCHAR,
  DUCKDB_TYPE_BLOB,
  DUCKDB_TYPE_DECIMAL,
  DUCKDB_TYPE_TIMESTAMP_S,
  DUCKDB_TYPE_TIMESTAMP_MS,
  DUCKDB_TYPE_TIMESTAMP_NS,
  DUCKDB_TYPE_ENUM,
  DUCKDB_TYPE_LIST,
  DUCKDB_TYPE_STRUCT,
  DUCKDB_TYPE_MAP,
  DUCKDB_TYPE_UUID,
  DUCKDB_TYPE_JSON
} duckdb_type;
```

The enum type of a column in the result can be obtained using the `duckdb_column_type` function. The logical type of a column can be obtained using the `duckdb_column_logical_type` function.

#### **duckdb_value**
The `duckdb_value` functions will auto-cast values as required. For example, it is no problem to use
`duckdb_value_double` on a column of type `duckdb_value_int32`. The value will be auto-cast and returned as a double.
Note that in certain cases the cast may fail. For example, this can happen if we request a `duckdb_value_int8` and the value does not fit within an `int8` value. In this case, a default value will be returned (usually `0` or `nullptr`). The same default value will also be returned if the corresponding value is `NULL`.

The `duckdb_value_is_null` function can be used to check if a specific value is `NULL` or not.

The exception to the auto-cast rule is the `duckdb_value_varchar_internal` function. This function does not auto-cast and only works for `VARCHAR` columns. The reason this function exists is that the result does not need to be freed.

> Note that `duckdb_value_varchar` and `duckdb_value_blob` require the result to be de-allocated using `duckdb_free`.

#### **duckdb_result_get_chunk**

The `duckdb_result_get_chunk` function can be used to read data chunks from a DuckDB result set, and is the most efficient way of reading data from a DuckDB result using the C API. It is also the only way of reading data of certain types from a DuckDB result. For example, the `duckdb_value` functions do not support structural reading of composite types (lists or structs) or more complex types like enums and decimals.

For more information about data chunks, see the [documentation on data chunks](data_chunk).

## **API Reference**
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_data_chunk</span> <span class="nf"><a href="#duckdb_result_get_chunk">duckdb_result_get_chunk</a></span>(<span class="kt">duckdb_result</span> <span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">chunk_index</span>);
<span class="kt">bool</span> <span class="nf"><a href="#duckdb_result_is_streaming">duckdb_result_is_streaming</a></span>(<span class="kt">duckdb_result</span> <span class="k">result</span>);
<span class="kt">idx_t</span> <span class="nf"><a href="#duckdb_result_chunk_count">duckdb_result_chunk_count</a></span>(<span class="kt">duckdb_result</span> <span class="k">result</span>);
<span class="kt">bool</span> <span class="nf"><a href="#duckdb_value_boolean">duckdb_value_boolean</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">int8_t</span> <span class="nf"><a href="#duckdb_value_int8">duckdb_value_int8</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">int16_t</span> <span class="nf"><a href="#duckdb_value_int16">duckdb_value_int16</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">int32_t</span> <span class="nf"><a href="#duckdb_value_int32">duckdb_value_int32</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">int64_t</span> <span class="nf"><a href="#duckdb_value_int64">duckdb_value_int64</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">duckdb_hugeint</span> <span class="nf"><a href="#duckdb_value_hugeint">duckdb_value_hugeint</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="k">duckdb_decimal</span> <span class="nf"><a href="#duckdb_value_decimal">duckdb_value_decimal</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">uint8_t</span> <span class="nf"><a href="#duckdb_value_uint8">duckdb_value_uint8</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">uint16_t</span> <span class="nf"><a href="#duckdb_value_uint16">duckdb_value_uint16</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">uint32_t</span> <span class="nf"><a href="#duckdb_value_uint32">duckdb_value_uint32</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">uint64_t</span> <span class="nf"><a href="#duckdb_value_uint64">duckdb_value_uint64</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">float</span> <span class="nf"><a href="#duckdb_value_float">duckdb_value_float</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">double</span> <span class="nf"><a href="#duckdb_value_double">duckdb_value_double</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">duckdb_date</span> <span class="nf"><a href="#duckdb_value_date">duckdb_value_date</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">duckdb_time</span> <span class="nf"><a href="#duckdb_value_time">duckdb_value_time</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">duckdb_timestamp</span> <span class="nf"><a href="#duckdb_value_timestamp">duckdb_value_timestamp</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">duckdb_interval</span> <span class="nf"><a href="#duckdb_value_interval">duckdb_value_interval</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">char</span> *<span class="nf"><a href="#duckdb_value_varchar">duckdb_value_varchar</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">char</span> *<span class="nf"><a href="#duckdb_value_varchar_internal">duckdb_value_varchar_internal</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="k">duckdb_string</span> <span class="nf"><a href="#duckdb_value_string_internal">duckdb_value_string_internal</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">duckdb_blob</span> <span class="nf"><a href="#duckdb_value_blob">duckdb_value_blob</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">bool</span> <span class="nf"><a href="#duckdb_value_is_null">duckdb_value_is_null</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
</code></pre></div></div>
#### Date/Time/Timestamp Helpers
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_date_struct</span> <span class="nf"><a href="#duckdb_from_date">duckdb_from_date</a></span>(<span class="kt">duckdb_date</span> <span class="k">date</span>);
<span class="kt">duckdb_date</span> <span class="nf"><a href="#duckdb_to_date">duckdb_to_date</a></span>(<span class="kt">duckdb_date_struct</span> <span class="k">date</span>);
<span class="kt">duckdb_time_struct</span> <span class="nf"><a href="#duckdb_from_time">duckdb_from_time</a></span>(<span class="kt">duckdb_time</span> <span class="k">time</span>);
<span class="kt">duckdb_time</span> <span class="nf"><a href="#duckdb_to_time">duckdb_to_time</a></span>(<span class="kt">duckdb_time_struct</span> <span class="k">time</span>);
<span class="kt">duckdb_timestamp_struct</span> <span class="nf"><a href="#duckdb_from_timestamp">duckdb_from_timestamp</a></span>(<span class="kt">duckdb_timestamp</span> <span class="k">ts</span>);
<span class="kt">duckdb_timestamp</span> <span class="nf"><a href="#duckdb_to_timestamp">duckdb_to_timestamp</a></span>(<span class="kt">duckdb_timestamp_struct</span> <span class="k">ts</span>);
</code></pre></div></div>
#### Hugeint Helpers
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">double</span> <span class="nf"><a href="#duckdb_hugeint_to_double">duckdb_hugeint_to_double</a></span>(<span class="kt">duckdb_hugeint</span> <span class="k">val</span>);
<span class="kt">duckdb_hugeint</span> <span class="nf"><a href="#duckdb_double_to_hugeint">duckdb_double_to_hugeint</a></span>(<span class="kt">double</span> <span class="k">val</span>);
<span class="k">duckdb_decimal</span> <span class="nf"><a href="#duckdb_double_to_decimal">duckdb_double_to_decimal</a></span>(<span class="kt">double</span> <span class="k">val</span>, <span class="kt">uint8_t</span> <span class="k">width</span>, <span class="kt">uint8_t</span> <span class="k">scale</span>);
</code></pre></div></div>
#### Decimal Helpers
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">double</span> <span class="nf"><a href="#duckdb_decimal_to_double">duckdb_decimal_to_double</a></span>(<span class="k">duckdb_decimal</span> <span class="k">val</span>);
</code></pre></div></div>
#### Logical Type Interface
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="nf"><a href="#duckdb_create_logical_type">duckdb_create_logical_type</a></span>(<span class="k">duckdb_type</span> <span class="k">type</span>);
<span class="kt">duckdb_logical_type</span> <span class="nf"><a href="#duckdb_create_list_type">duckdb_create_list_type</a></span>(<span class="kt">duckdb_logical_type</span> <span class="k">type</span>);
<span class="kt">duckdb_logical_type</span> <span class="nf"><a href="#duckdb_create_map_type">duckdb_create_map_type</a></span>(<span class="kt">duckdb_logical_type</span> <span class="k">key_type</span>, <span class="kt">duckdb_logical_type</span> <span class="k">value_type</span>);
<span class="kt">duckdb_logical_type</span> <span class="nf"><a href="#duckdb_create_union_type">duckdb_create_union_type</a></span>(<span class="kt">duckdb_logical_type</span> <span class="k">member_types</span>, <span class="kt">const</span> <span class="kt">char</span> **<span class="k">member_names</span>, <span class="kt">idx_t</span> <span class="k">member_count</span>);
<span class="kt">duckdb_logical_type</span> <span class="nf"><a href="#duckdb_create_decimal_type">duckdb_create_decimal_type</a></span>(<span class="kt">uint8_t</span> <span class="k">width</span>, <span class="kt">uint8_t</span> <span class="k">scale</span>);
<span class="k">duckdb_type</span> <span class="nf"><a href="#duckdb_get_type_id">duckdb_get_type_id</a></span>(<span class="kt">duckdb_logical_type</span> <span class="k">type</span>);
<span class="kt">uint8_t</span> <span class="nf"><a href="#duckdb_decimal_width">duckdb_decimal_width</a></span>(<span class="kt">duckdb_logical_type</span> <span class="k">type</span>);
<span class="kt">uint8_t</span> <span class="nf"><a href="#duckdb_decimal_scale">duckdb_decimal_scale</a></span>(<span class="kt">duckdb_logical_type</span> <span class="k">type</span>);
<span class="k">duckdb_type</span> <span class="nf"><a href="#duckdb_decimal_internal_type">duckdb_decimal_internal_type</a></span>(<span class="kt">duckdb_logical_type</span> <span class="k">type</span>);
<span class="k">duckdb_type</span> <span class="nf"><a href="#duckdb_enum_internal_type">duckdb_enum_internal_type</a></span>(<span class="kt">duckdb_logical_type</span> <span class="k">type</span>);
<span class="kt">uint32_t</span> <span class="nf"><a href="#duckdb_enum_dictionary_size">duckdb_enum_dictionary_size</a></span>(<span class="kt">duckdb_logical_type</span> <span class="k">type</span>);
<span class="kt">char</span> *<span class="nf"><a href="#duckdb_enum_dictionary_value">duckdb_enum_dictionary_value</a></span>(<span class="kt">duckdb_logical_type</span> <span class="k">type</span>, <span class="kt">idx_t</span> <span class="k">index</span>);
<span class="kt">duckdb_logical_type</span> <span class="nf"><a href="#duckdb_list_type_child_type">duckdb_list_type_child_type</a></span>(<span class="kt">duckdb_logical_type</span> <span class="k">type</span>);
<span class="kt">duckdb_logical_type</span> <span class="nf"><a href="#duckdb_map_type_key_type">duckdb_map_type_key_type</a></span>(<span class="kt">duckdb_logical_type</span> <span class="k">type</span>);
<span class="kt">duckdb_logical_type</span> <span class="nf"><a href="#duckdb_map_type_value_type">duckdb_map_type_value_type</a></span>(<span class="kt">duckdb_logical_type</span> <span class="k">type</span>);
<span class="kt">idx_t</span> <span class="nf"><a href="#duckdb_struct_type_child_count">duckdb_struct_type_child_count</a></span>(<span class="kt">duckdb_logical_type</span> <span class="k">type</span>);
<span class="kt">char</span> *<span class="nf"><a href="#duckdb_struct_type_child_name">duckdb_struct_type_child_name</a></span>(<span class="kt">duckdb_logical_type</span> <span class="k">type</span>, <span class="kt">idx_t</span> <span class="k">index</span>);
<span class="kt">duckdb_logical_type</span> <span class="nf"><a href="#duckdb_struct_type_child_type">duckdb_struct_type_child_type</a></span>(<span class="kt">duckdb_logical_type</span> <span class="k">type</span>, <span class="kt">idx_t</span> <span class="k">index</span>);
<span class="kt">idx_t</span> <span class="nf"><a href="#duckdb_union_type_member_count">duckdb_union_type_member_count</a></span>(<span class="kt">duckdb_logical_type</span> <span class="k">type</span>);
<span class="kt">char</span> *<span class="nf"><a href="#duckdb_union_type_member_name">duckdb_union_type_member_name</a></span>(<span class="kt">duckdb_logical_type</span> <span class="k">type</span>, <span class="kt">idx_t</span> <span class="k">index</span>);
<span class="kt">duckdb_logical_type</span> <span class="nf"><a href="#duckdb_union_type_member_type">duckdb_union_type_member_type</a></span>(<span class="kt">duckdb_logical_type</span> <span class="k">type</span>, <span class="kt">idx_t</span> <span class="k">index</span>);
<span class="kt">void</span> <span class="nf"><a href="#duckdb_destroy_logical_type">duckdb_destroy_logical_type</a></span>(<span class="kt">duckdb_logical_type</span> *<span class="k">type</span>);
</code></pre></div></div>
### duckdb_result_get_chunk
---
Fetches a data chunk from the duckdb_result. This function should be called repeatedly until the result is exhausted.

The result must be destroyed with `duckdb_destroy_data_chunk`.

This function supersedes all `duckdb_value` functions, as well as the `duckdb_column_data` and `duckdb_nullmask_data`
functions. It results in significantly better performance, and should be preferred in newer code-bases.

If this function is used, none of the other result functions can be used and vice versa (i.e. this function cannot be
mixed with the legacy result functions).

Use `duckdb_result_chunk_count` to figure out how many chunks there are in the result.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_data_chunk</span> <span class="k">duckdb_result_get_chunk</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> <span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">chunk_index
</span>);
</code></pre></div></div>
#### Parameters
---
* `result`

The result object to fetch the data chunk from.
* `chunk_index`

The chunk index to fetch from.
* `returns`

The resulting data chunk. Returns `NULL` if the chunk index is out of bounds.

<br>

### duckdb_result_is_streaming
---
Checks if the type of the internal result is StreamQueryResult.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">bool</span> <span class="k">duckdb_result_is_streaming</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> <span class="k">result
</span>);
</code></pre></div></div>
#### Parameters
---
* `result`

The result object to check.
* `returns`

Whether or not the result object is of the type StreamQueryResult

<br>

### duckdb_result_chunk_count
---
Returns the number of data chunks present in the result.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="k">duckdb_result_chunk_count</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> <span class="k">result
</span>);
</code></pre></div></div>
#### Parameters
---
* `result`

The result object
* `returns`

The resulting data chunk. Returns `NULL` if the chunk index is out of bounds.

<br>

### duckdb_value_boolean
---
#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">bool</span> <span class="k">duckdb_value_boolean</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### Parameters
---
* `returns`

The boolean value at the specified location, or false if the value cannot be converted.

<br>

### duckdb_value_int8
---
#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">int8_t</span> <span class="k">duckdb_value_int8</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### Parameters
---
* `returns`

The int8_t value at the specified location, or 0 if the value cannot be converted.

<br>

### duckdb_value_int16
---
#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">int16_t</span> <span class="k">duckdb_value_int16</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### Parameters
---
* `returns`

The int16_t value at the specified location, or 0 if the value cannot be converted.

<br>

### duckdb_value_int32
---
#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">int32_t</span> <span class="k">duckdb_value_int32</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### Parameters
---
* `returns`

The int32_t value at the specified location, or 0 if the value cannot be converted.

<br>

### duckdb_value_int64
---
#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">int64_t</span> <span class="k">duckdb_value_int64</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### Parameters
---
* `returns`

The int64_t value at the specified location, or 0 if the value cannot be converted.

<br>

### duckdb_value_hugeint
---
#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_hugeint</span> <span class="k">duckdb_value_hugeint</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### Parameters
---
* `returns`

The duckdb_hugeint value at the specified location, or 0 if the value cannot be converted.

<br>

### duckdb_value_decimal
---
#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">duckdb_decimal</span> <span class="k">duckdb_value_decimal</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### Parameters
---
* `returns`

The duckdb_decimal value at the specified location, or 0 if the value cannot be converted.

<br>

### duckdb_value_uint8
---
#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">uint8_t</span> <span class="k">duckdb_value_uint8</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### Parameters
---
* `returns`

The uint8_t value at the specified location, or 0 if the value cannot be converted.

<br>

### duckdb_value_uint16
---
#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">uint16_t</span> <span class="k">duckdb_value_uint16</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### Parameters
---
* `returns`

The uint16_t value at the specified location, or 0 if the value cannot be converted.

<br>

### duckdb_value_uint32
---
#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">uint32_t</span> <span class="k">duckdb_value_uint32</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### Parameters
---
* `returns`

The uint32_t value at the specified location, or 0 if the value cannot be converted.

<br>

### duckdb_value_uint64
---
#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">uint64_t</span> <span class="k">duckdb_value_uint64</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### Parameters
---
* `returns`

The uint64_t value at the specified location, or 0 if the value cannot be converted.

<br>

### duckdb_value_float
---
#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">float</span> <span class="k">duckdb_value_float</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### Parameters
---
* `returns`

The float value at the specified location, or 0 if the value cannot be converted.

<br>

### duckdb_value_double
---
#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">double</span> <span class="k">duckdb_value_double</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### Parameters
---
* `returns`

The double value at the specified location, or 0 if the value cannot be converted.

<br>

### duckdb_value_date
---
#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_date</span> <span class="k">duckdb_value_date</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### Parameters
---
* `returns`

The duckdb_date value at the specified location, or 0 if the value cannot be converted.

<br>

### duckdb_value_time
---
#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_time</span> <span class="k">duckdb_value_time</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### Parameters
---
* `returns`

The duckdb_time value at the specified location, or 0 if the value cannot be converted.

<br>

### duckdb_value_timestamp
---
#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_timestamp</span> <span class="k">duckdb_value_timestamp</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### Parameters
---
* `returns`

The duckdb_timestamp value at the specified location, or 0 if the value cannot be converted.

<br>

### duckdb_value_interval
---
#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_interval</span> <span class="k">duckdb_value_interval</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### Parameters
---
* `returns`

The duckdb_interval value at the specified location, or 0 if the value cannot be converted.

<br>

### duckdb_value_varchar
---
#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">char</span> *<span class="k">duckdb_value_varchar</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### Parameters
---
* `DEPRECATED`

use duckdb_value_string instead. This function does not work correctly if the string contains null bytes.
* `returns`

The text value at the specified location as a null-terminated string, or nullptr if the value cannot be
converted. The result must be freed with `duckdb_free`.

<br>

### duckdb_value_varchar_internal
---
#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">char</span> *<span class="k">duckdb_value_varchar_internal</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### Parameters
---
* `DEPRECATED`

use duckdb_value_string_internal instead. This function does not work correctly if the string contains
null bytes.
* `returns`

The char* value at the specified location. ONLY works on VARCHAR columns and does not auto-cast.
If the column is NOT a VARCHAR column this function will return NULL.

The result must NOT be freed.

<br>

### duckdb_value_string_internal
---
#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">duckdb_string</span> <span class="k">duckdb_value_string_internal</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### Parameters
---
* `DEPRECATED`

use duckdb_value_string_internal instead. This function does not work correctly if the string contains
null bytes.
* `returns`

The char* value at the specified location. ONLY works on VARCHAR columns and does not auto-cast.
If the column is NOT a VARCHAR column this function will return NULL.

The result must NOT be freed.

<br>

### duckdb_value_blob
---
#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_blob</span> <span class="k">duckdb_value_blob</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### Parameters
---
* `returns`

The duckdb_blob value at the specified location. Returns a blob with blob.data set to nullptr if the
value cannot be converted. The resulting "blob.data" must be freed with `duckdb_free.`

<br>

### duckdb_value_is_null
---
#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">bool</span> <span class="k">duckdb_value_is_null</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### Parameters
---
* `returns`

Returns true if the value at the specified index is NULL, and false otherwise.

<br>

### duckdb_from_date
---
Decompose a `duckdb_date` object into year, month and date (stored as `duckdb_date_struct`).

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_date_struct</span> <span class="k">duckdb_from_date</span>(<span class="k">
</span>  <span class="kt">duckdb_date</span> <span class="k">date
</span>);
</code></pre></div></div>
#### Parameters
---
* `date`

The date object, as obtained from a `DUCKDB_TYPE_DATE` column.
* `returns`

The `duckdb_date_struct` with the decomposed elements.

<br>

### duckdb_to_date
---
Re-compose a `duckdb_date` from year, month and date (`duckdb_date_struct`).

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_date</span> <span class="k">duckdb_to_date</span>(<span class="k">
</span>  <span class="kt">duckdb_date_struct</span> <span class="k">date
</span>);
</code></pre></div></div>
#### Parameters
---
* `date`

The year, month and date stored in a `duckdb_date_struct`.
* `returns`

The `duckdb_date` element.

<br>

### duckdb_from_time
---
Decompose a `duckdb_time` object into hour, minute, second and microsecond (stored as `duckdb_time_struct`).

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_time_struct</span> <span class="k">duckdb_from_time</span>(<span class="k">
</span>  <span class="kt">duckdb_time</span> <span class="k">time
</span>);
</code></pre></div></div>
#### Parameters
---
* `time`

The time object, as obtained from a `DUCKDB_TYPE_TIME` column.
* `returns`

The `duckdb_time_struct` with the decomposed elements.

<br>

### duckdb_to_time
---
Re-compose a `duckdb_time` from hour, minute, second and microsecond (`duckdb_time_struct`).

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_time</span> <span class="k">duckdb_to_time</span>(<span class="k">
</span>  <span class="kt">duckdb_time_struct</span> <span class="k">time
</span>);
</code></pre></div></div>
#### Parameters
---
* `time`

The hour, minute, second and microsecond in a `duckdb_time_struct`.
* `returns`

The `duckdb_time` element.

<br>

### duckdb_from_timestamp
---
Decompose a `duckdb_timestamp` object into a `duckdb_timestamp_struct`.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_timestamp_struct</span> <span class="k">duckdb_from_timestamp</span>(<span class="k">
</span>  <span class="kt">duckdb_timestamp</span> <span class="k">ts
</span>);
</code></pre></div></div>
#### Parameters
---
* `ts`

The ts object, as obtained from a `DUCKDB_TYPE_TIMESTAMP` column.
* `returns`

The `duckdb_timestamp_struct` with the decomposed elements.

<br>

### duckdb_to_timestamp
---
Re-compose a `duckdb_timestamp` from a duckdb_timestamp_struct.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_timestamp</span> <span class="k">duckdb_to_timestamp</span>(<span class="k">
</span>  <span class="kt">duckdb_timestamp_struct</span> <span class="k">ts
</span>);
</code></pre></div></div>
#### Parameters
---
* `ts`

The de-composed elements in a `duckdb_timestamp_struct`.
* `returns`

The `duckdb_timestamp` element.

<br>

### duckdb_hugeint_to_double
---
Converts a duckdb_hugeint object (as obtained from a `DUCKDB_TYPE_HUGEINT` column) into a double.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">double</span> <span class="k">duckdb_hugeint_to_double</span>(<span class="k">
</span>  <span class="kt">duckdb_hugeint</span> <span class="k">val
</span>);
</code></pre></div></div>
#### Parameters
---
* `val`

The hugeint value.
* `returns`

The converted `double` element.

<br>

### duckdb_double_to_hugeint
---
Converts a double value to a duckdb_hugeint object.

If the conversion fails because the double value is too big the result will be 0.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_hugeint</span> <span class="k">duckdb_double_to_hugeint</span>(<span class="k">
</span>  <span class="kt">double</span> <span class="k">val
</span>);
</code></pre></div></div>
#### Parameters
---
* `val`

The double value.
* `returns`

The converted `duckdb_hugeint` element.

<br>

### duckdb_double_to_decimal
---
Converts a double value to a duckdb_decimal object.

If the conversion fails because the double value is too big, or the width/scale are invalid the result will be 0.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">duckdb_decimal</span> <span class="k">duckdb_double_to_decimal</span>(<span class="k">
</span>  <span class="kt">double</span> <span class="k">val</span>,<span class="k">
</span>  <span class="kt">uint8_t</span> <span class="k">width</span>,<span class="k">
</span>  <span class="kt">uint8_t</span> <span class="k">scale
</span>);
</code></pre></div></div>
#### Parameters
---
* `val`

The double value.
* `returns`

The converted `duckdb_decimal` element.

<br>

### duckdb_decimal_to_double
---
Converts a duckdb_decimal object (as obtained from a `DUCKDB_TYPE_DECIMAL` column) into a double.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">double</span> <span class="k">duckdb_decimal_to_double</span>(<span class="k">
</span>  <span class="k">duckdb_decimal</span> <span class="k">val
</span>);
</code></pre></div></div>
#### Parameters
---
* `val`

The decimal value.
* `returns`

The converted `double` element.

<br>

### duckdb_create_logical_type
---
Creates a `duckdb_logical_type` from a standard primitive type.
The resulting type should be destroyed with `duckdb_destroy_logical_type`.

This should not be used with `DUCKDB_TYPE_DECIMAL`.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="k">duckdb_create_logical_type</span>(<span class="k">
</span>  <span class="k">duckdb_type</span> <span class="k">type
</span>);
</code></pre></div></div>
#### Parameters
---
* `type`

The primitive type to create.
* `returns`

The logical type.

<br>

### duckdb_create_list_type
---
Creates a list type from its child type.
The resulting type should be destroyed with `duckdb_destroy_logical_type`.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="k">duckdb_create_list_type</span>(<span class="k">
</span>  <span class="kt">duckdb_logical_type</span> <span class="k">type
</span>);
</code></pre></div></div>
#### Parameters
---
* `type`

The child type of list type to create.
* `returns`

The logical type.

<br>

### duckdb_create_map_type
---
Creates a map type from its key type and value type.
The resulting type should be destroyed with `duckdb_destroy_logical_type`.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="k">duckdb_create_map_type</span>(<span class="k">
</span>  <span class="kt">duckdb_logical_type</span> <span class="k">key_type</span>,<span class="k">
</span>  <span class="kt">duckdb_logical_type</span> <span class="k">value_type
</span>);
</code></pre></div></div>
#### Parameters
---
* `type`

The key type and value type of map type to create.
* `returns`

The logical type.

<br>

### duckdb_create_union_type
---
Creates a UNION type from the passed types array
The resulting type should be destroyed with `duckdb_destroy_logical_type`.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="k">duckdb_create_union_type</span>(<span class="k">
</span>  <span class="kt">duckdb_logical_type</span> <span class="k">member_types</span>,<span class="k">
</span>  <span class="kt">const</span> <span class="kt">char</span> **<span class="k">member_names</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">member_count
</span>);
</code></pre></div></div>
#### Parameters
---
* `types`

The array of types that the union should consist of.
* `type_amount`

The size of the types array.
* `returns`

The logical type.

<br>

### duckdb_create_decimal_type
---
Creates a `duckdb_logical_type` of type decimal with the specified width and scale
The resulting type should be destroyed with `duckdb_destroy_logical_type`.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="k">duckdb_create_decimal_type</span>(<span class="k">
</span>  <span class="kt">uint8_t</span> <span class="k">width</span>,<span class="k">
</span>  <span class="kt">uint8_t</span> <span class="k">scale
</span>);
</code></pre></div></div>
#### Parameters
---
* `width`

The width of the decimal type
* `scale`

The scale of the decimal type
* `returns`

The logical type.

<br>

### duckdb_get_type_id
---
Retrieves the type class of a `duckdb_logical_type`.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">duckdb_type</span> <span class="k">duckdb_get_type_id</span>(<span class="k">
</span>  <span class="kt">duckdb_logical_type</span> <span class="k">type
</span>);
</code></pre></div></div>
#### Parameters
---
* `type`

The logical type object
* `returns`

The type id

<br>

### duckdb_decimal_width
---
Retrieves the width of a decimal type.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">uint8_t</span> <span class="k">duckdb_decimal_width</span>(<span class="k">
</span>  <span class="kt">duckdb_logical_type</span> <span class="k">type
</span>);
</code></pre></div></div>
#### Parameters
---
* `type`

The logical type object
* `returns`

The width of the decimal type

<br>

### duckdb_decimal_scale
---
Retrieves the scale of a decimal type.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">uint8_t</span> <span class="k">duckdb_decimal_scale</span>(<span class="k">
</span>  <span class="kt">duckdb_logical_type</span> <span class="k">type
</span>);
</code></pre></div></div>
#### Parameters
---
* `type`

The logical type object
* `returns`

The scale of the decimal type

<br>

### duckdb_decimal_internal_type
---
Retrieves the internal storage type of a decimal type.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">duckdb_type</span> <span class="k">duckdb_decimal_internal_type</span>(<span class="k">
</span>  <span class="kt">duckdb_logical_type</span> <span class="k">type
</span>);
</code></pre></div></div>
#### Parameters
---
* `type`

The logical type object
* `returns`

The internal type of the decimal type

<br>

### duckdb_enum_internal_type
---
Retrieves the internal storage type of an enum type.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">duckdb_type</span> <span class="k">duckdb_enum_internal_type</span>(<span class="k">
</span>  <span class="kt">duckdb_logical_type</span> <span class="k">type
</span>);
</code></pre></div></div>
#### Parameters
---
* `type`

The logical type object
* `returns`

The internal type of the enum type

<br>

### duckdb_enum_dictionary_size
---
Retrieves the dictionary size of the enum type

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">uint32_t</span> <span class="k">duckdb_enum_dictionary_size</span>(<span class="k">
</span>  <span class="kt">duckdb_logical_type</span> <span class="k">type
</span>);
</code></pre></div></div>
#### Parameters
---
* `type`

The logical type object
* `returns`

The dictionary size of the enum type

<br>

### duckdb_enum_dictionary_value
---
Retrieves the dictionary value at the specified position from the enum.

The result must be freed with `duckdb_free`

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">char</span> *<span class="k">duckdb_enum_dictionary_value</span>(<span class="k">
</span>  <span class="kt">duckdb_logical_type</span> <span class="k">type</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">index
</span>);
</code></pre></div></div>
#### Parameters
---
* `type`

The logical type object
* `index`

The index in the dictionary
* `returns`

The string value of the enum type. Must be freed with `duckdb_free`.

<br>

### duckdb_list_type_child_type
---
Retrieves the child type of the given list type.

The result must be freed with `duckdb_destroy_logical_type`

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="k">duckdb_list_type_child_type</span>(<span class="k">
</span>  <span class="kt">duckdb_logical_type</span> <span class="k">type
</span>);
</code></pre></div></div>
#### Parameters
---
* `type`

The logical type object
* `returns`

The child type of the list type. Must be destroyed with `duckdb_destroy_logical_type`.

<br>

### duckdb_map_type_key_type
---
Retrieves the key type of the given map type.

The result must be freed with `duckdb_destroy_logical_type`

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="k">duckdb_map_type_key_type</span>(<span class="k">
</span>  <span class="kt">duckdb_logical_type</span> <span class="k">type
</span>);
</code></pre></div></div>
#### Parameters
---
* `type`

The logical type object
* `returns`

The key type of the map type. Must be destroyed with `duckdb_destroy_logical_type`.

<br>

### duckdb_map_type_value_type
---
Retrieves the value type of the given map type.

The result must be freed with `duckdb_destroy_logical_type`

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="k">duckdb_map_type_value_type</span>(<span class="k">
</span>  <span class="kt">duckdb_logical_type</span> <span class="k">type
</span>);
</code></pre></div></div>
#### Parameters
---
* `type`

The logical type object
* `returns`

The value type of the map type. Must be destroyed with `duckdb_destroy_logical_type`.

<br>

### duckdb_struct_type_child_count
---
Returns the number of children of a struct type.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="k">duckdb_struct_type_child_count</span>(<span class="k">
</span>  <span class="kt">duckdb_logical_type</span> <span class="k">type
</span>);
</code></pre></div></div>
#### Parameters
---
* `type`

The logical type object
* `returns`

The number of children of a struct type.

<br>

### duckdb_struct_type_child_name
---
Retrieves the name of the struct child.

The result must be freed with `duckdb_free`

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">char</span> *<span class="k">duckdb_struct_type_child_name</span>(<span class="k">
</span>  <span class="kt">duckdb_logical_type</span> <span class="k">type</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">index
</span>);
</code></pre></div></div>
#### Parameters
---
* `type`

The logical type object
* `index`

The child index
* `returns`

The name of the struct type. Must be freed with `duckdb_free`.

<br>

### duckdb_struct_type_child_type
---
Retrieves the child type of the given struct type at the specified index.

The result must be freed with `duckdb_destroy_logical_type`

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="k">duckdb_struct_type_child_type</span>(<span class="k">
</span>  <span class="kt">duckdb_logical_type</span> <span class="k">type</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">index
</span>);
</code></pre></div></div>
#### Parameters
---
* `type`

The logical type object
* `index`

The child index
* `returns`

The child type of the struct type. Must be destroyed with `duckdb_destroy_logical_type`.

<br>

### duckdb_union_type_member_count
---
Returns the number of members that the union type has.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="k">duckdb_union_type_member_count</span>(<span class="k">
</span>  <span class="kt">duckdb_logical_type</span> <span class="k">type
</span>);
</code></pre></div></div>
#### Parameters
---
* `type`

The logical type (union) object
* `returns`

The number of members of a union type.

<br>

### duckdb_union_type_member_name
---
Retrieves the name of the union member.

The result must be freed with `duckdb_free`

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">char</span> *<span class="k">duckdb_union_type_member_name</span>(<span class="k">
</span>  <span class="kt">duckdb_logical_type</span> <span class="k">type</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">index
</span>);
</code></pre></div></div>
#### Parameters
---
* `type`

The logical type object
* `index`

The child index
* `returns`

The name of the union member. Must be freed with `duckdb_free`.

<br>

### duckdb_union_type_member_type
---
Retrieves the child type of the given union member at the specified index.

The result must be freed with `duckdb_destroy_logical_type`

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="k">duckdb_union_type_member_type</span>(<span class="k">
</span>  <span class="kt">duckdb_logical_type</span> <span class="k">type</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">index
</span>);
</code></pre></div></div>
#### Parameters
---
* `type`

The logical type object
* `index`

The child index
* `returns`

The child type of the union member. Must be destroyed with `duckdb_destroy_logical_type`.

<br>

### duckdb_destroy_logical_type
---
Destroys the logical type and de-allocates all memory allocated for that type.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="k">duckdb_destroy_logical_type</span>(<span class="k">
</span>  <span class="kt">duckdb_logical_type</span> *<span class="k">type
</span>);
</code></pre></div></div>
#### Parameters
---
* `type`

The logical type to destroy.

<br>

