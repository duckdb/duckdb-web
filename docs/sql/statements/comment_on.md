---
layout: docu
title: COMMENT ON Statement
railroad: statements/comment.js
---

The `COMMENT ON` statement allows adding metadata to catalog entries (tables, columns, etc.).
It follows the [PostgreSQL syntax](https://www.postgresql.org/docs/16/sql-comment.html).

## Examples

Create a comment on a `TABLE`:

```sql
COMMENT ON TABLE test_table IS 'very nice table';
```

Create a comment on a `COLUMN`:

```sql
COMMENT ON COLUMN test_table.test_table_column IS 'very nice column';
```

Create a comment on a `VIEW`:

```sql
COMMENT ON VIEW test_view IS 'very nice view';
```

Create a comment on an `INDEX`:

```sql
COMMENT ON INDEX test_index IS 'very nice index';
```

Create a comment on a `SEQUENCE`:

```sql
COMMENT ON SEQUENCE test_sequence IS 'very nice sequence';
```

Create a comment on a `TYPE`:

```sql
COMMENT ON TYPE test_type IS 'very nice type';
```

Create a comment on a `MACRO`:

```sql
COMMENT ON MACRO test_macro IS 'very nice macro';
```

Create a comment on a `MACRO TABLE`:

```sql
COMMENT ON MACRO TABLE test_table_macro IS 'very nice table macro';
```

To unset a comment, set it to `NULL`, e.g.:

```sql
COMMENT ON TABLE test_table IS NULL;
```

## Reading Comments

Comments can be read by querying the `comment` column of the respective [metadata functions]({% link docs/sql/duckdb_table_functions.md %}):

List comments on `TABLE`s:

```sql
SELECT comment FROM duckdb_tables();
```

List comments on `COLUMN`s:

```sql
SELECT comment FROM duckdb_columns();
```

List comments on `VIEW`s:

```sql
SELECT comment FROM duckdb_views();
```

List comments on `INDEX`s:

```sql
SELECT comment FROM duckdb_indexes();
```

List comments on `SEQUENCE`s:

```sql
SELECT comment FROM duckdb_sequences();
```

List comments on `TYPE`s:

```sql
SELECT comment FROM duckdb_types();
```

List comments on `MACRO`s:

```sql
SELECT comment FROM duckdb_functions();
```

List comments on `MACRO TABLE`s:

```sql
SELECT comment FROM duckdb_functions();
```

## Limitations

The `COMMENT ON` statement currently has the following limitations:

* It is not possible to comment on schemas or databases.
* It is not possible to comment on things that have a dependency (e.g., a table with an index).

## Syntax

<div id="rrdiagram1"></div>
