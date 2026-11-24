---
layout: docu
redirect_from:
- /docs/current/sql/statements/register_external_resource
- /docs/lts/sql/statements/register_external_resource
- /docs/preview/sql/statements/register_external_resource
- /docs/stable/sql/statements/register_external_resource
title: REGISTER EXTERNAL RESOURCE Statement
---

<!-- ref: duckdb/duckdb#23736 duckdb/duckdb-web#7004 -->

> New The `REGISTER EXTERNAL RESOURCE` statement was introduced in DuckDB 2.0.0.

The `REGISTER EXTERNAL RESOURCE` statement records an [external resource]({% link docs/2.0/sql/statements/create_external_resource.md %}) that already exists under a name, from its handle: the `MAP` that the create function of its type would return. The create function is not called; the endpoint of the resource comes from the status function of its type. A registered resource is attached and destroyed like one created with [`CREATE EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/create_external_resource.md %}).

## Syntax

```sql
REGISTER EXTERNAL RESOURCE ⟨type⟩ AS ⟨name⟩ FROM ⟨handle⟩;
```

The handle is an expression. The type is written as for [`CREATE EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/create_external_resource.md %}#writing-a-type-name).

## Examples

Register an existing resource. The type's create function, `r_create`, does not exist; it is not called:

```sql
CREATE MACRO r_status(h) AS TABLE SELECT 'ready' AS state, MAP {'uri': ':memory:', 'attached_db_type': 'duckdb'} AS result;
CALL register_external_resource_type('mem@local', kind := 'catalog', create_function := 'r_create', status_function := 'r_status');
REGISTER EXTERNAL RESOURCE 'mem@local' AS existing FROM MAP {'id': 'm1'};
SELECT name, type, managed FROM (SHOW EXTERNAL RESOURCES);
```

| name     | type      | managed |
|----------|-----------|---------|
| existing | mem@local | true    |
