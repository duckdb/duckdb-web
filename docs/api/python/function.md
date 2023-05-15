---
layout: docu
title: Python Function API
selected: Client APIs
---

You can create a DuckDB function out of a python function so it can be used in SQL queries.
Just like regular [functions](../../sql/functions/overview.md) they need to have a name, a return type and parameter types.

### Creating Functions

The `create_function` method is used to add a function, the parameters to this method are:  

`name: str`  
The name that will be used to identify the function.  
  
`function: Callable`  
The python function that will be used.

`argument_type_list: Optional[List]`  
The types of the arguments that the function expects.

`return_type: Optional[DuckDBPyType]`  
The type of the value returned from the function.

`type: Optional[str]`  
The type of python function, either `native` or `arrow`.

`null_handling: Optional[str]`  
The way NULL value parameters should be handled.

`exception_handling: Optional[str]`  
The way exceptions that occurred during execution of the function should be handled.

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
def dont_intercept_null(x):
	return 5

duckdb.register_scalar_udf('dont_intercept', dont_intercept_null, [BIGINT], BIGINT)
res = duckdb.sql("""
	select dont_intercept(NULL)
""").fetchall()
print(res)
# [(None,)]

duckdb.unregister_udf('dont_intercept')
duckdb.register_scalar_udf('dont_intercept', dont_intercept_null, [BIGINT], BIGINT, null_handling='special')
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
def will_throw():
    raise ValueError("ERROR")

duckdb.register_scalar_udf('throws', will_throw, [], BIGINT)
try:
    res = duckdb.sql("""
        select throws()
    """).fetchall()
except duckdb.InvalidInputException as e:
    print(e)

duckdb.register_scalar_udf('doesnt_throw', will_throw, [], BIGINT, exception_handling='return_null')
res = duckdb.sql("""
    select doesnt_throw()
""").fetchall()
print(res)
# [(None,)]
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

duckdb.register_scalar_udf('random_date', random_date, [], DATE)
res = duckdb.sql('select random_date()').fetchall()
print(res)
# [(datetime.date(2019, 5, 15),)]
```
