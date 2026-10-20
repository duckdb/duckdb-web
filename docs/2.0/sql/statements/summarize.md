---
layout: docu
redirect_from:
- /docs/sql/statements/summarize
- /docs/stable/sql/statements/summarize
- /docs/current/sql/statements/summarize
- /docs/lts/sql/statements/summarize
- /docs/preview/sql/statements/summarize
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

For more examples, see the [guide on `SUMMARIZE`]({% link docs/2.0/guides/meta/summarize.md %}).
