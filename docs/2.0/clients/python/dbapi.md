---
layout: docu
redirect_from:
- /docs/api/python/dbapi
- /docs/clients/python/dbapi
- /docs/stable/clients/python/dbapi
- /docs/current/clients/python/dbapi
- /docs/lts/clients/python/dbapi
- /docs/preview/clients/python/dbapi
title: Python DB API
---

The standard DuckDB Python API provides a SQL interface compliant with the [DB-API 2.0 specification described by PEP 249](https://www.python.org/dev/peps/pep-0249/) similar to the [SQLite Python API](https://docs.python.org/3/library/sqlite3.html).

## Connection

To use the module, you must first create a `DuckDBPyConnection` object that represents a connection to a database.
This is done through the [`duckdb.connect`]({% link docs/2.0/clients/python/reference/index.md %}#duckdb.connect) method, which takes three arguments: `database`, `read_only` and `config`.

The `config` keyword argument can be used to provide a `dict` that contains key-value pairs referencing [settings]({% link docs/2.0/configuration/overview.md %}#configuration-reference) understood by DuckDB.

### In-Memory Connection

The special value `:memory:` can be used to create an **in-memory database**. Note that for an in-memory database no data is persisted to disk (i.e., all data is lost when you exit the Python process).

#### Named In-memory Connections

The special value `:memory:` can also be postfixed with a name, for example: `:memory:conn3`.
When a name is provided, subsequent `duckdb.connect` calls will create a new connection to the same database, sharing the catalogs (views, tables, macros etc.).

Using `:memory:` without a name will always create a new and separate database instance.

### Default Connection

The `duckdb` module has a default connection to an unnamed **in-memory database**.
Functions such as `duckdb.sql()` and `duckdb.execute()` use the default connection; the first function that needs it creates it. Some module functions differ from connection methods; see [Connection Object and Module]({% link docs/2.0/clients/python/overview.md %}#connection-object-and-module).

The special value `:default:` and the `duckdb.default_connection()` function return the default connection:

```python
import duckdb

duckdb.execute("CREATE TABLE tbl AS SELECT 42 AS a")
con = duckdb.connect(":default:")
con.sql("SELECT * FROM tbl")
# or
duckdb.default_connection().sql("SELECT * FROM tbl")
```

```text
┌───────┐
│   a   │
│ int32 │
├───────┤
│    42 │
└───────┘
```

To make another connection the default connection, pass it to `duckdb.set_default_connection()`:

```python
import duckdb

con = duckdb.connect()
con.execute("CREATE TABLE answer AS SELECT 42 AS a")
duckdb.set_default_connection(con)
duckdb.sql("SELECT * FROM answer").fetchall()
```

```text
[(42,)]
```

### File-Based Connection

If the `database` is a file path, a connection to a persistent database is established.
If the file does not exist the file will be created (the extension of the file is irrelevant and can be `.db`, `.duckdb` or anything else).

#### `read_only` Connections

If you would like to connect in read-only mode, you can set the `read_only` flag to `True`. If the file does not exist, it is **not** created when connecting in read-only mode.
Read-only mode is required if multiple Python processes want to access the same database file at the same time.

Within one Python process, all connections to a database file must use the same configuration, `read_only` included.

```python
import duckdb

# to start an in-memory database
con = duckdb.connect(database=":memory:")
# to use a database file (not shared between processes)
con = duckdb.connect(database="my-db.duckdb", read_only=False)
con.close()
# to use a database file (shared between processes)
con = duckdb.connect(database="my-db.duckdb", read_only=True)
con.close()
# to explicitly get the default connection
con = duckdb.connect(database=":default:")
```

You can open another connection to the same database with the `cursor()` method. A cursor has its own transaction and its own session settings, and cursors can run queries at the same time. A single connection runs one call at a time: a call from another thread while it is busy raises a `ResourceInUseException` instead of waiting, so give each thread its own cursor. Closing a connection closes its cursors. See [About `cursor()`]({% link docs/2.0/clients/python/overview.md %}#about-cursor) for details.

Connections are closed implicitly when they go out of scope or if they are explicitly closed using `close()`. Once the last connection to a database instance is closed, the database instance is closed as well.

## Querying

SQL queries can be sent to DuckDB using the `execute()` method of connections. Once a query has been executed, results can be retrieved using the `fetchone`, `fetchmany` and `fetchall` methods on the connection. `fetchone()` returns the next row, or `None` when no rows are left. `fetchmany(size)` returns a list of at most `size` rows, one by default. `fetchall()` returns all remaining rows. `df()` and `fetchnumpy()` return the remaining rows as a pandas DataFrame or as NumPy arrays. Below are some short examples:

```python
import duckdb

con = duckdb.connect()
# create a table
con.execute("CREATE TABLE items (item VARCHAR, value DECIMAL(10, 2), count INTEGER)")
# insert two items into the table
con.execute("INSERT INTO items VALUES ('jeans', 20.0, 1), ('hammer', 42.2, 2)")
print(con.rowcount)

# retrieve the items again
con.execute("SELECT * FROM items")
print(con.fetchall())

# retrieve the items one at a time
con.execute("SELECT * FROM items")
print(con.fetchone())
print(con.fetchmany(5))
print(con.fetchone())
```

```text
2
[('jeans', Decimal('20.00'), 1), ('hammer', Decimal('42.20'), 2)]
('jeans', Decimal('20.00'), 1)
[('hammer', Decimal('42.20'), 2)]
None
```

The `description` property of the connection object contains the column names as per the standard. The `rowcount` property holds the number of rows that the last `INSERT`, `UPDATE` or `DELETE` changed, counted over all parameter sets of an `executemany()` call. It is `-1` after a query and after a statement with a `RETURNING` clause.

### Query Parameters

Pass parameter values as the second argument to `execute()`. Use `?` with a list in placeholder order, `$1` to reuse a list value or `$name` with a dictionary. Pass values separately from the SQL text. The query then runs as a [prepared statement]({% link docs/2.0/sql/query_syntax/prepared_statements.md %}), and the values are converted according to the [conversion rules]({% link docs/2.0/clients/python/conversion.md %}#object-conversion-python-object-to-duckdb).

```python
rows = con.execute(
    "SELECT item FROM items WHERE value > $minimum",
    {"minimum": 40},
).fetchall()
print(rows)
```

```text
[('hammer',)]
```

Parameter names are not case sensitive: the key `"ABC"` binds `$abc`, so do not pass two keys that differ only in case.

Insert a row with `?` placeholders, and several rows with `executemany()`, which runs the statement once for each list of values:

```python
con.execute("INSERT INTO items VALUES (?, ?, ?)", ["laptop", 2000, 1])
con.executemany("INSERT INTO items VALUES (?, ?, ?)", [["chainsaw", 500, 10], ["iphone", 300, 2]])
```

```python
con.execute("SELECT item FROM items WHERE value > ?", [400])
print(con.fetchall())
```

```text
[('laptop',), ('chainsaw',)]
```

`$1` stands for the first value of the list, so a value can appear more than once:

```python
con.execute("SELECT $1, $1, $2", ["duck", "goose"])
print(con.fetchall())
```

```text
[('duck', 'duck', 'goose')]
```

> Warning Do *not* use `executemany` to insert large amounts of data into DuckDB. For rows that Python code produces, use the [appender]({% link docs/2.0/clients/python/appender.md %}); see the [data ingestion page]({% link docs/2.0/clients/python/data_ingestion.md %}) for other options.

### Open Results

`execute()` starts the statement and returns the connection. A query runs until its first rows are ready, so an error up to that point raises from `execute()`, and an error further into the query raises from the fetch that reaches it. Any other statement, `INSERT ... RETURNING` included, runs to its end inside `execute()`.

The result of a query stays open until a fetch returns no rows, or until `fetchall()`, `df()` or `fetchnumpy()` reads the rest of it. After a partial read with `fetchone()` or `fetchmany()`, these methods return the rows not fetched yet. `con.complete()` runs an open result to its end without reading its rows, and `con.abort()` cancels it, which fails an open transaction when the statement may write. Both are also functions of the `duckdb` module. The next `execute()` replaces an open result. If the replaced result may have side effects then it runs to its end first.

While a result is open, everything that runs a query on the connection raises an error, including reading a relation, `register()` and `create_function()`. Building a relation, the `description` property and `cursor()` still work, so a cursor can run other queries in the meantime.

```python
con.execute("SELECT * FROM items")
con.sql("SELECT 42").fetchall()
```

```console
_duckdb.ResourceInUseException: Resource In Use Error: connection has an unfinished result from execute(); call complete() or abort(), or fetch until a fetch returns no rows, before other work on this connection, or use a separate connection from cursor()
```

```python
con.complete()
con.sql("SELECT 42").fetchall()
```

```text
[(42,)]
```

### Arrow and Polars Output

A result of `execute()` has no `fetch_arrow_table()`, `fetch_record_batch()`, `arrow()` or `pl()` method. Its `to_arrow_table()` and `to_arrow_reader()` methods copy the rows and emit a `UserWarning`, and that reader does not stream: its first batch arrives after the whole query ran. For Arrow and Polars output, use a [relation]({% link docs/2.0/clients/python/relational_api.md %}) instead: `con.sql(query).to_arrow_table()`, `con.sql(query).pl()` or `con.sql(query).to_arrow_reader()`, which streams.

### Transactions

`con.begin()`, `con.commit()` and `con.rollback()` start, commit and roll back a transaction, as the [`BEGIN`, `COMMIT` and `ROLLBACK` statements]({% link docs/2.0/sql/statements/transactions.md %}) do. Inside a transaction, any statement run with `execute()` that fails aborts the transaction, including one with a syntax error or one that names a missing table. After that, `commit()` rolls the transaction back without raising an error, and any other statement raises a `TransactionException` until you roll back:

```python
con.begin()
con.execute("INSERT INTO items VALUES ('drill', 80, 1)")
try:
    con.execute("SELECT * FROM missing_table")
except duckdb.CatalogException:
    pass
con.execute("SELECT count(*) FROM items")
```

```console
_duckdb.TransactionException: TransactionContext Error: Current transaction is aborted (please ROLLBACK)
```

```python
con.rollback()
con.execute("SELECT count(*) FROM items").fetchall()
```

```text
[(5,)]
```
