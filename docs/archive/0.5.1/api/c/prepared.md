---
layout: docu
title: C API - Prepared Statements
selected: Prepared Statements
---

A prepared statement is a parameterized query. The query is prepared with question marks (`?`) or dollar symbols (`$1`) indicating the parameters of the query. Values can then be bound to these parameters, after which the prepared statement can be executed using those parameters. A single query can be prepared once and executed many times.

Prepared statements are useful to:
* Easily supply parameters to functions while avoiding string concatenation/SQL injection attacks.
* Speeding up queries that will be executed many times with different parameters.

DuckDB supports prepared statements in the C API with the `duckdb_prepare` method. The `duckdb_bind` family of functions is used to supply values for subsequent execution of the prepared statement using `duckdb_execute_prepared`. After we are done with the prepared statement it can be cleaned up using the `duckdb_destroy_prepare` method.

### **Example**
```c
duckdb_prepared_statement stmt;
duckdb_result result;
if (duckdb_prepare(con, "INSERT INTO integers VALUES ($1, $2)", &stmt) == DuckDBError) {
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

After calling `duckdb_prepare`, the prepared statement parameters can be inspected using `duckdb_nparams` and `duckdb_param_type`. In case the prepare fails, the error can be obtained through `duckdb_prepare_error`.

It is not required that the `duckdb_bind` family of functions matches the prepared statement parameter type exactly. The values will be auto-cast to the required value as required. For example, calling `duckdb_bind_int8` on a parameter type of `DUCKDB_TYPE_INTEGER` will work as expected.

> Do **not** use prepared statements to insert large amounts of data into DuckDB. Instead it is recommended to use the [Appender](appender).

## **API Reference**
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_prepare">duckdb_prepare</a></span>(<span class="kt">duckdb_connection</span> <span class="k">connection</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="k">query</span>, <span class="kt">duckdb_prepared_statement</span> *<span class="k">out_prepared_statement</span>);
<span class="kt">void</span> <span class="nf"><a href="#duckdb_destroy_prepare">duckdb_destroy_prepare</a></span>(<span class="kt">duckdb_prepared_statement</span> *<span class="k">prepared_statement</span>);
<span class="kt">const</span> <span class="kt">char</span> *<span class="nf"><a href="#duckdb_prepare_error">duckdb_prepare_error</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>);
<span class="kt">idx_t</span> <span class="nf"><a href="#duckdb_nparams">duckdb_nparams</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>);
<span class="k">duckdb_type</span> <span class="nf"><a href="#duckdb_param_type">duckdb_param_type</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_clear_bindings">duckdb_clear_bindings</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_boolean">duckdb_bind_boolean</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">bool</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_int8">duckdb_bind_int8</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">int8_t</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_int16">duckdb_bind_int16</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">int16_t</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_int32">duckdb_bind_int32</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">int32_t</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_int64">duckdb_bind_int64</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">int64_t</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_hugeint">duckdb_bind_hugeint</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">duckdb_hugeint</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_uint8">duckdb_bind_uint8</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">uint8_t</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_uint16">duckdb_bind_uint16</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">uint16_t</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_uint32">duckdb_bind_uint32</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">uint32_t</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_uint64">duckdb_bind_uint64</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">uint64_t</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_float">duckdb_bind_float</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">float</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_double">duckdb_bind_double</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">double</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_date">duckdb_bind_date</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">duckdb_date</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_time">duckdb_bind_time</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">duckdb_time</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_timestamp">duckdb_bind_timestamp</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">duckdb_timestamp</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_interval">duckdb_bind_interval</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">duckdb_interval</span> <span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_varchar">duckdb_bind_varchar</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="k">val</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_varchar_length">duckdb_bind_varchar_length</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="k">val</span>, <span class="kt">idx_t</span> <span class="k">length</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_blob">duckdb_bind_blob</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>, <span class="kt">const</span> <span class="kt">void</span> *<span class="k">data</span>, <span class="kt">idx_t</span> <span class="k">length</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_bind_null">duckdb_bind_null</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">idx_t</span> <span class="k">param_idx</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_execute_prepared">duckdb_execute_prepared</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">duckdb_result</span> *<span class="k">out_result</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_execute_prepared_arrow">duckdb_execute_prepared_arrow</a></span>(<span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>, <span class="kt">duckdb_arrow</span> *<span class="k">out_result</span>);
</code></pre></div></div>
### **duckdb_prepare**
---
Create a prepared statement object from a query.

Note that after calling `duckdb_prepare`, the prepared statement should always be destroyed using
`duckdb_destroy_prepare`, even if the prepare fails.

If the prepare fails, `duckdb_prepare_error` can be called to obtain the reason why the prepare failed.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_prepare</span>(<span class="k">
</span>  <span class="kt">duckdb_connection</span> <span class="k">connection</span>,<span class="k">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="k">query</span>,<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> *<span class="k">out_prepared_statement
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `connection`

The connection object
* `query`

The SQL query to prepare
* `out_prepared_statement`

The resulting prepared statement object
* `returns`

`DuckDBSuccess` on success or `DuckDBError` on failure.

<br>

### **duckdb_destroy_prepare**
---
Closes the prepared statement and de-allocates all memory allocated for the statement.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="k">duckdb_destroy_prepare</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> *<span class="k">prepared_statement
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `prepared_statement`

The prepared statement to destroy.

<br>

### **duckdb_prepare_error**
---
Returns the error message associated with the given prepared statement.
If the prepared statement has no error message, this returns `nullptr` instead.

The error message should not be freed. It will be de-allocated when `duckdb_destroy_prepare` is called.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">const</span> <span class="kt">char</span> *<span class="k">duckdb_prepare_error</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `prepared_statement`

The prepared statement to obtain the error from.
* `returns`

The error message, or `nullptr` if there is none.

<br>

### **duckdb_nparams**
---
Returns the number of parameters that can be provided to the given prepared statement.

Returns 0 if the query was not successfully prepared.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="k">duckdb_nparams</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `prepared_statement`

The prepared statement to obtain the number of parameters for.

<br>

### **duckdb_param_type**
---
Returns the parameter type for the parameter at the given index.

Returns `DUCKDB_TYPE_INVALID` if the parameter index is out of range or the statement was not successfully prepared.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="k">duckdb_type</span> <span class="k">duckdb_param_type</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `prepared_statement`

The prepared statement.
* `param_idx`

The parameter index.
* `returns`

The parameter type

<br>

### **duckdb_clear_bindings**
---
Clear the params bind to the prepared statement.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_clear_bindings</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_boolean**
---
Binds a bool value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_boolean</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">bool</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_int8**
---
Binds an int8_t value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_int8</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">int8_t</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_int16**
---
Binds an int16_t value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_int16</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">int16_t</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_int32**
---
Binds an int32_t value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_int32</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">int32_t</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_int64**
---
Binds an int64_t value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_int64</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">int64_t</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_hugeint**
---
Binds an duckdb_hugeint value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_hugeint</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">duckdb_hugeint</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_uint8**
---
Binds an uint8_t value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_uint8</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">uint8_t</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_uint16**
---
Binds an uint16_t value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_uint16</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">uint16_t</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_uint32**
---
Binds an uint32_t value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_uint32</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">uint32_t</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_uint64**
---
Binds an uint64_t value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_uint64</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">uint64_t</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_float**
---
Binds an float value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_float</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">float</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_double**
---
Binds an double value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_double</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">double</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_date**
---
Binds a duckdb_date value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_date</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">duckdb_date</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_time**
---
Binds a duckdb_time value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_time</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">duckdb_time</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_timestamp**
---
Binds a duckdb_timestamp value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_timestamp</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">duckdb_timestamp</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_interval**
---
Binds a duckdb_interval value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_interval</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">duckdb_interval</span> <span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_varchar**
---
Binds a null-terminated varchar value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_varchar</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="k">val
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_varchar_length**
---
Binds a varchar value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_varchar_length</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="k">val</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">length
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_blob**
---
Binds a blob value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_blob</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx</span>,<span class="k">
</span>  <span class="kt">const</span> <span class="kt">void</span> *<span class="k">data</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">length
</span>);
</code></pre></div></div>
<br>

### **duckdb_bind_null**
---
Binds a NULL value to the prepared statement at the specified index.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_bind_null</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">param_idx
</span>);
</code></pre></div></div>
<br>

### **duckdb_execute_prepared**
---
Executes the prepared statement with the given bound parameters, and returns a materialized query result.

This method can be called multiple times for each prepared statement, and the parameters can be modified
between calls to this function.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_execute_prepared</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">duckdb_result</span> *<span class="k">out_result
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `prepared_statement`

The prepared statement to execute.
* `out_result`

The query result.
* `returns`

`DuckDBSuccess` on success or `DuckDBError` on failure.

<br>

### **duckdb_execute_prepared_arrow**
---
Executes the prepared statement with the given bound parameters, and returns an arrow query result.

#### **Syntax**
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_execute_prepared_arrow</span>(<span class="k">
</span>  <span class="kt">duckdb_prepared_statement</span> <span class="k">prepared_statement</span>,<span class="k">
</span>  <span class="kt">duckdb_arrow</span> *<span class="k">out_result
</span>);
</code></pre></div></div>
#### **Parameters**
---
* `prepared_statement`

The prepared statement to execute.
* `out_result`

The query result.
* `returns`

`DuckDBSuccess` on success or `DuckDBError` on failure.

<br>

