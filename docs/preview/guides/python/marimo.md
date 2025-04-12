---
layout: docu
redirect_from:
- /docs/guides/python/marimo
title: marimo notebooks
---

[marimo](https://github.com/marimo-team/marimo), an open-source reactive notebook for Python and SQL, ships with tight integration with DuckDB's Python client giving you powerful SQL cells that allow you to mix and match Python and SQL in a single notebook. Unlike traditional notebooks, when you run a cell or interact with a UI element, marimo automatically runs affected cells (or marks them as stale), keeping code and outputs consistent and preventing bugs before they happen. Its tight integration with DuckDB makes it perfect for data exploration and analysis.

## Installation

To get started, install marimo and duckdb from your terminal:

```bash
pip install "marimo[sql]"
# or
uv add "marimo[sql]"
```

## SQL in marimo

Start a new notebook from your terminal with `marimo edit <notebook-name>.py`. You can create SQL cells in one of three ways:

1. **Right-click** the "+" button and pick "SQL cell"
2. Convert any empty cell to SQL via the cell menu
3. Hit the SQL button at the bottom of your notebook

<img src="/images/guides/marimo/marimo-sql-button.png"/>

Under the hood, marimo converts your SQL into clean Python:

```python
df = mo.sql(f"SELECT 'Off and flying!' AS a_duckdb_column")
```

marimo does not have any "magic" SQL commands and serializes your cells as pure Python. This is because marimo stores your notebook as pure Python, [for many reasons](https://marimo.io/blog/python-not-json), such as git-friendly diffs and running notebooks as Python scripts.

The SQL statement itself is an f-string, letting you interpolate Python values into the query with `{}` (shown later). In particular, this means your SQL queries can depend on the values of UI elements or other Python values, all part of marimo's dataflow graph.

> Warning Heads up!
> If you have user-generated-content going into the SQL queries, be sure to santize your inputs to prevent SQL injection.

## Connecting a Custom DuckDB Connection

To connect to a custom DuckDB connection instead of using the default global connection, create a cell and create a DuckDB connection as Python variable:

```python
import duckdb

# Create a DuckDB connection
conn = duckdb.connect("path/to/my/duckdb.db")
```

marimo will automatically discover the connection and let you select it in the SQL cell's connection dropdown.

<div align="center">
  <figure>
    <img src="/images/guides/marimo/marimo-custom-connection.png"/>
    <figcaption>Custom connection</figcaption>
  </figure>
</div>


## Database, Schema, and Table Auto-Discovery

marimo will also automatically introspect connections and display the database, schemas, tables, and columns in the Data Sources panel. This panel lets you quickly navigate your schemas to pull tables and columns into your SQL queries.

<div align="center">
  <figure>
    <img src="/images/guides/marimo/marimo-datasource-discovery.png"/>
    <figcaption>Data Sources Panel</figcaption>
  </figure>
</div>


## Reference a Local Dataframe

You can reference a local dataframe in your SQL cell by using the name of the
Python variable that holds the dataframe. If you have a database connection
with a table of the same name, the database table will be used instead.

```python
import polars as pl
df = pl.DataFrame({"column": [1, 2, 3]})
```

```sql
SELECT * FROM df WHERE column > 2
```

## Reference the Output of a SQL Cell

Defining a non-private (non-underscored) output variable in the SQL cell allows you to reference the resulting dataframe in other Python and SQL cells.

<div align="center">
  <figure>
    <img src="/images/guides/marimo/marimo-sql-result.png"/>
    <figcaption>Reference the SQL result in Python</figcaption>
  </figure>
</div>

## Reactive SQL Cells

marimo allows you to create reactive SQL cells that automatically update when their dependencies change. **Working with expensive queries or large datasets?** You can configure marimo's runtime to be "lazy". By doing so, dependent cells are only marked as stale letting the user choose when they should be re-run.

```python
digits = mo.ui.slider(label="Digits", start=100, stop=10000, step=200)
digits
```

```sql
CREATE TABLE random_data AS
SELECT i AS id, RANDOM() AS random_value,
FROM range({digits.value}) AS t(i);

SELECT * FROM random_data;
```

Interacting with UI elements, like a slider, makes your data more tangible.

<div align="center">
  <figure>
    <img src="/images/guides/marimo/marimo-reactive-sql.gif"/>
    <figcaption>Reactively run SQL from UI elements</figcaption>
  </figure>
</div>


## Why marimo + DuckDB?

marimo's reactive execution model keeps your cells in sync, eliminating manual refreshes and letting you focus on analysis instead of notebook management:

1. **Live Updates**: Change a slider or update a cell? Your dependent queries and charts update instantly.
2. **Smart Execution**: Only cells that need to run do run.
3. **Built-in UI**: Create interactive dashboards without leaving your notebook.
4. **Python Native**: Mix Python and SQL naturally.
5. **Reusable**: marimo notebooks double as data apps and Python scripts.

## Next Steps

* Dive into the [marimo docs](https://docs.marimo.io/).
* Run the SQL tutorial from your terminal: `marimo tutorial sql`.
* Checkout the code for this guide is [available on GitHub](https://github.com/marimo-team/marimo/blob/main/examples/sql/duckdb_example.py).

## Wrapping Up

marimo + DuckDB = a reactive data analysis powerhouse. Your queries and visualizations stay in sync automatically, and you can build interactive tools right in your notebook.
