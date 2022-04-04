---
layout: docu
title: Export To Apache Arrow
selected: Export To Apache Arrow
---

# How to export data to Apache Arrow
All results of a query can be exported to an [Apache Arrow Table](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html) using the `arrow` function. Alternatively, results can be returned as a [RecordBatchReader](https://arrow.apache.org/docs/python/generated/pyarrow.ipc.RecordBatchStreamReader.html) using the `fetch_record_batch` function and results can be read one batch at a time.

## Export to an Arrow Table
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

## Export as a RecordBatchReader
```python
import duckdb
import pyarrow as pa

# connect to an in-memory database
con = duckdb.connect()

my_arrow_table = pa.Table.from_pydict({'i':[1,2,3,4],
                                       'j':["one", "two", "three", "four"]})
                                       
# query the Apache Arrow Table "my_arrow_table" and return as an Arrow RecordBatchReader
chunk_size = 1_000_000
results = con.execute("SELECT * FROM my_arrow_table").fetch_record_batch(chunk_size)

# Loop through the results. A StopIteration exception is thrown when the RecordBatchReader is empty
while True:
    try:
        # Process a single chunk here (just printing as an example)
        print(results.read_next_batch().to_pandas())
    except StopIteration:
        print('Already fetched all batches')
        break
```
