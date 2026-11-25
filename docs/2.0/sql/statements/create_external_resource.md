---
layout: docu
redirect_from:
- /docs/current/sql/statements/create_external_resource
- /docs/lts/sql/statements/create_external_resource
- /docs/preview/sql/statements/create_external_resource
- /docs/stable/sql/statements/create_external_resource
title: CREATE EXTERNAL RESOURCE Statement
---

<!-- ref: duckdb/duckdb#23731 duckdb/duckdb-web#7003 duckdb/duckdb#23736 duckdb/duckdb-web#7004 duckdb/duckdb#29056 duckdb/duckdb-web#7856 -->

> New External resources were introduced in DuckDB 2.0.0.

The `CREATE EXTERNAL RESOURCE` statement creates an [external resource]({% link docs/2.0/resources/overview.md %}), such as a database server, of a registered [resource type]({% link docs/2.0/resources/overview.md %}#resource-types), and records it under a name. The other statements on external resources are:

* [`REGISTER EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/register_external_resource.md %}) records a resource that already exists.
* [`ATTACH TO EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/attach.md %}#attach-to-external-resource) and [`CONNECT TO EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/connect.md %}) use the database of a resource.
* [`SHOW EXTERNAL RESOURCES`]({% link docs/2.0/sql/statements/show.md %}#show-external-resources-statement) lists the recorded resources.
* [`DESTROY EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/destroy_external_resource.md %}) destroys a resource.

> Note `CREATE EXTERNAL RESOURCE` is refused when external access is disabled. See [Restrictions]({% link docs/2.0/resources/overview.md %}#restrictions).

## Syntax

```sql
CREATE EXTERNAL RESOURCE ⟨type⟩ AS ⟨name⟩ [(⟨option⟩ [⟨value⟩], ...)];
```

* `⟨type⟩` is the name of a registered resource type, written as described in [Writing a Type Name]({% link docs/2.0/resources/overview.md %}#writing-a-type-name).
* `⟨name⟩` is the name under which the resource is recorded. Resource names are [unique]({% link docs/2.0/resources/overview.md %}#resources).
* The options and their values are passed to the [create function]({% link docs/2.0/resources/overview.md %}#type-functions) of the type.

`CREATE EXTERNAL RESOURCE` calls the create function of the type, then its status function until the resource is ready, and records the resource with its handle and endpoint.

The name is required:

```sql
CREATE EXTERNAL RESOURCE 'mem@local';
```

```console
Binder Error: EXTERNAL RESOURCE requires a name (AS <name>)
```

## Examples

Register a resource type defined with table macros, create a resource of that type, and list it:

```sql
CREATE MACRO dt_create(p) AS TABLE SELECT MAP {'id': 'd1'} AS handle;
CREATE MACRO dt_status(h) AS TABLE
    SELECT 'ready' AS state, MAP {'uri': ':memory:', 'attached_db_type': 'duckdb'} AS result;
CREATE MACRO dt_destroy(h) AS TABLE SELECT 'gone' AS status;
CALL register_external_resource_type(
    'test.dotted.type',
    kind := 'catalog',
    create_function := 'dt_create',
    status_function := 'dt_status',
    destroy_function := 'dt_destroy'
);
CREATE EXTERNAL RESOURCE test.dotted.type AS created;
SELECT name, type FROM (SHOW EXTERNAL RESOURCES);
```

| name    | type             |
|---------|------------------|
| created | test.dotted.type |
