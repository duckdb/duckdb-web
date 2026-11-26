---
layout: docu
redirect_from:
- /docs/current/sql/statements/destroy_external_resource
- /docs/lts/sql/statements/destroy_external_resource
- /docs/preview/sql/statements/destroy_external_resource
- /docs/stable/sql/statements/destroy_external_resource
title: DESTROY EXTERNAL RESOURCE Statement
---

<!-- ref: duckdb/duckdb#23736 duckdb/duckdb-web#7004 -->

> New The `DESTROY EXTERNAL RESOURCE` statement was introduced in DuckDB 2.0.0.

The `DESTROY EXTERNAL RESOURCE` statement [tears down]({% link docs/2.0/resources/overview.md %}#terms) the [underlying resource]({% link docs/2.0/resources/overview.md %}#terms) of a [resource registration]({% link docs/2.0/resources/resource_registrations.md %}), and removes the resource registration. It runs the deleter binding of the resource registration, which calls the destroy callback of its external resource type with the handle. The resource registration is removed only when the destroy callback raises no error; with an empty deleter binding, no lifecycle callback is called, and the resource registration is removed. Afterwards, the databases attached with [`ATTACH TO EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/attach.md %}#attach-to-external-resource) are detached. See [Resource Registrations]({% link docs/2.0/resources/resource_registrations.md %}).

## Syntax

```sql
DESTROY EXTERNAL RESOURCE ⟨name⟩;
```

`⟨name⟩` is the name of a resource registration.

> Note `DESTROY EXTERNAL RESOURCE` is refused when [`enable_external_access`]({% link docs/2.0/configuration/overview.md %}#configuration-reference) is `false`. See [Restrictions]({% link docs/2.0/resources/overview.md %}#restrictions).

## Examples

Create a resource registration and tear it down:

```sql
CREATE MACRO d_create(p) AS TABLE SELECT MAP {'id': 'd1'} AS handle;
CREATE MACRO d_status(h) AS TABLE
    SELECT 'ready' AS state, MAP {'uri': ':memory:', 'attached_db_type': 'duckdb'} AS result;
CREATE MACRO d_destroy(h) AS TABLE SELECT 'gone' AS status;
CALL register_external_resource_type(
    'mem@local',
    kind := 'catalog',
    create_function := 'd_create',
    status_function := 'd_status',
    destroy_function := 'd_destroy'
);
CREATE EXTERNAL RESOURCE 'mem@local' AS r;
DESTROY EXTERNAL RESOURCE r;
SELECT count(*) AS resources FROM (SHOW EXTERNAL RESOURCES);
```

| resources |
|-----------|
| 0         |

A name without a resource registration is an error:

```sql
DESTROY EXTERNAL RESOURCE nope;
```

```console
… not registered …
```
