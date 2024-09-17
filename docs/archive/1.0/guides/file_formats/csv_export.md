---
layout: docu
redirect_from:
- /docs/archive/1.0/guides/import/csv_export
title: CSV Export
---

To export the data from a table to a CSV file, use the `COPY` statement:

```sql
COPY tbl TO 'output.csv' (HEADER, DELIMITER ',');
```

The result of queries can also be directly exported to a CSV file:

```sql
COPY (SELECT * FROM tbl) TO 'output.csv' (HEADER, DELIMITER ',');
```

For additional options, see the [`COPY` statement documentation]({% link docs/archive/1.0/sql/statements/copy.md %}#csv-options).