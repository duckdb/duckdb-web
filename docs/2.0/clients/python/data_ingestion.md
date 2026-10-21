---
layout: docu
redirect_from:
- /docs/api/python/data_ingestion
- /docs/clients/python/data_ingestion
- /docs/stable/clients/python/data_ingestion
- /docs/current/clients/python/data_ingestion
- /docs/lts/clients/python/data_ingestion
- /docs/preview/clients/python/data_ingestion
title: Data Ingestion
---

This page contains examples for data ingestion to Python using DuckDB. First, import the DuckDB package:

```python
import duckdb
```

Then, proceed with any of the following sections.

## CSV Files

CSV files can be read using the `read_csv` function, called either from within Python or directly from within SQL. By default, the `read_csv` function attempts to auto-detect the CSV settings by sampling from the provided file.

Read from a file using fully auto-detected settings:

```python
duckdb.read_csv("example.csv")
```

Read multiple CSV files from a folder:

```python
duckdb.read_csv("folder/*.csv")
```

Specify options on how the CSV is formatted internally:

```python
duckdb.read_csv("example.csv", header = False, sep = ",")
```

Override types of the first two columns:

```python
duckdb.read_csv("example.csv", dtype = ["int", "varchar"])
```

Directly read a CSV file from within SQL:

```python
duckdb.sql("SELECT * FROM 'example.csv'")
```

Call `read_csv` from within SQL:

```python
duckdb.sql("SELECT * FROM read_csv('example.csv')")
```

Add a `filename` column that holds the file each row was read from:

```python
duckdb.read_csv("example.csv", filename=True)
```

Read a file-like object, such as an `io.BytesIO` or an open file; this needs the `fsspec` package:

```python
import io

duckdb.read_csv(io.BytesIO(b"a,b\n1,2\n"))
```

See the [CSV Import]({% link docs/2.0/data/csv/overview.md %}) page for more information. To write a relation to a CSV file, use [`write_csv`]({% link docs/2.0/clients/python/relational_api.md %}#write_csv). If you pass `overwrite=False` then it refuses to replace a file that exists.

## Parquet Files

Parquet files can be read using the `read_parquet` function, called either from within Python or directly from within SQL.

Read from a single Parquet file:

```python
duckdb.read_parquet("example.parquet")
```

Read multiple Parquet files from a folder:

```python
duckdb.read_parquet("folder/*.parquet")
```

Read a Parquet file over [https]({% link docs/2.0/core_extensions/httpfs/overview.md %}):

```python
duckdb.read_parquet("https://some.url/some_file.parquet")
```

Read a list of Parquet files:

```python
duckdb.read_parquet(["file1.parquet", "file2.parquet", "file3.parquet"])
```

Directly read a Parquet file from within SQL:

```python
duckdb.sql("SELECT * FROM 'example.parquet'")
```

Call `read_parquet` from within SQL:

```python
duckdb.sql("SELECT * FROM read_parquet('example.parquet')")
```

See the [Parquet Loading]({% link docs/2.0/data/parquet/overview.md %}) page for more information. To write a relation to a Parquet file, use [`write_parquet`]({% link docs/2.0/clients/python/relational_api.md %}#write_parquet); with `overwrite=False`, it refuses to replace a file that exists.

## JSON Files

JSON files can be read using the `read_json` function, called either from within Python or directly from within SQL. By default, the `read_json` function will automatically detect if a file contains newline-delimited JSON or regular JSON, and will detect the schema of the objects stored within the JSON file.

Read from a single JSON file:

```python
duckdb.read_json("example.json")
```

Read multiple JSON files from a folder:

```python
duckdb.read_json("folder/*.json")
```

Directly read a JSON file from within SQL:

```python
duckdb.sql("SELECT * FROM 'example.json'")
```

Call `read_json` from within SQL:

```python
duckdb.sql("SELECT * FROM read_json('example.json')")
```

## Directly Accessing DataFrames and Arrow Objects

DuckDB can query a Pandas DataFrame by the name of its variable, as if it were a table:

```python
import duckdb
import pandas as pd

test_df = pd.DataFrame.from_dict({"i": [1, 2, 3, 4], "j": ["one", "two", "three", "four"]})
print(duckdb.sql("SELECT * FROM test_df").fetchall())
```

```text
[(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]
```

The same works for Pandas Series, Polars DataFrames, LazyFrames and Series, NumPy arrays, a `dict` of one-dimensional NumPy arrays, [relations]({% link docs/2.0/clients/python/relational_api.md %}) and Arrow objects.

The masked elements in a NumPy masked array are `NULL`. In a `dict` of arrays, names that differ only in case get a suffix, so the keys `a` and `A` become the columns `a` and `A_1`.

Use `register()` to give a DataFrame or Arrow object a SQL name. This also works for objects stored in a dictionary or class attribute.

```python
import duckdb
import pandas as pd

my_dictionary = {}
my_dictionary["test_df"] = pd.DataFrame.from_dict({"i": [1, 2, 3, 4], "j": ["one", "two", "three", "four"]})
duckdb.register("test_df_view", my_dictionary["test_df"])
print(duckdb.sql("SELECT * FROM test_df_view").fetchall())
```

```text
[(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]
```

You can also create a table in DuckDB from the contents of the DataFrame (or the view):

```python
# create a new table from the contents of a DataFrame
duckdb.execute("CREATE TABLE test_df_table AS SELECT * FROM test_df")
# insert into an existing table from the contents of the registered view
duckdb.execute("INSERT INTO test_df_table SELECT * FROM test_df_view")
```

A relation's [`create`]({% link docs/2.0/clients/python/relational_api.md %}#create) method also makes a table. A name with a catalog, such as `other_db.main.test_df_table`, creates the table in that attached database.

Only variables that are visible to Python code at the location of the `sql()` or `execute()` call can be queried by name. To also look in the functions that called it, set `python_scan_all_frames` to `true`.
Accessing these variables is made possible by [replacement scans]({% link docs/2.0/clients/c/replacement_scans.md %}). To disable replacement scans entirely, use:

```sql
SET python_enable_replacements = false;
```

The precedence of objects with the same name is as follows:

* Objects explicitly registered via `register()`
* Native DuckDB tables and views
* [Replacement scans]({% link docs/2.0/clients/c/replacement_scans.md %})

DuckDB supports querying multiple types of Apache Arrow objects including [tables](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html), record batches, arrays and chunked arrays, [datasets](https://arrow.apache.org/docs/python/generated/pyarrow.dataset.Dataset.html), [RecordBatchReaders](https://arrow.apache.org/docs/python/generated/pyarrow.RecordBatchReader.html) and [scanners](https://arrow.apache.org/docs/python/generated/pyarrow.dataset.Scanner.html). See the Python [guides]({% link docs/2.0/guides/overview.md %}#python-client) for more examples.

* The filters of a query are pushed into Arrow datasets and Polars LazyFrames. Tables, record batches, readers, scanners and Polars DataFrames are read whole, and the filter applies to what they return.
* A `RecordBatchReader` can be read once. A second scan raises `InvalidInputException: This RecordBatchReader has already been consumed and cannot be scanned again.` To scan its data more than once, read it into a table first, for example with `read_all()`.
* Arrow tables and Polars DataFrames are scanned on all threads, even when they hold a single chunk. A query that depends on the order of rows without an `ORDER BY`, such as one using `first()`, can return different rows between runs.

### Custom Arrow Objects

DuckDB can also consume any object that implements the [Arrow PyCapsule interface](https://arrow.apache.org/docs/format/CDataInterface/PyCapsuleInterface.html) through an `__arrow_c_stream__` method. Such objects can be queried directly through replacement scans and passed to `duckdb.from_arrow()`:

```python
import duckdb
import pyarrow as pa

class MyArrowStream:
    def __init__(self, table):
        self._table = table

    def __arrow_c_stream__(self, requested_schema=None):
        return self._table.__arrow_c_stream__(requested_schema)

obj = MyArrowStream(pa.table({"i": [1, 2, 3]}))
print(duckdb.sql("SELECT sum(i) AS s FROM obj").fetchall())
print(duckdb.from_arrow(obj).fetchall())
```

```text
[(6,)]
[(1,), (2,), (3,)]
```

### Pandas DataFrames – `object` Columns

`pandas.DataFrame` columns of an `object` dtype require some special care, since this stores values of arbitrary type.
To convert these columns to DuckDB, we first go through an analyze phase before converting the values.
In this analyze phase a sample of all the rows of the column are analyzed to determine the target type.
This sample size is by default set to 1000.
If the type picked during the analyze step is incorrect, this will result in `Invalid Input Error: Failed to cast value`, in which case you will need to increase the sample size.
The sample size can be changed by setting the `pandas_analyze_sample` config option.

```python
# example setting the sample size to 100k
duckdb.execute("SET GLOBAL pandas_analyze_sample = 100_000")
```

## Appending Rows

Use the [appender]({% link docs/2.0/clients/python/appender.md %}) to insert rows produced by Python. The `with` block writes the rows to the table when it finishes without an exception:

```python
duckdb.execute("CREATE TABLE people (id INTEGER, name VARCHAR)")
with duckdb.appender("people") as appender:
    appender.append_row(1, "Mark")
```
