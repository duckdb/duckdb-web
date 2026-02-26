---
layout: docu
railroad: statements/delete.js
redirect_from:
  - /docs/sql/statements/delete
title: DELETE Statement
---

The `DELETE` statement removes rows from the table identified by the table-name.
If the `WHERE` clause is not present, all records in the table are deleted.
If a `WHERE` clause is supplied, then only those rows for which the `WHERE` clause results in true are deleted. Rows for which the expression is false or `NULL` are retained.

## Examples

Remove the rows matching the condition `i = 2` from the database:

```sql
DELETE FROM tbl WHERE i = 2;
```

Delete all rows in the table `tbl`:

```sql
DELETE FROM tbl;
```

### `USING` Clause

The `USING` clause allows deleting based on the content of other tables or subqueries.

### `RETURNING` Clause

The `RETURNING` clause allows returning the deleted values. It uses the same syntax as the `SELECT` clause except the `DISTINCT` modifier is not supported.

```sql
CREATE TABLE employees (name VARCHAR, age INTEGER);
INSERT INTO employees VALUES ('Kat', 32);
DELETE FROM employees RETURNING name, 2025 - age AS approx_birthyear;
```

| name | approx_birthyear |
|------|-----------------:|
| Kat  | 1993             |

## Syntax

<div id="rrdiagram"></div>

## The `TRUNCATE` Statement

The `TRUNCATE` statement removes all rows from a table, acting as an alias for `DELETE FROM` without a `WHERE` clause:

```sql
TRUNCATE tbl;
```

## Limitations on Reclaiming Memory and Disk Space

Running `DELETE` does not mean space is reclaimed. In general, rows are only marked as deleted. DuckDB reclaims space upon [performing a `CHECKPOINT`]({% link docs/stable/sql/statements/checkpoint.md %}). [`VACUUM`]({% link docs/stable/sql/statements/vacuum.md %}) currently does not reclaim space.
