---
layout: docu
title: CSV Export
redirect_from:
  - /docs/guides/import/csv_export
---

To export the data from a table to a CSV file, use the `COPY` statement:

```sql
COPY tbl TO 'output.csv' (HEADER, DELIMITER ',');
```

The result of queries can also be directly exported to a CSV file:

```sql
COPY (SELECT * FROM tbl) TO 'output.csv' (HEADER, DELIMITER ',');
```

For additional options, see the [`COPY` statement documentation]({% link docs/sql/statements/copy.md %}#csv-options).
