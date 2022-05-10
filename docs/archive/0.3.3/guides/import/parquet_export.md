---
layout: docu
title: Parquet Export
selected: Parquet Export
---

# How to export a table to a Parquet file

To export the data from a table to a Parquet file, use the `COPY` statement.

```sql
COPY tbl TO 'output.parquet' (FORMAT PARQUET);
```

The result of queries can also be directly exported to a Parquet file.

```sql
COPY (SELECT * FROM tbl) TO 'output.parquet' (FORMAT PARQUET);
```
