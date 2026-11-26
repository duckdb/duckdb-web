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

The `CREATE EXTERNAL RESOURCE` statement [provisions]({% link docs/2.0/resources/overview.md %}#terms) an [underlying resource]({% link docs/2.0/resources/overview.md %}#terms), such as a database server, of a registered [external resource type]({% link docs/2.0/resources/resource_types.md %}), and creates a [resource registration]({% link docs/2.0/resources/resource_registrations.md %}) for it under a name. The other [statements on external resources]({% link docs/2.0/resources/overview.md %}#sql-statements) are:

* [`REGISTER EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/register_external_resource.md %}) creates a resource registration for an underlying resource from its handle.
* [`ATTACH TO EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/attach.md %}#attach-to-external-resource) and [`CONNECT TO EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/connect.md %}) use the endpoint of an underlying resource.
* [`SHOW EXTERNAL RESOURCES`]({% link docs/2.0/sql/statements/show.md %}#show-external-resources-statement) lists the resource registrations.
* [`DESTROY EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/destroy_external_resource.md %}) tears down an underlying resource and removes its resource registration.

> Note `CREATE EXTERNAL RESOURCE` is refused when [`enable_external_access`]({% link docs/2.0/configuration/overview.md %}#configuration-reference) is `false`. See [Restrictions]({% link docs/2.0/resources/overview.md %}#restrictions).

## Syntax

```sql
CREATE EXTERNAL RESOURCE ⟨type⟩ AS ⟨name⟩ [(⟨option⟩ [⟨value⟩], ...)];
```

* `⟨type⟩` is the name of a registered external resource type, written as described in [External Resource Type Names]({% link docs/2.0/resources/resource_types.md %}#external-resource-type-names).
* `⟨name⟩` is the name of the resource registration. Resource registration names are [unique]({% link docs/2.0/resources/resource_registrations.md %}) within the DuckDB instance.
* The options and their values are passed to the create callback of the external resource type, as a `MAP(VARCHAR, VARCHAR)` with the option names in lowercase. See [Lifecycle Callbacks]({% link docs/2.0/resources/resource_types.md %}#lifecycle-callbacks).

`CREATE EXTERNAL RESOURCE` calls the create callback of the external resource type, then its status callback until it reports `ready`, and creates a resource registration with the handle and the endpoint they reported.

## Examples

Register an external resource type with table macros as its lifecycle callbacks, create a resource registration of that external resource type, and list it:

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

## Errors

The name is required:

```sql
CREATE EXTERNAL RESOURCE 'mem@local';
```

```console
Binder Error: EXTERNAL RESOURCE requires a name (AS <name>)
```

An unquoted [external resource type name]({% link docs/2.0/resources/resource_types.md %}#external-resource-type-names) is folded to lowercase, and a name that is not registered is an error:

```sql
CREATE EXTERNAL RESOURCE Nobody.Provides.THIS AS r;
```

```console
… unknown resource type "nobody.provides.this" …
```

A name with characters other than letters, digits, `_`, `.` and `-` must be written as a string literal:

```sql
CREATE EXTERNAL RESOURCE aws:cloudformation:stack AS r;
```

```console
Parser Error: …
```

A resource registration name that is already registered is an error:

```sql
CREATE MACRO n_create(p) AS TABLE SELECT MAP {'id': 'n1'} AS handle;
CREATE MACRO n_status(h) AS TABLE
    SELECT 'ready' AS state, MAP {'uri': ':memory:', 'attached_db_type': 'duckdb'} AS result;
CALL register_external_resource_type(
    'mem@local',
    kind := 'catalog',
    create_function := 'n_create',
    status_function := 'n_status'
);
CREATE EXTERNAL RESOURCE 'mem@local' AS r;
CREATE EXTERNAL RESOURCE 'mem@local' AS r;
```

```console
Invalid Input Error: external resource "r" is already registered
```

An external resource type without a status callback cannot provision an underlying resource:

```sql
CREATE MACRO s_create(p) AS TABLE SELECT MAP {'id': 's1'} AS handle;
CALL register_external_resource_type('mem@local', kind := 'catalog', create_function := 's_create');
CREATE EXTERNAL RESOURCE 'mem@local' AS r;
```

```console
… resource type "mem@local" has no status function (required to await readiness)
```

For a `catalog` external resource type, a status callback whose `result` lacks the `uri` is an error:

```sql
CREATE MACRO c_create(p) AS TABLE SELECT MAP {'id': 'c1'} AS handle;
CREATE MACRO c_status(h) AS TABLE SELECT 'ready' AS state, MAP {'foo': 'bar'} AS result;
CALL register_external_resource_type(
    'cat@local',
    kind := 'catalog',
    create_function := 'c_create',
    status_function := 'c_status'
);
CREATE EXTERNAL RESOURCE 'cat@local' AS r;
```

```console
… catalog resource "cat@local" is missing 'uri' in its status result
```

When [`enable_external_access`]({% link docs/2.0/configuration/overview.md %}#configuration-reference) is `false`, `CREATE EXTERNAL RESOURCE` is refused:

```sql
CREATE MACRO mock_create(p) AS TABLE SELECT MAP {'id': 'r1'} AS handle;
CALL register_external_resource_type(
    'mock@local',
    kind := 'catalog',
    create_function := 'mock_create'
);
SET enable_external_access = false;
CREATE EXTERNAL RESOURCE 'mock@local' AS res;
```

```console
Permission Error: External resources are disabled through configuration
```
