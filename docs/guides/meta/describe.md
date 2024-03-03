---
layout: docu
title: Describe
---

## Describing a Table

In order to view the schema of a table, use `DESCRIBE` or `SHOW` followed by the table name.

```sql
CREATE TABLE tbl (i INTEGER PRIMARY KEY, j VARCHAR);
DESCRIBE tbl;
SHOW tbl; -- equivalent to DESCRIBE tbl;
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

<div class="narrow_table"></div>

| column_name | column_type | null | key  | default | extra |
|-------------|-------------|------|------|---------|-------|
| i           | INTEGER     | YES  | NULL | NULL    | NULL  |
| j           | VARCHAR     | YES  | NULL | NULL    | NULL  |

Note that there are subtle differences: compared to the result when [describing a table](#describing-a-table), nullability (`null`) and key information (`key`) are lost.

## Using `DESCRIBE` in a Subquery

`DESCRIBE` can be used a subquery. This allows creating a table from the description, for example:

```sql
CREATE TABLE tbl_description AS SELECT * FROM (DESCRIBE tbl);
```

## Describing Remote Tables

It is possible to describe remote tables via the [`httpfs` extension](../../extensions/httpfs) using the `DESCRIBE TABLE` statement. For example:

```sql
DESCRIBE TABLE 'https://blobs.duckdb.org/data/Star_Trek-Season_1.csv';
```

```text
┌─────────────────────────────────────────┬─────────────┬─────────┬─────────┬─────────┬─────────┐
│               column_name               │ column_type │  null   │   key   │ default │  extra  │
│                 varchar                 │   varchar   │ varchar │ varchar │ varchar │ varchar │
├─────────────────────────────────────────┼─────────────┼─────────┼─────────┼─────────┼─────────┤
│ season_num                              │ BIGINT      │ YES     │         │         │         │
│ episode_num                             │ BIGINT      │ YES     │         │         │         │
│ aired_date                              │ DATE        │ YES     │         │         │         │
│ ...                                     │ ...         │ ...     │         │         │         │
├─────────────────────────────────────────┴─────────────┴─────────┴─────────┴─────────┴─────────┤
│ 18 rows                                                                             6 columns │
└───────────────────────────────────────────────────────────────────────────────────────────────┘
```
