---
layout: docu
redirect_from:
- docs/archive/0.9.2/guides/import/csv_export
- docs/archive/0.9.1/guides/import/csv_export
title: CSV Export
---

To export the data from a table to a CSV file, use the `COPY` statement.

```sql
COPY tbl TO 'output.csv' (HEADER, DELIMITER ',');
```

The result of queries can also be directly exported to a CSV file.

```sql
COPY (SELECT * FROM tbl) TO 'output.csv' (HEADER, DELIMITER ',');
```

For additional options, see the [`COPY` statement documentation](../../sql/statements/copy#csv-options).