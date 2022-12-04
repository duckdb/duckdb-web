---
layout: docu
title: DuckDB with DataFusion
selected: DuckDB with DataFusion
---

[DataFusion](https://github.com/apache/arrow-datafusion-python/) is a DataFrame and SQL library built in Rust with bindings for Python. It uses [Apache Arrow's columnar format](https://arrow.apache.org/docs/format/Columnar.html) as its memory model.
DataFusion can output results as Apache Arrow, and DuckDB can read those results directly.
DuckDB can also rapidly [output results to Apache Arrow](/docs/guides/python/export_arrow), which can be easily converted to a DataFusion DataFrame.
Due to the interoperability of Apache Arrow, workflows can alternate between DuckDB and DataFusion with ease!

This example workflow is also available as a [Google Collab notebook](https://colab.research.google.com/drive/1CHe6suiu7ZdDXejqJF6OacdXbJYpJoKr?usp=sharing).

# Installation

```python
pip install --quiet duckdb
pip install --quiet datafusion
pip install --quiet pyarrow
```

# DataFusion to DuckDB
To convert from DataFusion to DuckDB, first save DataFusion results into Arrow batches using the `collect` function. Then include that Arrow Table in the `FROM` clause of a DuckDB query. This example was based on the DataFusion Readme.

As a note, Pandas is not required as a first step prior to using DataFusion, but was helpful for generating example data to reuse in the second example below.

Import the libraries, create an example Pandas DataFrame, then convert to DataFusion.
```python
import duckdb
import pyarrow as pa
import pandas as pd
import datafusion as df
from datafusion import functions as f

pandas_df = pd.DataFrame(
    {
        "A": [1, 2, 3, 4, 5],
        "fruits": ["banana", "banana", "apple", "apple", "banana"],
        "B": [5, 4, 3, 2, 1],
        "cars": ["beetle", "audi", "beetle", "beetle", "beetle"],
    }
)

arrow_table = table = pa.Table.from_pandas(pandas_df)
arrow_batches = table.to_batches()

ctx = SessionContext()
datafusion_df = ctx.create_dataframe([arrow_batches])
datafusion_df
```

Calculate a new DataFusion DataFrame and output it to a variable as an Apache Arrow table.

```python
arrow_batches = (
    datafusion_df
    .aggregate(
        [df.col("fruits")],
        [f.sum(df.col("A")).alias("sum_A_by_fruits")]
    )
    .sort(df.col("fruits").sort(ascending=True))
    .collect()
)
datafusion_to_arrow = (
    pa.Table.from_batches(arrow_batches)
)
datafusion_to_arrow
```

Then query the Apache Arrow table using DuckDB, and output the results as another Apache Arrow table for use in a subsequent DuckDB or DataFusion operation.

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

# DuckDB to DataFusion
DuckDB can output results as Apache Arrow tables, which can be imported into DataFusion with the DataFusion DataFrame constructor.  The same approach could be used with Pandas DataFrames, but Arrow is a faster way to pass data between DuckDB and DataFusion.

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

Load the Apache Arrow table into DataFusion using the DataFusion DataFrame constructor.

```python
datafusion_df_2 = ctx.create_dataframe([duckdb_to_arrow.to_batches()])
datafusion_df_2
```

Complete a calculation using DataFusion, then output the results as another Apache Arrow table for use in a subsequent DuckDB or DataFusion operation.


```python
output_2 = (
    datafusion_df_2
    .aggregate(
        [df.col("fruits")],
        [f.sum(df.col('sum_A_by_fruits'))]
    )
).collect()
output_2
```

To learn more about DataFusion, feel free to explore their [GitHub repository](https://github.com/apache/arrow-datafusion-python/)! 
