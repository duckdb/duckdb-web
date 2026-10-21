---
github_repository: https://github.com/duckdb/duckdb-python
layout: docu
redirect_from:
- /docs/api/python
- /docs/api/python/overview
- /docs/clients/python/overview
- /docs/stable/clients/python/overview
- /docs/current/clients/python/overview
- /docs/lts/clients/python/overview
- /docs/preview/clients/python/overview
title: Python API
---

> Installation To use the DuckDB Python client, visit the [Python installation page]({% link install/index.html %}?environment=python).
>
> The latest stable version of the DuckDB Python client is {{ site.current_duckdb_version }}.

## Installation

The DuckDB Python API can be installed using [pip](https://pip.pypa.io): `pip install duckdb`. Please see the [installation page]({% link install/index.html %}?environment=python) for details. It is also possible to install DuckDB using [conda](https://docs.conda.io): `conda install python-duckdb -c conda-forge`.

**Python version:**
DuckDB requires Python 3.11 or newer. Free-threaded builds of CPython are not supported.

If you are upgrading from DuckDB 1.x, see [Migrating Python Code to DuckDB 2.0]({% link docs/2.0/clients/python/migration.md %}).

## Basic API Usage

The most straight-forward manner of running SQL queries using DuckDB is using the `duckdb.sql` command.

```python
import duckdb

duckdb.sql("SELECT 42").show()
```

This runs the query on an **in-memory database** that is stored globally inside the Python module. The first call that needs this database creates it.

`duckdb.sql()` returns a **relation**: an object you can query further or convert to Python data. A query that only reads data runs when you fetch or display its result. Reading it again runs the query again. Use `duckdb.execute()` for statements such as `CREATE TABLE` and `INSERT`. See [Lazy Evaluation]({% link docs/2.0/clients/python/relational_api.md %}#lazy-evaluation) for details.

Relations can be referenced in subsequent queries by storing them inside variables, and using them as tables. This way queries can be constructed incrementally.

```python
import duckdb

r1 = duckdb.sql("SELECT 42 AS i")
duckdb.sql("SELECT i * 2 AS k FROM r1").show()
```

## Data Input

DuckDB can ingest data from a wide variety of formats – both on-disk and in-memory. See the [data ingestion page]({% link docs/2.0/clients/python/data_ingestion.md %}) for more information.

```python
import duckdb

duckdb.read_csv("example.csv")                # read a CSV file into a Relation
duckdb.read_parquet("example.parquet")        # read a Parquet file into a Relation
duckdb.read_json("example.json")              # read a JSON file into a Relation

duckdb.sql("SELECT * FROM 'example.csv'")     # directly query a CSV file
duckdb.sql("SELECT * FROM 'example.parquet'") # directly query a Parquet file
duckdb.sql("SELECT * FROM 'example.json'")    # directly query a JSON file
```

### DataFrames

DuckDB can directly query Pandas DataFrames, Polars DataFrames and Arrow tables.
Note that these are read-only, i.e., editing these tables via [`INSERT`]({% link docs/2.0/sql/statements/insert.md %}) or [`UPDATE` statements]({% link docs/2.0/sql/statements/update.md %}) is not possible.

#### Pandas

To directly query a Pandas DataFrame, run:

```python
import duckdb
import pandas as pd

pandas_df = pd.DataFrame({"a": [42]})
duckdb.sql("SELECT * FROM pandas_df")
```

```text
┌───────┐
│   a   │
│ int64 │
├───────┤
│    42 │
└───────┘
```

#### Polars

To directly query a Polars DataFrame, run:

```python
import duckdb
import polars as pl

polars_df = pl.DataFrame({"a": [42]})
duckdb.sql("SELECT * FROM polars_df")
```

```text
┌───────┐
│   a   │
│ int64 │
├───────┤
│    42 │
└───────┘
```

#### PyArrow

To directly query a PyArrow table, run:

```python
import duckdb
import pyarrow as pa

arrow_table = pa.Table.from_pydict({"a": [42]})
duckdb.sql("SELECT * FROM arrow_table")
```

```text
┌───────┐
│   a   │
│ int64 │
├───────┤
│    42 │
└───────┘
```

## Result Conversion

DuckDB supports converting query results efficiently to a variety of formats. See the [result conversion page]({% link docs/2.0/clients/python/conversion.md %}) for more information.

```python
import duckdb

duckdb.sql("SELECT 42").fetchall()        # Python objects
duckdb.sql("SELECT 42").df()              # Pandas DataFrame
duckdb.sql("SELECT 42").pl()              # Polars DataFrame
duckdb.sql("SELECT 42").to_arrow_table()  # Arrow Table
duckdb.sql("SELECT 42").to_arrow_reader() # Arrow RecordBatchReader
duckdb.sql("SELECT 42").fetchnumpy()      # NumPy Arrays
```

## Writing Data to Disk

DuckDB supports writing Relation objects directly to disk in a variety of formats. The [`COPY` statement]({% link docs/2.0/sql/statements/copy.md %}) can be used to write data to disk using SQL as an alternative.

```python
import duckdb

duckdb.sql("SELECT 42").write_parquet("out.parquet")  # Write to a Parquet file
duckdb.sql("SELECT 42").write_csv("out.csv")          # Write to a CSV file
duckdb.execute("COPY (SELECT 42) TO 'out.parquet'")   # Copy to a Parquet file
```

## Connection Options

Applications can open a new DuckDB connection via the `duckdb.connect()` method.

### Using an In-Memory Database

When using DuckDB through `duckdb.sql()`, it operates on an **in-memory** database, i.e., no tables are persisted on disk.
Invoking the `duckdb.connect()` method without arguments returns a connection, which also uses an in-memory database:

```python
import duckdb

con = duckdb.connect()
con.sql("SELECT 42 AS x").show()
```

### Persistent Storage

The `duckdb.connect(dbname)` creates a connection to a **persistent** database.
Any data written to that connection will be persisted, and can be reloaded by reconnecting to the same file, both from Python and from other DuckDB clients.

```python
import duckdb

# create a connection to a file called 'file.db'
con = duckdb.connect("file.db")
# create a table and load data into it
con.execute("CREATE TABLE test (i INTEGER)")
con.execute("INSERT INTO test VALUES (42)")
# query the table
con.table("test").show()
# explicitly close the connection
con.close()
# Note: connections also closed implicitly when they go out of scope
```

When you reconnect with a context manager, the connection is closed at the end of the `with` block:

```python
import duckdb

with duckdb.connect("file.db") as con:
    con.execute("INSERT INTO test VALUES (43)")
    con.table("test").show()
    # the context manager closes the connection automatically
```

### Configuration

The `duckdb.connect()` method takes three arguments: `database`, `read_only` and `config`. Settings go into the `config` dictionary, where [configuration options]({% link docs/2.0/configuration/overview.md %}#configuration-reference) can be specified. For example:

```python
import duckdb

con = duckdb.connect(config={"threads": 1})
```

Besides its worker threads, each database starts a pool of [asynchronous I/O threads]({% link docs/2.0/data/io.md %}#thread-pools): by default four times the number of CPU cores, at most 256. To start fewer, set `async_threads`:

```python
con = duckdb.connect(config={"threads": 4, "async_threads": 4})
```

To specify the [storage version]({% link docs/2.0/internals/storage.md %}), pass the `storage_compatibility_version` option. DuckDB 1.5 cannot open a database file that DuckDB 2.0 wrote in its default format. To keep a file readable by DuckDB 1.5, write it with `v1.5.0`:

```python
con = duckdb.connect("compatible.db", config={"storage_compatibility_version": "v1.5.0"})
```

### Connection Object and Module

Nearly every method of a connection object is also a function of the `duckdb` module, which runs it on a global in-memory database. A few differ: `duckdb.df(frame)` builds a relation from a DataFrame, as `con.from_df(frame)` does, while `con.df()` fetches the result of `execute()`; `duckdb.arrow(obj)` builds a relation from an Arrow object; and `description` and `rowcount` are functions of the module but properties of a connection.

> If you are developing a package designed for others to use, and use DuckDB in the package, it is recommended that you create connection objects instead of using the methods on the `duckdb` module. That is because the `duckdb` module uses a shared global database, which can cause hard to debug issues if used from within multiple different packages.

### Using Connections in Parallel Python Programs

A connection runs one call at a time. A call from another thread while the connection is busy does not wait: it raises a `ResourceInUseException` saying `connection is busy with another call; it refuses instead of waiting, so use a separate connection from cursor()`.

`duckdb.sql()`, the other functions of the `duckdb` module and `duckdb.connect(":default:")` all use one shared default connection, so the same holds for them. To run queries in parallel, give each thread its own cursor:

```python
import threading

import duckdb

con = duckdb.connect()
con.execute("CREATE TABLE numbers AS SELECT range AS n FROM range(1000)")


def count_even(cursor, results):
    results.append(cursor.sql("SELECT count(*) FROM numbers WHERE n % 2 = 0").fetchall())


results = []
threads = [threading.Thread(target=count_even, args=(con.cursor(), results)) for _ in range(4)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
print(results)
```

```text
[[(500,)], [(500,)], [(500,)], [(500,)]]
```

#### About `cursor()`

The [`DuckDBPyConnection.cursor()` method]({% link docs/2.0/clients/python/reference/index.md %}#duckdb.DuckDBPyConnection.cursor) opens a new connection to the same database. A cursor has its own transaction and its own session settings, such as `search_path`, so cursors can run queries in parallel. A global setting, such as `threads` or `memory_limit`, applies to the whole database, also when a cursor sets it. Closing a connection closes its cursors.

Code that runs inside a query, such as a [Python function]({% link docs/2.0/clients/python/function.md %}) called from SQL, cannot use the connection that runs the query: the call raises an error saying `code running inside a query cannot use that query's connection; use a separate connection from cursor()`. Let the function use a cursor instead.

## Loading and Installing Extensions

The `install_extension()` and `load_extension()` methods install and load an [extension]({% link docs/2.0/extensions/overview.md %}), as the `INSTALL` and `LOAD` statements do. Many core extensions are [installed and loaded automatically]({% link docs/2.0/extensions/overview.md %}#autoloading-extensions) when a query uses them.

### Community Extensions

To load [community extensions]({% link community_extensions/index.md %}), use the `repository="community"` argument with the `install_extension` method.

For example, install and load the `h3` community extension as follows:

```python
import duckdb

con = duckdb.connect()
con.install_extension("h3", repository="community")
con.load_extension("h3")
```

### Unsigned Extensions

To load [unsigned extensions]({% link docs/2.0/extensions/extension_distribution.md %}#unsigned-extensions), use:

```python
con = duckdb.connect(config={"allow_unsigned_extensions": "true"})
```

> Warning Only load unsigned extensions from sources you trust.
> Avoid loading unsigned extensions over HTTP.
> Consult the [Securing DuckDB page]({% link docs/2.0/operations_manual/securing_duckdb/securing_extensions.md %}) for guidelines on how to set up DuckDB in a secure manner.
