---
layout: docu
redirect_from:
- /docs/guides/python/export_arrow
- /docs/stable/guides/python/export_arrow
- /docs/current/guides/python/export_arrow
- /docs/lts/guides/python/export_arrow
- /docs/preview/guides/python/export_arrow
title: Export to Apache Arrow
how_to_topic: python
---

All results of a query can be exported to an [Apache Arrow Table](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html) using the `to_arrow_table` function. Alternatively, results can be returned as a [RecordBatchReader](https://arrow.apache.org/docs/python/generated/pyarrow.RecordBatchReader.html) using the `to_arrow_reader` function and results can be read one batch at a time.

Call these functions on the relation that `duckdb.sql`, `con.sql`, or DuckDB's [Relational API]({% link docs/2.0/guides/python/relational_api_pandas.md %}) returns: its reader streams the result. On a `con.execute()` result they first copy all rows and warn with a `UserWarning`, and the reader does not stream. While a reader is partly read, other queries on its connection raise a `ResourceInUseException`. Read the reader to the end or close it first, or run the other queries on a cursor from `con.cursor()`.

> Deprecated On relations, `fetch_arrow_table`, `fetch_record_batch`, and `fetch_arrow_reader` are deprecated aliases of `to_arrow_table` and `to_arrow_reader`. Results of `con.execute()` and the `duckdb` module no longer have them.

## Export to an Arrow Table

```python
import duckdb
import pyarrow as pa

my_arrow_table = pa.Table.from_pydict({'i': [1, 2, 3, 4],
                                       'j': ["one", "two", "three", "four"]})

# query the Apache Arrow Table "my_arrow_table" and return as an Arrow Table
results = duckdb.sql("SELECT * FROM my_arrow_table").to_arrow_table()
```

## Export as a RecordBatchReader

```python
import duckdb

con = duckdb.connect()
rel = con.sql("SELECT i FROM range(5) AS t(i)")
with rel.to_arrow_reader(batch_size=2) as reader:
    for batch in reader:
        print(batch.to_pydict())
```

```text
{'i': [0, 1]}
{'i': [2, 3]}
{'i': [4]}
```

The small batch size makes the batches visible here. Omit it to use the default size.

## Export from Relational API

Arrow objects can also be exported from the Relational API. A relation can be converted to an Arrow table using `DuckDBPyRelation.to_arrow_table`, and to an Arrow record batch reader using `DuckDBPyRelation.to_arrow_reader`.

```python
import duckdb

# connect to an in-memory database
con = duckdb.connect()

con.execute('CREATE TABLE integers (i integer)')
con.execute('INSERT INTO integers VALUES (0), (1), (2), (3), (4), (5), (6), (7), (8), (9), (NULL)')

# Create a relation from the table and export the entire relation as Arrow
rel = con.table("integers")
relation_as_arrow = rel.to_arrow_table()

# Calculate a result using that relation and export that result to Arrow
res = rel.aggregate("sum(i)")
arrow_table = res.to_arrow_table()

# You can also create an Arrow record batch reader from a relation
arrow_batch_reader = res.to_arrow_reader()
for batch in arrow_batch_reader:
    # Process a single chunk here
    print(batch.to_pandas())
```

## Export through the Arrow PyCapsule Interface

A relation implements `__arrow_c_stream__` of the [Arrow PyCapsule interface](https://arrow.apache.org/docs/format/CDataInterface/PyCapsuleInterface.html), so libraries that accept an Arrow stream read it directly: `pyarrow.table(rel)`, `pyarrow.RecordBatchReader.from_stream(rel)`, and `polars.DataFrame(rel)`. Polars reads it this way even without `pyarrow` installed.

```python
import duckdb
import polars as pl
import pyarrow as pa

rel = duckdb.sql("SELECT i, 'v' || i AS s FROM range(3) AS t(i)")
print(pa.table(rel).to_pydict())
print(pl.DataFrame(rel))
```

```text
{'i': [0, 1, 2], 's': ['v0', 'v1', 'v2']}
shape: (3, 2)
┌─────┬─────┐
│ i   ┆ s   │
│ --- ┆ --- │
│ i64 ┆ str │
╞═════╪═════╡
│ 0   ┆ v0  │
│ 1   ┆ v1  │
│ 2   ┆ v2  │
└─────┴─────┘
```
