---
layout: docu
redirect_from:
- /docs/guides/python/polars
- /docs/stable/guides/python/polars
- /docs/current/guides/python/polars
- /docs/lts/guides/python/polars
- /docs/preview/guides/python/polars
title: Integration with Polars
how_to_topic: python
---

[Polars](https://github.com/pola-rs/polars) is a DataFrames library built in Rust with bindings for Python and Node.js. It uses [Apache Arrow's columnar format](https://arrow.apache.org/docs/format/Columnar.html) as its memory model. DuckDB can read Polars DataFrames and convert query results to Polars DataFrames. It does this internally using the efficient Apache Arrow integration. Note that the `pyarrow` library must be installed for the integration to work.

## Installation

```batch
pip install -U duckdb 'polars[pyarrow]'
```

## Polars to DuckDB

DuckDB can natively query Polars DataFrames and LazyFrames by referring to their names as they exist in the current scope. DuckDB pushes the column selections of a query, and the filters it can translate, into a LazyFrame, so Polars collects only the rows and columns the query needs. A DataFrame is converted in full and filtered afterwards.

```python
import duckdb
import polars as pl

df = pl.DataFrame(
    {
        "A": [1, 2, 3, 4, 5],
        "fruits": ["banana", "banana", "apple", "apple", "banana"],
        "B": [5, 4, 3, 2, 1],
        "cars": ["beetle", "audi", "beetle", "beetle", "beetle"],
    }
)
duckdb.sql("SELECT * FROM df").show()
```

## DuckDB to Polars

DuckDB can output results as Polars DataFrames using the `.pl()` method of a relation, the object that `duckdb.sql` and `con.sql` return. Results of `con.execute()` have no `.pl()` method.

```python
df = duckdb.sql("""
    SELECT 1 AS id, 'banana' AS fruit
    UNION ALL
    SELECT 2, 'apple'
    UNION ALL
    SELECT 3, 'mango'"""
).pl()
print(df)
```

```text
shape: (3, 2)
┌─────┬────────┐
│ id  ┆ fruit  │
│ --- ┆ ---    │
│ i32 ┆ str    │
╞═════╪════════╡
│ 1   ┆ banana │
│ 2   ┆ apple  │
│ 3   ┆ mango  │
└─────┴────────┘
```

The optional `lazy` parameter allows returning Polars LazyFrames.

```python
df = duckdb.sql("""
    SELECT 1 AS id, 'banana' AS fruit
    UNION ALL
    SELECT 2, 'apple'
    UNION ALL
    SELECT 3, 'mango'"""
).pl(lazy=True)
print(df)
```

```text
naive plan: (run LazyFrame.explain(optimized=True) to see the optimized plan)

PYTHON SCAN []
PROJECT */2 COLUMNS
```

A relation also implements the [Arrow PyCapsule interface]({% link docs/2.0/guides/python/export_arrow.md %}#export-through-the-arrow-pycapsule-interface), so `pl.DataFrame(rel)` reads it too, without `pyarrow` installed. `pl.from_arrow(rel)` returns a Series with one struct per row instead of a DataFrame.

To learn more about Polars, feel free to explore their [Python API Reference](https://docs.pola.rs/api/python/stable/reference/index.html).
