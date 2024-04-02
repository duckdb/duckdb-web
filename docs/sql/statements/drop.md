---
layout: docu
title: DROP Statement
railroad: statements/drop.js
---

The `DROP` statement removes a catalog entry added previously with the `CREATE` command.

## Examples

```sql
-- delete the table with the name "tbl"
DROP TABLE tbl;
-- drop the view with the name "v1"; do not throw an error if the view does not exist
DROP VIEW IF EXISTS v1;
```

```sql
-- drop function "fn"
DROP FUNCTION fn;
-- drop index "idx"
DROP INDEX idx;
-- drop schema "sch"
DROP SCHEMA sch;
-- drop sequence "seq"
DROP SEQUENCE seq;
-- drop macro "mcr"
DROP MACRO mcr;
-- drop macro table "mt"
DROP MACRO TABLE mt;
-- drop type "typ"
DROP TYPE typ;
```

## Syntax

<div id="rrdiagram"></div>

The optional `IF EXISTS` clause suppresses the error that would normally result if the table does not exist.

By default (or if the `RESTRICT` clause is provided), the entry will not be dropped if there are any other objects that depend on it. If the `CASCADE` clause is provided then all the objects that are dependent on the object will be dropped as well.

```sql
CREATE SCHEMA myschema;
CREATE TABLE myschema.t1 (i INTEGER);
-- ERROR: Cannot drop myschema because the table myschema.t1 depends on it.
DROP SCHEMA myschema;
-- Cascade drops both myschema and myschema.t1
DROP SCHEMA myschema CASCADE;
```

## Limitations on Reclaiming Disk Space

Running `DROP TABLE` should free the memory used by the table, but not always disk space.
Even if disk space does not decrease, the free blocks will be marked as "free".
For example, if we have a 2 GB file and we drop a 1 GB table, the file might still be 2 GB, but it should have 1 GB of free blocks in it.
To check this, use the following `PRAGMA` and check the number of `free_blocks` in the output:

```sql
PRAGMA database_size;
```
