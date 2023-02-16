---
layout: docu
title: DuckDB with Polars
selected: DuckDB with Polars
---

[Polars](https://github.com/pola-rs/polars) is a DataFrames library built in Rust with bindings for Python and Node.js. It uses [Apache Arrow's columnar format](https://arrow.apache.org/docs/format/Columnar.html) as its memory model. 
Polars can output results as Apache Arrow ([which is often a zero-copy operation](https://pola-rs.github.io/polars/py-polars/html/reference/dataframe/api/polars.DataFrame.to_arrow.html)), and DuckDB can read those results directly. 
DuckDB can also rapidly [output results to Apache Arrow](/docs/guides/python/export_arrow), which can be easily converted to a Polars DataFrame. 
Due to the interoperability of Apache Arrow, workflows can alternate between DuckDB and Polars with ease! 

This example workflow is also available as a [Google Collab notebook](https://colab.research.google.com/drive/1gz8YaVdwtoibNzP3gbY4VTdIlv_e02y_?usp=sharing).

# Installation

```python
pip install duckdb
pip install -U 'polars[pyarrow]'
```


# Polars to DuckDB
To convert from Polars to DuckDB, first save Polars results into an Arrow table using the `to_arrow` function. Then include that Arrow Table in the `FROM` clause of a DuckDB query. This example was based on the Polars Readme.

As a note, Pandas is not required as a first step prior to using Polars, but was helpful for generating example data to reuse in the second example below. 

Import the libraries, create an example Pandas DataFrame, then convert to Polars.
```python
import duckdb
import polars as pl
import pandas as pd

df = pd.DataFrame(
    {
        "A": [1, 2, 3, 4, 5],
        "fruits": ["banana", "banana", "apple", "apple", "banana"],
        "B": [5, 4, 3, 2, 1],
        "cars": ["beetle", "audi", "beetle", "beetle", "beetle"],
    }
)

polars_df = pl.DataFrame(df)
```

Calculate a new Polars DataFrame and output it to a variable as an Apache Arrow table. 

```python
polars_to_arrow = (
    polars_df
    .sort("fruits")
    .select(
        [
            "fruits",
            "cars",
            pl.lit("fruits").alias("literal_string_fruits"),
            pl.col("B").filter(pl.col("cars") == "beetle").sum(),
            pl.col("A").filter(pl.col("B") > 2).sum().over("cars").alias("sum_A_by_cars"),     # groups by "cars"
            pl.col("A").sum().over("fruits").alias("sum_A_by_fruits"),                         # groups by "fruits"
            pl.col("A").reverse().over("fruits").alias("rev_A_by_fruits"),                     # groups by "fruits
            pl.col("A").sort_by("B").over("fruits").alias("sort_A_by_B_by_fruits"),            # groups by "fruits"
        ]
    )
    .to_arrow()
)
```

Then query the Apache Arrow table using DuckDB, and output the results as another Apache Arrow table for use in a subsequent DuckDB or Polars operation.

```python
output = duckdb.query("""
  SELECT 
    fruits,
    first(sum_A_by_fruits) as sum_A
  FROM polars_to_arrow
  GROUP BY ALL
  ORDER BY ALL
""").arrow()
```

# DuckDB to Polars
DuckDB can output results as Apache Arrow tables, which can be imported into Polars with the Polars DataFrame constructor.  The same approach could be used with Pandas DataFrames, but Arrow is a faster way to pass data between DuckDB and Polars.

This example reuses the original Pandas DataFrame created above as a starting point. As a note, Pandas is not required as a first step, but was only used to generate example data.

After the import statements and example DataFrame creation above, query the Pandas DataFrame using DuckDB and output the results as an Arrow table.

```python
duckdb_to_arrow = duckdb.query("""
  SELECT
    fruits,
    cars,
    'fruits' as literal_string_fruits,
    SUM(B) FILTER (cars = 'beetle') OVER () as B,
    SUM(A) FILTER (B > 2) OVER (PARTITION BY cars) as sum_A_by_cars,
    SUM(A) OVER (PARTITION BY fruits) as sum_A_by_fruits
  FROM df
  ORDER BY
    fruits,
    df.B
""").arrow()
```

Load the Apache Arrow table into Polars using the Polars DataFrame constructor.

```python
polars_df_2 = pl.DataFrame(duckdb_to_arrow)
```

Complete a calculation using Polars, then output the results as another Apache Arrow table for use in a subsequent DuckDB or Polars operation.
```python
output = (
    polars_df_2
    .groupby('fruits')
    .agg(
        pl.col('sum_A_by_fruits')
        .first()
        .sort_by('fruits')
        )
).to_arrow()
```

To learn more about Polars, feel free to explore their [Python API Reference](https://pola-rs.github.io/polars/py-polars/html/reference/index.html)! 
