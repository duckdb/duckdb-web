---
layout: docu
title: SQLSmith Extension
github_repository: https://github.com/duckdb/duckdb-sqlsmith
---

The `sqlsmith` extension is used for testing.

## Installing and Loading

```sql
INSTALL sqlsmith;
LOAD sqlsmith;
```

## Functions

The `sqlsmith` extension registers the following functions:

* `sqlsmith`
* `fuzzyduck`
* `reduce_sql_statement`
* `fuzz_all_functions`
