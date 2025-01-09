---
layout: docu
title: DESCRIBE Statement
---

The `DESCRIBE` statement shows the schema of a table, view or query.

## Usage

```sql
DESCRIBE tbl;
```

In order to summarize a query, prepend `DESCRIBE` to a query.

```sql
DESCRIBE SELECT * FROM tbl;
```

## Alias

The `SHOW` statement is an alias for `DESCRIBE`.

## See Also

For more examples, see the [guide on `DESCRIBE`](../../guides/meta/describe).