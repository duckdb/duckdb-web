---
layout: docu
railroad: statements/delete.js
title: DELETE Statement
---

The `DELETE` statement removes rows from the table identified by the table-name.

## Examples

Remove the rows matching the condition `i = 2` from the database:

```sql
DELETE FROM tbl WHERE i = 2;
```

Delete all rows in the table `tbl`:

```sql
DELETE FROM tbl;
```

The `TRUNCATE` statement removes all rows from a table, acting as an alias for `DELETE FROM` without a `WHERE` clause:

```sql
TRUNCATE tbl;
```

## Syntax

<div id="rrdiagram"></div>

The `DELETE` statement removes rows from the table identified by the table-name.

If the `WHERE` clause is not present, all records in the table are deleted. If a `WHERE` clause is supplied, then only those rows for which the `WHERE` clause results in true are deleted. Rows for which the expression is false or NULL are retained.

The `USING` clause allows deleting based on the content of other tables or subqueries.

## Limitations on Reclaiming Memory and Disk Space

Running `DELETE` does not mean space is reclaimed. In general, rows are only marked as deleted. DuckDB reclaims space upon [performing a `CHECKPOINT`]({% link docs/archive/1.1/sql/statements/checkpoint.md %}). [`VACUUM`]({% link docs/archive/1.1/sql/statements/vacuum.md %}) currently does not reclaim space.