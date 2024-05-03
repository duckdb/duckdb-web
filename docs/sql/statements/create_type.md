---
layout: docu
title: CREATE TYPE Statement
railroad: statements/createtype.js
---

The `CREATE TYPE` statement defines a new type in the catalog.

## Examples

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

## Syntax

<div id="rrdiagram"></div>

The `CREATE TYPE` clause defines a new data type available to this DuckDB instance.
These new types can then be inspected in the [`duckdb_types` table](../duckdb_table_functions#duckdb_types).

## Limitations

Extending types to support custom operators (such as the PostgreSQL `&&` operator) is not possible via plain SQL.
Instead, it requires adding additional C++ code. To do this, create an [extension](../../extensions/overview).
