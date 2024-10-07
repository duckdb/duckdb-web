---
layout: docu
railroad: statements/createschema.js
title: CREATE SCHEMA Statement
---

The `CREATE SCHEMA` statement creates a schema in the catalog. The default schema is `main`.

## Examples

Create a schema:

```sql
CREATE SCHEMA s1;
```

Create a schema if it does not exist yet:

```sql
CREATE SCHEMA IF NOT EXISTS s2;
```

Create table in the schemas:

```sql
CREATE TABLE s1.t (id INTEGER PRIMARY KEY, other_id INTEGER);
CREATE TABLE s2.t (id INTEGER PRIMARY KEY, j VARCHAR);
```

Compute a join between tables from two schemas:

```sql
SELECT *
FROM s1.t s1t, s2.t s2t
WHERE s1t.other_id = s2t.id;
```

## Syntax

<div id="rrdiagram"></div>