---
layout: docu
title: Data Ingestion
---

This page contains examples for data ingestion to Python using DuckDB. First, import the DuckDB page:

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

See the [CSV Import]({% link docs/archive/1.1/data/csv/overview.md %}) page for more information.

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

Read a Parquet file over [https]({% link docs/archive/1.1/extensions/httpfs/overview.md %}):

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

See the [Parquet Loading]({% link docs/archive/1.1/data/parquet/overview.md %}) page for more information.

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
duckdb.sql("SELECT * FROM read_json_auto('example.json')")
```

## Directly Accessing DataFrames and Arrow Objects

DuckDB is automatically able to query certain Python variables by referring to their variable name (as if it was a table).
These types include the following: Pandas DataFrame, Polars DataFrame, Polars LazyFrame, NumPy arrays, [relations]({% link docs/archive/1.1/api/python/relational_api.md %}), and Arrow objects.

Only variables that are visible to Python code at the location of the `sql()` or `execute()` call can be used in this manner.
Accessing these variables is made possible by [replacement scans]({% link docs/archive/1.1/api/c/replacement_scans.md %}). To disable replacement scans entirely, use:

```sql
SET python_enable_replacements = false;
```

DuckDB supports querying multiple types of Apache Arrow objects including [tables](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html), [datasets](https://arrow.apache.org/docs/python/generated/pyarrow.dataset.Dataset.html), [RecordBatchReaders](https://arrow.apache.org/docs/python/generated/pyarrow.ipc.RecordBatchStreamReader.html), and [scanners](https://arrow.apache.org/docs/python/generated/pyarrow.dataset.Scanner.html). See the Python [guides]({% link docs/archive/1.1/guides/overview.md %}#python-client) for more examples.

```python
import duckdb
import pandas as pd

test_df = pd.DataFrame.from_dict({"i": [1, 2, 3, 4], "j": ["one", "two", "three", "four"]})
print(duckdb.sql("SELECT * FROM test_df").fetchall())
```

```text
[(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]
```

DuckDB also supports “registering” a DataFrame or Arrow object as a virtual table, comparable to a SQL `VIEW`. This is useful when querying a DataFrame/Arrow object that is stored in another way (as a class variable, or a value in a dictionary). Below is a Pandas example:

If your Pandas DataFrame is stored in another location, here is an example of manually registering it:

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

You can also create a persistent table in DuckDB from the contents of the DataFrame (or the view):

```python
# create a new table from the contents of a DataFrame
con.execute("CREATE TABLE test_df_table AS SELECT * FROM test_df")
# insert into an existing table from the contents of a DataFrame
con.execute("INSERT INTO test_df_table SELECT * FROM test_df")
```

### Pandas DataFrames – `object` Columns

`pandas.DataFrame` columns of an `object` dtype require some special care, since this stores values of arbitrary type.
To convert these columns to DuckDB, we first go through an analyze phase before converting the values.
In this analyze phase a sample of all the rows of the column are analyzed to determine the target type.
This sample size is by default set to 1000.
If the type picked during the analyze step is incorrect, this will result in a "Failed to cast value:" error, in which case you will need to increase the sample size.
The sample size can be changed by setting the `pandas_analyze_sample` config option.

```python
# example setting the sample size to 100k
duckdb.execute("SET GLOBAL pandas_analyze_sample = 100_000")
```

### Registering Objects

You can register Python objects as DuckDB tables using the [`DuckDBPyConnection.register()` function]({% link docs/archive/1.1/api/python/reference/index.md %}#duckdb.DuckDBPyConnection.register).

The precedence of objects with the same name is as follows:

* Objects explicitly registered via `DuckDBPyConnection.register()`
* Native DuckDB tables and views
* [Replacement scans]({% link docs/archive/1.1/api/c/replacement_scans.md %})