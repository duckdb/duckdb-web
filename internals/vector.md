---
layout: docu
title: Execution Format
---

`Vector` is the container format used to store in-memory data during execution.  
`DataChunk` is a collection of Vectors, used for instance to represent a column list in a PhysicalProjection operator.

### Data Flow

DuckDB uses a vectorized query execution model.  
This means that our operators are optimized to work on Vectors of a fixed size.  

This fixed size is commonly referred to in the code as `STANDARD_VECTOR_SIZE`.  
The default STANDARD_VECTOR_SIZE is 2048 tuples.

### Internals

`ValidityMask validity`  
Tracks which elements in the Vector are NULL.  

`data_ptr_t data`  
A non-owning pointer to the data of the Vector.  
Vectors do not need to own their data, but when they do this memory is owned by the `buffer`.

`VectorBuffer buffer`  
An interface implemented based on the type of the vector and the data type it's representing.  

`VectorBuffer auxiliary`  
Optionally stores additional data needed by the Vector, explained later.  

### Vector Format

Vectors logically represent arrays that hold a single type, but it wouldn't be efficient to also represent them as such physically.
That's what we use Vector Formats for, to change the physical representation without affecting the logical side.

#### FLAT_VECTOR

Flat vector is a sequential array, this is the default format.  
In a flat vector the logical and physical representation are identical.

<img src="/images/internals/flat.png" alt="Flat Vector example" style="max-width:40%;width:40%;height:auto;margin:auto"/>

#### CONSTANT_VECTOR

Constant vector can be used to prevent duplicating an entry across the entire Vector.
For example when representing the result of a constant expression in a function call, using a constant vector we only need to physically store the result once.
```sql
select lst, 'duckdb' from range(1000) tbl(lst);
```
Since `duckdb` is a string literal, we know it's a single entry, but operators expect a DataChunk to have the same amount of tuples.  
If we only had FlatVector we would have to duplicate 'duckdb' a thousand times.  
Instead we can use a ConstantVector to only store 'duckdb' once.

<img src="/images/internals/constant.png" alt="Constant Vector example" style="max-width:40%;width:40%;height:auto;margin:auto"/>

Constant vectors are also emitted by the storage when decompression from constant compression.  
This allows us to work directly on compressed data.

#### DICTIONARY_VECTOR

Dictionary vector holds a dictionary of values, and a selection vector that contains indices into this dictionary.  
This means it can be used for example in a transformation that would not change any elements of the data, but only change the order of the elements.  
For example:  
```sql
select * from range(1000) order by 1 desc;
```
Instead of duplicating the result of the `range` result and sorting that, we can use the same data but represent it in a different shape.  
In the example above a request for the data at index 0 would instead retrieve the data at index 999.

<img src="/images/internals/dictionary.png" alt="Dictionary Vector example" style="max-width:40%;width:40%;height:auto;margin:auto"/>

Just like constant vectors, dictionary vectors are also emitted by the storage.  
When deserializing a dictionary compressed column segment, we store this in a dictionary vector so we can keep the data compressed during query execution.

#### SEQUENCE_VECTOR

Sequence vectors are used when the data is a sequence with a fixed increment.  
Instead of storing all the elements, we only need to store the beginning and the increment.

<img src="/images/internals/sequence.png" alt="Sequence Vector example" style="max-width:40%;width:40%;height:auto;margin:auto"/>

#### Unified Vector Format

These properties of the different vector formats are great for optimization purposes, for example you can imagine the scenario where all the parameters to a function are constant, we can just compute the result once and emit a constant vector.  
But if we need to write specialized code for every combination of vector type, this would be a nightmare and be a huge source of bugs.  

Instead of doing this, whenever you want to generically use a vector regardless of the type, we use a UnifiedVectorFormat.  
This format essentially acts as a generic view over the contents of the Vector. Every type of Vector can convert to this format.

### Nested Types

For nested types, like LIST, STRUCT and MAP we use the internals of the Vector class in a special way.

#### LIST
Vectors that represent a LIST use the `auxiliary` to store a "child" Vector.  
This contains the data for the entire list Vector (all rows).  

The `data` variable is used to store `list_entry_t` objects for each row.
```c++
struct list_entry_t {
	idx_t offset;
	idx_t length;
};
```
The offset refers to the row in the "child" Vector, the length keeps track of the size of the list of this row.

If the LIST has more than one dimension, then for every dimension that isn't the last one (deepest), the "child" Vector will be another LIST Vector.  
For example a mock representation of a Vector of type `BIGINT[][]`:  
```json
{
   "type": "list",
   "data": "list_entry_t",
   "child": {
      "type": "list",
      "data": "list_entry_t",
      "child": {
         "type": "bigint",
         "data": "int64_t"
      }
   }
}
```

#### STRUCT
Struct is designed to function as a nested table, with as little overhead as possible.  
For structs, the `auxiliary` is used to store a list of "child" Vectors.  
The `data` and `buffer` variables are unused by a struct Vector.

#### MAP
Internally `MAP` is represented as a `LIST[STRUCT(key KEY_TYPE, value VALUE_TYPE)]`.

#### UNION
Internally `UNION` utilizes the same structure as a `STRUCT`.
The first "child" is always occupied by the Tag Vector of the UNION, which records for each row which of the UNION's types apply to that row.

### Strings

To efficiently store strings, we make use of our `string_t` class.
```c++
struct string_t {
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
};
```
The details of this class and the benefits are explained in greater detail [here](https://github.com/duckdb/duckdb/pull/431).  

When the Vector stores VARCHAR/BLOB types, the `auxiliary` is used to store a StringHeap.  
This owns the memory pointed to by the `string_t` `ptr` variable.
