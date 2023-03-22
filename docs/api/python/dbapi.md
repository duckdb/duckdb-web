---
layout: docu
title: Python DB API
selected: Client APIs
---

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

DuckDB also supports prepared statements in the API with the `execute` and `executemany` methods. The values may be passed as an additional parameter after a query that contains `?` or `$1` (dollar symbol and a number) placeholders. Using the `?` notation adds the values in the same sequence as passed within the Python parameter. Using the `$` notation allows for values to be reused within the SQL statement based on the number and index of the value found within the Python parameter.

Here are some examples:

```python
# insert a row using prepared statements
con.execute("INSERT INTO items VALUES (?, ?, ?)", ['laptop', 2000, 1])

# insert several rows using prepared statements
con.executemany("INSERT INTO items VALUES (?, ?, ?)", [['chainsaw', 500, 10], ['iphone', 300, 2]] )

# query the database using a prepared statement
con.execute("SELECT item FROM items WHERE value > ?", [400])
print(con.fetchall())
# [('laptop',), ('chainsaw',)]

# query using $ notation for prepared statement and reused values
con.execute("select $1, $1, $2", ["duck", "goose"])
print(con.fetchall())
# [('duck', 'duck', 'goose')]
```

### Named parameters

Besides the standard unnamed parameters, like `$1`, `$2` etc, it's also possible to supply named parameters, like `$my_parameter`.  
When using named parameters, you have to provide a dictionary mapping of `str` to value in the `parameters` argument  
An example use:
```py
import duckdb

duckdb.execute("""
  select
    $my_param,
    $other_param,
    $also_param
""",
  {
    'my_param': 5,
    'other_param': 'DuckDB',
    'also_param': [42]
  }
 ).fetchall()
# [(5, 'DuckDB', [42])]
```

> Do *not* use `executemany` to insert large amounts of data into DuckDB. See the [data ingestion page](data_ingestion) for better options.
