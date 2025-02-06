---
layout: docu
title: List Tables
---

The `SHOW TABLES` command can be used to obtain a list of all tables within the selected schema.

```sql
CREATE TABLE tbl (i INTEGER);
SHOW TABLES;
```

| name |
|------|
| tbl  |

`SHOW` or `SHOW ALL TABLES` can be used to obtain a list of all tables within **all** attached databases and schemas.

```sql
CREATE TABLE tbl (i INTEGER);
CREATE SCHEMA s1;
CREATE TABLE s1.tbl (v VARCHAR);
SHOW ALL TABLES;
```

| database | schema | table_name | column_names | column_types | temporary |
|----------|--------|------------|--------------|--------------|-----------|
| memory   | main   | tbl        | [i]          | [INTEGER]    | false     |
| memory   | s1     | tbl        | [v]          | [VARCHAR]    | false     |

To view the schema of an individual table, use the [`DESCRIBE` command]({% link docs/archive/1.1/guides/meta/describe.md %}).

## See Also

The SQL-standard [`information_schema`]({% link docs/archive/1.1/sql/meta/information_schema.md %}) views are also defined. Moreover, DuckDB defines `sqlite_master` and many [PostgreSQL system catalog tables](https://www.postgresql.org/docs/16/catalogs.html) for compatibility with SQLite and PostgreSQL respectively.