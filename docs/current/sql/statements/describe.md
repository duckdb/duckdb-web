---
layout: docu
redirect_from:
- /docs/preview/sql/statements/describe
- /docs/sql/statements/describe
- /docs/stable/sql/statements/describe
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

The `SHOW` statement is an alias for `DESCRIBE`.

## See Also

For more examples, see the [guide on `DESCRIBE`]({% link docs/current/guides/meta/describe.md %}).
