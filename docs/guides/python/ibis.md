---
layout: docu
title: DuckDB with Ibis
selected: DuckDB with Ibis
---

[Ibis](https://github.com/ibis-project/ibis) is a Python library that allows queries to be written in a pythonic relational style and then be compiled into SQL.
Ibis supports multiple database backends, including [DuckDB](https://ibis-project.org/docs/dev/backends/DuckDB/) by using DuckDB's SQLAlchemy driver. 

# Installation
To install only the DuckDB backed for Ibis, use the commands below. See the [Ibis DuckDB installation instructions](https://ibis-project.org/docs/dev/backends/DuckDB/) for a conda alternative.
```python
pip install duckdb
pip install 'ibis-framework[duckdb]'
pip install sqlalchemy # Used by Ibis
pip install duckdb-engine # DuckDB SQLAlchemy driver
```

# Querying DuckDB with Ibis
The following example is borrowed from the [Introduction to Ibis tutorial](https://ibis-project.org/docs/dev/tutorial/01-Introduction-to-Ibis/), which uses SQLite. 

