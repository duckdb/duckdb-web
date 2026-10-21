---
layout: docu
title: Conversion between DuckDB and Python
---

This page documents the rules for converting [DuckDB results to Python](#result-conversion-duckdb-results-to-python) and [Python objects to DuckDB](#object-conversion-python-object-to-duckdb).

## Result Conversion: DuckDB Results to Python

A result is read from a [relation]({% link docs/preview/clients/python/relational_api.md %}) or, when using the [DB-API]({% link docs/preview/clients/python/dbapi.md %}) / `con.execute()`, from the connection. `con.sql()`, `con.table()`, the readers and the other relational methods return relations. Each has its own methods:

<div class="monospace_table"></div>

| Result               | Relation                                             | DB-API 2.0 (`con.execute()`)                                  |
|:---------------------|:-----------------------------------------------------|:--------------------------------------------------------------|
| Python tuples        | `fetchall()`, `iter_rows(batch_size=1024)`           | `fetchone()`, `fetchmany(size=1)`, `fetchall()`               |
| Python dicts         | `to_dicts()`                                         |                                                               |
| NumPy                | `fetchnumpy()`                                       | `fetchnumpy()`                                                |
| Pandas               | `df()`, `fetchdf()`                                  | `df()`, `fetchdf()`, `fetch_df()`, `fetch_df_chunk()`         |
| Apache Arrow         | `to_arrow_table()`, `to_arrow_reader()`, `arrow()`   | `to_arrow_table()`, `to_arrow_reader()`, both make a copy     |
| Polars               | `pl()`                                               |                                                               |
| PyTorch              | `torch()`                                            | `torch()`                                                     |
| TensorFlow           | `tf()`                                               | `tf()`                                                        |

Relations are recommended for most conversion, except when you want to do row-based work. A relation has no `fetchone()`, `fetchmany()` or `fetch_df_chunk()` because it is stateless, i.e. it does not hold a result itself. To get specific rows of a result with the relational API you would use `limit(n).fetchall()`, `iter_rows()` or `to_arrow_reader()` instead. Note that with the DB-API, after a partial read with `fetchone()` or `fetchmany()`, the `df()`, `fetchnumpy()` and Arrow methods of the connection return only the remaining rows.

### Examples

Below are some examples. See the [Python guides]({% link docs/preview/guides/overview.md %}#python-client) for more. To run the examples, use this table:

```python
import duckdb

con = duckdb.connect()
con.execute("CREATE TABLE items (item VARCHAR, value DECIMAL(10, 2), count INTEGER)")
con.execute("""
    INSERT INTO items VALUES
        ('jeans', 20.0, 1),
        ('hammer', 42.2, 2),
        ('laptop', 2000.0, 1),
        ('chainsaw', 500.0, 10),
        ('iphone', 300.0, 2)
""")
```

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
{'item': array(['jeans', 'hammer', 'laptop', 'chainsaw', 'iphone'], dtype=object), 'value': array([  20. ,   42.2, 2000. ,  500. ,  300. ]), 'count': array([ 1,  2,  1, 10,  2], dtype=int32)}
```

Fetch as an Arrow table. Converting to Pandas afterwards just for pretty printing:

```python
tbl = con.sql("SELECT * FROM items").to_arrow_table()
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

### NumPy

* `fetchnumpy()` fetches the data as a dictionary of NumPy arrays. A column without `NULL` values is a plain array. A column with `NULL` values is a masked array.

### Pandas

* `df()` fetches the data as a Pandas DataFrame
* `fetchdf()` is an alias of `df()`
* `fetch_df()` is an alias of `df()`, on the connection only
* `fetch_df_chunk(vectors_per_chunk)` fetches the next portion of the results of `con.execute()` into a DataFrame. Each chunk has at most the vector size (2048 by default) times `vectors_per_chunk` (1 by default) rows.

### Apache Arrow

* `to_arrow_table()` fetches the data as an [Arrow table](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html)
* `to_arrow_reader(batch_size)` returns an [Arrow record batch reader](https://arrow.apache.org/docs/python/generated/pyarrow.RecordBatchReader.html) with _at most_ `batch_size` rows per batch (the default is 131072)
* `arrow()` is an alias of `to_arrow_reader()`, on relations only
* A relation is also an Arrow stream through the [Arrow PyCapsule Interface](https://arrow.apache.org/docs/format/CDataInterface/PyCapsuleInterface.html). `pyarrow.table(rel)` returns an Arrow table and `polars.DataFrame(rel)` a Polars DataFrame, which unlike `pl()` needs no pyarrow

After `con.execute()`, `to_arrow_table()` and `to_arrow_reader()` first fetch the rows and then convert them, so they make an extra copy of the result, and the reader returns its first batch only after the whole query ran. They warn: `UserWarning: Arrow output on a DB-API result makes an extra copy of the rows, use con.sql(query).to_arrow_table() instead.` The module functions `duckdb.to_arrow_table()` and `duckdb.to_arrow_reader()` read the result of `duckdb.execute()` and warn the same way. For Arrow output, run the query with `con.sql(query)`.

> Deprecated on relations, `fetch_arrow_table()`, `fetch_record_batch()` and `fetch_arrow_reader()` are deprecated aliases of `to_arrow_table()` and `to_arrow_reader()`. After `con.execute()`, `fetch_arrow_table()`, `fetch_record_batch()`, `arrow()` and `pl()` no longer exist, and neither do the module functions `duckdb.fetch_arrow_table()`, `duckdb.fetch_record_batch()` and `duckdb.pl()`.

DuckDB has a single `INTERVAL` type that stores months, days and microseconds, so it maps onto Arrow's `month_day_nano_interval` type. On import, every Arrow interval and duration type, including `duration[s]`, `duration[ms]`, `duration[us]` and `duration[ns]`, is read into that one `INTERVAL` type. As a result, a `duration` column that is passed through DuckDB and read back as Arrow is returned as a `month_day_nano_interval` rather than as its original `duration` type. This is expected. The resolution and unit of the original Arrow type are not preserved.

### Polars

* `pl()` fetches the data of a relation as a Polars DataFrame, and `pl(lazy=True)` returns a Polars LazyFrame

## Object Conversion: Python Object to DuckDB

Python objects are converted when they are passed as query parameters (`execute()`, `executemany()` and `sql(..., params=...)`), as rows of `values()`, as constants in [expressions]({% link docs/preview/clients/python/expression.md %}) and as the value of a `duckdb.Value`. The rules are the same on all of these paths, except where a section below says otherwise.

This is a mapping of Python object types to DuckDB [Logical Types]({% link docs/preview/sql/data_types/overview.md %}):

* `None` → `NULL`
* `bool` → `BOOLEAN`
* `datetime.timedelta` → `INTERVAL`
* `str` → `VARCHAR`
* `bytearray` → `BLOB`
* `memoryview` → `BLOB`
* `decimal.Decimal` → `DECIMAL` / `DOUBLE` / `FLOAT`
* `uuid.UUID` → `UUID`

The rest of the conversion rules are as follows.

### `str`

A `str` that UTF-8 cannot encode, such as one that holds a lone surrogate (`"\ud800"`), raises an `InvalidInputException` that says it `cannot encode str as UTF-8`. The connection stays usable.

### `memoryview`

A `memoryview` converts to a `BLOB` of the bytes it shows. As a query parameter, it must be contiguous: a strided view such as `memoryview(b"abcdef")[::2]` raises `BufferError: memoryview: underlying buffer is not C-contiguous`. `values()` and expressions accept it and read its bytes in order, here `b'ace'`.

### `decimal.Decimal`

A `Decimal` becomes a `DECIMAL` whose width and scale follow from its digits and its exponent: `Decimal("12.5")` is a `DECIMAL(3,1)`, `Decimal("1E+2")` is a `DECIMAL(3,0)` that holds 100 and `Decimal("1E-7")` is a `DECIMAL(8,7)`. A value that needs more than 38 digits becomes a `DOUBLE`, such as `Decimal("1E+38")` or `Decimal(0.1)`, which holds the 55 decimal digits of the binary float 0.1. `NaN` and the infinities become `FLOAT`.

### `int`

Since integers can be of arbitrary size in Python, there is not a one-to-one conversion possible for ints. An `int` becomes the first of these types that fits it:

* `INTEGER`
* `BIGINT`
* `UBIGINT`
* `HUGEINT`
* `UHUGEINT`

So `2**31` is a `BIGINT`, `2**63` a `UBIGINT`, `2**64` and `-(2**63) - 1` are `HUGEINT` and `2**127` is a `UHUGEINT`. An integer that does not fit in 128 bits raises `InvalidInputException: Python integer too large for 128-bit integer type`. A subclass of `int` converts by the value it stores.

When using the DuckDB Value class, it's possible to set a target type, which will influence the conversion:

```python
import duckdb
from duckdb.sqltypes import TINYINT

con = duckdb.connect()
print(con.execute("SELECT typeof(?), typeof(?), typeof(?)", [5, 2**64, duckdb.Value(5, TINYINT)]).fetchall())
```

```text
[('INTEGER', 'HUGEINT', 'TINYINT')]
```

### `float`

A `float` is always a `DOUBLE`.

### `datetime.datetime`

For `datetime` we will check `pandas.isnull` if it's available and return `NULL` if it returns `true`.

If the `datetime` has tzinfo, we will use `TIMESTAMPTZ`, otherwise it becomes `TIMESTAMP`. Fetching a `TIMESTAMPTZ` value into Python needs the `pytz` package, which is not installed with DuckDB; without it, the fetch raises `InvalidInputException: Required module 'pytz' failed to import`.

`datetime.datetime.max` and `datetime.datetime.min` convert to ordinary timestamps, not to infinity. In the other direction, the timestamp `infinity` is returned as `datetime.datetime.max` and `-infinity` as `datetime.datetime.min`.

### `datetime.time`

If the `time` has tzinfo, we will use `TIMETZ`, otherwise it becomes `TIME`.

### `datetime.date`

`date` converts to the `DATE` type. `datetime.date.max` and `datetime.date.min` convert to ordinary dates; the date `infinity` is returned as `datetime.date.max` and `-infinity` as `datetime.date.min`.

### `bytes`

`bytes` converts to `BLOB` by default. When it's used to construct a Value object of type `BIT`, it maps to `BIT` instead, and its bytes are read as the characters `0` and `1`, as in `duckdb.Value(b"0101", duckdb.sqltypes.BIT)`.

### `list`

`list` becomes a `LIST` type of the “most permissive” type of its children. For example, `[12345, "test"]` becomes `VARCHAR[]`, because 12345 can convert to `VARCHAR` but `test` can not convert to `INTEGER`:

```python
print(con.execute("SELECT ?", [[12345, "test"]]).fetchall())
```

```text
[(['12345', 'test'],)]
```

A `NaN` stays `NaN` inside a list, a struct, a map or a `duckdb.Value` of a nested type. A list that mixes `datetime` values with and without tzinfo becomes a `TIMESTAMPTZ` list as a query parameter and in `values()`, which read the values without tzinfo as UTC.

### `dict`

The `dict` object can convert to either `STRUCT(...)` or `MAP(..., ...)`, depending on its keys and on where it is used:

* A dict whose keys are all strings becomes a `STRUCT` with one field per key.
* A dict with exactly the two keys `key` and `value`, each holding a list and both lists of the same length, becomes a `MAP` of the two lists zipped together when passed as a query parameter and in `values()`. In an expression, it is a `STRUCT` like any other dict with string keys.
* A dict with a key that is not a string becomes a `MAP` in `values()` and in expressions, written as a SQL [`MAP` literal]({% link docs/preview/sql/data_types/map.md %}). As a query parameter, it becomes a `STRUCT` whose field names are the keys converted to strings. Keys or values of types that SQL cannot combine raise an error.

A dict in the `key` and `value` form:

```python
my_map_dict = {
    "key": [
        1, 2, 3
    ],
    "value": [
        "one", "two", "three"
    ]
}

duckdb.values(my_map_dict).show()
```

becomes a `MAP(INTEGER, VARCHAR)`:

```text
┌─────────────────────────┐
│          col0           │
│  map(integer, varchar)  │
├─────────────────────────┤
│ {1=one, 2=two, 3=three} │
└─────────────────────────┘
```

A dict with string keys becomes a `STRUCT`:

```python
my_struct_dict = {
    "name": "duck",
    "count": 2,
    "tags": [1, 2, 3],
    "active": True
}

duckdb.values(my_struct_dict).show()
```

```text
┌───────────────────────────────────────────────────────────────────────┐
│                                 col0                                  │
│ struct("name" varchar, count integer, tags integer[], active boolean) │
├───────────────────────────────────────────────────────────────────────┤
│ {'name': duck, 'count': 2, 'tags': [1, 2, 3], 'active': true}         │
└───────────────────────────────────────────────────────────────────────┘
```

As a query parameter, a dict with other keys becomes a `STRUCT` with string field names:

```python
my_mixed_dict = {1: "one", "2": 2, "three": [1, 2, 3], False: True}
print(con.execute("SELECT typeof(?)", [my_mixed_dict]).fetchone()[0])
```

```text
STRUCT("1" VARCHAR, "2" INTEGER, three INTEGER[], "False" BOOLEAN)
```

A dict returned by a [function]({% link docs/preview/clients/python/function.md %}) converts to the function's return type. For a `MAP` return type, a dict in the `key` and `value` form gives the entries of the map, so the return type has to describe those entries:

```python
duckdb_conn = duckdb.connect()

def get_map() -> dict[str, list[str] | list[int]]:
    return {
        "key": [
            1, 2, 3
        ],
        "value": [
            "one", "two", "three"
        ]
    }

duckdb_conn.create_function("get_map", get_map, return_type=dict[int, str])

duckdb_conn.sql("SELECT get_map()").show()
```

```text
┌─────────────────────────┐
│        get_map()        │
│  map(bigint, varchar)   │
├─────────────────────────┤
│ {1=one, 2=two, 3=three} │
└─────────────────────────┘
```

Without `return_type`, the annotation `dict[str, list[str] | list[int]]` is the return type, so each value, such as `"one"`, has to convert to a `UNION(u1 VARCHAR[], u2 BIGINT[])`, and the query fails:

```python
duckdb_conn.create_function("get_map_error", get_map)

duckdb_conn.sql("SELECT get_map_error()").show()
```

```console
_duckdb.ConversionException: Conversion Error: Could not convert value of type VARCHAR to UNION(u1 VARCHAR[], u2 BIGINT[])
```

A function annotated to return a `dict` returns a `MAP`, due to [automatic conversion]({% link docs/preview/clients/python/types.md %}#dictkey_type-value_type). To return a `STRUCT`, the `return_type` has to be provided:

```python
from duckdb import list_type, struct_type
from duckdb.sqltypes import BOOLEAN, INTEGER, VARCHAR

def get_struct() -> dict[str, str | int | list[int] | bool]:
    return my_struct_dict

duckdb_conn.create_function("get_struct_as_map", get_struct)

duckdb_conn.sql("SELECT get_struct_as_map()").show()

duckdb_conn.create_function("get_struct", get_struct, return_type=struct_type({
    "name": VARCHAR,
    "count": INTEGER,
    "tags": list_type(INTEGER),
    "active": BOOLEAN
}))

duckdb_conn.sql("SELECT get_struct()").show()
```

```text
┌─────────────────────────────────────────────────────────────────────┐
│                         get_struct_as_map()                         │
│ map(varchar, union(u1 varchar, u2 bigint, u3 bigint[], u4 boolean)) │
├─────────────────────────────────────────────────────────────────────┤
│ {name=duck, count=2, tags=[1, 2, 3], active=true}                   │
└─────────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────────────┐
│                             get_struct()                              │
│ struct("name" varchar, count integer, tags integer[], active boolean) │
├───────────────────────────────────────────────────────────────────────┤
│ {'name': duck, 'count': 2, 'tags': [1, 2, 3], 'active': true}         │
└───────────────────────────────────────────────────────────────────────┘
```

A `STRUCT` type, as a return type or as the type of a `duckdb.Value`, takes each field from the dict key of the same name, ignoring case. A dict whose keys do not match the fields raises `InvalidInputException: We could not convert the object ... to the desired target type`.

### `tuple`

`tuple` converts to `LIST` by default, when it's used to construct a Value object of type `STRUCT` it will convert to `STRUCT` instead.

### NumPy Objects

`numpy.ndarray` and `numpy.datetime64` are converted by calling `tolist()` and converting the result of that.

A NumPy integer scalar such as `numpy.int64(5)` is read by its value in `values()` and in expressions. As a query parameter, it raises `NotImplementedException: Unable to transform python value of type ...`; pass its Python value, `numpy.int64(5).item()`, instead.
