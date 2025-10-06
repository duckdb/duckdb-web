---
layout: docu
title: Export to Apache Arrow
---

All results of a query can be exported to an [Apache Arrow Table](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html) using the `arrow` function. Alternatively, results can be returned as a [RecordBatchReader](https://arrow.apache.org/docs/python/generated/pyarrow.ipc.RecordBatchStreamReader.html) using the `fetch_record_batch` function and results can be read one batch at a time. In addition, relations built using DuckDB's [Relational API]({% link docs/preview/guides/python/relational_api_pandas.md %}) can also be exported.

## Export to an Arrow Table

```python
import duckdb
import pyarrow as pa

my_arrow_table = pa.Table.from_pydict({'i': [1, 2, 3, 4],
                                       'j': ["one", "two", "three", "four"]})

# query the Apache Arrow Table "my_arrow_table" and return as an Arrow Table
results = duckdb.sql("SELECT * FROM my_arrow_table").fetch_arrow_table()
```

## Export as a RecordBatchReader

```python
import duckdb
import pyarrow as pa

my_arrow_table = pa.Table.from_pydict({'i': [1, 2, 3, 4],
                                       'j': ["one", "two", "three", "four"]})

# query the Apache Arrow Table "my_arrow_table" and return as an Arrow RecordBatchReader
chunk_size = 1_000_000
result = duckdb.sql("SELECT * FROM my_arrow_table").arrow(chunk_size)

# Loop through the results. A StopIteration exception is thrown when the RecordBatchReader is empty
while (batch := result.read_next_batch()):
    # Process a single chunk here
    print(batch.to_pandas())
```

## Export from Relational API

Arrow objects can also be exported from the Relational API. A relation can be converted to an Arrow table using either the `DuckDBPyRelation.fetch_arrow_table` or `DuckDBPyRelation.to_arrow_table` function, and to an Arrow record batch reader using either the `DuckDBPyRelation.arrow` or `DuckDBPyRelation.fetch_arrow_reader` function.

```python
import duckdb

# connect to an in-memory database
con = duckdb.connect()

con.execute('CREATE TABLE integers (i integer)')
con.execute('INSERT INTO integers VALUES (0), (1), (2), (3), (4), (5), (6), (7), (8), (9), (NULL)')

# Create a relation from the table and export the entire relation as Arrow
rel = con.table("integers")
relation_as_arrow = rel.to_arrow_table() # or .fetch_arrow_table()

# Calculate a result using that relation and export that result to Arrow
res = rel.aggregate("sum(i)").execute()
arrow_table = res.to_arrow_table() # or .fetch_arrow_table()

# You can also create an Arrow record batch reader from a relation
arrow_batch_reader = res.arrow() # or .fetch_arrow_reader()
while (batch := arrow_batch_reader.read_next_batch()):
    # Process a single chunk here
    print(batch.to_pandas())
```
