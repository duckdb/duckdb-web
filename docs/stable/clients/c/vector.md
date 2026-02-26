---
layout: docu
redirect_from:
- /docs/api/c/vector
- /docs/clients/c/vector
title: Vectors
---

Vectors represent a horizontal slice of a column. They hold a number of values of a specific type, similar to an array. Vectors are the core data representation used in DuckDB. Vectors are typically stored within [data chunks]({% link docs/stable/clients/c/data_chunk.md %}).

The vector and data chunk interfaces are the most efficient way of interacting with DuckDB, allowing for the highest performance. However, the interfaces are also difficult to use and care must be taken when using them.

## Vector Format

Vectors are arrays of a specific data type. The logical type of a vector can be obtained using `duckdb_vector_get_column_type`. The type id of the logical type can then be obtained using `duckdb_get_type_id`.

Vectors themselves do not have sizes. Instead, the parent data chunk has a size (that can be obtained through `duckdb_data_chunk_get_size`). All vectors that belong to a data chunk have the same size.

### Primitive Types

For primitive types, the underlying array can be obtained using the `duckdb_vector_get_data` method. The array can then be accessed using the correct native type. Below is a table that contains a mapping of the `duckdb_type` to the native type of the array.

<div class="monospace_table"></div>

|       duckdb_type        |    NativeType    |
|--------------------------|------------------|
| DUCKDB_TYPE_BOOLEAN      | bool             |
| DUCKDB_TYPE_TINYINT      | int8_t           |
| DUCKDB_TYPE_SMALLINT     | int16_t          |
| DUCKDB_TYPE_INTEGER      | int32_t          |
| DUCKDB_TYPE_BIGINT       | int64_t          |
| DUCKDB_TYPE_UTINYINT     | uint8_t          |
| DUCKDB_TYPE_USMALLINT    | uint16_t         |
| DUCKDB_TYPE_UINTEGER     | uint32_t         |
| DUCKDB_TYPE_UBIGINT      | uint64_t         |
| DUCKDB_TYPE_FLOAT        | float            |
| DUCKDB_TYPE_DOUBLE       | double           |
| DUCKDB_TYPE_TIMESTAMP    | duckdb_timestamp |
| DUCKDB_TYPE_DATE         | duckdb_date      |
| DUCKDB_TYPE_TIME         | duckdb_time      |
| DUCKDB_TYPE_INTERVAL     | duckdb_interval  |
| DUCKDB_TYPE_HUGEINT      | duckdb_hugeint   |
| DUCKDB_TYPE_UHUGEINT     | duckdb_uhugeint  |
| DUCKDB_TYPE_VARCHAR      | duckdb_string_t  |
| DUCKDB_TYPE_BLOB         | duckdb_string_t  |
| DUCKDB_TYPE_TIMESTAMP_S  | duckdb_timestamp |
| DUCKDB_TYPE_TIMESTAMP_MS | duckdb_timestamp |
| DUCKDB_TYPE_TIMESTAMP_NS | duckdb_timestamp |
| DUCKDB_TYPE_UUID         | duckdb_hugeint   |
| DUCKDB_TYPE_TIME_TZ      | duckdb_time_tz   |
| DUCKDB_TYPE_TIMESTAMP_TZ | duckdb_timestamp |

### `NULL` Values

Any value in a vector can be `NULL`. When a value is `NULL`, the values contained within the primary array at that index is undefined (and can be uninitialized). The validity mask is a bitmask consisting of `uint64_t` elements. For every `64` values in the vector, one `uint64_t` element exists (rounded up). The validity mask has its bit set to 1 if the value is valid, or set to 0 if the value is invalid (i.e., `NULL`).

The bits of the bitmask can be read directly, or the slower helper method `duckdb_validity_row_is_valid` can be used to check whether or not a value is `NULL`.

The `duckdb_vector_get_validity` returns a pointer to the validity mask. Note that if all values in a vector are valid, this function **might** return `nullptr` in which case the validity mask does not need to be checked.

### Strings

String values are stored as a `duckdb_string_t`. This is a special struct that stores the string inline (if it is short, i.e., `<= 12 bytes`) or a pointer to the string data if it is longer than `12` bytes.

```c
typedef struct {
	union {
		struct {
			uint32_t length;
			char prefix[4];
			char *ptr;
		} pointer;
		struct {
			uint32_t length;
			char inlined[12];
		} inlined;
	} value;
} duckdb_string_t;
```

The length can either be accessed directly, or the `duckdb_string_is_inlined` can be used to check if a string is inlined.

### Decimals

Decimals are stored as integer values internally. The exact native type depends on the `width` of the decimal type, as shown in the following table:

<div class="monospace_table"></div>

| Width |   NativeType   |
|-------|----------------|
| <= 4  | int16_t        |
| <= 9  | int32_t        |
| <= 18 | int64_t        |
| <= 38 | duckdb_hugeint |

The `duckdb_decimal_internal_type` can be used to obtain the internal type of the decimal.

Decimals are stored as integer values multiplied by `10^scale`. The scale of a decimal can be obtained using `duckdb_decimal_scale`. For example, a decimal value of `10.5` with type `DECIMAL(8, 3)` is stored internally as an `int32_t` value of `10500`. In order to obtain the correct decimal value, the value should be divided by the appropriate power-of-ten.

### Enums

Enums are stored as unsigned integer values internally. The exact native type depends on the size of the enum dictionary, as shown in the following table:

<div class="monospace_table"></div>

| Dictionary size | NativeType |
|-----------------|------------|
| <= 255          | uint8_t    |
| <= 65535        | uint16_t   |
| <= 4294967295   | uint32_t   |

The `duckdb_enum_internal_type` can be used to obtain the internal type of the enum.

In order to obtain the actual string value of the enum, the `duckdb_enum_dictionary_value` function must be used to obtain the enum value that corresponds to the given dictionary entry. Note that the enum dictionary is the same for the entire column – and so only needs to be constructed once.

### Structs

Structs are nested types that contain any number of child types. Think of them like a `struct` in C. The way to access struct data using vectors is to access the child vectors recursively using the `duckdb_struct_vector_get_child` method.

The struct vector itself does not have any data (i.e., you should not use `duckdb_vector_get_data` method on the struct). **However**, the struct vector itself **does** have a validity mask. The reason for this is that the child elements of a struct can be `NULL`, but the struct **itself** can also be `NULL`.

### Lists

Lists are nested types that contain a single child type, repeated `x` times per row. Think of them like a variable-length array in C. The way to access list data using vectors is to access the child vector using the `duckdb_list_vector_get_child` method.

The `duckdb_vector_get_data` must be used to get the offsets and lengths of the lists stored as `duckdb_list_entry`, that can then be applied to the child vector.

```c
typedef struct {
	uint64_t offset;
	uint64_t length;
} duckdb_list_entry;
```

Note that both list entries itself **and** any children stored in the lists can also be `NULL`. This must be checked using the validity mask again.

### Arrays

Arrays are nested types that contain a single child type, repeated exactly `array_size` times per row. Think of them like a fixed-size array in C. Arrays work exactly the same as lists, **except** the length and offset of each entry is fixed. The fixed array size can be obtained by using `duckdb_array_type_array_size`. The data for entry `n` then resides at `offset = n * array_size` and always has `length = array_size`.

Note that much like lists, arrays can still be `NULL`, which must be checked using the validity mask.

## Examples

Below are several full end-to-end examples of how to interact with vectors.

### Example: Reading an int64 Vector with `NULL` Values

```c
duckdb_database db;
duckdb_connection con;
duckdb_open(nullptr, &db);
duckdb_connect(db, &con);

duckdb_result res;
duckdb_query(con, "SELECT CASE WHEN i%2=0 THEN NULL ELSE i END res_col FROM range(10) t(i)", &res);

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
	duckdb_vector res_col = duckdb_data_chunk_get_vector(result, 0);
	// get the native array and the validity mask of the vector
	int64_t *vector_data = (int64_t *) duckdb_vector_get_data(res_col);
	uint64_t *vector_validity = duckdb_vector_get_validity(res_col);
	// iterate over the rows
	for (idx_t row = 0; row < row_count; row++) {
		if (duckdb_validity_row_is_valid(vector_validity, row)) {
			printf("%lld\n", vector_data[row]);
		} else {
			printf("NULL\n");
		}
	}
	duckdb_destroy_data_chunk(&result);
}
// clean-up
duckdb_destroy_result(&res);
duckdb_disconnect(&con);
duckdb_close(&db);
```

### Example: Reading a String Vector

```c
duckdb_database db;
duckdb_connection con;
duckdb_open(nullptr, &db);
duckdb_connect(db, &con);

duckdb_result res;
duckdb_query(con, "SELECT CASE WHEN i%2=0 THEN CONCAT('short_', i) ELSE CONCAT('longstringprefix', i) END FROM range(10) t(i)", &res);

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
	duckdb_vector res_col = duckdb_data_chunk_get_vector(result, 0);
	// get the native array and the validity mask of the vector
	duckdb_string_t *vector_data = (duckdb_string_t *) duckdb_vector_get_data(res_col);
	uint64_t *vector_validity = duckdb_vector_get_validity(res_col);
	// iterate over the rows
	for (idx_t row = 0; row < row_count; row++) {
		if (duckdb_validity_row_is_valid(vector_validity, row)) {
			duckdb_string_t str = vector_data[row];
			if (duckdb_string_is_inlined(str)) {
				// use inlined string
				printf("%.*s\n", str.value.inlined.length, str.value.inlined.inlined);
			} else {
				// follow string pointer
				printf("%.*s\n", str.value.pointer.length, str.value.pointer.ptr);
			}
		} else {
			printf("NULL\n");
		}
	}
	duckdb_destroy_data_chunk(&result);
}
// clean-up
duckdb_destroy_result(&res);
duckdb_disconnect(&con);
duckdb_close(&db);
```

### Example: Reading a Struct Vector

```c
duckdb_database db;
duckdb_connection con;
duckdb_open(nullptr, &db);
duckdb_connect(db, &con);

duckdb_result res;
duckdb_query(con, "SELECT CASE WHEN i%5=0 THEN NULL ELSE {'col1': i, 'col2': CASE WHEN i%2=0 THEN NULL ELSE 100 + i * 42 END} END FROM range(10) t(i)", &res);

// iterate until result is exhausted
while (true) {
	duckdb_data_chunk result = duckdb_fetch_chunk(res);
	if (!result) {
		// result is exhausted
		break;
	}
	// get the number of rows from the data chunk
	idx_t row_count = duckdb_data_chunk_get_size(result);
	// get the struct column
	duckdb_vector struct_col = duckdb_data_chunk_get_vector(result, 0);
	uint64_t *struct_validity = duckdb_vector_get_validity(struct_col);
	// get the child columns of the struct
	duckdb_vector col1_vector = duckdb_struct_vector_get_child(struct_col, 0);
	int64_t *col1_data = (int64_t *) duckdb_vector_get_data(col1_vector);
	uint64_t *col1_validity = duckdb_vector_get_validity(col1_vector);

	duckdb_vector col2_vector = duckdb_struct_vector_get_child(struct_col, 1);
	int64_t *col2_data = (int64_t *) duckdb_vector_get_data(col2_vector);
	uint64_t *col2_validity = duckdb_vector_get_validity(col2_vector);

	// iterate over the rows
	for (idx_t row = 0; row < row_count; row++) {
		if (!duckdb_validity_row_is_valid(struct_validity, row)) {
			// entire struct is NULL
			printf("NULL\n");
			continue;
		}
		// read col1
		printf("{'col1': ");
		if (!duckdb_validity_row_is_valid(col1_validity, row)) {
			// col1 is NULL
			printf("NULL");
		} else {
			printf("%lld", col1_data[row]);
		}
		printf(", 'col2': ");
		if (!duckdb_validity_row_is_valid(col2_validity, row)) {
			// col2 is NULL
			printf("NULL");
		} else {
			printf("%lld", col2_data[row]);
		}
		printf("}\n");
	}
	duckdb_destroy_data_chunk(&result);
}
// clean-up
duckdb_destroy_result(&res);
duckdb_disconnect(&con);
duckdb_close(&db);
```

### Example: Reading a List Vector

```c
duckdb_database db;
duckdb_connection con;
duckdb_open(nullptr, &db);
duckdb_connect(db, &con);

duckdb_result res;
duckdb_query(con, "SELECT CASE WHEN i % 5 = 0 THEN NULL WHEN i % 2 = 0 THEN [i, i + 1] ELSE [i * 42, NULL, i * 84] END FROM range(10) t(i)", &res);

// iterate until result is exhausted
while (true) {
	duckdb_data_chunk result = duckdb_fetch_chunk(res);
	if (!result) {
		// result is exhausted
		break;
	}
	// get the number of rows from the data chunk
	idx_t row_count = duckdb_data_chunk_get_size(result);
	// get the list column
	duckdb_vector list_col = duckdb_data_chunk_get_vector(result, 0);
	duckdb_list_entry *list_data = (duckdb_list_entry *) duckdb_vector_get_data(list_col);
	uint64_t *list_validity = duckdb_vector_get_validity(list_col);
	// get the child column of the list
	duckdb_vector list_child = duckdb_list_vector_get_child(list_col);
	int64_t *child_data = (int64_t *) duckdb_vector_get_data(list_child);
	uint64_t *child_validity = duckdb_vector_get_validity(list_child);

	// iterate over the rows
	for (idx_t row = 0; row < row_count; row++) {
		if (!duckdb_validity_row_is_valid(list_validity, row)) {
			// entire list is NULL
			printf("NULL\n");
			continue;
		}
		// read the list offsets for this row
		duckdb_list_entry list = list_data[row];
		printf("[");
		for (idx_t child_idx = list.offset; child_idx < list.offset + list.length; child_idx++) {
			if (child_idx > list.offset) {
				printf(", ");
			}
			if (!duckdb_validity_row_is_valid(child_validity, child_idx)) {
				// col1 is NULL
				printf("NULL");
			} else {
				printf("%lld", child_data[child_idx]);
			}
		}
		printf("]\n");
	}
	duckdb_destroy_data_chunk(&result);
}
// clean-up
duckdb_destroy_result(&res);
duckdb_disconnect(&con);
duckdb_close(&db);
```

## API Reference Overview

<!-- This section is generated by scripts/generate_c_api_docs.py -->

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_vector</span> <a href="#duckdb_create_vector"><span class="nf">duckdb_create_vector</span></a>(<span class="kt">duckdb_logical_type</span> <span class="nv">type</span>, <span class="kt">idx_t</span> <span class="nv">capacity</span>);
<span class="kt">void</span> <a href="#duckdb_destroy_vector"><span class="nf">duckdb_destroy_vector</span></a>(<span class="kt">duckdb_vector</span> *<span class="nv">vector</span>);
<span class="kt">duckdb_logical_type</span> <a href="#duckdb_vector_get_column_type"><span class="nf">duckdb_vector_get_column_type</span></a>(<span class="kt">duckdb_vector</span> <span class="nv">vector</span>);
<span class="kt">void</span> *<a href="#duckdb_vector_get_data"><span class="nf">duckdb_vector_get_data</span></a>(<span class="kt">duckdb_vector</span> <span class="nv">vector</span>);
<span class="kt">uint64_t</span> *<a href="#duckdb_vector_get_validity"><span class="nf">duckdb_vector_get_validity</span></a>(<span class="kt">duckdb_vector</span> <span class="nv">vector</span>);
<span class="kt">void</span> <a href="#duckdb_vector_ensure_validity_writable"><span class="nf">duckdb_vector_ensure_validity_writable</span></a>(<span class="kt">duckdb_vector</span> <span class="nv">vector</span>);
<span class="kt">void</span> <a href="#duckdb_vector_assign_string_element"><span class="nf">duckdb_vector_assign_string_element</span></a>(<span class="kt">duckdb_vector</span> <span class="nv">vector</span>, <span class="kt">idx_t</span> <span class="nv">index</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">str</span>);
<span class="kt">void</span> <a href="#duckdb_vector_assign_string_element_len"><span class="nf">duckdb_vector_assign_string_element_len</span></a>(<span class="kt">duckdb_vector</span> <span class="nv">vector</span>, <span class="kt">idx_t</span> <span class="nv">index</span>, <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">str</span>, <span class="kt">idx_t</span> <span class="nv">str_len</span>);
<span class="kt">duckdb_vector</span> <a href="#duckdb_list_vector_get_child"><span class="nf">duckdb_list_vector_get_child</span></a>(<span class="kt">duckdb_vector</span> <span class="nv">vector</span>);
<span class="kt">idx_t</span> <a href="#duckdb_list_vector_get_size"><span class="nf">duckdb_list_vector_get_size</span></a>(<span class="kt">duckdb_vector</span> <span class="nv">vector</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_list_vector_set_size"><span class="nf">duckdb_list_vector_set_size</span></a>(<span class="kt">duckdb_vector</span> <span class="nv">vector</span>, <span class="kt">idx_t</span> <span class="nv">size</span>);
<span class="kt">duckdb_state</span> <a href="#duckdb_list_vector_reserve"><span class="nf">duckdb_list_vector_reserve</span></a>(<span class="kt">duckdb_vector</span> <span class="nv">vector</span>, <span class="kt">idx_t</span> <span class="nv">required_capacity</span>);
<span class="kt">duckdb_vector</span> <a href="#duckdb_struct_vector_get_child"><span class="nf">duckdb_struct_vector_get_child</span></a>(<span class="kt">duckdb_vector</span> <span class="nv">vector</span>, <span class="kt">idx_t</span> <span class="nv">index</span>);
<span class="kt">duckdb_vector</span> <a href="#duckdb_array_vector_get_child"><span class="nf">duckdb_array_vector_get_child</span></a>(<span class="kt">duckdb_vector</span> <span class="nv">vector</span>);
<span class="kt">void</span> <a href="#duckdb_slice_vector"><span class="nf">duckdb_slice_vector</span></a>(<span class="kt">duckdb_vector</span> <span class="nv">vector</span>, <span class="nv">duckdb_selection_vector</span> <span class="nv">sel</span>, <span class="kt">idx_t</span> <span class="nv">len</span>);
<span class="kt">void</span> <a href="#duckdb_vector_copy_sel"><span class="nf">duckdb_vector_copy_sel</span></a>(<span class="kt">duckdb_vector</span> <span class="nv">src</span>, <span class="kt">duckdb_vector</span> <span class="nv">dst</span>, <span class="nv">duckdb_selection_vector</span> <span class="nv">sel</span>, <span class="kt">idx_t</span> <span class="nv">src_count</span>, <span class="kt">idx_t</span> <span class="nv">src_offset</span>, <span class="kt">idx_t</span> <span class="nv">dst_offset</span>);
<span class="kt">void</span> <a href="#duckdb_vector_reference_value"><span class="nf">duckdb_vector_reference_value</span></a>(<span class="kt">duckdb_vector</span> <span class="nv">vector</span>, <span class="kt">duckdb_value</span> <span class="nv">value</span>);
<span class="kt">void</span> <a href="#duckdb_vector_reference_vector"><span class="nf">duckdb_vector_reference_vector</span></a>(<span class="kt">duckdb_vector</span> <span class="nv">to_vector</span>, <span class="kt">duckdb_vector</span> <span class="nv">from_vector</span>);
</code></pre></div></div>

### Validity Mask Functions

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">bool</span> <a href="#duckdb_validity_row_is_valid"><span class="nf">duckdb_validity_row_is_valid</span></a>(<span class="kt">uint64_t</span> *<span class="nv">validity</span>, <span class="kt">idx_t</span> <span class="nv">row</span>);
<span class="kt">void</span> <a href="#duckdb_validity_set_row_validity"><span class="nf">duckdb_validity_set_row_validity</span></a>(<span class="kt">uint64_t</span> *<span class="nv">validity</span>, <span class="kt">idx_t</span> <span class="nv">row</span>, <span class="kt">bool</span> <span class="nv">valid</span>);
<span class="kt">void</span> <a href="#duckdb_validity_set_row_invalid"><span class="nf">duckdb_validity_set_row_invalid</span></a>(<span class="kt">uint64_t</span> *<span class="nv">validity</span>, <span class="kt">idx_t</span> <span class="nv">row</span>);
<span class="kt">void</span> <a href="#duckdb_validity_set_row_valid"><span class="nf">duckdb_validity_set_row_valid</span></a>(<span class="kt">uint64_t</span> *<span class="nv">validity</span>, <span class="kt">idx_t</span> <span class="nv">row</span>);
</code></pre></div></div>

#### `duckdb_create_vector`

Creates a flat vector. Must be destroyed with `duckdb_destroy_vector`.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_vector</span> <span class="nv">duckdb_create_vector</span>(<span class="nv">
</span>  <span class="kt">duckdb_logical_type</span> <span class="nv">type</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">capacity
</span>);
</code></pre></div></div>

##### Parameters

* `type`: The logical type of the vector.
* `capacity`: The capacity of the vector.

##### Return Value

The vector.

<br>

#### `duckdb_destroy_vector`

Destroys the vector and de-allocates its memory.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nv">duckdb_destroy_vector</span>(<span class="nv">
</span>  <span class="kt">duckdb_vector</span> *<span class="nv">vector
</span>);
</code></pre></div></div>

##### Parameters

* `vector`: A pointer to the vector.

<br>

#### `duckdb_vector_get_column_type`

Retrieves the column type of the specified vector.

The result must be destroyed with `duckdb_destroy_logical_type`.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_logical_type</span> <span class="nv">duckdb_vector_get_column_type</span>(<span class="nv">
</span>  <span class="kt">duckdb_vector</span> <span class="nv">vector
</span>);
</code></pre></div></div>

##### Parameters

* `vector`: The vector get the data from

##### Return Value

The type of the vector

<br>

#### `duckdb_vector_get_data`

Retrieves the data pointer of the vector.

The data pointer can be used to read or write values from the vector.
How to read or write values depends on the type of the vector.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> *<span class="nv">duckdb_vector_get_data</span>(<span class="nv">
</span>  <span class="kt">duckdb_vector</span> <span class="nv">vector
</span>);
</code></pre></div></div>

##### Parameters

* `vector`: The vector to get the data from

##### Return Value

The data pointer

<br>

#### `duckdb_vector_get_validity`

Retrieves the validity mask pointer of the specified vector.

If all values are valid, this function MIGHT return NULL!

The validity mask is a bitset that signifies null-ness within the data chunk.
It is a series of uint64_t values, where each uint64_t value contains validity for 64 tuples.
The bit is set to 1 if the value is valid (i.e., not NULL) or 0 if the value is invalid (i.e., NULL).

Validity of a specific value can be obtained like this:

idx_t entry_idx = row_idx / 64;
idx_t idx_in_entry = row_idx % 64;
bool is_valid = validity_mask[entry_idx] & (1 << idx_in_entry);

Alternatively, the (slower) duckdb_validity_row_is_valid function can be used.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">uint64_t</span> *<span class="nv">duckdb_vector_get_validity</span>(<span class="nv">
</span>  <span class="kt">duckdb_vector</span> <span class="nv">vector
</span>);
</code></pre></div></div>

##### Parameters

* `vector`: The vector to get the data from

##### Return Value

The pointer to the validity mask, or NULL if no validity mask is present

<br>

#### `duckdb_vector_ensure_validity_writable`

Ensures the validity mask is writable by allocating it.

After this function is called, `duckdb_vector_get_validity` will ALWAYS return non-NULL.
This allows NULL values to be written to the vector, regardless of whether a validity mask was present before.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nv">duckdb_vector_ensure_validity_writable</span>(<span class="nv">
</span>  <span class="kt">duckdb_vector</span> <span class="nv">vector
</span>);
</code></pre></div></div>

##### Parameters

* `vector`: The vector to alter

<br>

#### `duckdb_vector_assign_string_element`

Assigns a string element in the vector at the specified location.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nv">duckdb_vector_assign_string_element</span>(<span class="nv">
</span>  <span class="kt">duckdb_vector</span> <span class="nv">vector</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">index</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">str
</span>);
</code></pre></div></div>

##### Parameters

* `vector`: The vector to alter
* `index`: The row position in the vector to assign the string to
* `str`: The null-terminated string

<br>

#### `duckdb_vector_assign_string_element_len`

Assigns a string element in the vector at the specified location. You may also use this function to assign BLOBs.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nv">duckdb_vector_assign_string_element_len</span>(<span class="nv">
</span>  <span class="kt">duckdb_vector</span> <span class="nv">vector</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">index</span>,<span class="nv">
</span>  <span class="kt">const</span> <span class="kt">char</span> *<span class="nv">str</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">str_len
</span>);
</code></pre></div></div>

##### Parameters

* `vector`: The vector to alter
* `index`: The row position in the vector to assign the string to
* `str`: The string
* `str_len`: The length of the string (in bytes)

<br>

#### `duckdb_list_vector_get_child`

Retrieves the child vector of a list vector.

The resulting vector is valid as long as the parent vector is valid.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_vector</span> <span class="nv">duckdb_list_vector_get_child</span>(<span class="nv">
</span>  <span class="kt">duckdb_vector</span> <span class="nv">vector
</span>);
</code></pre></div></div>

##### Parameters

* `vector`: The vector

##### Return Value

The child vector

<br>

#### `duckdb_list_vector_get_size`

Returns the size of the child vector of the list.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">idx_t</span> <span class="nv">duckdb_list_vector_get_size</span>(<span class="nv">
</span>  <span class="kt">duckdb_vector</span> <span class="nv">vector
</span>);
</code></pre></div></div>

##### Parameters

* `vector`: The vector

##### Return Value

The size of the child list

<br>

#### `duckdb_list_vector_set_size`

Sets the total size of the underlying child-vector of a list vector.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_list_vector_set_size</span>(<span class="nv">
</span>  <span class="kt">duckdb_vector</span> <span class="nv">vector</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">size
</span>);
</code></pre></div></div>

##### Parameters

* `vector`: The list vector.
* `size`: The size of the child list.

##### Return Value

The duckdb state. Returns DuckDBError if the vector is nullptr.

<br>

#### `duckdb_list_vector_reserve`

Sets the total capacity of the underlying child-vector of a list.

After calling this method, you must call `duckdb_vector_get_validity` and `duckdb_vector_get_data` to obtain current
data and validity pointers

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_state</span> <span class="nv">duckdb_list_vector_reserve</span>(<span class="nv">
</span>  <span class="kt">duckdb_vector</span> <span class="nv">vector</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">required_capacity
</span>);
</code></pre></div></div>

##### Parameters

* `vector`: The list vector.
* `required_capacity`: the total capacity to reserve.

##### Return Value

The duckdb state. Returns DuckDBError if the vector is nullptr.

<br>

#### `duckdb_struct_vector_get_child`

Retrieves the child vector of a struct vector.
The resulting vector is valid as long as the parent vector is valid.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_vector</span> <span class="nv">duckdb_struct_vector_get_child</span>(<span class="nv">
</span>  <span class="kt">duckdb_vector</span> <span class="nv">vector</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">index
</span>);
</code></pre></div></div>

##### Parameters

* `vector`: The vector
* `index`: The child index

##### Return Value

The child vector

<br>

#### `duckdb_array_vector_get_child`

Retrieves the child vector of an array vector.
The resulting vector is valid as long as the parent vector is valid.
The resulting vector has the size of the parent vector multiplied by the array size.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">duckdb_vector</span> <span class="nv">duckdb_array_vector_get_child</span>(<span class="nv">
</span>  <span class="kt">duckdb_vector</span> <span class="nv">vector
</span>);
</code></pre></div></div>

##### Parameters

* `vector`: The vector

##### Return Value

The child vector

<br>

#### `duckdb_slice_vector`

Slice a vector with a selection vector.
The length of the selection vector must be less than or equal to the length of the vector.
Turns the vector into a dictionary vector.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nv">duckdb_slice_vector</span>(<span class="nv">
</span>  <span class="kt">duckdb_vector</span> <span class="nv">vector</span>,<span class="nv">
</span>  <span class="nv">duckdb_selection_vector</span> <span class="nv">sel</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">len
</span>);
</code></pre></div></div>

##### Parameters

* `vector`: The vector to slice.
* `sel`: The selection vector.
* `len`: The length of the selection vector.

<br>

#### `duckdb_vector_copy_sel`

Copy the src vector to the dst with a selection vector that identifies which indices to copy.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nv">duckdb_vector_copy_sel</span>(<span class="nv">
</span>  <span class="kt">duckdb_vector</span> <span class="nv">src</span>,<span class="nv">
</span>  <span class="kt">duckdb_vector</span> <span class="nv">dst</span>,<span class="nv">
</span>  <span class="nv">duckdb_selection_vector</span> <span class="nv">sel</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">src_count</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">src_offset</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">dst_offset
</span>);
</code></pre></div></div>

##### Parameters

* `src`: The vector to copy from.
* `dst`: The vector to copy to.
* `sel`: The selection vector. The length of the selection vector should not be more than the length of the src
vector
* `src_count`: The number of entries from selection vector to copy. Think of this as the effective length of the
selection vector starting from index 0
* `src_offset`: The offset in the selection vector to copy from (important: actual number of items copied =
src_count - src_offset).
* `dst_offset`: The offset in the dst vector to start copying to.

<br>

#### `duckdb_vector_reference_value`

Copies the value from `value` to `vector`.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nv">duckdb_vector_reference_value</span>(<span class="nv">
</span>  <span class="kt">duckdb_vector</span> <span class="nv">vector</span>,<span class="nv">
</span>  <span class="kt">duckdb_value</span> <span class="nv">value
</span>);
</code></pre></div></div>

##### Parameters

* `vector`: The receiving vector.
* `value`: The value to copy into the vector.

<br>

#### `duckdb_vector_reference_vector`

Changes `to_vector` to reference `from_vector. After, the vectors share ownership of the data.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nv">duckdb_vector_reference_vector</span>(<span class="nv">
</span>  <span class="kt">duckdb_vector</span> <span class="nv">to_vector</span>,<span class="nv">
</span>  <span class="kt">duckdb_vector</span> <span class="nv">from_vector
</span>);
</code></pre></div></div>

##### Parameters

* `to_vector`: The receiving vector.
* `from_vector`: The vector to reference.

<br>

#### `duckdb_validity_row_is_valid`

Returns whether or not a row is valid (i.e., not NULL) in the given validity mask.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">bool</span> <span class="nv">duckdb_validity_row_is_valid</span>(<span class="nv">
</span>  <span class="kt">uint64_t</span> *<span class="nv">validity</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">row
</span>);
</code></pre></div></div>

##### Parameters

* `validity`: The validity mask, as obtained through `duckdb_vector_get_validity`
* `row`: The row index

##### Return Value

true if the row is valid, false otherwise

<br>

#### `duckdb_validity_set_row_validity`

In a validity mask, sets a specific row to either valid or invalid.

Note that `duckdb_vector_ensure_validity_writable` should be called before calling `duckdb_vector_get_validity`,
to ensure that there is a validity mask to write to.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nv">duckdb_validity_set_row_validity</span>(<span class="nv">
</span>  <span class="kt">uint64_t</span> *<span class="nv">validity</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">row</span>,<span class="nv">
</span>  <span class="kt">bool</span> <span class="nv">valid
</span>);
</code></pre></div></div>

##### Parameters

* `validity`: The validity mask, as obtained through `duckdb_vector_get_validity`.
* `row`: The row index
* `valid`: Whether or not to set the row to valid, or invalid

<br>

#### `duckdb_validity_set_row_invalid`

In a validity mask, sets a specific row to invalid.

Equivalent to `duckdb_validity_set_row_validity` with valid set to false.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nv">duckdb_validity_set_row_invalid</span>(<span class="nv">
</span>  <span class="kt">uint64_t</span> *<span class="nv">validity</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">row
</span>);
</code></pre></div></div>

##### Parameters

* `validity`: The validity mask
* `row`: The row index

<br>

#### `duckdb_validity_set_row_valid`

In a validity mask, sets a specific row to valid.

Equivalent to `duckdb_validity_set_row_validity` with valid set to true.

##### Syntax

<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code><span class="kt">void</span> <span class="nv">duckdb_validity_set_row_valid</span>(<span class="nv">
</span>  <span class="kt">uint64_t</span> *<span class="nv">validity</span>,<span class="nv">
</span>  <span class="kt">idx_t</span> <span class="nv">row
</span>);
</code></pre></div></div>

##### Parameters

* `validity`: The validity mask
* `row`: The row index

<br>
