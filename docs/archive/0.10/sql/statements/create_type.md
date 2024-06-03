---
layout: docu
railroad: statements/createtype.js
title: CREATE TYPE Statement
---

The `CREATE TYPE` statement defines a new type in the catalog.

## Examples

Create a simple `ENUM` type:

```sql
CREATE TYPE mood AS ENUM ('happy', 'sad', 'curious');
```

Create a simple `STRUCT` type:

```sql
CREATE TYPE many_things AS STRUCT(k INTEGER, l VARCHAR);
```

Create a simple `UNION` type:

```sql
CREATE TYPE one_thing AS UNION(number INTEGER, string VARCHAR);
```

Create a type alias:

```sql
CREATE TYPE x_index AS INTEGER;
```

## Syntax

<div id="rrdiagram"></div>

The `CREATE TYPE` clause defines a new data type available to this DuckDB instance.
These new types can then be inspected in the [`duckdb_types` table](../duckdb_table_functions#duckdb_types).

## Limitations

Extending types to support custom operators (such as the PostgreSQL `&&` operator) is not possible via plain SQL.
Instead, it requires adding additional C++ code. To do this, create an [extension](../../extensions/overview).