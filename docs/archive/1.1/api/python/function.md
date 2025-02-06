---
layout: docu
title: Python Function API
---

You can create a DuckDB user-defined function (UDF) from a Python function so it can be used in SQL queries.
Similarly to regular [functions]({% link docs/archive/1.1/sql/functions/overview.md %}), they need to have a name, a return type and parameter types.

Here is an example using a Python function that calls a third-party library.

```python
import duckdb
from duckdb.typing import *
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
5. `type` (optional): DuckDB supports both built-in Python types and PyArrow Tables. By default, built-in types are assumed, but you can specify `type = 'arrow'` to use PyArrow Tables.
6. `null_handling` (optional): By default, `NULL` values are automatically handled as `NULL`-in `NULL`-out. Users can specify a desired behavior for `NULL` values by setting `null_handling = 'special'`.
7. `exception_handling` (optional): By default, when an exception is thrown from the Python function, it will be re-thrown in Python. Users can disable this behavior, and instead return `NULL`, by setting this parameter to `'return_null'`
8. `side_effects` (optional): By default, functions are expected to produce the same result for the same input. If the result of a function is impacted by any type of randomness, `side_effects` must be set to `True`.

To unregister a UDF, you can call the `remove_function` method with the UDF name:

```python
con.remove_function(name)
```

## Type Annotation

When the function has type annotation it's often possible to leave out all of the optional parameters.
Using `DuckDBPyType` we can implicitly convert many known types to DuckDBs type system.
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
from duckdb.typing import *

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
from duckdb.typing import *

def dont_intercept_null(x):
    return 5

duckdb.create_function("dont_intercept", dont_intercept_null, [BIGINT], BIGINT, null_handling="special")
res = duckdb.sql("SELECT dont_intercept(NULL)").fetchall()
print(res)
```

```text
[(5,)]
```

## Exception Handling

By default, when an exception is thrown from the Python function, we'll forward (re-throw) the exception.
If you want to disable this behavior, and instead return `NULL`, you'll need to set this parameter to `"return_null"`.

```python
import duckdb
from duckdb.typing import *

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

### Native

When the function type is set to `native` the function will be provided with a single tuple at a time, and expect only a single value to be returned.
This can be useful to interact with Python libraries that don't operate on Arrow, such as `faker`:

```python
import duckdb

from duckdb.typing import *
from faker import Faker

def random_date():
    fake = Faker()
    return fake.date_between()

duckdb.create_function("random_date", random_date, [], DATE, type="native")
res = duckdb.sql("SELECT random_date()").fetchall()
print(res)
```

```text
[(datetime.date(2019, 5, 15),)]
```