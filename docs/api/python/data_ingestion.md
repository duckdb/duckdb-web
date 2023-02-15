---
layout: docu
title: Data Ingestion
selected: Client APIs
---

#### CSV Files
CSV files can be read using the `read_csv` function, called either from within Python or directly from within SQL. By default, the `read_csv` function attempts to auto-detect the CSV settings by sampling from the provided file. 

```py
import duckdb
# read from a file using fully auto-detected settings
duckdb.read_csv('example.csv')
# read multiple CSV files from a folder
duckdb.read_csv('folder/*.csv')
# specify options on how the CSV is formatted internally
duckdb.read_csv('example.csv', header=False, sep=',')
# override types of the first two columns
duckdb.read_csv('example.csv', dtype=['int', 'varchar'])
# use the (experimental) parallel CSV reader
duckdb.read_csv('example.csv', parallel=True)
# directly read a CSV file from within SQL
duckdb.sql("SELECT * FROM 'example.csv'")
# call read_csv from within SQL
duckdb.sql("SELECT * FROM read_csv_auto('example.csv')")
```

See the [CSV Loading](../../data/csv) page for more information.

#### Parquet Files
Parquet files can be read using the `read_parquet` function, called either from within Python or directly from within SQL.

```py
import duckdb
# read from a single Parquet file
duckdb.read_parquet('example.parquet')
# read multiple Parquet files from a folder
duckdb.read_parquet('folder/*.parquet')
# directly read a Parquet file from within SQL
duckdb.sql("SELECT * FROM 'example.parquet'")
# call read_parquet from within SQL
duckdb.sql("SELECT * FROM read_parquet('example.parquet')")
```

See the [Parquet Loading](../../data/parquet) page for more information.

#### JSON Files
JSON files can be read using the `read_json` function, called either from within Python or directly from within SQL. By default, the `read_json` function will automatically detect if a file contains newline-delimited JSON or regular JSON, and will detect the schema of the objects stored within the JSON file.

```py
import duckdb
# read from a single JSON file
duckdb.read_json('example.json')
# read multiple JSON files from a folder
duckdb.read_json('folder/*.json')
# directly read a JSON file from within SQL
duckdb.sql("SELECT * FROM 'example.json'")
# call read_json from within SQL
duckdb.sql("SELECT * FROM read_json_auto('example.json')")
```

#### DataFrames & Arrow Tables

DuckDB is automatically able to query a Pandas DataFrame, Polars DataFrame, or Arrow object that is stored in a Python variable by name. DuckDB supports querying multiple types of Apache Arrow objects including [tables](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html), [datasets](https://arrow.apache.org/docs/python/generated/pyarrow.dataset.Dataset.html), [RecordBatchReaders](https://arrow.apache.org/docs/python/generated/pyarrow.ipc.RecordBatchStreamReader.html), and [scanners](https://arrow.apache.org/docs/python/generated/pyarrow.dataset.Scanner.html). See the Python [guides](../../guides/index#python-client) for more examples.

```python
import duckdb
import pandas as pd
test_df = pd.DataFrame.from_dict({"i":[1, 2, 3, 4], "j":["one", "two", "three", "four"]})
duckdb.sql('SELECT * FROM test_df').fetchall()
# [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]
```

DuckDB also supports "registering" a DataFrame or Arrow object as a virtual table, comparable to a SQL `VIEW`. This is useful when querying a DataFrame/Arrow object that is stored in another way (as a class variable, or a value in a dictionary). Below is a Pandas example:

If your Pandas DataFrame is stored in another location, here is an example of manually registering it:
```python
import duckdb
import pandas as pd
my_dictionary = {}
my_dictionary['test_df'] = pd.DataFrame.from_dict({"i":[1, 2, 3, 4], "j":["one", "two", "three", "four"]})
duckdb.register('test_df_view', my_dictionary['test_df'])
duckdb.sql('SELECT * FROM test_df_view').fetchall()
# [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]
```

You can also create a persistent table in DuckDB from the contents of the DataFrame (or the view):

```python
# create a new table from the contents of a DataFrame
con.execute('CREATE TABLE test_df_table AS SELECT * FROM test_df')
# insert into an existing table from the contents of a DataFrame
con.execute('INSERT INTO test_df_table SELECT * FROM test_df')
```

##### Pandas DataFrames - 'object' columns

pandas.DataFrame columns of an `object` dtype require some special care, since this stores values of arbitrary type.

To convert these columns to DuckDB, we first go through an analyze phase before converting the values.

In this analyze phase a sample of all the rows of the column are analyzed to determine the target type.

This sample size is by default set to 1000.

If the type picked during the analyze step is wrong, this will result in a "Failed to cast value:" error, in which case you will need to increase the sample size.

The sample size can be changed by setting the `pandas_analyze_sample` config option.
```py
# example setting the sample size to 100000
duckdb.default_connection.execute("SET GLOBAL pandas_analyze_sample=100000")
```
