---
layout: docu
title: Create Type
selected: Documentation/SQL/Create Type
expanded: SQL
railroad: statements/createtype.js
---
The `CREATE Type` statement defines a new type in the catalog.

### Examples

```sql
-- create a simple enum type
CREATE TYPE mood AS ENUM ('happy', 'sad', 'curious');
-- create a simple struct type
CREATE TYPE many_things AS STRUCT(k INTEGER, l VARCHAR);
-- create a simple union type
CREATE TYPE one_thing AS UNION(number INTEGER, string VARCHAR);
-- create a type alias
CREATE TYPE x_index AS INTEGER;
```

### Syntax

<div id="rrdiagram"></div>

`CREATE TYPE` defines a new data type available to this duckdb instance. These new
types can then be inspected in the `duckdb_types` table.

Extending these custom types to support custom operators (such as the Postgres `&&` operator)
would require C++ development. But that can be done in an extension!
