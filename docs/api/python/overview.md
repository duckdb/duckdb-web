---
layout: docu
title: Python API
redirect_from:
  - /docs/api/python
  - /docs/api/python/
---

## Installation

The DuckDB Python API can be installed using [pip](https://pip.pypa.io): `pip install duckdb`. Please see the [installation page]({% link docs/installation/index.html %}?environment=python) for details. It is also possible to install DuckDB using [conda](https://docs.conda.io): `conda install python-duckdb -c conda-forge`.

**Python version:**
DuckDB requires Python 3.7 or newer.

## Basic API Usage

The most straight-forward manner of running SQL queries using DuckDB is using the `duckdb.sql` command.

```python
import duckdb
duckdb.sql("SELECT 42").show()
```

This will run queries using an **in-memory database** that is stored globally inside the Python module. The result of the query is returned as a **Relation**. A relation is a symbolic representation of the query. The query is not executed until the result is fetched or requested to be printed to the screen.

Relations can be referenced in subsequent queries by storing them inside variables, and using them as tables. This way queries can be constructed incrementally.

```python
import duckdb
r1 = duckdb.sql("SELECT 42 AS i")
duckdb.sql("SELECT i * 2 AS k FROM r1").show()
```

## Data Input

DuckDB can ingest data from a wide variety of formats – both on-disk and in-memory. See the [data ingestion page]({% link docs/api/python/data_ingestion.md %}) for more information.

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
Note that these are read-only, i.e., editing these tables via [`INSERT`]({% link docs/sql/statements/insert.md %}) or [`UPDATE` statements]({% link docs/sql/statements/update.md %}) is not possible.

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

DuckDB supports converting query results efficiently to a variety of formats. See the [result conversion page]({% link docs/api/python/conversion.md %}) for more information.

```python
import duckdb
duckdb.sql("SELECT 42").fetchall()   # Python objects
duckdb.sql("SELECT 42").df()         # Pandas DataFrame
duckdb.sql("SELECT 42").pl()         # Polars DataFrame
duckdb.sql("SELECT 42").arrow()      # Arrow Table
duckdb.sql("SELECT 42").fetchnumpy() # NumPy Arrays
```

## Writing Data to Disk

DuckDB supports writing Relation objects directly to disk in a variety of formats. The [`COPY`]({% link docs/sql/statements/copy.md %}) statement can be used to write data to disk using SQL as an alternative.

```python
import duckdb
duckdb.sql("SELECT 42").write_parquet("out.parquet") # Write to a Parquet file
duckdb.sql("SELECT 42").write_csv("out.csv")         # Write to a CSV file
duckdb.sql("COPY (SELECT 42) TO 'out.parquet'")      # Copy to a Parquet file
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
con.sql("CREATE TABLE test (i INTEGER)")
con.sql("INSERT INTO test VALUES (42)")
# query the table
con.table("test").show()
# explicitly close the connection
con.close()
# Note: connections also closed implicitly when they go out of scope
```

You can also use a context manager to ensure that the connection is closed:

```python
import duckdb

with duckdb.connect("file.db") as con:
    con.sql("CREATE TABLE test (i INTEGER)")
    con.sql("INSERT INTO test VALUES (42)")
    con.table("test").show()
    # the context manager closes the connection automatically
```

### Configuration

The `duckdb.connect()` accepts a `config` dictionary, where [configuration options]({% link docs/configuration/overview.md %}#configuration-reference) can be specified. For example:

```python
import duckdb

con = duckdb.connect(config = {'threads': 1})
```

### Connection Object and Module

The connection object and the `duckdb` module can be used interchangeably – they support the same methods. The only difference is that when using the `duckdb` module a global in-memory database is used.

> If you are developing a package designed for others to use, and use DuckDB in the package, it is recommend that you create connection objects instead of using the methods on the `duckdb` module. That is because the `duckdb` module uses a shared global database – which can cause hard to debug issues if used from within multiple different packages.

### Using Connections in Parallel Python Programs

The `DuckDBPyConnection` object is not thread-safe. If you would like to write to the same database from multiple threads, create a cursor for each thread with the [`DuckDBPyConnection.cursor()` method]({% link docs/api/python/reference/index.md %}#duckdb.DuckDBPyConnection.cursor).

## Loading and Installing Extensions

DuckDB's Python API provides functions for installing and loading [extensions]({% link docs/extensions/overview.md %}), which perform the equivalent operations to running the `INSTALL` and `LOAD` SQL commands, respectively. An example that installs and loads the [`spatial` extension]({% link docs/extensions/spatial.md %}) looks like follows:

```python
import duckdb

con = duckdb.connect()
con.install_extension("spatial")
con.load_extension("spatial")
```

To load [unsigned extensions]({% link docs/extensions/overview.md %}#unsigned-extensions), use the `config = {"allow_unsigned_extensions": "true"}` argument to the `duckdb.connect()` method.
