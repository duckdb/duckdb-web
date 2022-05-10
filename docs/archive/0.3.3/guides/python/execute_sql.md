---
layout: docu
title: Execute SQL
selected: Execute SQL
---

# How to execute SQL queries


First connect to a database using the `connect` command. By default an in-memory database will be opened.

```py
import duckdb
con = duckdb.connect()
```

After connecting, SQL queries can be executed using the `execute` command.

```py
results = con.execute("SELECT 42").fetchall()
```

By default, a list of Python objects is returned. Use `df` if you would like the result to be returned as a Python dataframe instead.

```py
results = con.execute("SELECT 42").df()
```

