---
layout: docu
title: SQL on Apache Arrow
selected: SQL on Apache Arrow
---

# How to execute SQL on Apache Arrow
DuckDB can query multiple different types of Apache Arrow objects. 

## Apache Arrow Tables
[Arrow Tables](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html) stored in local variables can be queried as if they are regular tables within DuckDB.

```py
import duckdb
import pyarrow as pa

# connect to an in-memory database
con = duckdb.connect()

my_arrow_table = pa.Table.from_pydict({'i':[1,2,3,4],
                                       'j':["one", "two", "three", "four"]})

# query the Apache Arrow Table "my_arrow_table" and return as an Arrow Table
results = con.execute("SELECT * FROM my_arrow_dataset WHERE i = 2").arrow()
```

## Apache Arrow Datasets
[Arrow Datasets](https://arrow.apache.org/docs/python/dataset.html) stored as variables can also be queried as if they were regular tables.
Datasets are useful to point towards directories of Parquet files to analyze large datasets.
DuckDB will push column selections and row filters down into the dataset scan operation so that only the necessary data is pulled into memory.

```python
import duckdb
import pyarrow as pa
import tempfile
import pathlib
import pyarrow.parquet as pq
import pyarrow.dataset as ds

# connect to an in-memory database
con = duckdb.connect()

my_arrow_table = pa.Table.from_pydict({'i':[1,2,3,4],
                                       'j':["one", "two", "three", "four"]})

# create example parquet files and save in a folder
base_path = pathlib.Path(tempfile.gettempdir())
(base_path / "parquet_folder").mkdir(exist_ok=True)
pq.write_to_dataset(my_arrow_table, str(base_path / "parquet_folder"))

# link to parquet files using an Arrow Dataset
my_arrow_dataset = ds.dataset(str(base_path / 'parquet_folder/'))

# query the Apache Arrow Dataset "my_arrow_dataset" and return as an Arrow Table
results = con.execute("SELECT * FROM my_arrow_dataset WHERE i = 2").arrow()
```

## Apache Arrow Scanners
[Arrow Scanners](https://arrow.apache.org/docs/python/generated/pyarrow.dataset.Scanner.html) stored as variables can also be queried as if they were regular tables. Scanners read over a dataset and select specific columns or apply row-wise filtering. This is similar to how DuckDB pushes column selections and filters down into an Arrow Dataset, but using Arrow compute operations instead. Arrow can use asynchronous IO to quickly access files.

```python
import duckdb
import pyarrow as pa
import tempfile
import pathlib
import pyarrow.parquet as pq
import pyarrow.dataset as ds
import pyarrow.compute as pc

# connect to an in-memory database
con = duckdb.connect()

my_arrow_table = pa.Table.from_pydict({'i':[1,2,3,4],
                                       'j':["one", "two", "three", "four"]})

# create example parquet files and save in a folder
base_path = pathlib.Path(tempfile.gettempdir())
(base_path / "parquet_folder").mkdir(exist_ok=True)
pq.write_to_dataset(my_arrow_table, str(base_path / "parquet_folder"))

# link to parquet files using an Arrow Dataset
my_arrow_dataset = ds.dataset(str(base_path / 'parquet_folder/'))

# define the filter to be applied while scanning
# equivalent to "WHERE i = 2"
scanner_filter = (pc.field("i") == pc.scalar(2))

arrow_scanner = ds.Scanner.from_dataset(my_arrow_dataset, filter=scanner_filter)

# query the Apache Arrow scanner "arrow_scanner" and return as an Arrow Table
results = con.execute("SELECT * FROM arrow_scanner").arrow()
```