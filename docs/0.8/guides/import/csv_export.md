---
layout: docu
redirect_from:
- docs/archive/0.8.1/guides/import/csv_export
selected: CSV Export
title: CSV Export
---

# How to export a table to a CSV file

To export the data from a table to a CSV file, use the `COPY` statement.

```sql
COPY tbl TO 'output.csv' (HEADER, DELIMITER ',');
```

The result of queries can also be directly exported to a CSV file.

```sql
COPY (SELECT * FROM tbl) TO 'output.csv' (HEADER, DELIMITER ',');
```

For additional options, see the [COPY statement documentation](../../sql/statements/copy#csv-export).