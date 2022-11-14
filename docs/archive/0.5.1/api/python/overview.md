---
layout: docu
title: Python API
selected: Client APIs
---
## Installation
The DuckDB Python API can be installed using [pip](https://pip.pypa.io): `pip install duckdb`. Please see the [installation page](../../installation?environment=python) for details. It is also possible to install DuckDB using [conda](https://docs.conda.io): `conda install python-duckdb -c conda-forge`.

## Basic API Usage
The standard DuckDB Python API provides a SQL interface compliant with the [DB-API 2.0 specification described by PEP 249](https://www.python.org/dev/peps/pep-0249/) similar to the [SQLite Python API](https://docs.python.org/3.7/library/sqlite3.html).

### Startup & Shutdown
To use the module, you must first create a `Connection` object that represents the database. The connection object takes as parameter the database file to read and write from. If the database file does not exist, it will be created (the file extension may be `.db`, `.duckdb`, or anything else). The special value `:memory:` (the default) can be used to create an **in-memory database**. Note that for an in-memory database no data is persisted to disk (i.e. all data is lost when you exit the Python process). If you would like to connect to an existing database in read-only mode, you can set the `read_only` flag to `True`. Read-only mode is required if multiple Python processes want to access the same database file at the same time.

```python
import duckdb
# to start an in-memory database
con = duckdb.connect(database=':memory:')
# to use a database file (not shared between processes)
con = duckdb.connect(database='my-db.duckdb', read_only=False)
# to use a database file (shared between processes)
con = duckdb.connect(database='my-db.duckdb', read_only=True)
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
Transferring large datasets to and from DuckDB uses a separate API built around [NumPy](https://numpy.org) and [Pandas](https://pandas.pydata.org), or [Apache Arrow](https://arrow.apache.org/). This API works with entire columns of data instead of scalar values and is therefore far more efficient.

By default, DuckDB will automatically be able to query a Pandas DataFrame or Arrow object that is stored in a Python variable by name. DuckDB supports querying multiple types of Apache Arrow objects including [tables](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html), [datasets](https://arrow.apache.org/docs/python/generated/pyarrow.dataset.Dataset.html), [recordbatchreaders](https://arrow.apache.org/docs/python/generated/pyarrow.ipc.RecordBatchStreamReader.html), and [scanners](https://arrow.apache.org/docs/python/generated/pyarrow.dataset.Scanner.html). See the Python [guides](../../guides/index#python-client) for more examples.

DuckDB also supports "registering" a DataFrame or Arrow object as a virtual table, comparable to a SQL `VIEW`. This is useful when querying a DataFrame/Arrow object that is stored in another way (as a class variable, or a value in a dictionary). Below is a Pandas example:

```python
import pandas as pd
test_df = pd.DataFrame.from_dict({"i":[1, 2, 3, 4], "j":["one", "two", "three", "four"]})
con.execute('SELECT * FROM test_df')
con.fetchall()
# [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]
```

If your Pandas DataFrame is stored in another location, here is an example of manually registering it:
```python
import pandas as pd
my_dictionary = {}
my_dictionary['test_df'] = pd.DataFrame.from_dict({"i":[1, 2, 3, 4], "j":["one", "two", "three", "four"]})
con.register('test_df_view', my_dictionary['test_df'])
con.execute('SELECT * FROM test_df_view')
con.fetchall()
# [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]
```

Pyarrow tables work in much the same way:
```python
import pyarrow as pa
arrow_table = pa.Table.from_pydict({'i':[1,2,3,4], 'j':["one", "two", "three", "four"]})
con.execute('SELECT * FROM arrow_table')
con.fetchall()
```

You can also create a persistent table in DuckDB from the contents of the DataFrame (or the view):
```python
con.execute('CREATE TABLE test_df_table AS SELECT * FROM test_df')
```
> DuckDB keeps a reference to the Pandas DataFrame or Arrow object after registration. This prevents them from being garbage-collected by the Python runtime. The reference is cleared when the connection is closed, but can also be cleared manually using the `unregister()` method.

When retrieving the data from DuckDB back into Python, the standard method of calling `fetchall()` is inefficient as individual Python objects need to be created for every value in the result set. When retrieving a lot of data, this can become very slow.

DuckDB's Python client provides multiple additional methods that can be used to efficiently retrieve data.
### NumPy
* `fetchnumpy()` fetches the data as a dictionary of NumPy arrays

### Pandas
* `df()` fetches the data as a Pandas DataFrame
* `fetchdf()` is an alias of `df()`
* `fetch_df()` is an alias of `df()`
* `fetch_df_chunk(vector_multiple)` fetches a portion of the results into a DataFrame. The number of rows returned in each chunk is the vector size (1024 by default) * vector_multiple (1 by default).

### Apache Arrow
* `arrow()` fetches the data as an [Arrow table](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html)
* `fetch_arrow_table()` is an alias of `arrow()`
* `fetch_record_batch(chunk_size)` returns an [Arrow record batch reader](https://arrow.apache.org/docs/python/generated/pyarrow.ipc.RecordBatchStreamReader.html) with `chunk_size` rows per batch


Below are some examples using this functionality. See the Python [guides](../../guides/index#python-client) for more examples.

```python
# fetch as Pandas DataFrame
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

# fetch as an Arrow table. Converting to Pandas afterwards just for pretty printing
tbl = con.execute("SELECT * FROM items").fetch_arrow_table()
print(tbl.to_pandas())
#        item    value  count
# 0     jeans    20.00      1
# 1    hammer    42.20      2
# 2    laptop  2000.00      1
# 3  chainsaw   500.00     10
# 4    iphone   300.00      2

```

Also refer to [the data import documentation](../../data/overview) for more options of efficiently importing data.


## Relational API
In addition to the SQL API DuckDB supports a programmatic method to construct queries. See [https://github.com/duckdb/duckdb/blob/master/examples/python/duckdb-python.py](https://github.com/duckdb/duckdb/blob/master/examples/python/duckdb-python.py) for an example.
