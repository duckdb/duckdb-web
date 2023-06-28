---
layout: docu
title: Python UDFs
selected: Client APIs
---

DuckDB's Python client provides the functionality for users to implement their own Scalar Python functions as User Defined Functions and execute them directly via SQL.

### API Documentation

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

### Example
In the example below you can see the usage of a Python UDF that returns the number of world cups won by each country. Note that it will return `None` if the country never won a world cup before.
```python
import duckdb
from duckdb.typing import *

con = duckdb.connect()

# Dictionary that maps countries and world cups they won
world_cup_titles = {
    "Brazil": 5,
    "Germany": 4,
    "Italy": 4,
    "Argentina": 2,
    "Uruguay": 2,
    "France": 2,
    "England": 1,
    "Spain": 1
}

# Function that will be registered as an UDF, simply does a lookup in the python dictionary
def world_cups(x):
     return world_cup_titles.get(x)

# We register the function
con.create_function("wc_titles", world_cups, [VARCHAR], INTEGER)
```

That's it, the function is then registered and ready to be called through SQL.
```python
# Let's create an example countries table with the countries we are interested in using
con.execute("CREATE TABLE countries(country VARCHAR)")
con.execute("INSERT INTO countries VALUES ('Brazil'), ('Germany'), ('Italy'), ('Argentina'), ('Uruguay'), ('France'), ('England'), ('Spain'), ('Netherlands')")
# We can simply call the function through SQL
con.sql("SELECT country, wc_titles(country) as world_cups from countries").fetchall()
```