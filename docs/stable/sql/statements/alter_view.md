---
layout: docu
redirect_from:
  - /docs/sql/statements/alter_view
title: ALTER VIEW Statement
---

The `ALTER VIEW` statement changes the schema of an existing view in the catalog.

## Examples

Rename a view:

```sql
ALTER VIEW view1 RENAME TO view2;
```

`ALTER VIEW` changes the schema of an existing view. All the changes made by `ALTER VIEW` fully respect the transactional semantics, i.e., they will not be visible to other transactions until committed, and can be fully reverted through a rollback. Note that other views that rely on the table are **not** automatically updated.
