---
github_repository: https://github.com/duckdb/duckdb-sqlsmith
layout: docu
title: SQLSmith Extension
redirect_from:
- /docs/stable/extensions/sqlsmith
- /docs/stable/extensions/sqlsmith/
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
