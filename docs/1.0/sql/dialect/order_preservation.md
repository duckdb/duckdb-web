---
layout: docu
title: Order Preservation
---

For many operations, DuckDB preserves the insertion order of rows, similarly to data frame libraries such as Pandas.
The following operations and components respect insertion order:

* [The CSV reader]({% link docs/1.0/data/csv/overview.md %}#order-preservation)

Preservation of insertion order is controlled by the  `preserve_insertion_order` [configuration option]({% link docs/1.0/configuration/overview.md %}).
This setting is `true` by default, indicating that the order should be preserved.
To change this setting, use:

```sql
SET preserve_insertion_order = false;
```