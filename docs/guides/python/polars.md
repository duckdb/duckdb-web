---
layout: docu
title: DuckDB with Polars
selected: DuckDB with Polars
---

[Polars](https://github.com/pola-rs/polars) is a DataFrames library built in Rust with bindings for Python and Node.js. It uses [Apache Arrow's columnar format](https://arrow.apache.org/docs/format/Columnar.html) as its memory model. DuckDB can read Polars DataFrames and convert query results to Polars DataFrames. It does this internally using the efficient Apache Arrow integration. Note that the `pyarrow` library must be installed for the integration to work.

# Installation

```python
pip install duckdb
pip install -U 'polars[pyarrow]'
```

# Polars to DuckDB
DuckDB can natively query Polars DataFrames by referring to the name of Polars DataFrames as they exist in the current scope.

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
duckdb.sql('SELECT * FROM df').show()
```

# DuckDB to Polars
DuckDB can output results as Polars DataFrames using the `.pl()` result-conversion method.

```python
df = duckdb.sql("""
SELECT 1 AS id, 'banana' AS fruit
UNION ALL
SELECT 2, 'apple'
UNION ALL
SELECT 3, 'mango'""").pl()
print(df)
```

To learn more about Polars, feel free to explore their [Python API Reference](https://pola-rs.github.io/polars/py-polars/html/reference/index.html)! 
