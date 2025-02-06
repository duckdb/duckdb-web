---
layout: docu
title: Python DB API
---

The standard DuckDB Python API provides a SQL interface compliant with the [DB-API 2.0 specification described by PEP 249](https://www.python.org/dev/peps/pep-0249/) similar to the [SQLite Python API](https://docs.python.org/3.7/library/sqlite3.html).

## Connection

To use the module, you must first create a `DuckDBPyConnection` object that represents a connection to a database.
This is done through the [`duckdb.connect`]({% link docs/archive/1.1/api/python/reference/index.md %}#duckdb.connect) method.

The 'config' keyword argument can be used to provide a `dict` that contains key->value pairs referencing [settings]({% link docs/archive/1.1/configuration/overview.md %}#configuration-reference) understood by DuckDB.

### In-Memory Connection

The special value `:memory:` can be used to create an **in-memory database**. Note that for an in-memory database no data is persisted to disk (i.e., all data is lost when you exit the Python process).

#### Named in-memory Connections

The special value `:memory:` can also be postfixed with a name, for example: `:memory:conn3`.
When a name is provided, subsequent `duckdb.connect` calls will create a new connection to the same database, sharing the catalogs (views, tables, macros etc..).

Using `:memory:` without a name will always create a new and separate database instance.

### Default Connection

By default we create an (unnamed) **in-memory-database** that lives inside the `duckdb` module.
Every method of `DuckDBPyConnection` is also available on the `duckdb` module, this connection is what's used by these methods.

The special value `:default:` can be used to get this default connection.

### File-Based Connection

If the `database` is a file path, a connection to a persistent database is established.
If the file does not exist the file will be created (the extension of the file is irrelevant and can be `.db`, `.duckdb` or anything else).

#### `read_only` Connections

If you would like to connect in read-only mode, you can set the `read_only` flag to `True`. If the file does not exist, it is **not** created when connecting in read-only mode.
Read-only mode is required if multiple Python processes want to access the same database file at the same time.

```python
import duckdb

duckdb.execute("CREATE TABLE tbl AS SELECT 42 a")
con = duckdb.connect(":default:")
con.sql("SELECT * FROM tbl")
# or
duckdb.default_connection.sql("SELECT * FROM tbl")
```

```text
┌───────┐
│   a   │
│ int32 │
├───────┤
│    42 │
└───────┘
```

```python
import duckdb

# to start an in-memory database
con = duckdb.connect(database = ":memory:")
# to use a database file (not shared between processes)
con = duckdb.connect(database = "my-db.duckdb", read_only = False)
# to use a database file (shared between processes)
con = duckdb.connect(database = "my-db.duckdb", read_only = True)
# to explicitly get the default connection
con = duckdb.connect(database = ":default:")
```

If you want to create a second connection to an existing database, you can use the `cursor()` method. This might be useful for example to allow parallel threads running queries independently. A single connection is thread-safe but is locked for the duration of the queries, effectively serializing database access in this case.

Connections are closed implicitly when they go out of scope or if they are explicitly closed using `close()`. Once the last connection to a database instance is closed, the database instance is closed as well.

## Querying

SQL queries can be sent to DuckDB using the `execute()` method of connections. Once a query has been executed, results can be retrieved using the `fetchone` and `fetchall` methods on the connection. `fetchall` will retrieve all results and complete the transaction. `fetchone` will retrieve a single row of results each time that it is invoked until no more results are available. The transaction will only close once `fetchone` is called and there are no more results remaining (the return value will be `None`). As an example, in the case of a query only returning a single row, `fetchone` should be called once to retrieve the results and a second time to close the transaction. Below are some short examples:

```python
# create a table
con.execute("CREATE TABLE items (item VARCHAR, value DECIMAL(10, 2), count INTEGER)")
# insert two items into the table
con.execute("INSERT INTO items VALUES ('jeans', 20.0, 1), ('hammer', 42.2, 2)")

# retrieve the items again
con.execute("SELECT * FROM items")
print(con.fetchall())
# [('jeans', Decimal('20.00'), 1), ('hammer', Decimal('42.20'), 2)]

# retrieve the items one at a time
con.execute("SELECT * FROM items")
print(con.fetchone())
# ('jeans', Decimal('20.00'), 1)
print(con.fetchone())
# ('hammer', Decimal('42.20'), 2)
print(con.fetchone()) # This closes the transaction. Any subsequent calls to .fetchone will return None
# None
```

The `description` property of the connection object contains the column names as per the standard.

### Prepared Statements

DuckDB also supports [prepared statements]({% link docs/archive/1.1/sql/query_syntax/prepared_statements.md %}) in the API with the `execute` and `executemany` methods. The values may be passed as an additional parameter after a query that contains `?` or `$1` (dollar symbol and a number) placeholders. Using the `?` notation adds the values in the same sequence as passed within the Python parameter. Using the `$` notation allows for values to be reused within the SQL statement based on the number and index of the value found within the Python parameter. Values are converted according to the [conversion rules]({% link docs/archive/1.1/api/python/conversion.md %}#object-conversion-python-object-to-duckdb).

Here are some examples. First, insert a row using a [prepared statement]({% link docs/archive/1.1/sql/query_syntax/prepared_statements.md %}):

```python
con.execute("INSERT INTO items VALUES (?, ?, ?)", ["laptop", 2000, 1])
```

Second, insert several rows using a [prepared statement]({% link docs/archive/1.1/sql/query_syntax/prepared_statements.md %}):

```python
con.executemany("INSERT INTO items VALUES (?, ?, ?)", [["chainsaw", 500, 10], ["iphone", 300, 2]] )
```

Query the database using a [prepared statement]({% link docs/archive/1.1/sql/query_syntax/prepared_statements.md %}):

```python
con.execute("SELECT item FROM items WHERE value > ?", [400])
print(con.fetchall())
```

```text
[('laptop',), ('chainsaw',)]
```

Query using the `$` notation for a [prepared statement]({% link docs/archive/1.1/sql/query_syntax/prepared_statements.md %}) and reused values:

```python
con.execute("SELECT $1, $1, $2", ["duck", "goose"])
print(con.fetchall())
```

```text
[('duck', 'duck', 'goose')]
```

> Warning Do *not* use `executemany` to insert large amounts of data into DuckDB. See the [data ingestion page]({% link docs/archive/1.1/api/python/data_ingestion.md %}) for better options.

## Named Parameters

Besides the standard unnamed parameters, like `$1`, `$2` etc., it's also possible to supply named parameters, like `$my_parameter`.
When using named parameters, you have to provide a dictionary mapping of `str` to value in the `parameters` argument.
An example use is the following:

```python
import duckdb

res = duckdb.execute("""
    SELECT
        $my_param,
        $other_param,
        $also_param
    """,
    {
        "my_param": 5,
        "other_param": "DuckDB",
        "also_param": [42]
    }
).fetchall()
print(res)
```

```text
[(5, 'DuckDB', [42])]
```