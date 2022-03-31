---
layout: docu
title: SQL on Apache Arrow
selected: SQL on Apache Arrow
---

# How to execute SQL on Apache Arrow
DuckDB can query multiple different types of Apache Arrow objects. 

## Apache Arrow Tables
Arrow Tables stored in local variables can be queried as if they are regular tables within DuckDB.

```py
import duckdb
import pyarrow as pa

# connect to an in-memory database
con = duckdb.connect()

my_arrow_table = pa.Table.from_pydict({'i':[1,2,3,4],
                                       'j':["one", "two", "three", "four"]})

# query the Apache Arrow Table "my_arrow_table" and return as an Arrow Table
results = con.execute("SELECT * FROM my_arrow_table").arrow()
```

## Apache Arrow Datasets
Datasets stored as variables can also be queried as if they were regular tables.
Datasets are useful to point towards directories of Parquet files to analyze large datasets.
DuckDB will push filters down into the dataset scan operation so that only the necessary data is pulled into memory.

```python
import tempfile
import pathlib
import pyarrow.parquet as pq
import pyarrow.dataset as ds

# create example parquet files and save in a folder
base_path = pathlib.Path(tempfile.gettempdir())
(base_path / "parquet_folder").mkdir(exist_ok=True)
pq.write_to_dataset(my_arrow_table, str(base_path / "parquet_folder"))

# link to parquet files using an Arrow Dataset
my_arrow_dataset = ds.dataset(str(base_path / 'parquet_folder/'))

# query the Apache Arrow Dataset "my_arrow_dataset" and return as an Arrow Table
results = con.execute("SELECT * FROM my_arrow_dataset").arrow()
```

