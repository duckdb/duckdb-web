---
layout: docu
title: SUMMARIZE Statement
---

The `SUMMARIZE` statement returns summary statistics for a table, view or a query.

## Usage

```sql
SUMMARIZE tbl;
```

In order to summarize a query, prepend `SUMMARIZE` to a query.

```sql
SUMMARIZE SELECT * FROM tbl;
```

## See Also

For more examples, see the [guide on `SUMMARIZE`](../../guides/meta/summarize).
