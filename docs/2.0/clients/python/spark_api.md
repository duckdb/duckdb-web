---
layout: docu
redirect_from:
- /docs/api/python/spark_api
- /docs/clients/python/spark_api
- /docs/stable/clients/python/spark_api
- /docs/current/clients/python/spark_api
- /docs/lts/clients/python/spark_api
- /docs/preview/clients/python/spark_api
title: Spark API
---

The DuckDB Spark API implements the [PySpark API](https://spark.apache.org/docs/4.2.0/api/python/reference/index.html), allowing you to use the familiar Spark API to interact with DuckDB.
All statements are translated to DuckDB's internal plans using our [relational API]({% link docs/2.0/clients/python/relational_api.md %}) and executed using DuckDB's query engine.
The functions it covers are tested against PySpark 4.2.0 and 3.5.9.

> Warning The DuckDB Spark API is experimental and receives bug fixes only: missing features will not be added, and a later release will deprecate it. We recommend [SQLFrame](https://github.com/eakmanrq/sqlframe), which runs PySpark DataFrame code on DuckDB, as its replacement. SQLFrame does not support DuckDB 2.0 yet: SQLFrame 4.5.0 requires `duckdb<1.6` for its DuckDB engine. Please report bugs in the Spark API on [GitHub](https://github.com/duckdb/duckdb-python/issues).

## Example

```python
from duckdb.experimental.spark.sql import SparkSession as session
from duckdb.experimental.spark.sql.functions import lit, col

spark = session.builder.getOrCreate()

df = spark.createDataFrame(
    [(34, "Joan"), (45, "Peter"), (23, "John"), (56, "Bob")],
    ["age", "name"],
)
df = df.withColumn("location", lit("Seattle"))
res = df.select(col("age"), col("location")).collect()

print(res)
```

```text
[Row(age=34, location='Seattle'), Row(age=45, location='Seattle'), Row(age=23, location='Seattle'), Row(age=56, location='Seattle')]
```

`createDataFrame` also accepts a pandas DataFrame, which needs pandas to be installed.

## Contribution Guidelines

The experimental Spark API accepts bug fixes only. When contributing a fix, please test it with our `pytest` testing framework instead of using temporary files.
