---
layout: docu
railroad: statements/delete.js
redirect_from:
- /docs/sql/statements/delete
title: DELETE Statement
---

The `DELETE` statement removes rows from the table identified by the table-name.

## Examples

```sql
-- remove the rows matching the condition "i = 2" from the database
DELETE FROM tbl WHERE i = 2;
-- delete all rows in the table "tbl"
DELETE FROM tbl;
```

## Syntax

<div id="rrdiagram"></div>

The `DELETE` statement removes rows from the table identified by the table-name.

If the `WHERE` clause is not present, all records in the table are deleted. If a `WHERE` clause is supplied, then only those rows for which the `WHERE` clause results in true are deleted. Rows for which the expression is false or NULL are retained.

The `USING` clause allows deleting based on the content of other tables or subqueries.

## Limitations on Reclaiming Memory and Disk Space

Running `DELETE` does not mean space is reclaimed. In general, rows are only marked as deleted. DuckDB's support for [`VACUUM`](vacuum) is limited to vacuuming entire row groups.
