---
layout: docu
redirect_from:
- /docs/guides/python/import_pandas
- /docs/stable/guides/python/import_pandas
- /docs/current/guides/python/import_pandas
- /docs/lts/guides/python/import_pandas
- /docs/preview/guides/python/import_pandas
title: Import from Pandas
how_to_topic: python
---

[`CREATE TABLE ... AS`]({% link docs/2.0/sql/statements/create_table.md %}#create-table--as-select-ctas) and [`INSERT INTO`]({% link docs/2.0/sql/statements/insert.md %}) can be used to create a table from any query.
We can then create tables or insert into existing tables by referring to the [Pandas](https://pandas.pydata.org/) DataFrame in the query.
There is no need to register the DataFrames manually –
DuckDB can find them in the Python process by name thanks to [replacement scans]({% link docs/2.0/guides/glossary.md %}#replacement-scan).

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

If the order of columns is different or not all columns are present in the DataFrame, use [`INSERT INTO ... BY NAME`]({% link docs/2.0/sql/statements/insert.md %}#insert-into--by-name):

```python
duckdb.sql("INSERT INTO my_table BY NAME SELECT * FROM my_df")
```

Alternatively, the [`append`]({% link docs/2.0/clients/python/reference/index.md %}#duckdb.DuckDBPyConnection.append) method appends a DataFrame to an existing table directly, without writing a SQL query. Pass `by_name=True` to match columns by name rather than by position:

```python
con = duckdb.connect()
con.sql("CREATE TABLE my_table (a INTEGER)")
con.append("my_table", my_df)
```

## See Also

DuckDB also supports [exporting to Pandas]({% link docs/2.0/guides/python/export_pandas.md %}).
