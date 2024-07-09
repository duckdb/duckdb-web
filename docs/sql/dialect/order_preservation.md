---
layout: docu
title: Order Preservation
---

For many operations, DuckDB preserves the insertion order of rows, similarly to data frame libraries such as Pandas.

To change this setting, use the `preserve_insertion_order` [configuration option]({% link docs/configuration/overview.md %}):

```sql
SET preserve_insertion_order = false;
```
