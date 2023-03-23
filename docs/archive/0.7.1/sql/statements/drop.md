---
layout: docu
title: Drop Statement
selected: Documentation/SQL/Drop
expanded: SQL
railroad: statements/drop.js
---
The `DROP` statement removes a catalog entry added previously with the `CREATE` command.

### Examples
```sql
-- delete the table with the name "tbl"
DROP TABLE tbl;
-- drop the view with the name "v1"; do not throw an error if the view does not exist
DROP VIEW IF EXISTS v1;
```

### Syntax
<div id="rrdiagram"></div>

The optional `IF EXISTS` clause suppresses the error that would normally result if the table does not exist.

By default (or if the `RESTRICT` clause is provided), the entry will not be dropped if there are any other objects that depend on it. If the `CASCADE` clause is provided then all the objects that are dependent on the object will be dropped as well.

```sql
CREATE SCHEMA myschema;
CREATE TABLE myschema.t1(i INTEGER);
-- ERROR: Cannot drop myschema because the table myschema.t1 depends on it.
DROP SCHEMA myschema;
-- Cascade drops both myschema and myschema.1
DROP SCHEMA myschema CASCADE;
```

