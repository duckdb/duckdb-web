---
layout: docu
railroad: statements/drop.js
title: DROP Statement
---

The `DROP` statement removes a catalog entry added previously with the `CREATE` command.

## Examples

Delete the table with the name `tbl`:

```sql
DROP TABLE tbl;
```

Drop the view with the name `view1`; do not throw an error if the view does not exist:

```sql
DROP VIEW IF EXISTS view1;
```

Drop function `fn`:

```sql
DROP FUNCTION fn;
```

Drop index `idx`:

```sql
DROP INDEX idx;
```

Drop schema `sch`:

```sql
DROP SCHEMA sch;
```

Drop sequence `seq`:

```sql
DROP SEQUENCE seq;
```

Drop macro `mcr`:

```sql
DROP MACRO mcr;
```

Drop macro table `mt`:

```sql
DROP MACRO TABLE mt; -- the `TABLE` is optional since v1.4.0
```

Drop type `typ`:

```sql
DROP TYPE typ;
```

## Syntax

<div id="rrdiagram"></div>

## Dependencies of Dropped Objects

DuckDB performs limited dependency tracking for some object types.
By default or if the `RESTRICT` clause is provided, the entry will not be dropped if there are any other objects that depend on it.
If the `CASCADE` clause is provided then all the objects that are dependent on the object will be dropped as well.

```sql
CREATE SCHEMA myschema;
CREATE TABLE myschema.t1 (i INTEGER);
DROP SCHEMA myschema;
```

```console
Dependency Error:
Cannot drop entry "myschema" because there are entries that depend on it.
table "t1" depends on schema "myschema".
Use DROP...CASCADE to drop all dependents.
```

The `CASCADE` modifier drops both myschema and `myschema.t1`:

```sql
CREATE SCHEMA myschema;
CREATE TABLE myschema.t1 (i INTEGER);
DROP SCHEMA myschema CASCADE;
```

The following dependencies are tracked and thus will raise an error if the user tries to drop the depending object without the `CASCADE` modifier.

| Depending object type | Dependent object type |
|--|--|
| `SCHEMA` | `FUNCTION` |
| `SCHEMA` | `INDEX` |
| `SCHEMA` | `MACRO TABLE` |
| `SCHEMA` | `MACRO` |
| `SCHEMA` | `SCHEMA` |
| `SCHEMA` | `SEQUENCE` |
| `SCHEMA` | `TABLE` |
| `SCHEMA` | `TYPE` |
| `SCHEMA` | `VIEW` |
| `TABLE`  | `INDEX` |

## Limitations

### Dependencies on Views

Currently, dependencies are not tracked for views. For example, if a view is created that references a table and the table is dropped, then the view will be in an invalid state:

```sql
CREATE TABLE tbl (i INTEGER);
CREATE VIEW view1 AS
    SELECT i FROM tbl;
DROP TABLE tbl RESTRICT;
SELECT * FROM view1;
```

This returns the following error message:

```console
Catalog Error:
Table with name tbl does not exist!
```

## Limitations on Reclaiming Disk Space

Running `DROP TABLE` should free the memory used by the table, but not always disk space.
Even if disk space does not decrease, the free blocks will be marked as `free`.
For example, if we have a 2 GB file and we drop a 1 GB table, the file might still be 2 GB, but it should have 1 GB of free blocks in it.
To check this, use the following `PRAGMA` and check the number of `free_blocks` in the output:

```sql
PRAGMA database_size;
```

For instructions on reclaiming space after dropping a table, refer to the [“Reclaiming space” page]({% link docs/preview/operations_manual/footprint_of_duckdb/reclaiming_space.md %}).
