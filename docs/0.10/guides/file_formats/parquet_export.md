---
layout: docu
redirect_from:
- /docs/archive/0.10/guides/import/parquet_export
title: Parquet Export
---

To export the data from a table to a Parquet file, use the `COPY` statement.

```sql
COPY tbl TO 'output.parquet' (FORMAT PARQUET);
```

The result of queries can also be directly exported to a Parquet file.

```sql
COPY (SELECT * FROM tbl) TO 'output.parquet' (FORMAT PARQUET);
```

The flags for setting compression, row group size, etc. are listed in the [Reading and Writing Parquet files](../../data/parquet/overview) page.