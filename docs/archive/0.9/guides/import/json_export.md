---
layout: docu
redirect_from:
- docs/archive/0.9.2/guides/import/json_export
- docs/archive/0.9.1/guides/import/json_export
- docs/archive/0.9.0/guides/import/json_export
title: JSON Export
---

To export the data from a table to a JSON file, use the `COPY` statement.

```sql
COPY tbl TO 'output.json';
```

The result of queries can also be directly exported to a JSON file.

```sql
COPY (SELECT * FROM tbl) TO 'output.json';
```

For additional options, see the [`COPY` statement documentation](../../sql/statements/copy).