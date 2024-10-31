---
layout: docu
title: JSON Export
redirect_from:
  - /docs/guides/import/json_export
---

To export the data from a table to a JSON file, use the `COPY` statement:

```sql
COPY tbl TO 'output.json';
```

The result of queries can also be directly exported to a JSON file:

```sql
COPY (SELECT * FROM tbl) TO 'output.json';
```

The JSON export writes JSON lines by default. The `ARRAY` option can be used to write a JSON array instead.

```sql
COPY tbl TO 'output.json' (ARRAY);
```

For additional options, see the [`COPY` statement documentation]({% link docs/sql/statements/copy.md %}).
