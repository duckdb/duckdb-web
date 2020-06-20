---
layout: docu
title: Python API
selected: Client APIs
---
## Installation
The DuckDB Python API can be installed using [pip](https://pip.pypa.io): `pip install duckdb`. Please see the [installation page](/docs/installation?environment=python) for details. It is also possible to install DuckDB using [conda](https://docs.conda.io): `conda install python-duckdb -c conda-forge`.

## Basic API Usage
The standard DuckDB Python API provides a SQL interface compliant with the [DB-API 2.0 specification described by PEP 249](https://www.python.org/dev/peps/pep-0249/) similar to the [SQLite Python API](https://docs.python.org/3.7/library/sqlite3.html).

### Startup & Shutdown
To use the module, you must first create a `Connection` object that represents the database. The connection object takes as parameter the database file to read and write from. The special value `:memory:` (the default) can be used to create an **in-memory database**. Note that for an in-memory database no data is persisted to disk (i.e. all data is lost when you exit the Python process). If you would like to connect to an existing database in read-only mode, you can set the `read_only` flag to `True`. Read-only mode is required if multiple Python processes want to access the same database file at the same time. 

```python
import duckdb
con = duckdb.connect(database=':memory:', read_only=False)
```
If you want to create a second connection to an existing database, you can use the `cursor()` method. This might be useful for example to allow parallel threads running queries independently. A single connection is thread-safe but is locked for the duration of the queries, effectively serializing database access in this case. 

Connections are closed implicitly when they go out of scope or if they are explicitly closed using `close()`.  Once the last connection to a database instance is closed, the database instance is closed as well.

### Querying
SQL queries can be sent to DuckDB using the `execute()` method of connections. Once a query has been executed, results can be retrieved using the `fetchone` and `fetchall` methods on the connection. Below is a short example:

```python
# create a table
con.execute("CREATE TABLE items(item VARCHAR, value DECIMAL(10,2), count INTEGER)")
# insert two items into the table
con.execute("INSERT INTO items VALUES ('jeans', 20.0, 1), ('hammer', 42.2, 2)")

# retrieve the items again
con.execute("SELECT * FROM items")
print(con.fetchall())
# [('jeans', 20.0, 1), ('hammer', 42.2, 2)]
```

The `description` property of the connection object contains the column names as per the standard.

DuckDB also supports prepared statements in the API with the `execute` and `executemany` methods. In this case, the parameters are passed as an additional parameter after a query that contains `?` placeholders. Here is an example:
```python
# insert a row using prepared statements
con.execute("INSERT INTO items VALUES (?, ?, ?)", ['laptop', 2000, 1])

# insert several rows using prepared statements
con.executemany("INSERT INTO items VALUES (?, ?, ?)", [['chainsaw', 500, 10], ['iphone', 300, 2]] )

# query the database using a prepared statement
con.execute("SELECT item FROM items WHERE value > ?", [400])
print(con.fetchall())
# [('laptop',), ('chainsaw',)]

```

> Do *not* use `executemany` to insert large amounts of data into DuckDB. See below for better options.

## Efficient Transfer
Transferring large datasets to and from DuckDB uses a separate API built around [NumPy](https://numpy.org) and [Pandas](https://pandas.pydata.org) da. This API works with entire columns of data instead of scalar values and is therefore far more efficient. 

DuckDB supports "registering" a Pandas data frame as a virtual table, comparable to a SQL `VIEW`. Below is an example:

```python
import pandas as pd
test_df = pd.DataFrame.from_dict({"i":[1, 2, 3, 4], "j":["one", "two", "three", "four"]})
con.register('test_df_view', test_df)
con.execute('SELECT * FROM test_df_view')
con.fetchall()
# [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]
```

You can now use the registered view to create a persistent table in DuckDB:
```python
con.execute('CREATE TABLE test_df_table AS SELECT * FROM test_df_view')
```
> DuckDB keeps a reference to the Pandas data frame after registration. This prevents the data frame from being garbage-collected by the Python runtime. The reference is cleared when the connection is closed, but can also be cleared manually using the `unregister()` method.

When retrieving the data from DuckDB back into Python, the standard method of calling `fetchall()` is inefficient as individual Python objects need to be created for every value in the result set. When retrieving a lot of data, this can become very slow.

In DuckDB, there are two additional methods that can be used to efficiently retrieve dat: `fetchnumpy()` and `fetchdf()`. `fetchnumpy()` fetches the data as a dictionary of `NumPy` arrays. `fetchdf()` fetches the data as a Pandas DataFrame.

Below is an example of using this functionality:

```python
# fetch as pandas data frame
df = con.execute("SELECT * FROM items").fetchdf()
print(df)
#        item   value  count
# 0     jeans    20.0      1
# 1    hammer    42.2      2
# 2    laptop  2000.0      1
# 3  chainsaw   500.0     10
# 4    iphone   300.0      2

# fetch as dictionary of numpy arrays
arr = con.execute("SELECT * FROM items").fetchnumpy()
print(arr)
# {'item': masked_array(data=['jeans', 'hammer', 'laptop', 'chainsaw', 'iphone'],
#              mask=[False, False, False, False, False],
#        fill_value='?',
#             dtype=object), 'value': masked_array(data=[20.0, 42.2, 2000.0, 500.0, 300.0],
#              mask=[False, False, False, False, False],
#        fill_value=1e+20), 'count': masked_array(data=[1, 2, 1, 10, 2],
#              mask=[False, False, False, False, False],
#        fill_value=999999,
#             dtype=int32)}

```

Also refer to [the data import documentation](/docs/data/import) for more options of efficiently importing data.


## Relational API
In addition to the SQL API DuckDB supports a programmatic method to construct queries. See [https://github.com/cwida/duckdb/blob/master/examples/python/duckdb-python.py](https://github.com/cwida/duckdb/blob/master/examples/python/duckdb-python.py) for an example.
