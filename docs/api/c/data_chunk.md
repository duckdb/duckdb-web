---
layout: docu
title: C API - Data Chunks
selected: Data Chunks
---

Data chunks represent a horizontal slice of a table. They hold a number of vectors, that can each hold up to the `VECTOR_SIZE` rows. The vector size can be obtained through the `duckdb_vector_size` function and is configurable, but is usually set to `2048`.

Data chunks and vectors are what DuckDB uses natively to store and represent data. For this reason, the data chunk interface is the most efficient way of interfacing with DuckDB. Be aware, however, that correctly interfacing with DuckDB using the data chunk API does require knowledge of DuckDB's internal vector format.

The primary manner of interfacing with data chunks is by obtaining the internal vectors of the data chunk using the `duckdb_data_chunk_get_vector` method, and subsequently using the `duckdb_vector_get_data` and `duckdb_vector_get_validity` methods to read the internal data and the validity mask of the vector. For composite types (list and struct vectors), `duckdb_list_vector_get_child` and `duckdb_struct_vector_get_child` should be used to read child vectors.



## **API Reference**
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_data_chunk</span> <span class="nf"><a href="#duckdb_create_data_chunk">duckdb_create_data_chunk</a></span>(<span class="kt">duckdb_logical_type</span> *<span class="k">types</span>, <span class="kt">idx_t</span> <span class="k">column_count</span>);
<span class="kt">void</span> <span class="nf"><a href="#duckdb_destroy_data_chunk">duckdb_destroy_data_chunk</a></span>(<span class="kt">duckdb_data_chunk</span> *<span class="k">chunk</span>);
<span class="kt">void</span> <span class="nf"><a href="#duckdb_data_chunk_reset">duckdb_data_chunk_reset</a></span>(<span class="kt">duckdb_data_chunk</span> <span class="k">chunk</span>);
<span class="kt">idx_t</span> <span class="nf"><a href="#duckdb_data_chunk_get_column_count">duckdb_data_chunk_get_column_count</a></span>(<span class="kt">duckdb_data_chunk</span> <span class="k">chunk</span>);
<span class="kt">duckdb_vector</span> <span class="nf"><a href="#duckdb_data_chunk_get_vector">duckdb_data_chunk_get_vector</a></span>(<span class="kt">duckdb_data_chunk</span> <span class="k">chunk</span>, <span class="kt">idx_t</span> <span class="k">col_idx</span>);
<span class="kt">idx_t</span> <span class="nf"><a href="#duckdb_data_chunk_get_size">duckdb_data_chunk_get_size</a></span>(<span class="kt">duckdb_data_chunk</span> <span class="k">chunk</span>);
<span class="kt">void</span> <span class="nf"><a href="#duckdb_data_chunk_set_size">duckdb_data_chunk_set_size</a></span>(<span class="kt">duckdb_data_chunk</span> <span class="k">chunk</span>, <span class="kt">idx_t</span> <span class="k">size</span>);
</code></pre></div></div>
#### Vector Interface
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="nf"><a href="#duckdb_vector_get_column_type">duckdb_vector_get_column_type</a></span>(<span class="kt">duckdb_vector</span> <span class="k">vector</span>);
<span class="kt">void</span> *<span class="nf"><a href="#duckdb_vector_get_data">duckdb_vector_get_data</a></span>(<span class="kt">duckdb_vector</span> <span class="k">vector</span>);
<span class="kt">uint64_t</span> *<span class="nf"><a href="#duckdb_vector_get_validity">duckdb_vector_get_validity</a></span>(<span class="kt">duckdb_vector</span> <span class="k">vector</span>);
<span class="kt">void</span> <span class="nf"><a href="#duckdb_vector_ensure_validity_writable">duckdb_vector_ensure_validity_writable</a></span>(<span class="kt">duckdb_vector</span> <span class="k">vector</span>);
<span class="kt">void</span> <span class="nf"><a href="#duckdb_vector_assign_string_element">duckdb_vector_assign_string_element</a></span>(<span class="kt">duckdb_vector</span> <span class="k">vector</span>, <span class="kt">idx_t</span> <span class="k">index</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="k">str</span>);
<span class="kt">void</span> <span class="nf"><a href="#duckdb_vector_assign_string_element_len">duckdb_vector_assign_string_element_len</a></span>(<span class="kt">duckdb_vector</span> <span class="k">vector</span>, <span class="kt">idx_t</span> <span class="k">index</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="k">str</span>, <span class="kt">idx_t</span> <span class="k">str_len</span>);
<span class="kt">duckdb_vector</span> <span class="nf"><a href="#duckdb_list_vector_get_child">duckdb_list_vector_get_child</a></span>(<span class="kt">duckdb_vector</span> <span class="k">vector</span>);
<span class="kt">idx_t</span> <span class="nf"><a href="#duckdb_list_vector_get_size">duckdb_list_vector_get_size</a></span>(<span class="kt">duckdb_vector</span> <span class="k">vector</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_list_vector_set_size">duckdb_list_vector_set_size</a></span>(<span class="kt">duckdb_vector</span> <span class="k">vector</span>, <span class="kt">idx_t</span> <span class="k">size</span>);
<span class="kt">duckdb_state</span> <span class="nf"><a href="#duckdb_list_vector_reserve">duckdb_list_vector_reserve</a></span>(<span class="kt">duckdb_vector</span> <span class="k">vector</span>, <span class="kt">idx_t</span> <span class="k">required_capacity</span>);
<span class="kt">duckdb_vector</span> <span class="nf"><a href="#duckdb_struct_vector_get_child">duckdb_struct_vector_get_child</a></span>(<span class="kt">duckdb_vector</span> <span class="k">vector</span>, <span class="kt">idx_t</span> <span class="k">index</span>);
</code></pre></div></div>
#### Validity Mask Functions
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">bool</span> <span class="nf"><a href="#duckdb_validity_row_is_valid">duckdb_validity_row_is_valid</a></span>(<span class="kt">uint64_t</span> *<span class="k">validity</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">void</span> <span class="nf"><a href="#duckdb_validity_set_row_validity">duckdb_validity_set_row_validity</a></span>(<span class="kt">uint64_t</span> *<span class="k">validity</span>, <span class="kt">idx_t</span> <span class="k">row</span>, <span class="kt">bool</span> <span class="k">valid</span>);
<span class="kt">void</span> <span class="nf"><a href="#duckdb_validity_set_row_invalid">duckdb_validity_set_row_invalid</a></span>(<span class="kt">uint64_t</span> *<span class="k">validity</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
<span class="kt">void</span> <span class="nf"><a href="#duckdb_validity_set_row_valid">duckdb_validity_set_row_valid</a></span>(<span class="kt">uint64_t</span> *<span class="k">validity</span>, <span class="kt">idx_t</span> <span class="k">row</span>);
</code></pre></div></div>
### duckdb_create_data_chunk
---
Creates an empty DataChunk with the specified set of types.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_data_chunk</span> <span class="k">duckdb_create_data_chunk</span>(<span class="k">
</span>  <span class="kt">duckdb_logical_type</span> *<span class="k">types</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">column_count
</span>);
</code></pre></div></div>
#### Parameters
---
* `types`

An array of types of the data chunk.
* `column_count`

The number of columns.
* `returns`

The data chunk.

<br>

### duckdb_destroy_data_chunk
---
Destroys the data chunk and de-allocates all memory allocated for that chunk.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="k">duckdb_destroy_data_chunk</span>(<span class="k">
</span>  <span class="kt">duckdb_data_chunk</span> *<span class="k">chunk
</span>);
</code></pre></div></div>
#### Parameters
---
* `chunk`

The data chunk to destroy.

<br>

### duckdb_data_chunk_reset
---
Resets a data chunk, clearing the validity masks and setting the cardinality of the data chunk to 0.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="k">duckdb_data_chunk_reset</span>(<span class="k">
</span>  <span class="kt">duckdb_data_chunk</span> <span class="k">chunk
</span>);
</code></pre></div></div>
#### Parameters
---
* `chunk`

The data chunk to reset.

<br>

### duckdb_data_chunk_get_column_count
---
Retrieves the number of columns in a data chunk.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="k">duckdb_data_chunk_get_column_count</span>(<span class="k">
</span>  <span class="kt">duckdb_data_chunk</span> <span class="k">chunk
</span>);
</code></pre></div></div>
#### Parameters
---
* `chunk`

The data chunk to get the data from
* `returns`

The number of columns in the data chunk

<br>

### duckdb_data_chunk_get_vector
---
Retrieves the vector at the specified column index in the data chunk.

The pointer to the vector is valid for as long as the chunk is alive.
It does NOT need to be destroyed.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_vector</span> <span class="k">duckdb_data_chunk_get_vector</span>(<span class="k">
</span>  <span class="kt">duckdb_data_chunk</span> <span class="k">chunk</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">col_idx
</span>);
</code></pre></div></div>
#### Parameters
---
* `chunk`

The data chunk to get the data from
* `returns`

The vector

<br>

### duckdb_data_chunk_get_size
---
Retrieves the current number of tuples in a data chunk.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="k">duckdb_data_chunk_get_size</span>(<span class="k">
</span>  <span class="kt">duckdb_data_chunk</span> <span class="k">chunk
</span>);
</code></pre></div></div>
#### Parameters
---
* `chunk`

The data chunk to get the data from
* `returns`

The number of tuples in the data chunk

<br>

### duckdb_data_chunk_set_size
---
Sets the current number of tuples in a data chunk.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="k">duckdb_data_chunk_set_size</span>(<span class="k">
</span>  <span class="kt">duckdb_data_chunk</span> <span class="k">chunk</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">size
</span>);
</code></pre></div></div>
#### Parameters
---
* `chunk`

The data chunk to set the size in
* `size`

The number of tuples in the data chunk

<br>

### duckdb_vector_get_column_type
---
Retrieves the column type of the specified vector.

The result must be destroyed with `duckdb_destroy_logical_type`.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="k">duckdb_vector_get_column_type</span>(<span class="k">
</span>  <span class="kt">duckdb_vector</span> <span class="k">vector
</span>);
</code></pre></div></div>
#### Parameters
---
* `vector`

The vector get the data from
* `returns`

The type of the vector

<br>

### duckdb_vector_get_data
---
Retrieves the data pointer of the vector.

The data pointer can be used to read or write values from the vector.
How to read or write values depends on the type of the vector.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> *<span class="k">duckdb_vector_get_data</span>(<span class="k">
</span>  <span class="kt">duckdb_vector</span> <span class="k">vector
</span>);
</code></pre></div></div>
#### Parameters
---
* `vector`

The vector to get the data from
* `returns`

The data pointer

<br>

### duckdb_vector_get_validity
---
Retrieves the validity mask pointer of the specified vector.

If all values are valid, this function MIGHT return NULL!

The validity mask is a bitset that signifies null-ness within the data chunk.
It is a series of uint64_t values, where each uint64_t value contains validity for 64 tuples.
The bit is set to 1 if the value is valid (i.e. not NULL) or 0 if the value is invalid (i.e. NULL).

Validity of a specific value can be obtained like this:

idx_t entry_idx = row_idx / 64;
idx_t idx_in_entry = row_idx % 64;
bool is_valid = validity_mask[entry_idx] & (1 << idx_in_entry);

Alternatively, the (slower) duckdb_validity_row_is_valid function can be used.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">uint64_t</span> *<span class="k">duckdb_vector_get_validity</span>(<span class="k">
</span>  <span class="kt">duckdb_vector</span> <span class="k">vector
</span>);
</code></pre></div></div>
#### Parameters
---
* `vector`

The vector to get the data from
* `returns`

The pointer to the validity mask, or NULL if no validity mask is present

<br>

### duckdb_vector_ensure_validity_writable
---
Ensures the validity mask is writable by allocating it.

After this function is called, `duckdb_vector_get_validity` will ALWAYS return non-NULL.
This allows null values to be written to the vector, regardless of whether a validity mask was present before.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="k">duckdb_vector_ensure_validity_writable</span>(<span class="k">
</span>  <span class="kt">duckdb_vector</span> <span class="k">vector
</span>);
</code></pre></div></div>
#### Parameters
---
* `vector`

The vector to alter

<br>

### duckdb_vector_assign_string_element
---
Assigns a string element in the vector at the specified location.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="k">duckdb_vector_assign_string_element</span>(<span class="k">
</span>  <span class="kt">duckdb_vector</span> <span class="k">vector</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">index</span>,<span class="k">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="k">str
</span>);
</code></pre></div></div>
#### Parameters
---
* `vector`

The vector to alter
* `index`

The row position in the vector to assign the string to
* `str`

The null-terminated string

<br>

### duckdb_vector_assign_string_element_len
---
Assigns a string element in the vector at the specified location.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="k">duckdb_vector_assign_string_element_len</span>(<span class="k">
</span>  <span class="kt">duckdb_vector</span> <span class="k">vector</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">index</span>,<span class="k">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="k">str</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">str_len
</span>);
</code></pre></div></div>
#### Parameters
---
* `vector`

The vector to alter
* `index`

The row position in the vector to assign the string to
* `str`

The string
* `str_len`

The length of the string (in bytes)

<br>

### duckdb_list_vector_get_child
---
Retrieves the child vector of a list vector.

The resulting vector is valid as long as the parent vector is valid.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_vector</span> <span class="k">duckdb_list_vector_get_child</span>(<span class="k">
</span>  <span class="kt">duckdb_vector</span> <span class="k">vector
</span>);
</code></pre></div></div>
#### Parameters
---
* `vector`

The vector
* `returns`

The child vector

<br>

### duckdb_list_vector_get_size
---
Returns the size of the child vector of the list

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="k">duckdb_list_vector_get_size</span>(<span class="k">
</span>  <span class="kt">duckdb_vector</span> <span class="k">vector
</span>);
</code></pre></div></div>
#### Parameters
---
* `vector`

The vector
* `returns`

The size of the child list

<br>

### duckdb_list_vector_set_size
---
Sets the total size of the underlying child-vector of a list vector.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_list_vector_set_size</span>(<span class="k">
</span>  <span class="kt">duckdb_vector</span> <span class="k">vector</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">size
</span>);
</code></pre></div></div>
#### Parameters
---
* `vector`

The list vector.
* `size`

The size of the child list.
* `returns`

The duckdb state. Returns DuckDBError if the vector is nullptr.

<br>

### duckdb_list_vector_reserve
---
Sets the total capacity of the underlying child-vector of a list.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="k">duckdb_list_vector_reserve</span>(<span class="k">
</span>  <span class="kt">duckdb_vector</span> <span class="k">vector</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">required_capacity
</span>);
</code></pre></div></div>
#### Parameters
---
* `vector`

The list vector.
* `required_capacity`

the total capacity to reserve.
* `return`

The duckdb state. Returns DuckDBError if the vector is nullptr.

<br>

### duckdb_struct_vector_get_child
---
Retrieves the child vector of a struct vector.

The resulting vector is valid as long as the parent vector is valid.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_vector</span> <span class="k">duckdb_struct_vector_get_child</span>(<span class="k">
</span>  <span class="kt">duckdb_vector</span> <span class="k">vector</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">index
</span>);
</code></pre></div></div>
#### Parameters
---
* `vector`

The vector
* `index`

The child index
* `returns`

The child vector

<br>

### duckdb_validity_row_is_valid
---
Returns whether or not a row is valid (i.e. not NULL) in the given validity mask.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">bool</span> <span class="k">duckdb_validity_row_is_valid</span>(<span class="k">
</span>  <span class="kt">uint64_t</span> *<span class="k">validity</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### Parameters
---
* `validity`

The validity mask, as obtained through `duckdb_data_chunk_get_validity`
* `row`

The row index
* `returns`

true if the row is valid, false otherwise

<br>

### duckdb_validity_set_row_validity
---
In a validity mask, sets a specific row to either valid or invalid.

Note that `duckdb_data_chunk_ensure_validity_writable` should be called before calling `duckdb_data_chunk_get_validity`,
to ensure that there is a validity mask to write to.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="k">duckdb_validity_set_row_validity</span>(<span class="k">
</span>  <span class="kt">uint64_t</span> *<span class="k">validity</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row</span>,<span class="k">
</span>  <span class="kt">bool</span> <span class="k">valid
</span>);
</code></pre></div></div>
#### Parameters
---
* `validity`

The validity mask, as obtained through `duckdb_data_chunk_get_validity`.
* `row`

The row index
* `valid`

Whether or not to set the row to valid, or invalid

<br>

### duckdb_validity_set_row_invalid
---
In a validity mask, sets a specific row to invalid.

Equivalent to `duckdb_validity_set_row_validity` with valid set to false.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="k">duckdb_validity_set_row_invalid</span>(<span class="k">
</span>  <span class="kt">uint64_t</span> *<span class="k">validity</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### Parameters
---
* `validity`

The validity mask
* `row`

The row index

<br>

### duckdb_validity_set_row_valid
---
In a validity mask, sets a specific row to valid.

Equivalent to `duckdb_validity_set_row_validity` with valid set to true.

#### Syntax
---
<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="k">duckdb_validity_set_row_valid</span>(<span class="k">
</span>  <span class="kt">uint64_t</span> *<span class="k">validity</span>,<span class="k">
</span>  <span class="kt">idx_t</span> <span class="k">row
</span>);
</code></pre></div></div>
#### Parameters
---
* `validity`

The validity mask
* `row`

The row index

<br>

