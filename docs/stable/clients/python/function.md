---
layout: docu
redirect_from:
- /docs/api/python/function
- /docs/clients/python/function
title: Python Function API
---

You can create a DuckDB user-defined function (UDF) from a Python function so it can be used in SQL queries.
Similarly to regular [functions]({% link docs/stable/sql/functions/overview.md %}), they need to have a name, a return type and parameter types.

Here is an example using a Python function that calls a third-party library.

```python
import duckdb
from duckdb.sqltypes import VARCHAR
from faker import Faker

def generate_random_name():
    fake = Faker()
    return fake.name()

duckdb.create_function("random_name", generate_random_name, [], VARCHAR)
res = duckdb.sql("SELECT random_name()").fetchall()
print(res)
```

```text
[('Gerald Ashley',)]
```

## Creating Functions

To register a Python UDF, use the `create_function` method from a DuckDB connection. Here is the syntax:

```python
import duckdb
con = duckdb.connect()
con.create_function(name, function, parameters, return_type)
```

The `create_function` method takes the following parameters:

1. `name` A string representing the unique name of the UDF within the connection catalog.
2. `function` The Python function you wish to register as a UDF.
3. `parameters` Scalar functions can operate on one or more columns. This parameter takes a list of column types used as input.
4. `return_type` Scalar functions return one element per row. This parameter specifies the return type of the function.
5. `type` (optional): DuckDB supports both native Python types and PyArrow Arrays. By default, `type = 'native'` is assumed, but you can specify `type = 'arrow'` to use PyArrow Arrays. In general, using an Arrow UDF will be much more efficient than native because it will be able to operate in batches.
6. `null_handling` (optional): By default, `NULL` values are automatically handled as `NULL`-in `NULL`-out. Users can specify a desired behavior for `NULL` values by setting `null_handling = 'special'`.
7. `exception_handling` (optional): By default, when an exception is thrown from the Python function, it will be re-thrown in Python. Users can disable this behavior, and instead return `NULL`, by setting this parameter to `'return_null'`
8. `side_effects` (optional): By default, functions are expected to produce the same result for the same input. If the result of a function is impacted by any type of randomness, `side_effects` must be set to `True`.

To unregister a UDF, you can call the `remove_function` method with the UDF name:

```python
con.remove_function(name)
```

### Using Partial Functions

DuckDB UDFs can also be created with [Python partial functions](https://docs.python.org/3/library/functools.html#functools.partial).

In the below example, we show how a custom logger will return the concatenation of the execution datetime in ISO format, always followed by 
argument passed at UDF creation and the input parameter provided to the function call:

```python
from datetime import datetime
import duckdb
import functools


def get_datetime_iso_format() -> str:
    return datetime.now().isoformat()


def logger_udf(func, arg1: str, arg2: int) -> str:
    return ' '.join([func(), arg1, str(arg2)])
    
    
with duckdb.connect() as con:
    con.sql("select * from range(10) tbl(id)").to_table("example_table")
    
    con.create_function(
        'custom_logger',
        functools.partial(logger_udf, get_datetime_iso_format, 'logging data')
    )
    rel = con.sql("SELECT custom_logger(id) from example_table;")
    rel.show()

    con.create_function(
        'another_custom_logger',
        functools.partial(logger_udf, get_datetime_iso_format, ':')
    )
    rel = con.sql("SELECT another_custom_logger(id) from example_table;")
    rel.show()
```

```text
┌───────────────────────────────────────────┐
│             custom_logger(id)             │
│                  varchar                  │
├───────────────────────────────────────────┤
│ 2025-03-27T12:07:56.811251 logging data 0 │
│ 2025-03-27T12:07:56.811264 logging data 1 │
│ 2025-03-27T12:07:56.811266 logging data 2 │
│ 2025-03-27T12:07:56.811268 logging data 3 │
│ 2025-03-27T12:07:56.811269 logging data 4 │
│ 2025-03-27T12:07:56.811270 logging data 5 │
│ 2025-03-27T12:07:56.811271 logging data 6 │
│ 2025-03-27T12:07:56.811272 logging data 7 │
│ 2025-03-27T12:07:56.811274 logging data 8 │
│ 2025-03-27T12:07:56.811275 logging data 9 │
├───────────────────────────────────────────┤
│                  10 rows                  │
└───────────────────────────────────────────┘

┌────────────────────────────────┐
│   another_custom_logger(id)    │
│            varchar             │
├────────────────────────────────┤
│ 2025-03-27T12:07:56.812106 : 0 │
│ 2025-03-27T12:07:56.812116 : 1 │
│ 2025-03-27T12:07:56.812118 : 2 │
│ 2025-03-27T12:07:56.812119 : 3 │
│ 2025-03-27T12:07:56.812121 : 4 │
│ 2025-03-27T12:07:56.812122 : 5 │
│ 2025-03-27T12:07:56.812123 : 6 │
│ 2025-03-27T12:07:56.812124 : 7 │
│ 2025-03-27T12:07:56.812126 : 8 │
│ 2025-03-27T12:07:56.812127 : 9 │
├────────────────────────────────┤
│            10 rows             │
└────────────────────────────────┘
```

## Type Annotation

When the function has type annotation it's often possible to leave out all of the optional parameters.
Using `DuckDBPyType` we can implicitly convert many known types to DuckDB's type system.
For example:

```python
import duckdb

def my_function(x: int) -> str:
    return x

duckdb.create_function("my_func", my_function)
print(duckdb.sql("SELECT my_func(42)"))
```

```text
┌─────────────┐
│ my_func(42) │
│   varchar   │
├─────────────┤
│ 42          │
└─────────────┘
```

If only the parameter list types can be inferred, you'll need to pass in `None` as `parameters`.

## `NULL` Handling

By default when functions receive a `NULL` value, this instantly returns `NULL`, as part of the default `NULL`-handling.
When this is not desired, you need to explicitly set this parameter to `"special"`.

```python
import duckdb
from duckdb.sqltypes import BIGINT

def dont_intercept_null(x):
    return 5

duckdb.create_function("dont_intercept", dont_intercept_null, [BIGINT], BIGINT)
res = duckdb.sql("SELECT dont_intercept(NULL)").fetchall()
print(res)
```

```text
[(None,)]
```

With `null_handling="special"`:

```python
import duckdb
from duckdb.sqltypes import BIGINT

def dont_intercept_null(x):
    return 5

duckdb.create_function("dont_intercept", dont_intercept_null, [BIGINT], BIGINT, null_handling="special")
res = duckdb.sql("SELECT dont_intercept(NULL)").fetchall()
print(res)
```

```text
[(5,)]
```

> Always use `null_handling="special"` when the function can return NULL.


```python
import duckdb
from duckdb.sqltypes import VARCHAR


def return_str_or_none(x: str) -> str | None:
    if not x:
        return None
    
    return x

duckdb.create_function(
    "return_str_or_none",
    return_str_or_none,
    [VARCHAR],
    VARCHAR,
    null_handling="special"
)
res = duckdb.sql("SELECT return_str_or_none('')").fetchall()
print(res)
```

```text
[(None,)]
```

## Exception Handling

By default, when an exception is thrown from the Python function, we'll forward (re-throw) the exception.
If you want to disable this behavior, and instead return `NULL`, you'll need to set this parameter to `"return_null"`.

```python
import duckdb
from duckdb.sqltypes import BIGINT

def will_throw():
    raise ValueError("ERROR")

duckdb.create_function("throws", will_throw, [], BIGINT)
try:
    res = duckdb.sql("SELECT throws()").fetchall()
except duckdb.InvalidInputException as e:
    print(e)

duckdb.create_function("doesnt_throw", will_throw, [], BIGINT, exception_handling="return_null")
res = duckdb.sql("SELECT doesnt_throw()").fetchall()
print(res)
```

```console
Invalid Input Error: Python exception occurred while executing the UDF: ValueError: ERROR

At:
  ...(5): will_throw
  ...(9): <module>
```

```text
[(None,)]
```

## Side Effects

By default DuckDB will assume the created function is a *pure* function, meaning it will produce the same output when given the same input.
If your function does not follow that rule, for example when your function makes use of randomness, then you will need to mark this function as having `side_effects`.

For example, this function will produce a new count for every invocation.

```python
def count() -> int:
    old = count.counter;
    count.counter += 1
    return old

count.counter = 0
```

If we create this function without marking it as having side effects, the result will be the following:

```python
con = duckdb.connect()
con.create_function("my_counter", count, side_effects=False)
res = con.sql("SELECT my_counter() FROM range(10)").fetchall()
print(res)
```

```text
[(0,), (0,), (0,), (0,), (0,), (0,), (0,), (0,), (0,), (0,)]
```

Which is obviously not the desired result, when we add `side_effects=True`, the result is as we would expect:

```python
con.remove_function("my_counter")
count.counter = 0
con.create_function("my_counter", count, side_effects=True)
res = con.sql("SELECT my_counter() FROM range(10)").fetchall()
print(res)
```

```text
[(0,), (1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,)]
```

## Python Function Types

Currently, two function types are supported, `native` (default) and `arrow`.

### Arrow

If the function is expected to receive arrow arrays, set the `type` parameter to `'arrow'`.

This will let the system know to provide arrow arrays of up to `STANDARD_VECTOR_SIZE` tuples to the function, and also expect an array of the same amount of tuples to be returned from the function.

In general, using an Arrow UDF will be much more efficient than native because it will be able to operate in batches.

```python
import duckdb
import pyarrow as pa
from duckdb.sqltypes import VARCHAR
from pyarrow import compute as pc


def mirror(strings: pa.Array, sep: pa.Array) -> pa.Array:
    assert isinstance(strings, pa.ChunkedArray)
    assert isinstance(sep, pa.ChunkedArray)
    return pc.binary_join_element_wise(strings, pc.ascii_reverse(strings), sep)


duckdb.create_function(
    "mirror",
    mirror,
    [VARCHAR, VARCHAR],
    return_type=VARCHAR,
    type="arrow",
)

duckdb.sql(
    "CREATE OR REPLACE TABLE strings AS SELECT 'hello' AS str UNION ALL SELECT 'world' AS str;"
)
print(duckdb.sql("SELECT mirror(str, '|') FROM strings;").fetchall())
```

```text
[('hello|olleh',), ('world|dlrow',)]
```

### Native

When the function type is set to `native` the function will be provided with a single tuple at a time, and expect only a single value to be returned.
This can be useful to interact with Python libraries that don't operate on Arrow, such as `faker`:

```python
import duckdb

from duckdb.sqltypes import DATE
from faker import Faker

def random_date():
    fake = Faker()
    return fake.date_between()

duckdb.create_function(
    "random_date",
    random_date,
    parameters=[],
    return_type=DATE,
    type="native",
)
res = duckdb.sql("SELECT random_date()").fetchall()
print(res)
```

```text
[(datetime.date(2019, 5, 15),)]
```
