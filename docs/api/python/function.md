---
layout: docu
title: Python Function API
selected: Client APIs
---

You can create a DuckDB User Defined Function (UDF) out of a python function so it can be used in SQL queries.
Just like regular [functions](../../sql/functions/overview) they need to have a name, a return type and parameter types.

Example using a python function that calls a third party library.
```py
import duckdb
import duckdb
from duckdb.typing import *
from faker import Faker

def random_name():
	fake = Faker()
	return fake.name()

duckdb.create_function('random_name', random_name, [], VARCHAR)
res = duckdb.sql('select random_name()').fetchall()
print(res)
# [('Gerald Ashley',)]
```

### Creating Functions

To register a Python UDF, simply use the `create_function` method from a DuckDB connection. Here is the syntax:
```python 
import duckdb
con = duckdb.connect()
con.create_function(name, function, argument_type_list, return_type, type, null_handling)
```

The `create_function` method requires the following parameters:

1. **Name**: A string representing the unique name of the UDF within the connection catalog.
2. **Function**: The Python function you wish to register as a UDF.
3. **Argument Type List**: Scalar functions can operate on one or more columns. This parameter takes a list of column types used as input.
4. **Return Type**: Scalar functions return one element per row. This parameter specifies the return type of the function.
5. **Type** (Optional): DuckDB supports both built-in Python types and PyArrow Tables. By default, built-in types are assumed, but you can specify `type='arrow'` to use PyArrow Tables.
6. **Null Handling** (Optional): By default, null values are automatically handled as Null-In Null-Out. Users can specify a desired behavior for null values by setting `null_handling='special'`.

To unregister a UDF, you can call the `remove_function` method with the UDF name:

```python
con.remove_function(name)
```

### Type Annotation

When the function has type annotation it's often possible to leave out all of the optional parameters.  
Using `DuckDBPyType` we can implicitly convert many known types to DuckDBs type system.  
For example:
```python
import duckdb

def my_function(x: int) -> str:
	return x

duckdb.create_function('my_func', my_function)
duckdb.sql('select my_func(42)')
# ┌─────────────┐
# │ my_func(42) │
# │   varchar   │
# ├─────────────┤
# │ 42          │
# └─────────────┘
```

If only the parameter list types can be inferred, you'll need to pass in `None` as `argument_type_list`.

### Null Handling
By default when functions receive a NULL value, this instantly returns NULL, as part of the default null handling.  
When this is not desired, you need to explicitly set this parameter to `'special'`.

```py
import duckdb
from duckdb.typing import *

def dont_intercept_null(x):
	return 5

duckdb.create_function('dont_intercept', dont_intercept_null, [BIGINT], BIGINT)
res = duckdb.sql("""
	select dont_intercept(NULL)
""").fetchall()
print(res)
# [(None,)]

duckdb.remove_function('dont_intercept')
duckdb.create_function('dont_intercept', dont_intercept_null, [BIGINT], BIGINT, null_handling='special')
res = duckdb.sql("""
	select dont_intercept(NULL)
""").fetchall()
print(res)
# [(5,)]
```

### Exception Handling

By default, when an exception is thrown from the python function, we'll forward (re-throw) the exception.  
If you want to disable this behavior, and instead return null, you'll need to set this parameter to `'return_null'`

```py
import duckdb
from duckdb.typing import *

def will_throw():
    raise ValueError("ERROR")

duckdb.create_function('throws', will_throw, [], BIGINT)
try:
    res = duckdb.sql("""
        select throws()
    """).fetchall()
except duckdb.InvalidInputException as e:
    print(e)

duckdb.create_function('doesnt_throw', will_throw, [], BIGINT, exception_handling='return_null')
res = duckdb.sql("""
    select doesnt_throw()
""").fetchall()
print(res)
# [(None,)]
```

### Side Effects

By default DuckDB will assume the created function is a *pure* function, meaning it will produce the same output when given the same input. 
If your function does not follow that rule, for example when your function makes use of randomness, then you will need to mark this function as having `side_effects`.

For example, this function will produce a new count for every invocation
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
con.create_function('my_counter', count, side_effects=False)
res = con.sql('select my_counter() from range(10)').fetchall()
# [(0,), (0,), (0,), (0,), (0,), (0,), (0,), (0,), (0,), (0,)]
```
Which is obviously not the desired result, when we add `side_effects=True`, the result is as we would expect:
```python
con.create_function('my_counter', count, side_effects=True)
res = con.sql('select my_counter() from range(10)').fetchall()
# [(0,), (1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,)]
```

### Python Function Types

Currently two function types are supported, `native` (default) and `arrow`.

#### Arrow

If the function is expected to receive arrow arrays, set the `type` parameter to `'arrow'`.  

This will let the system know to provide arrow arrays of up to `STANDARD_VECTOR_SIZE` tuples to the function, and also expect an array of the same amount of tuples to be returned from the function.

#### Native

When the function type is set to `native` the function will be provided with a single tuple at a time, and expect only a single value to be returned.  
This can be useful to interact with python libraries that don't operate on Arrow, such as `faker`:
```py
import duckdb

from duckdb.typing import *
from faker import Faker

def random_date():
	fake = Faker()
	return fake.date_between()

duckdb.create_function('random_date', random_date, [], DATE)
res = duckdb.sql('select random_date()').fetchall()
print(res)
# [(datetime.date(2019, 5, 15),)]
```
