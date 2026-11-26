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

The `REGISTER EXTERNAL RESOURCE` statement [adopts]({% link docs/2.0/resources/overview.md %}#terms) an [underlying resource]({% link docs/2.0/resources/overview.md %}#terms) by its [handle]({% link docs/2.0/resources/overview.md %}#terms), and creates a [resource registration]({% link docs/2.0/resources/resource_registrations.md %}) for it under a name. The handle is the `MAP(VARCHAR, VARCHAR)` that the create callback of the external resource type returns for the underlying resource. The create callback is not called: DuckDB calls the status callback with the handle until it reports `ready`, and the endpoint of the resource registration is the one the status callback reports. See [Lifecycle Callbacks]({% link docs/2.0/resources/resource_types.md %}#lifecycle-callbacks).

A resource registration created with `REGISTER EXTERNAL RESOURCE` is used and torn down like one created with [`CREATE EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/create_external_resource.md %}): [`DESTROY EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/destroy_external_resource.md %}) calls the destroy callback of its external resource type.

> Note `REGISTER EXTERNAL RESOURCE` is refused when [`enable_external_access`]({% link docs/2.0/configuration/overview.md %}#configuration-reference) is `false`. See [Restrictions]({% link docs/2.0/resources/overview.md %}#restrictions).

## Syntax

```sql
REGISTER EXTERNAL RESOURCE ⟨type⟩ AS ⟨name⟩ FROM ⟨handle⟩;
```

`⟨type⟩` is the name of a registered external resource type, written as described in [External Resource Type Names]({% link docs/2.0/resources/resource_types.md %}#external-resource-type-names). `⟨handle⟩` is an expression. `⟨name⟩` is the name of the resource registration.

## Examples

Create a resource registration from a handle. The create callback of the external resource type, `r_create`, does not exist; it is not called:

```sql
CREATE MACRO r_status(h) AS TABLE
    SELECT 'ready' AS state, MAP {'uri': ':memory:', 'attached_db_type': 'duckdb'} AS result;
CALL register_external_resource_type(
    'mem@local',
    kind := 'catalog',
    create_function := 'r_create',
    status_function := 'r_status'
);
REGISTER EXTERNAL RESOURCE 'mem@local' AS existing FROM MAP {'id': 'm1'};
SELECT name, type, managed FROM (SHOW EXTERNAL RESOURCES);
```

| name     | type      | managed |
|----------|-----------|---------|
| existing | mem@local | true    |
