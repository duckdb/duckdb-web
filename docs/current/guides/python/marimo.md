---
layout: docu
title: marimo Notebooks
---

[marimo](https://github.com/marimo-team/marimo) is an open-source reactive
notebook for Python and SQL that's tightly integrated with DuckDB's Python
client, letting you mix and match Python and SQL in a single git-versionable
notebook. Unlike traditional notebooks, when you run a cell or interact with a
UI element, marimo automatically (or lazily) runs affected cells, keeping code
and outputs consistent. Its integration with DuckDB makes it well-suited to
interactively working with data, and its representation as a Python file makes
it simple to run notebooks as scripts.

## Installation

To get started, install marimo and DuckDB from your terminal:

```batch
pip install "marimo[sql]" # or uv add "marimo[sql]"
```

Install supporting libraries:

```batch
pip install "polars[pyarrow]" # or uv add "polars[pyarrow]"
```

Run a tutorial:

```batch
marimo tutorial sql
```

## SQL in marimo

Create a notebook from your terminal with `marimo edit notebook.py`. Create SQL
cells in one of three ways:

1. Right-click the **+** button and pick **SQL cell**
2. Convert any empty cell to SQL via the cell menu
3. Hit the SQL button at the bottom of your notebook

<img src="/images/guides/marimo/marimo-sql-button.png"/>

In marimo, SQL cells give the appearance of writing SQL while being serialized as standard Python code using the `mo.sql()` function, which keeps your notebook as pure Python code without requiring special syntax or magic commands.

```python
df = mo.sql(f"SELECT 'Off and flying!' AS a_duckdb_column")
```

This is because marimo stores notebooks as pure Python, [for many reasons](https://marimo.io/blog/python-not-json), such as git-friendly diffs and running notebooks as Python scripts.

The SQL statement itself is an f-string, letting you interpolate Python values into the query with `{}` (shown later). In particular, this means your SQL queries can depend on the values of UI elements or other Python values, all part of marimo's dataflow graph.

> Warning Heads up!
> If you have user-generated content going into the SQL queries, be sure to sanitize your inputs to prevent SQL injection.

## Connecting a Custom DuckDB Connection

To connect to a custom DuckDB connection instead of using the default global connection, create a cell and create a DuckDB connection as a Python variable:

```python
import duckdb

# Create a DuckDB connection
conn = duckdb.connect("path/to/my/duckdb.db")
```

marimo automatically discovers the connection and lets you select it in the SQL cell's connection dropdown.

<div align="center">
  <figure>
    <img src="/images/guides/marimo/marimo-custom-connection.png"/>
    <figcaption>Custom connection</figcaption>
  </figure>
</div>


## Database, Schema, and Table Auto-Discovery

marimo introspects connections and displays the database, schemas, tables, and columns in the Data Sources panel. This panel lets you quickly navigate your schemas to pull tables and columns into your SQL queries.

<div align="center">
  <figure>
    <img src="/images/guides/marimo/marimo-datasource-discovery.png"/>
    <figcaption>Data Sources Panel</figcaption>
  </figure>
</div>


## Reference a Local Dataframe

Reference a local dataframe in your SQL cell by using the name of the
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

marimo allows you to create reactive SQL cells that automatically update when their dependencies change. **Working with expensive queries or large datasets?** You can configure marimo's runtime to be “lazy”. By doing so, dependent cells are only marked as stale, letting the user choose when they should be re-run.

```python
digits = mo.ui.slider(label="Digits", start=100, stop=10000, step=200)
digits
```

```sql
CREATE TABLE random_data AS
    SELECT i AS id, random() AS random_value,
    FROM range({digits.value}) AS t(i);

SELECT * FROM random_data;
```

Interacting with UI elements, like a slider, makes your data more tangible.

<div align="center">
  <img src="/images/guides/marimo/marimo-reactive-sql.gif"/>
</div>


## DuckDB-Powered OLAP Analytics in marimo

marimo provides several features that work well with DuckDB for analytical workflows:

* Seamless integration between Python and SQL
* Reactive execution that automatically updates dependent cells when queries change
* Interactive UI elements that can be used to parameterize SQL queries
* Ability to export notebooks as standalone applications or Python scripts, or even run entirely in the browser [with WebAssembly](https://docs.marimo.io/guides/wasm/).

## Next Steps

* Read the [marimo docs](https://docs.marimo.io/).
* Try the SQL tutorial: `marimo tutorial sql`.
* The code for this guide is [available on GitHub](https://github.com/marimo-team/marimo/blob/main/examples/sql/duckdb_example.py). Run it with `marimo edit ⟨github_url⟩`.
