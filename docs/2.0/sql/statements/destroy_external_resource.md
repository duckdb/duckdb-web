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

The `DESTROY EXTERNAL RESOURCE` statement destroys an [external resource]({% link docs/2.0/resources/overview.md %}): it calls the [destroy function]({% link docs/2.0/resources/overview.md %}#type-functions) of its type and removes the record of the resource. Databases attached to the resource with [`ATTACH TO EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/attach.md %}#attach-to-external-resource) are detached.

## Syntax

```sql
DESTROY EXTERNAL RESOURCE ⟨name⟩;
```

## Examples

Create a resource and destroy it:

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

Destroying a name that is not registered is an error:

```sql
DESTROY EXTERNAL RESOURCE nope;
```

```console
… not registered …
```
