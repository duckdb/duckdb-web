---
layout: docu
title: Conversion between DuckDB and Python
---

This page documents the rules for converting [Python objects to DuckDB](#object-conversion-python-object-to-duckdb) and [DuckDB results to Python](#result-conversion-duckdb-results-to-python).

## Object Conversion: Python Object to DuckDB

This is a mapping of Python object types to DuckDB [Logical Types]({% link docs/preview/sql/data_types/overview.md %}):

* `None` → `NULL`
* `bool` → `BOOLEAN`
* `datetime.timedelta` → `INTERVAL`
* `str` → `VARCHAR`
* `bytearray` → `BLOB`
* `memoryview` → `BLOB`
* `decimal.Decimal` → `DECIMAL` / `DOUBLE`
* `uuid.UUID` → `UUID`

The rest of the conversion rules are as follows.

### `int`

Since integers can be of arbitrary size in Python, there is not a one-to-one conversion possible for ints.
Instead we perform these casts in order until one succeeds:

* `BIGINT`
* `INTEGER`
* `UBIGINT`
* `UINTEGER`
* `DOUBLE`

When using the DuckDB Value class, it's possible to set a target type, which will influence the conversion.

### `float`

These casts are tried in order until one succeeds:

* `DOUBLE`
* `FLOAT`

### `datetime.datetime`

For `datetime` we will check `pandas.isnull` if it's available and return `NULL` if it returns `true`.
We check against `datetime.datetime.min` and `datetime.datetime.max` to convert to `-inf` and `+inf` respectively.

If the `datetime` has tzinfo, we will use `TIMESTAMPTZ`, otherwise it becomes `TIMESTAMP`.

### `datetime.time`

If the `time` has tzinfo, we will use `TIMETZ`, otherwise it becomes `TIME`.

### `datetime.date`

`date` converts to the `DATE` type.
We check against `datetime.date.min` and `datetime.date.max` to convert to `-inf` and `+inf` respectively.

### `bytes`

`bytes` converts to `BLOB` by default, when it's used to construct a Value object of type `BITSTRING`, it maps to `BITSTRING` instead.

### `list`

`list` becomes a `LIST` type of the “most permissive” type of its children, for example:

```python
my_list_value = [
    12345,
    "test"
]
```

Will become `VARCHAR[]` because 12345 can convert to `VARCHAR` but `test` can not convert to `INTEGER`.

```sql
[12345, test]
```

### `dict`

The `dict` object can convert to either `STRUCT(...)` or `MAP(..., ...)` depending on its structure.
If the dict has a structure similar to:

```python
import duckdb

my_map_dict = {
    "key": [
        1, 2, 3
    ],
    "value": [
        "one", "two", "three"
    ]
}

duckdb.values(my_map_dict)
```

Then we'll convert it to a `MAP` of key-value pairs of the two lists zipped together.
The example above becomes a `MAP(INTEGER, VARCHAR)`:

```text
┌─────────────────────────┐
│ {1=one, 2=two, 3=three} │
│  map(integer, varchar)  │
├─────────────────────────┤
│ {1=one, 2=two, 3=three} │
└─────────────────────────┘
```

If the dict is returned by a [function]({% link docs/preview/clients/python/function.md %}), 
the function will return a `MAP`, therefore the function `return_type` has to be specified. Providing
a return type which cannot convert to `MAP` will raise an error:
```python
import duckdb
duckdb_conn = duckdb.connect()

def get_map() -> dict[str,list[str]|list[int]]:
    return {
        "key": [
            1, 2, 3
        ],
        "value": [
            "one", "two", "three"
        ]
    }

duckdb_conn.create_function("get_map", get_map, return_type=dict[int, str])

duckdb_conn.sql("select get_map()").show()

duckdb_conn.create_function("get_map_error", get_map)

duckdb_conn.sql("select get_map_error()").show()
```
 ```text
┌─────────────────────────┐
│        get_map()        │
│  map(bigint, varchar)   │
├─────────────────────────┤
│ {1=one, 2=two, 3=three} │
└─────────────────────────┘

ConversionException: Conversion Error: Type VARCHAR can't be cast as UNION(u1 VARCHAR[], u2 BIGINT[]). VARCHAR can't be implicitly cast to any of the union member types: VARCHAR[], BIGINT[]
```

> The names of the fields matter and the two lists need to have the same size.

Otherwise we'll try to convert it to a `STRUCT`.

```python
import duckdb

my_struct_dict = {
    1: "one",
    "2": 2,
    "three": [1, 2, 3],
    False: True
}

duckdb.values(my_struct_dict)
```
Becomes:

```text
┌────────────────────────────────────────────────────────────────────┐
│      {'1': 'one', '2': 2, 'three': [1, 2, 3], 'False': true}       │
│ struct("1" varchar, "2" integer, three integer[], "false" boolean) │
├────────────────────────────────────────────────────────────────────┤
│ {'1': one, '2': 2, 'three': [1, 2, 3], 'False': true}              │
└────────────────────────────────────────────────────────────────────┘
```

If the dict is returned by a [function]({% link docs/preview/clients/python/function.md %}), 
the function will return a `MAP`, due to [automatic conversion]({% link docs/preview/clients/python/types.md %}#dictkey_type-value_type).
To return a `STRUCT`, the `return_type` has to be provided:
```python
import duckdb
from duckdb.sqltypes import BOOLEAN, INTEGER, VARCHAR
from duckdb import list_type, struct_type

duckdb_conn = duckdb.connect()

my_struct_dict = {
    1: "one",
    "2": 2,
    "three": [1, 2, 3],
    False: True
}

def get_struct() -> dict[str|int|bool,str|int|list[int]|bool]:
    return my_struct_dict

duckdb_conn.create_function("get_struct_as_map", get_struct)

duckdb_conn.sql("select get_struct_as_map()").show()

duckdb_conn.create_function("get_struct", get_struct, return_type=struct_type({
    1: VARCHAR,
    "2": INTEGER,
    "three": list_type(INTEGER),
    False: BOOLEAN
}))

duckdb_conn.sql("select get_struct()").show()
```

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                         get_struct_as_map()                                          │
│ map(union(u1 varchar, u2 bigint, u3 boolean), union(u1 varchar, u2 bigint, u3 bigint[], u4 boolean)) │
├──────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ {1=one, 2=2, three=[1, 2, 3], false=true}                                                            │
└──────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│                            get_struct()                            │
│ struct("1" varchar, "2" integer, three integer[], "false" boolean) │
├────────────────────────────────────────────────────────────────────┤
│ {'1': one, '2': 2, 'three': [1, 2, 3], 'False': true}              │
└────────────────────────────────────────────────────────────────────┘
```
> Every `key` of the dictionary is converted to string.

### `tuple`

`tuple` converts to `LIST` by default, when it's used to construct a Value object of type `STRUCT` it will convert to `STRUCT` instead.

### `numpy.ndarray` and `numpy.datetime64`

`ndarray` and `datetime64` are converted by calling `tolist()` and converting the result of that.

## Result Conversion: DuckDB Results to Python

DuckDB's Python client provides multiple additional methods that can be used to efficiently retrieve data.

### NumPy

* `fetchnumpy()` fetches the data as a dictionary of NumPy arrays

### Pandas

* `df()` fetches the data as a Pandas DataFrame
* `fetchdf()` is an alias of `df()`
* `fetch_df()` is an alias of `df()`
* `fetch_df_chunk(vector_multiple)` fetches a portion of the results into a DataFrame. The number of rows returned in each chunk is the vector size (2048 by default) * vector_multiple (1 by default).

### Apache Arrow

* `arrow_table()` fetches the data as an [Arrow table](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html)
* `arrow_reader(chunk_size)` returns an [Arrow record batch reader](https://arrow.apache.org/docs/python/generated/pyarrow.ipc.RecordBatchStreamReader.html) with `chunk_size` rows per batch

> Deprecated `arrow()`, `fetch_arrow_table()`, and `fetch_record_batch()` are deprecated. Use `arrow_table()` and `arrow_reader()` instead.

### Polars

* `pl()` fetches the data as a Polars DataFrame

### Examples

Below are some examples using this functionality. See the [Python guides]({% link docs/preview/guides/overview.md %}#python-client) for more examples.

Fetch as Pandas DataFrame:

```python
df = con.execute("SELECT * FROM items").fetchdf()
print(df)
```

```text
       item   value  count
0     jeans    20.0      1
1    hammer    42.2      2
2    laptop  2000.0      1
3  chainsaw   500.0     10
4    iphone   300.0      2
```

Fetch as dictionary of NumPy arrays:

```python
arr = con.execute("SELECT * FROM items").fetchnumpy()
print(arr)
```

```text
{'item': masked_array(data=['jeans', 'hammer', 'laptop', 'chainsaw', 'iphone'],
             mask=[False, False, False, False, False],
       fill_value='?',
            dtype=object), 'value': masked_array(data=[20.0, 42.2, 2000.0, 500.0, 300.0],
             mask=[False, False, False, False, False],
       fill_value=1e+20), 'count': masked_array(data=[1, 2, 1, 10, 2],
             mask=[False, False, False, False, False],
       fill_value=999999,
            dtype=int32)}
```

Fetch as an Arrow table. Converting to Pandas afterwards just for pretty printing:

```python
tbl = con.execute("SELECT * FROM items").arrow_table()
print(tbl.to_pandas())
```

```text
       item    value  count
0     jeans    20.00      1
1    hammer    42.20      2
2    laptop  2000.00      1
3  chainsaw   500.00     10
4    iphone   300.00      2
```
