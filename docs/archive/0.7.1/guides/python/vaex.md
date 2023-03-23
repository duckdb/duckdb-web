---
layout: docu
title: DuckDB with Vaex
selected: DuckDB with Vaex
---

[Vaex](https://github.com/vaexio/vaex/) is a high performance DataFrame library in Python. Vaex is a hybrid DataFrame, as it supports both [Numpy's](https://numpy.org/doc/stable/) and [Apache Arrow's](https://arrow.apache.org/docs/python/index.html) data structures.
Vaex DataFrames can export data as Apache Arrow Table, which can be directly used by DuckDB. Since DuckDB can output results as an Apache Arrow Table which can be easily turned into a Vaex DataFrame, one can easily alternate between DuckDB and Vaex.

The following example shows how one can use both DuckDB and Vaex DataFrame for a simple exploratory work.

# Installation

```python
pip install duckdb
pip install vaex
```

# Vaex DataFrame to DuckDB
A Vaex DataFrame can be exported as an Arrow Table via the `to_arrow_table()` method. This operation does not take extra memory if the data being exported is already in memory or memory-mapped. The exported Arrow Table can be queried directly via DuckDB.

Let's use the well known Titanic dataset that also ships with Vaex, to do some operations like filling missing values and creating new columns. Then we will export the DataFrame to an Arrow Table:

```python
import duckdb
import vaex

df = vaex.datasets.titanic()

df['age'] = df.age.fillna(df.age.mean())
df['fare'] = df.age.fillna(df.fare.mean())
df['family_size'] = (df.sibsp + df.parch + 1)
df['fare_per_family_member'] = df.fare / df.family_size
df['name_title'] = df['name'].str.replace('.* ([A-Z][a-z]+)\..*', "\\1", regex=True)

arrow_table  = df.to_arrow_table()
```

Now we can directly query the Arrow Table using DuckDB, the output of which can be another Arrow Table, which can be used for subsequent DuckDB queries, or it can be converted to a Vaex DataFrame:

```python
query_result_arrow_table = duckdb.query('''

    SELECT

        pclass,
        MEAN(age) as age,
        MEAN(family_size) as family_size,
        MEAN(fare_per_family_member) as fare_per_family_member,
        COUNT(DISTINCT(name_title)) as distinct_titles,
        LIST(DISTINCT(name_title))

    FROM arrow_table

    GROUP BY pclass
    ORDER BY pclass
''').arrow()
```

# DuckDB to Vaex DataFrame
The output of a DuckDB query can be an Arrow Table, which can be easily converted to a Vaex DataFrame via the `vaex.from_arrow_table()` method. One can also pass data around via [Pandas](https://pandas.pydata.org/docs/) DataFrames, but Arrow is faster.

We can use the query result from above and convert it to a vaex DataFrame:

```python
df_from_duckdb = vaex.from_arrow_table(query_result_arrow_table)
```

One can then continue to use Vaex, and also export the data or part of it to an Arrow Table to be used with DuckDB as needed.

To learn more about Vaex, feel free to explore their [Documentation](https://vaex.readthedocs.io/en/latest/index.html).
