---
layout: docu
title: Export to Apache Arrow
---

All results of a query can be exported to an [Apache Arrow Table](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html) using the `arrow_table` function. Alternatively, results can be returned as a [RecordBatchReader](https://arrow.apache.org/docs/python/generated/pyarrow.ipc.RecordBatchStreamReader.html) using the `arrow_reader` function and results can be read one batch at a time. In addition, relations built using DuckDB's [Relational API]({% link docs/stable/guides/python/relational_api_pandas.md %}) can also be exported.

> Deprecated The `fetch_arrow_table`, `to_arrow_table`, `arrow` (for fetching results), `fetch_record_batch`, and `fetch_arrow_reader` functions are deprecated. Use `arrow_table` and `arrow_reader` instead.

## Export to an Arrow Table

```python
import duckdb
import pyarrow as pa

my_arrow_table = pa.Table.from_pydict({'i': [1, 2, 3, 4],
                                       'j': ["one", "two", "three", "four"]})

# query the Apache Arrow Table "my_arrow_table" and return as an Arrow Table
results = duckdb.sql("SELECT * FROM my_arrow_table").arrow_table()
```

## Export as a RecordBatchReader

```python
import duckdb
import pyarrow as pa

my_arrow_table = pa.Table.from_pydict({'i': [1, 2, 3, 4],
                                       'j': ["one", "two", "three", "four"]})

# query the Apache Arrow Table "my_arrow_table" and return as an Arrow RecordBatchReader
chunk_size = 1_000_000
result = duckdb.sql("SELECT * FROM my_arrow_table").arrow_reader(chunk_size)

# Loop through the results. A StopIteration exception is thrown when the RecordBatchReader is empty
while (batch := result.read_next_batch()):
    # Process a single chunk here
    print(batch.to_pandas())
```

## Export from Relational API

Arrow objects can also be exported from the Relational API. A relation can be converted to an Arrow table using `DuckDBPyRelation.arrow_table`, and to an Arrow record batch reader using `DuckDBPyRelation.arrow_reader`.

```python
import duckdb

# connect to an in-memory database
con = duckdb.connect()

con.execute('CREATE TABLE integers (i integer)')
con.execute('INSERT INTO integers VALUES (0), (1), (2), (3), (4), (5), (6), (7), (8), (9), (NULL)')

# Create a relation from the table and export the entire relation as Arrow
rel = con.table("integers")
relation_as_arrow = rel.arrow_table()

# Calculate a result using that relation and export that result to Arrow
res = rel.aggregate("sum(i)").execute()
arrow_table = res.arrow_table()

# You can also create an Arrow record batch reader from a relation
arrow_batch_reader = res.arrow_reader()
while (batch := arrow_batch_reader.read_next_batch()):
    # Process a single chunk here
    print(batch.to_pandas())
```
