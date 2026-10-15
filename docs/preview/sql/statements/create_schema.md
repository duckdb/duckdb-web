---
layout: docu
railroad: statements/createschema.js
tested: true
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

Create a schema or replace a schema if it exists:

```sql
CREATE OR REPLACE SCHEMA s2;
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

## Nested Schemas

> New Support for nested schemas is introduced in DuckDB 2.0.

Schemas can be nested within other schemas. Objects in a nested schema are referenced using their fully qualified, dot-separated path:

```sql
CREATE SCHEMA finance;
CREATE SCHEMA finance.reports;
CREATE TABLE finance.reports.q3 (revenue DECIMAL);
```

## Syntax

<div id="rrdiagram"></div>
