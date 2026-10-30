---
layout: docu
redirect_from:
- /docs/guides/file_formats/parquet_export
- /docs/guides/import/parquet_export
- /docs/stable/guides/file_formats/parquet_export
- /docs/current/guides/file_formats/parquet_export
- /docs/lts/guides/file_formats/parquet_export
- /docs/preview/guides/file_formats/parquet_export
title: Parquet Export
how_to_topic: file-formats
---

To export the data from a table to a Parquet file, use the [`COPY` statement]({% link docs/2.0/sql/statements/copy.md %}):

```sql
COPY tbl TO 'output.parquet' (FORMAT parquet);
```

The result of queries can also be directly exported to a Parquet file:

```sql
COPY (SELECT * FROM tbl) TO 'output.parquet' (FORMAT parquet);
```

The flags for setting compression, row group size, etc. are listed in the [Reading and Writing Parquet files]({% link docs/2.0/data/parquet/overview.md %}) page.
