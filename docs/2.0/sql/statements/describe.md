---
layout: docu
redirect_from:
- /docs/sql/statements/describe
- /docs/stable/sql/statements/describe
- /docs/current/sql/statements/describe
- /docs/lts/sql/statements/describe
- /docs/preview/sql/statements/describe
title: DESCRIBE Statement
---

The `DESCRIBE` statement shows the schema of a table, view or query.

## Usage

```sql
DESCRIBE tbl;
```

To describe a query, prepend `DESCRIBE` to a query.

```sql
DESCRIBE SELECT * FROM tbl;
```

## Alias

The `SHOW` statement can also describe tables and queries, but this usage is deprecated as of DuckDB 2.0 and prints a warning.

## See Also

For more examples, see the [guide on `DESCRIBE`]({% link docs/2.0/guides/meta/describe.md %}).
