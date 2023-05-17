---
layout: docu
title: DuckDB with Fugue
selected: DuckDB with Fugue
---

[Fugue](https://github.com/fugue-project/fugue/) is a unified interface for distributed computing. Fugue executes Python, Pandas, and SQL code on top of Spark, Dask, and Ray. The focus of this tutorial will be on [FugueSQL](https://fugue-tutorials.readthedocs.io/tutorials/quick_look/ten_minutes_sql.html#), an enhanced SQL interface that allows to define end-to-end workflows in SQL rather than juggling between Python and SQL code.

There are three main use cases for FugueSQL with DuckDB:

1. Simplified syntax and additional operators (with a notebook extension)
2. Running Python/Pandas code alongside SQL code seamlessly
3. Testing code on small data, and then running it on SparkSQL or dask-sql when ready to scale

For any questions, see the [FugueSQL](https://fugue-tutorials.readthedocs.io/tutorials/quick_look/ten_minutes_sql.html#) tutorials or message in the [Fugue Slack](http://slack.fugue.ai/). You can also follow along with [this Collab Notebook](https://colab.research.google.com/drive/10J84_Ydq6NdYUqOOSidN495ERfwZ6N4_?usp=sharing). 

# Installation

```python
pip install -U 'fugue[duckdb]'
```

This will install DuckDB and Fugue together.

# Simplified SQL Syntax 

Fugue is compatible with standard SQL, but also extends it with additional keywords and syntax. For example, the `LOAD` and `SAVE` keywords can be used to load and save files, and the `=` operator can be used for intermediate tables. The code below shows an example.

```python
# Setup
import pandas as pd

df = pd.DataFrame({"a": [1,2,3], "b": [2,3,4]})
df.to_parquet("/tmp/f.parquet")
```
Here, the file is loaded, processed, and then saved in the query.
```python
import fugue.api as fa

query = """
df = LOAD "/tmp/f.parquet"

res = SELECT *
        FROM df
       WHERE a > 1

SAVE res OVERWRITE "/tmp/f2.parquet"
"""
fa.fugue_sql_flow(query, engine="duckdb")
```

For other available keywords, check the [SQL Operators](https://fugue-tutorials.readthedocs.io/tutorials/fugue_sql/operators.html) available.

There is also a [Jupyter extension](https://github.com/fugue-project/fugue-jupyter) for FugueSQL to be used inside a notebook with syntax highlighting. To use it with DuckDB, simply use `%%fsql duckdb` as the cell magic.

# Running Python/Pandas Functions

There will be operations that Python or Pandas can express more succinctly than SQL. For example, we can use the Pandas `cumsum()` method to get the cumulative sum of a column. Annotated Python or Pandas code can be invoked using the `TRANSFORM` keyword. In the example below, a Python function is defined, and then invoked in the FugueSQL query.

```python
# schema: *, b_cumsum:int
def new_col(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values("b")
    return df.assign(b_cumsum=df['b'].cumsum())
```

```python
query = """
df = LOAD "/tmp/f.parquet"

df2 = SELECT *
        FROM df
       WHERE a < 3

df3 = TRANSFORM df2 USING new_col

SELECT *, a+b AS c
  FROM df3
 """
pandas_df = fa.as_pandas(fa.fugue_sql(query, engine="duckdb"))
```

The `fugue_sql()` function automatically returns the last DataFrame of the query. When using the `TRANSFORM` function, FugueSQL will bring the DuckDB table to Pandas to execute the Python code. By using `TRANSFORM`, there is no more need to break up the SQL to invoke Python code. FugueSQL is a first-class interface for defining the end-to-end logic.

Because we used the `"duckdb"` engine, the output of the query will be a DuckDB DataFrame. It can be converted to Pandas by using `as_pandas()`. Also notice FugueSQL can handle multiple `SELECT` statements in one query.

# Distributing with SparkSQL

One of the features of Fugue is that the same code will be able to run on top of Spark and Dask, just by changing the execution engine. This allows users to prototype locally with DuckDB on smaller data, and then bring the execution to a Spark cluster when ready to execute on the full-sized data. Developing on Spark can be cumbersome even if using the local version of Spark. DuckDB will significantly speed up iterations because of its fast execution.

```python
query = """
df = LOAD "/tmp/f.parquet"

df2 = SELECT *
        FROM df
       WHERE a < 3

df3 = TRANSFORM df2 USING new_col

SELECT *, a+b AS c
  FROM df3
 """
spark_df = fa.fugue_sql(query, engine="spark")
```

The output of the code above will be a Spark DataFrame.

More information on Fugue can be found on their [Github](https://github.com/fugue-project/fugue/)
