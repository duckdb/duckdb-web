---
layout: docu
title: Parquet Loading Tips
---

Below is a collection of tips to help when dealing with Parquet files.

#### Use `union_by_name` when loading files with different schemas

The `union_by_name` option can be used to unify the schema of files that have different or missing columns. For files that do not have certain columns, `NULL` values are filled in.  

```sql
SELECT * FROM read_parquet('flights*.parquet', union_by_name=True);
```
