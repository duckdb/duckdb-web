---
layout: docu
title: Spark API
---

The DuckDB Spark API implements the [PySpark API](https://spark.apache.org/docs/3.5.0/api/python/reference/index.html), allowing you to use the familiar Spark API to interact with DuckDB.
All statements are translated to DuckDB's internal plans using our [relational API](relational_api) and executed using DuckDB's query engine.

> The DuckDB Spark API is currently experimental and features are still missing. We are very interested in feedback. Please report any functionality that you are missing, either through [Discord](https://discord.duckdb.org) or on [GitHub](https://github.com/duckdb/duckdb/issues).

## Example

```python
from duckdb.experimental.spark.sql import SparkSession as session
from duckdb.experimental.spark.sql.functions import lit, col
import pandas as pd

spark = session.builder.getOrCreate()

pandas_df = pd.DataFrame({
    'age': [34, 45, 23, 56],
    'name': ['Joan', 'Peter', 'John', 'Bob']
})

df = spark.createDataFrame(pandas_df)
df = df.withColumn(
    'location', lit('Seattle')
)
res = df.select(
    col('age'),
    col('location')
).collect()

print(res)
```
```text
[
    Row(age=34, location='Seattle'),
    Row(age=45, location='Seattle'),
    Row(age=23, location='Seattle'),
    Row(age=56, location='Seattle')
]
```