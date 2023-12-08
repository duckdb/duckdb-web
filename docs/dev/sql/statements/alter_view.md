---
layout: docu
redirect_from:
- /docs/sql/statements/alter_view
title: ALTER VIEW Statement
---

The `ALTER VIEW` statement changes the schema of an existing view in the catalog.

## Examples

```sql
-- rename a view
ALTER VIEW v1 RENAME TO v2;
```

`ALTER VIEW` changes the schema of an existing table. All the changes made by `ALTER VIEW` fully respect the transactional semantics, i.e., they will not be visible to other transactions until committed, and can be fully reverted through a rollback. Note that other views that rely on the table are **not** automatically updated.
