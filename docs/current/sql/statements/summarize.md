---
layout: docu
redirect_from:
- /docs/preview/sql/statements/summarize
- /docs/sql/statements/summarize
- /docs/stable/sql/statements/summarize
title: SUMMARIZE Statement
---

The `SUMMARIZE` statement returns summary statistics for a table, view or a query.

## Usage

```sql
SUMMARIZE tbl;
```

To summarize a query, prepend `SUMMARIZE` to a query.

```sql
SUMMARIZE SELECT * FROM tbl;
```

## See Also

For more examples, see the [guide on `SUMMARIZE`]({% link docs/current/guides/meta/summarize.md %}).
