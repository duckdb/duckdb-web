---
layout: docu
title: Python API
selected: Client APIs
---
## Installation
The DuckDB Python API can be installed using [pip](https://pip.pypa.io): `pip install duckdb`. Please see the [installation page](../../installation?environment=python) for details. It is also possible to install DuckDB using [conda](https://docs.conda.io): `conda install python-duckdb -c conda-forge`.

## Basic API Usage
The most straight-forward manner of running SQL queries using DuckDB is using the `duckdb.sql` command.

```py
import duckdb
duckdb.sql('SELECT 42').show()
```

This will run queries using an **in-memory database** that is stored globally inside the Python module. The result of the query is returned as a **Relation**. A relation is a symbolic representation of the query. The query is not executed until the result is fetched or requested to be printed to the screen.

Relations can be referenced in subsequent queries by storing them inside variables, and using them as tables. This way queries can be constructed incrementally.

```py
import duckdb
r1 = duckdb.sql('SELECT 42 AS i')
duckdb.sql('SELECT i * 2 AS k FROM r1').show()
```

## Data Input
DuckDB can ingest data from a wide variety of formats - both on-disk and in-memory. See the [data ingestion page](data_ingestion) for more information.

```py
import duckdb
duckdb.read_csv('example.csv')                # read a CSV file into a Relation
duckdb.read_parquet('example.parquet')        # read a Parquet file into a Relation
duckdb.read_json('example.json')              # read a JSON file into a Relation

duckdb.sql('SELECT * FROM "example.csv"')     # directly query a CSV file
duckdb.sql('SELECT * FROM "example.parquet"') # directly query a Parquet file
duckdb.sql('SELECT * FROM "example.json"')    # directly query a JSON file
```

#### DataFrames
DuckDB can also directly query Pandas DataFrames, Polars DataFrames and Arrow tables. 

```py
import duckdb

# directly query a Pandas DataFrame
import pandas as pd
pandas_df = pd.DataFrame({'a': [42]})
duckdb.sql('SELECT * FROM pandas_df')

# directly query a Polars DataFrame
import polars as pl
polars_df = pl.DataFrame({'a': [42]})
duckdb.sql('SELECT * FROM polars_df')

# directly query a pyarrow table
import pyarrow as pa
arrow_table = pa.Table.from_pydict({'a':[42]})
duckdb.sql('SELECT * FROM arrow_table')
```

## Result Conversion
DuckDB supports converting query results efficiently to a variety of formats. See the [result conversion page](result_conversion) for more information.

```py
import duckdb
duckdb.sql('SELECT 42').fetchall()   # Python objects
duckdb.sql('SELECT 42').df()         # Pandas DataFrame
duckdb.sql('SELECT 42').pl()         # Polars DataFrame
duckdb.sql('SELECT 42').arrow()      # Arrow Table
duckdb.sql('SELECT 42').fetchnumpy() # NumPy Arrays
```

## Writing Data To Disk
DuckDB supports writing Relation objects directly to disk in a variety of formats.

```py
import duckdb
duckdb.sql('SELECT 42').write_parquet('out.parquet')   # Write to a Parquet file
duckdb.sql('SELECT 42').write_csv('out.csv')           # Write to a CSV file
```

## Persistent Storage
By default DuckDB operates on an **in-memory** database. That means that any tables that are created are not persisted to disk. Using the `.connect` method a connection can be made to a **persistent** database. Any data written to that connection will be persisted, and can be reloaded by re-connecting to the same file. 

```py
import duckdb

# create a connection to a file called 'file.db'
con = duckdb.connect('file.db')
# create a table and load data into it
con.sql('CREATE TABLE test(i INTEGER)')
con.sql('INSERT INTO test VALUES (42)')
# query the table
con.table('test').show()
```

The connection object and the `duckdb` module can be used interchangeably - they support the same methods. The only difference is that when using the `duckdb` module a global in-memory database is used.

Note that if you are developing a package designed for others to use using duckdb, it is recommend that you create connection objects instead of using the methods on the `duckdb` module. That is because the `duckdb` module uses a shared global database - which can cause hard to debug issues if used from within multiple different packages. 