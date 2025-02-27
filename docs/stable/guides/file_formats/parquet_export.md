---
layout: docu
redirect_from:
- /docs/guides/import/parquet_export
- /docs/guides/import/parquet_export/
- /docs/guides/file_formats/parquet_export
title: Parquet Export
---

To export the data from a table to a Parquet file, use the `COPY` statement:

```sql
COPY tbl TO 'output.parquet' (FORMAT parquet);
```

The result of queries can also be directly exported to a Parquet file:

```sql
COPY (SELECT * FROM tbl) TO 'output.parquet' (FORMAT parquet);
```

The flags for setting compression, row group size, etc. are listed in the [Reading and Writing Parquet files]({% link docs/stable/data/parquet/overview.md %}) page.