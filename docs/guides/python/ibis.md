---
layout: docu
title: DuckDB with Ibis
selected: DuckDB with Ibis
---

[Ibis](https://github.com/ibis-project/ibis) is a Python library that allows queries to be written in a pythonic relational style and then be compiled into SQL.
Ibis supports multiple database backends, including [DuckDB](https://ibis-project.org/docs/dev/backends/DuckDB/) by using DuckDB's SQLAlchemy driver. 

# Installation
To install only the DuckDB backend for Ibis, use the commands below. See the [Ibis DuckDB installation instructions](https://ibis-project.org/docs/dev/backends/DuckDB/) for a conda alternative.
```python
pip install 'ibis-framework[duckdb]' # duckdb, sqlalchemy, duckdb_engine and more are installed as dependencies
```

# Querying DuckDB with Ibis
The following example is borrowed from the [Introduction to Ibis tutorial](https://ibis-project.org/docs/dev/tutorial/01-Introduction-to-Ibis/), which uses SQLite. 

```python
import ibis

connection = ibis.duckdb.connect(':memory:') # Use an In Memory DuckDB
# connection = ibis.duckdb.connect('/path/to/my_db.db') # Use or create a physical DuckDB at this path

connection.list_tables()
```
```python
# Output:
['pragma_database_list', 'duckdb_tables', 'duckdb_views', 'duckdb_indexes',
 'sqlite_master', 'sqlite_schema', 'sqlite_temp_master', 'sqlite_temp_schema', 
 'duckdb_constraints', 'duckdb_columns', 'duckdb_schemas', 'duckdb_types']
```
