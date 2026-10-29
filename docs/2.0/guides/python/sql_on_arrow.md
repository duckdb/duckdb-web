---
layout: docu
redirect_from:
- /docs/guides/python/sql_on_arrow
- /docs/stable/guides/python/sql_on_arrow
- /docs/current/guides/python/sql_on_arrow
- /docs/lts/guides/python/sql_on_arrow
- /docs/preview/guides/python/sql_on_arrow
title: SQL on Apache Arrow
how_to_topic: python
---

DuckDB can query multiple different types of Apache Arrow objects.

> DuckDB pushes the filters of a query that it can translate, such as comparisons, into the scan of an Arrow dataset. Arrow tables, record batches, scanners, and RecordBatchReaders are read in full and filtered afterwards. A RecordBatchReader can be scanned only once; to query its data more than once, read it into a table with `read_all()` before the first query. Arrow tables are scanned on all threads, so an aggregate that depends on row order, such as `first(i)` without `ORDER BY`, can return a different row on each run.

## Apache Arrow Tables

[Arrow Tables](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html) stored in local variables can be queried as if they are regular tables within DuckDB.

```python
import duckdb
import pyarrow as pa

# connect to an in-memory database
con = duckdb.connect()

my_arrow_table = pa.Table.from_pydict({'i': [1, 2, 3, 4],
                                       'j': ["one", "two", "three", "four"]})

# query the Apache Arrow Table "my_arrow_table" and return as an Arrow Table
results = con.sql("SELECT * FROM my_arrow_table WHERE i = 2").to_arrow_table()
```

## Apache Arrow Datasets

[Arrow Datasets](https://arrow.apache.org/docs/python/dataset.html) stored as variables can also be queried as if they were regular tables.
Datasets are useful to point towards directories of Parquet files to analyze large datasets.
DuckDB will push column selections and the row filters it can translate down into the dataset scan operation so that only the necessary data is pulled into memory.

```python
import duckdb
import pyarrow as pa
import tempfile
import pyarrow.parquet as pq
import pyarrow.dataset as ds

# connect to an in-memory database
con = duckdb.connect()

my_arrow_table = pa.Table.from_pydict({'i': [1, 2, 3, 4],
                                       'j': ["one", "two", "three", "four"]})

# create example Parquet files and save in a folder
parquet_folder = tempfile.mkdtemp()
pq.write_to_dataset(my_arrow_table, parquet_folder)

# link to Parquet files using an Arrow Dataset
my_arrow_dataset = ds.dataset(parquet_folder)

# query the Apache Arrow Dataset "my_arrow_dataset" and return as an Arrow Table
results = con.sql("SELECT * FROM my_arrow_dataset WHERE i = 2").to_arrow_table()
```

## Apache Arrow Scanners

[Arrow Scanners](https://arrow.apache.org/docs/python/generated/pyarrow.dataset.Scanner.html) stored as variables can also be queried as if they were regular tables. Scanners read over a dataset and select specific columns or apply row-wise filtering. This is similar to how DuckDB pushes column selections and filters down into an Arrow Dataset, but using Arrow compute operations instead. Arrow can use asynchronous IO to quickly access files.

```python
import duckdb
import pyarrow as pa
import tempfile
import pyarrow.parquet as pq
import pyarrow.dataset as ds
import pyarrow.compute as pc

# connect to an in-memory database
con = duckdb.connect()

my_arrow_table = pa.Table.from_pydict({'i': [1, 2, 3, 4],
                                       'j': ["one", "two", "three", "four"]})

# create example Parquet files and save in a folder
parquet_folder = tempfile.mkdtemp()
pq.write_to_dataset(my_arrow_table, parquet_folder)

# link to Parquet files using an Arrow Dataset
my_arrow_dataset = ds.dataset(parquet_folder)

# define the filter to be applied while scanning
# equivalent to "WHERE i = 2"
scanner_filter = (pc.field("i") == pc.scalar(2))

arrow_scanner = ds.Scanner.from_dataset(my_arrow_dataset, filter = scanner_filter)

# query the Apache Arrow scanner "arrow_scanner" and return as an Arrow Table
results = con.sql("SELECT * FROM arrow_scanner").to_arrow_table()
```

## Apache Arrow RecordBatchReaders

[Arrow RecordBatchReaders](https://arrow.apache.org/docs/python/generated/pyarrow.RecordBatchReader.html) are a reader for Arrow's streaming binary format and can also be queried directly as if they were tables. This streaming format is useful when sending Arrow data for tasks like interprocess communication or communicating between language runtimes.

```python
import duckdb
import pyarrow as pa

# connect to an in-memory database
con = duckdb.connect()

my_recordbatch = pa.RecordBatch.from_pydict({'i': [1, 2, 3, 4],
                                             'j': ["one", "two", "three", "four"]})

my_recordbatchreader = pa.ipc.RecordBatchReader.from_batches(my_recordbatch.schema, [my_recordbatch])

# query the Apache Arrow RecordBatchReader "my_recordbatchreader" and return as an Arrow Table
results = con.sql("SELECT * FROM my_recordbatchreader WHERE i = 2").to_arrow_table()
```
