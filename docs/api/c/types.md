---
layout: docu
title: C API - Types
selected: Types
---

DuckDB is a strongly typed database system. As such, every column has a single type specified. This type is constant
over the entire column. That is to say, a column that is labeled as an `INTEGER` column will only contain `INTEGER`
values.

The supported types are listed below:

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
  DUCKDB_TYPE_BLOB
} duckdb_type;
```

The type of a column in the result can be obtained using the `duckdb_column_type` function. The internal type of the
columns is especially relevant for correct usage of the `duckdb_column_data` function.

The mapping from column type to internal type is provided in the table below.

|      Column Type      |    Data Type     |
|-----------------------|------------------|
| DUCKDB_TYPE_BOOLEAN   | bool             |
| DUCKDB_TYPE_TINYINT   | int8_t           |
| DUCKDB_TYPE_SMALLINT  | int16_t          |
| DUCKDB_TYPE_INTEGER   | int32_t          |
| DUCKDB_TYPE_BIGINT    | int64_t          |
| DUCKDB_TYPE_UTINYINT  | uint8_t          |
| DUCKDB_TYPE_USMALLINT | uint16_t         |
| DUCKDB_TYPE_UINTEGER  | uint32_t         |
| DUCKDB_TYPE_UBIGINT   | uint64_t         |
| DUCKDB_TYPE_FLOAT     | float            |
| DUCKDB_TYPE_DOUBLE    | double           |
| DUCKDB_TYPE_TIMESTAMP | duckdb_timestamp |
| DUCKDB_TYPE_DATE      | duckdb_date      |
| DUCKDB_TYPE_TIME      | duckdb_time      |
| DUCKDB_TYPE_INTERVAL  | duckdb_interval  |
| DUCKDB_TYPE_HUGEINT   | duckdb_hugeint   |
| DUCKDB_TYPE_VARCHAR   | const char*      |
| DUCKDB_TYPE_BLOB      | duckdb_blob      |

#### **duckdb_value**
The `duckdb_value` functions will auto-cast values as required. For example, it is no problem to use
`duckdb_value_double` on a column of type `duckdb_value_int32`. The value will be auto-cast and returned as a double.
Note that in certain cases the cast may fail. For example, this can happen if we request a `duckdb_value_int8` and the value does not fit within an `int8` value. In this case, a default value will be returned (usually `0` or `nullptr`). The same default value will also be returned if the corresponding value is `NULL`.

The `duckdb_value_is_null` function can be used to check if a specific value is `NULL` or not.

The exception to the auto-cast rule is the `duckdb_value_varchar_internal` function. This function does not auto-cast and only works for `VARCHAR` columns. The reason this function exists is that the result does not need to be freed.

> Note that `duckdb_value_varchar` and `duckdb_value_blob` require the result to be de-allocated using `duckdb_free`.

#### **duckdb_column_data**
The `duckdb_column_data` returns a pointer to an internal array within the result. The type of the elements of the array
depends on the internal type of the column, as obtained using `duckdb_column_type`. The corresponding null values can
be obtained using the `duckdb_nullmask_data` function.

The exact data types can be seen in the table above. For numeric types, the internal types of the columns are standard built-in types. For example, for a column of type `DUCKDB_TYPE_INTEGER` the internal type is a `int32_t`. For text
(varchar) columns, the internal type is a pointer to a null-terminated string.

For dates, times, timestamps, blobs, intervals and hugeints, the internal types are DuckDB-specific structs as defined below:

```c
//! Days are stored as days since 1970-01-01
//! Use the duckdb_from_date/duckdb_to_date function to extract individual information
typedef struct {
	int32_t days;
} duckdb_date;

//! Time is stored as microseconds since 00:00:00
//! Use the duckdb_from_time/duckdb_to_time function to extract individual information
typedef struct {
	int64_t micros;
} duckdb_time;

//! Timestamps are stored as microseconds since 1970-01-01
//! Use the duckdb_from_timestamp/duckdb_to_timestamp function to extract individual information
typedef struct {
	int64_t micros;
} duckdb_timestamp;

typedef struct {
	int32_t months;
	int32_t days;
	int64_t micros;
} duckdb_interval;

//! Hugeints are composed in a (lower, upper) component
//! The value of the hugeint is upper * 2^64 + lower
//! For easy usage, the functions duckdb_hugeint_to_double/duckdb_double_to_hugeint are recommended
typedef struct {
	uint64_t lower;
	int64_t upper;
} duckdb_hugeint;

typedef struct {
	void *data;
	idx_t size;
} duckdb_blob;
```

For hugeints, dates, times and timestamps there are also several helper functions available in order to facilitate easier usage of these types. See the API reference below for the available functions.

```c
// helper structs, as used by the Date/Time/Timestamp Helpers
typedef struct {
	int32_t year;
	int8_t month;
	int8_t day;
} duckdb_date_struct;

typedef struct {
	int8_t hour;
	int8_t min;
	int8_t sec;
	int32_t micros;
} duckdb_time_struct;

typedef struct {
	duckdb_date_struct date;
	duckdb_time_struct time;
} duckdb_timestamp_struct;
```

## **API Reference**
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">bool</span> <span class="nf"><a href="#duckdb_value_boolean">duckdb_value_boolean</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">int8_t</span> <span class="nf"><a href="#duckdb_value_int8">duckdb_value_int8</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">int16_t</span> <span class="nf"><a href="#duckdb_value_int16">duckdb_value_int16</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">int32_t</span> <span class="nf"><a href="#duckdb_value_int32">duckdb_value_int32</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">int64_t</span> <span class="nf"><a href="#duckdb_value_int64">duckdb_value_int64</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">duckdb_hugeint</span> <span class="nf"><a href="#duckdb_value_hugeint">duckdb_value_hugeint</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
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
<span class="kt">duckdb_blob</span> <span class="nf"><a href="#duckdb_value_blob">duckdb_value_blob</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">bool</span> <span class="nf"><a href="#duckdb_value_is_null">duckdb_value_is_null</a></span>(<span class="kt">duckdb_result</span> *<span class="k">result</span>, <span class="kt">idx_t</span> <span class="k">col</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
</code></pre></div></div>
#### **Date/Time/Timestamp Helpers**
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_date_struct</span> <span class="nf"><a href="#duckdb_from_date">duckdb_from_date</a></span>(<span class="kt">duckdb_date</span> <span class="k">date</span>);
<span class="kt">duckdb_date</span> <span class="nf"><a href="#duckdb_to_date">duckdb_to_date</a></span>(<span class="kt">duckdb_date_struct</span> <span class="k">date</span>);
<span class="kt">duckdb_time_struct</span> <span class="nf"><a href="#duckdb_from_time">duckdb_from_time</a></span>(<span class="kt">duckdb_time</span> <span class="k">time</span>);
<span class="kt">duckdb_time</span> <span class="nf"><a href="#duckdb_to_time">duckdb_to_time</a></span>(<span class="kt">duckdb_time_struct</span> <span class="k">time</span>);
<span class="kt">duckdb_timestamp_struct</span> <span class="nf"><a href="#duckdb_from_timestamp">duckdb_from_timestamp</a></span>(<span class="kt">duckdb_timestamp</span> <span class="k">ts</span>);
<span class="kt">duckdb_timestamp</span> <span class="nf"><a href="#duckdb_to_timestamp">duckdb_to_timestamp</a></span>(<span class="kt">duckdb_timestamp_struct</span> <span class="k">ts</span>);
</code></pre></div></div>
#### **Hugeint Helpers**
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">double</span> <span class="nf"><a href="#duckdb_hugeint_to_double">duckdb_hugeint_to_double</a></span>(<span class="kt">duckdb_hugeint</span> <span class="k">val</span>);
<span class="kt">duckdb_hugeint</span> <span class="nf"><a href="#duckdb_double_to_hugeint">duckdb_double_to_hugeint</a></span>(<span class="kt">double</span> <span class="k">val</span>);
</code></pre></div></div>
### **duckdb_value_boolean**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">bool</span> <span class="k">duckdb_value_boolean</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The boolean value at the specified location, or false if the value cannot be converted.

<br>

### **duckdb_value_int8**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">int8_t</span> <span class="k">duckdb_value_int8</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The int8_t value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_int16**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">int16_t</span> <span class="k">duckdb_value_int16</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The int16_t value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_int32**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">int32_t</span> <span class="k">duckdb_value_int32</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The int32_t value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_int64**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">int64_t</span> <span class="k">duckdb_value_int64</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The int64_t value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_hugeint**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_hugeint</span> <span class="k">duckdb_value_hugeint</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The duckdb_hugeint value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_uint8**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">uint8_t</span> <span class="k">duckdb_value_uint8</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The uint8_t value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_uint16**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">uint16_t</span> <span class="k">duckdb_value_uint16</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The uint16_t value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_uint32**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">uint32_t</span> <span class="k">duckdb_value_uint32</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The uint32_t value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_uint64**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">uint64_t</span> <span class="k">duckdb_value_uint64</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The uint64_t value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_float**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">float</span> <span class="k">duckdb_value_float</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The float value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_double**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">double</span> <span class="k">duckdb_value_double</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The double value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_date**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_date</span> <span class="k">duckdb_value_date</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The duckdb_date value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_time**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_time</span> <span class="k">duckdb_value_time</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The duckdb_time value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_timestamp**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_timestamp</span> <span class="k">duckdb_value_timestamp</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The duckdb_timestamp value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_interval**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_interval</span> <span class="k">duckdb_value_interval</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The duckdb_interval value at the specified location, or 0 if the value cannot be converted.

<br>

### **duckdb_value_varchar**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">char</span> *<span class="k">duckdb_value_varchar</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The char* value at the specified location, or nullptr if the value cannot be converted.
The result must be freed with `duckdb_free`.

<br>

### **duckdb_value_varchar_internal**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">char</span> *<span class="k">duckdb_value_varchar_internal</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The char* value at the specified location. ONLY works on VARCHAR columns and does not auto-cast.
If the column is NOT a VARCHAR column this function will return NULL.

The result must NOT be freed.

<br>

### **duckdb_value_blob**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_blob</span> <span class="k">duckdb_value_blob</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

The duckdb_blob value at the specified location. Returns a blob with blob.data set to nullptr if the
value cannot be converted. The resulting "blob.data" must be freed with `duckdb_free.`

<br>

### **duckdb_value_is_null**
---
#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">bool</span> <span class="k">duckdb_value_is_null</span>(<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">result</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `returns`

Returns true if the value at the specified index is NULL, and false otherwise.

<br>

### **duckdb_from_date**
---
Decompose a `duckdb_date` object into year, month and date (stored as `duckdb_date_struct`).

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_date_struct</span> <span class="k">duckdb_from_date</span>(<span class="k">
</span>  <span class="kt">duckdb_date</span> <span class="k">date
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `date`

The date object, as obtained from a `DUCKDB_TYPE_DATE` column.
* `returns`

The `duckdb_date_struct` with the decomposed elements.

<br>

### **duckdb_to_date**
---
Re-compose a `duckdb_date` from year, month and date (`duckdb_date_struct`).

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_date</span> <span class="k">duckdb_to_date</span>(<span class="k">
</span>  <span class="kt">duckdb_date_struct</span> <span class="k">date
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `date`

The year, month and date stored in a `duckdb_date_struct`.
* `returns`

The `duckdb_date` element.

<br>

### **duckdb_from_time**
---
Decompose a `duckdb_time` object into hour, minute, second and microsecond (stored as `duckdb_time_struct`).

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_time_struct</span> <span class="k">duckdb_from_time</span>(<span class="k">
</span>  <span class="kt">duckdb_time</span> <span class="k">time
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `time`

The time object, as obtained from a `DUCKDB_TYPE_TIME` column.
* `returns`

The `duckdb_time_struct` with the decomposed elements.

<br>

### **duckdb_to_time**
---
Re-compose a `duckdb_time` from hour, minute, second and microsecond (`duckdb_time_struct`).

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_time</span> <span class="k">duckdb_to_time</span>(<span class="k">
</span>  <span class="kt">duckdb_time_struct</span> <span class="k">time
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `time`

The hour, minute, second and microsecond in a `duckdb_time_struct`.
* `returns`

The `duckdb_time` element.

<br>

### **duckdb_from_timestamp**
---
Decompose a `duckdb_timestamp` object into a `duckdb_timestamp_struct`.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_timestamp_struct</span> <span class="k">duckdb_from_timestamp</span>(<span class="k">
</span>  <span class="kt">duckdb_timestamp</span> <span class="k">ts
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `ts`

The ts object, as obtained from a `DUCKDB_TYPE_TIMESTAMP` column.
* `returns`

The `duckdb_timestamp_struct` with the decomposed elements.

<br>

### **duckdb_to_timestamp**
---
Re-compose a `duckdb_timestamp` from a duckdb_timestamp_struct.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_timestamp</span> <span class="k">duckdb_to_timestamp</span>(<span class="k">
</span>  <span class="kt">duckdb_timestamp_struct</span> <span class="k">ts
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `ts`

The de-composed elements in a `duckdb_timestamp_struct`.
* `returns`

The `duckdb_timestamp` element.

<br>

### **duckdb_hugeint_to_double**
---
Converts a duckdb_hugeint object (as obtained from a `DUCKDB_TYPE_HUGEINT` column) into a double.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">double</span> <span class="k">duckdb_hugeint_to_double</span>(<span class="k">
</span>  <span class="kt">duckdb_hugeint</span> <span class="k">val
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `val`

The hugeint value.
* `returns`

The converted `double` element.

<br>

### **duckdb_double_to_hugeint**
---
Converts a double value to a duckdb_hugeint object.

If the conversion fails because the double value is too big the result will be 0.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_hugeint</span> <span class="k">duckdb_double_to_hugeint</span>(<span class="k">
</span>  <span class="kt">double</span> <span class="k">val
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `val`

The double value.
* `returns`

The converted `duckdb_hugeint` element.

<br>

