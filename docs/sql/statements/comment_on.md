---
layout: docu
title: COMMENT ON Statement
railroad: statements/comment.js
---

The `COMMENT ON` statement allows adding metadata to catalog entries (tables, columns, etc.).
It follows the [PostgreSQL syntax](https://www.postgresql.org/docs/16/sql-comment.html).

## Examples

```sql
COMMENT ON TABLE test_table IS 'very nice table';
```

```sql
COMMENT ON COLUMN test_table.test_table_column IS 'very nice column';
```

```sql
COMMENT ON VIEW test_view IS 'very nice view';
```

```sql
COMMENT ON INDEX test_index IS 'very nice index';
```

```sql
COMMENT ON SEQUENCE test_sequence IS 'very nice sequence';
```

```sql
COMMENT ON TYPE test_type IS 'very nice type';
```

```sql
COMMENT ON MACRO test_macro IS 'very nice macro';
```

```sql
COMMENT ON MACRO TABLE test_table_macro IS 'very nice table macro';
```

To unset a comment, set it to `NULL`, e.g.::

```sql
COMMENT ON TABLE test_table IS NULL;
```

## Reading Comments

Comments can be read by querying the `comment` column of the respective [metadata functions](../duckdb_table_functions):

```sql
SELECT comment FROM duckdb_tables();    -- TABLE
SELECT comment FROM duckdb_columns();   -- COLUMN
SELECT comment FROM duckdb_views();     -- VIEW
SELECT comment FROM duckdb_indexes();   -- INDEX
SELECT comment FROM duckdb_sequences(); -- SEQUENCE
SELECT comment FROM duckdb_types();     -- TYPE
SELECT comment FROM duckdb_functions(); -- MACRO
SELECT comment FROM duckdb_functions(); -- MACRO TABLE
```

## Limitations

The `COMMENT ON` statement currently has the following limitations:

* It is not possible to comment on schemas or databases.
* It is not possible to comment on things that have a dependency (e.g., a table with an index).

## Syntax

<div id="rrdiagram1"></div>
