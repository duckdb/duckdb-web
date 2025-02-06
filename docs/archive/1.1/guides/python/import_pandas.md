---
layout: docu
title: Import from Pandas
---

[`CREATE TABLE ... AS`]({% link docs/archive/1.1/sql/statements/create_table.md %}#create-table--as-select-ctas) and [`INSERT INTO`]({% link docs/archive/1.1/sql/statements/insert.md %}) can be used to create a table from any query.
We can then create tables or insert into existing tables by referring to the [Pandas](https://pandas.pydata.org/) DataFrame in the query.
There is no need to register the DataFrames manually –
DuckDB can find them in the Python process by name thanks to [replacement scans]({% link docs/archive/1.1/guides/glossary.md %}#replacement-scan).

```python
import duckdb
import pandas

# Create a Pandas dataframe
my_df = pandas.DataFrame.from_dict({'a': [42]})

# create the table "my_table" from the DataFrame "my_df"
# Note: duckdb.sql connects to the default in-memory database connection
duckdb.sql("CREATE TABLE my_table AS SELECT * FROM my_df")

# insert into the table "my_table" from the DataFrame "my_df"
duckdb.sql("INSERT INTO my_table SELECT * FROM my_df")
```

If the order of columns is different or not all columns are present in the DataFrame, use [`INSERT INTO ... BY NAME`]({% link docs/archive/1.1/sql/statements/insert.md %}#insert-into--by-name):

```python
duckdb.sql("INSERT INTO my_table BY NAME SELECT * FROM my_df")
```

## See Also

DuckDB also supports [exporting to Pandas]({% link docs/archive/1.1/guides/python/export_pandas.md %}).