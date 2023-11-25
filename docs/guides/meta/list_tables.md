---
layout: docu
title: List Tables
---

The `SHOW TABLES` command can be used to obtain a list of all tables within the selected schema.

```sql
CREATE TABLE tbl (i INTEGER);
SHOW TABLES;
```

<div class="narrow_table"></div>

| name |
|------|
| tbl  |

`DESCRIBE`, `SHOW` or `SHOW ALL TABLES` can be used to obtain a list of all tables within **all** attached databases and schemas.

```sql
CREATE TABLE tbl (i INTEGER);
CREATE SCHEMA s1;
CREATE TABLE s1.tbl (v VARCHAR);
SHOW ALL TABLES;
```

<div class="narrow_table"></div>

| database | schema | table_name | column_names | column_types | temporary |
|----------|--------|------------|--------------|--------------|-----------|
| memory   | main   | tbl        | [i]          | [INTEGER]    | false     |
| memory   | s1     | tbl        | [v]          | [VARCHAR]    | false     |

To view the schema of an individual table, use the `DESCRIBE` command.

```sql
CREATE TABLE tbl (i INTEGER PRIMARY KEY, j VARCHAR);
DESCRIBE tbl;
```

<div class="narrow_table"></div>

| column_name | column_type | null | key  | default | extra |
|-------------|-------------|------|------|---------|-------|
| i           | INTEGER     | NO   | PRI  | NULL    | NULL  |
| j           | VARCHAR     | YES  | NULL | NULL    | NULL  |

The SQL-standard [`information_schema`](../../sql/information_schema) views are also defined. 

DuckDB also defines `sqlite_master` and many [PostgreSQL system catalog tables](https://www.postgresql.org/docs/14/catalogs.html) for compatibility with SQLite and PostgreSQL respectively.
