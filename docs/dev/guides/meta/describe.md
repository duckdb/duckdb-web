---
layout: docu
redirect_from:
- /docs/guides/meta/describe
title: Describe
---

## Describing a Table

In order to view the schema of a table, use `DESCRIBE` followed by the table name.

```sql
CREATE TABLE tbl (i INTEGER PRIMARY KEY, j VARCHAR);
DESCRIBE tbl;
```

<div class="narrow_table"></div>

| column_name | column_type | null | key  | default | extra |
|-------------|-------------|------|------|---------|-------|
| i           | INTEGER     | NO   | PRI  | NULL    | NULL  |
| j           | VARCHAR     | YES  | NULL | NULL    | NULL  |

## Describing a Query

In order to view the schema of the result of a query, prepend `DESCRIBE` to a query.

```sql
DESCRIBE SELECT * FROM tbl;
```

| column_name | column_type | null | key  | default | extra |
|-------------|-------------|------|------|---------|-------|
| i           | INTEGER     | YES  | NULL | NULL    | NULL  |
| j           | VARCHAR     | YES  | NULL | NULL    | NULL  |

Note that there are subtle differences: compared to the result when [describing a table](#describing-a-table), nullability (`null`) and key information (`key`) are lost.
