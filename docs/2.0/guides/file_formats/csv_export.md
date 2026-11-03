---
layout: docu
redirect_from:
- /docs/guides/file_formats/csv_export
- /docs/guides/import/csv_export
- /docs/stable/guides/file_formats/csv_export
- /docs/current/guides/file_formats/csv_export
- /docs/lts/guides/file_formats/csv_export
- /docs/preview/guides/file_formats/csv_export
title: CSV Export
how_to_topic: file-formats
---

To export the data from a table to a CSV file, use the `COPY` statement:

```sql
COPY tbl TO 'output.csv' (HEADER, DELIMITER ',');
```

The result of queries can also be directly exported to a CSV file:

```sql
COPY (SELECT * FROM tbl) TO 'output.csv' (HEADER, DELIMITER ',');
```

For additional options, see the [`COPY` statement documentation]({% link docs/2.0/sql/statements/copy.md %}#csv-options).
