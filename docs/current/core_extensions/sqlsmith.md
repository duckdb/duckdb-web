---
github_repository: https://github.com/duckdb/duckdb-sqlsmith
layout: docu
redirect_from:
- /docs/extensions/sqlsmith
- /docs/stable/extensions/sqlsmith
- /docs/preview/core_extensions/sqlsmith
- /docs/stable/core_extensions/sqlsmith
title: SQLSmith Extension
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
