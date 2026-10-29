---
layout: docu
redirect_from:
- /docs/api/python/function
- /docs/clients/python/function
- /docs/stable/clients/python/function
- /docs/current/clients/python/function
- /docs/lts/clients/python/function
- /docs/preview/clients/python/function
title: Python Function API
---

You can create a DuckDB user-defined function (UDF) from a Python function so it can be used in SQL queries.
Similarly to regular [functions]({% link docs/2.0/sql/functions/overview.md %}), they need to have a name, a return type, and parameter types.

## Creating Functions

To register a Python UDF, use the `create_function` method from a DuckDB connection:

```python
import duckdb

def add_one(x: int) -> int:
    return x + 1

con = duckdb.connect()
con.create_function("add_one", add_one)
print(con.sql("SELECT add_one(41)").fetchall())
```

```text
[(42,)]
```

UDFs need NumPy. Without the `numpy` package, `create_function` raises `InvalidInputException: 'numpy' is required for this operation, but it wasn't installed`.

The signature is `create_function(name, function, parameters=None, return_type=None, *, type=..., null_handling=..., exception_handling=..., side_effects=False)`. The last four parameters are keyword only, and a value they do not accept raises a `TypeError`:

1. `name` A string representing the unique name of the UDF within the connection catalog.
2. `function` The Python function you wish to register as a UDF.
3. `parameters` Scalar functions can operate on one or more columns. This parameter takes a list of column types used as input.
4. `return_type` Scalar functions return one element per row. This parameter specifies the return type of the function.
5. `type` (optional): DuckDB supports both native Python types and PyArrow Arrays. By default, `type = 'native'` is assumed, but you can specify `type = 'arrow'` to use PyArrow Arrays. In general, using an Arrow UDF will be much more efficient than native because it will be able to operate in batches.
6. `null_handling` (optional): By default, `NULL` values are automatically handled as `NULL`-in `NULL`-out. Users can specify a desired behavior for `NULL` values by setting `null_handling = 'special'`.
7. `exception_handling` (optional): By default, when an exception is thrown from the Python function, the query fails with an error that names it. Users can disable this behavior, and instead return `NULL`, by setting this parameter to `'return_null'`.
8. `side_effects` (optional): By default, functions are expected to produce the same result for the same input. If the result of a function is impacted by any type of randomness, `side_effects` must be set to `True`.

A type given as a string, such as `"INTEGER"` or the name of a type created with `CREATE TYPE`, is looked up on the connection that registers the function. While an `execute()` result of the connection is still open, `create_function` raises a `ResourceInUseException`.

To unregister a UDF, you can call the `remove_function` method with the UDF name:

```python
con.remove_function("add_one")
```

### Using the Connection from a Function

A UDF cannot use the connection that runs its query: such a call raises a `ResourceInUseException`, and the query fails with `InvalidInputException: Python exception occurred while executing the UDF: ResourceInUseException: Resource In Use Error: code running inside a query cannot use that query's connection; use a separate connection from cursor()`. A cursor of that connection works:

```python
def lookup(x: int) -> int:
    cur = con.cursor()
    try:
        return cur.execute("SELECT 41 + ?", [x]).fetchone()[0]
    finally:
        cur.close()

con.create_function("lookup", lookup)
print(con.sql("SELECT lookup(1)").fetchall())
```

```text
[(42,)]
```

### Using Partial Functions

DuckDB UDFs can also be created with [Python partial functions](https://docs.python.org/3/library/functools.html#functools.partial). The arguments the partial function fixes are not parameters of the UDF:

```python
from functools import partial
import duckdb

def add(x: int, y: int) -> int:
    return x + y

with duckdb.connect() as con:
    con.create_function("add_ten", partial(add, 10))
    print(con.sql("SELECT add_ten(5)").fetchall())
```

```text
[(15,)]
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

When `parameters` is left out, the parameter types come from the annotations, and a parameter without an annotation accepts any type. The return type must be annotated or given as `return_type`; otherwise `create_function` raises `InvalidInputException: Could not infer the return type, please set it explicitly`.

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

duckdb.create_function("dont_intercept_special", dont_intercept_null, [BIGINT], BIGINT, null_handling="special")
res = duckdb.sql("SELECT dont_intercept_special(NULL)").fetchall()
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

By default, when an exception is thrown from the Python function, the query fails with a `duckdb.InvalidInputException` that names the Python exception.
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

```text
Invalid Input Error: Python exception occurred while executing the UDF: ValueError: ERROR
[(None,)]
```

`"return_null"` turns an `Exception` other than `MemoryError` into `NULL`. A `MemoryError` still fails the query, and so does an exception that does not derive from `Exception`, such as `KeyboardInterrupt`.

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

This will let the system know to provide each argument as a `pyarrow.ChunkedArray` of at most 2048 rows to the function, and also expect an array of the same amount of rows to be returned from the function.

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
    side_effects=True,
)
res = duckdb.sql("SELECT random_date()").fetchall()
print(res)
```

```text
[(datetime.date(2019, 5, 15),)]
```
