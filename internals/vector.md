---
layout: docu
title: Execution Format
---

`Vector` is the container format used to store in-memory data during execution.  
`DataChunk` is a collection of Vectors, used for instance to represent a column list in a PhysicalProjection operator.

### Data Flow

DuckDB uses a vectorized query execution model. This means that our operators are optimized to work on Vectors of a fixed size.
This fixed size is commonly referred to in the code as `STANDARD_VECTOR_SIZE`.  
The default STANDARD_VECTOR_SIZE is 2048 tuples.

### Internals

`ValidityMask validity`  
Tracks which elements in the Vector are NULL.  

`data_ptr_t data`  
The element data of the Vector.  

`VectorBuffer buffer`  
An interface implemented based on the type of the vector and the data type it's representing.  
Usually owns the `data` memory.  

`VectorBuffer auxiliary`  
Optionally stores additional data needed by the Vector, explained later.  


### Vector Format

To efficiently represent different shapes of collections, we use different Vector formats.

#### FLAT_VECTOR

Flat vector is a sequential array, this is the default format.

#### CONSTANT_VECTOR

Constant vector is used to represent a single element as an entire vector.  
For example:  
```sql
select lst, 'duckdb' from range(1000) tbl(lst);
```
Since `duckdb` is Constant Expression, we know it's a single entry, but operators expect a DataChunk to have the same amount of tuples.  
If we only had FlatVector we would have to duplicate 'duckdb' a thousand times.  
Instead we can use a ConstantVector to only store 'duckdb' once.

#### DICTIONARY_VECTOR

Dictionary vector is used when a transformation would not change any elements of the data, but only change the order of the elements.  
For example:  
```sql
select * from range(1000) order by 1 desc;
```
Instead of duplicating the result of the `range` result and sorting that, we can use the same data, but just represent it in a different shape.  
How the dictionary vector works internally is that it adds a layer of indirection between the requested index and the retrieved index.  
In the example above a request for the data at index 0 would instead retrieve the data at index 999.

#### SEQUENCE_VECTOR

Sequence vectors are used when the data is a sequence with a fixed increment.  
Instead of storing all the elements, we just store the beginning and the increment.

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
These offsets refer to the "child" Vector and register for each row how many elements are in the list.

If the LIST has more than one dimension, then for every dimension that isn't the last one (deepest), the "child" Vector will be another LIST Vector.

#### STRUCT
Struct is designed to function as a nested table, with as little overhead as possible.  
For structs, the `auxiliary` is used to store a list of "child" Vectors.  
The `data` and `buffer` variables are unused by a struct Vector.

#### MAP
Internally `MAP` is just a `LIST[STRUCT(key KEY_TYPE, value VALUE_TYPE)]`.

#### UNION
Internally `UNION` utilizes the same structure as a `STRUCT`.

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
