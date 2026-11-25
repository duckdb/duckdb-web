---
layout: docu
redirect_from:
- /docs/current/resources/overview
- /docs/lts/resources/overview
- /docs/preview/resources/overview
- /docs/stable/resources/overview
title: External Resources
---

<!-- ref: duckdb/duckdb#23731 duckdb/duckdb-web#7003 duckdb/duckdb#23736 duckdb/duckdb-web#7004 -->

> New External resources were introduced in DuckDB 2.0.0.

An external resource is something outside DuckDB, such as a database server, that DuckDB creates, uses and destroys through SQL. How a resource is created, checked and destroyed is defined by its [resource type](#resource-types): a named set of functions that DuckDB calls at each step of the resource's lifecycle. DuckDB tracks each resource it manages under a local name, so that statements refer to the resource by that name while the details of the resource stay with its type.

## Resource Types

A resource type is registered by calling the `register_external_resource_type` function with the name of the type, its [kind](#resource-type-kinds) and the names of its [type functions](#type-functions):

```sql
register_external_resource_type(⟨name⟩, kind := ⟨kind⟩, create_function := ⟨function⟩ [, status_function := ⟨function⟩] [, destroy_function := ⟨function⟩] [, list_function := ⟨function⟩] [, resolve_function := ⟨function⟩])
```

`kind` and `create_function` are required. Extensions register their own types when they are loaded; a type can also be defined in SQL, with table macros as its type functions. The registered types are listed by [`SHOW EXTERNAL RESOURCE TYPES`]({% link docs/2.0/sql/statements/show.md %}#show-external-resource-types-statement) and [`duckdb_external_resource_types()`]({% link docs/2.0/sql/meta/duckdb_table_functions.md %}#duckdb_external_resource_types).

A type name is registered only once; registering it again is an error, and a registered type cannot be changed or removed:

```sql
CREATE MACRO t_create(p) AS TABLE SELECT MAP {'id': 't1'} AS handle;
CALL register_external_resource_type('mem@local', kind := 'catalog', create_function := 't_create');
CALL register_external_resource_type('mem@local', kind := 'catalog', create_function := 't_create');
```

```console
Invalid Input Error: external resource type "mem@local" is already registered
```

### Writing a Type Name

<!-- ref: duckdb/duckdb#29056 duckdb/duckdb-web#7856 -->

A type name is a string literal, such as `'mem@local'`. Since DuckDB 2.0.1, a type name can also be written as a dotted name without quotes. A dotted name is folded to lowercase like an identifier; a quoted type name is taken as written:

```sql
CREATE EXTERNAL RESOURCE Nobody.Provides.THIS AS r;
```

```console
… unknown resource type "nobody.provides.this" …
```

```sql
CREATE EXTERNAL RESOURCE 'Nobody.Provides.THIS' AS r;
```

```console
… unknown resource type "Nobody.Provides.THIS" …
```

A type name with other characters, such as a colon, with spaces around a dot, or with a trailing or doubled dot, must be quoted:

```sql
CREATE EXTERNAL RESOURCE aws:cloudformation:stack AS r;
```

```console
Parser Error: …
```

This applies wherever a statement takes a type name: [`CREATE EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/create_external_resource.md %}), [`REGISTER EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/register_external_resource.md %}), `ATTACH TO NEW TEMPORARY EXTERNAL RESOURCE`, `CONNECT TO NEW TEMPORARY EXTERNAL RESOURCE` and `SHOW EXTERNAL RESOURCES WITH TYPE`.

### Types Provided by Extensions

If a type is not registered but a known extension provides it, DuckDB autoloads that extension. With autoloading disabled, the error names the extension and the statements to install and load it.

## Type Functions

The type functions of a resource type are table functions or table macros. DuckDB calls them, not the user: each statement and function on this page calls the type functions it needs. DuckDB runs them on a separate internal connection, so they must be visible to every connection: a `TEMP` macro cannot be a type function. Unqualified function names are resolved in the search path that was in effect when the type was registered.

* The **create function** creates a resource. It receives the options of the statement as a `MAP(VARCHAR, VARCHAR)` and returns one row with a `handle` column: a `MAP` that identifies the resource to its type.
* The **status function** reports the state of a resource. It receives the handle and returns a `state` and a `result`. DuckDB calls it repeatedly until the state is `ready`; a state of `failed` is an error. When the state is `ready`, `result` is a `MAP` with the endpoint of the resource: its `uri` and `attached_db_type`, and further options for attaching it.
* The **destroy function** destroys a resource. It receives the handle.
* The **list function** reports the resources of the type that exist outside DuckDB, for [discovery](#discovery). It returns one row per resource, with a `handle`, a `name`, a `reference` and a `state`.
* The **resolve function** is recorded with the type and shown by `duckdb_external_resource_types()`; DuckDB does not call it.

Creating a resource requires a status function:

```sql
CREATE MACRO s_create(p) AS TABLE SELECT MAP {'id': 's1'} AS handle;
CALL register_external_resource_type('mem@local', kind := 'catalog', create_function := 's_create');
CREATE EXTERNAL RESOURCE 'mem@local' AS r;
```

```console
… resource type "mem@local" has no status function (required to await readiness)
```

## Resource Type Kinds

The `kind` of a resource type classifies it. It is chosen by whoever registers the type and is shown in the listings of types. The types of the [`aws` extension]({% link docs/2.0/core_extensions/aws.md %}), for example, have the following kinds:

| Type | Kind |
|:--|:--|
| `aws.cloudformation.stack` | `storage` |
| `aws.s3.bucket` | `storage` |
| `aws.s3tables.bucket` | `catalog` |
| `aws.system-table` | `catalog` |

The kind `catalog` marks a type whose resources provide a database. For a `catalog` type, the `result` of the status function must contain the endpoint of the database: its `uri` and its `attached_db_type`. Such a resource can be attached with [`ATTACH TO EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/attach.md %}#attach-to-external-resource) or connected to with [`CONNECT TO EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/connect.md %}). A status result that lacks the `uri` is an error when the resource is created:

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

## Resources

DuckDB records each resource created with [`CREATE EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/create_external_resource.md %}) or registered with [`REGISTER EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/register_external_resource.md %}). A record holds:

* the **name** of the resource: a local name, given with `AS ⟨name⟩`, by which statements refer to the resource. Resource names are unique.
* the **type** of the resource.
* the **handle**: the `MAP` that identifies the resource to its type, passed to the status and destroy functions.
* the **endpoint**: the `uri` and `attached_db_type` from the status function, used to attach the resource. A resource created or registered with a statement must have a `uri`.
* the **deleter binding**: the destroy function of the type and the handle, used to destroy the resource.

A resource with a name that is already recorded is an error:

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

The records are kept in memory and shared by all connections of a DuckDB instance; they are not stored in a database file. The resources themselves exist outside DuckDB and outlive the instance: after a restart, a resource that still exists is recorded again with `REGISTER EXTERNAL RESOURCE`. The records are not transactional: a record is kept when the transaction that made it is rolled back, because the resource exists whether or not the transaction commits.

The recorded resources are listed by [`SHOW EXTERNAL RESOURCES`]({% link docs/2.0/sql/statements/show.md %}#show-external-resources-statement) and [`duckdb_external_resources()`]({% link docs/2.0/sql/meta/duckdb_table_functions.md %}#duckdb_external_resources).

## Lifecycle

Each resource is destroyed by whatever owns it. Depending on how a statement refers to a resource, the resource is owned by the statement, recorded until it is destroyed, or borrowed:

| Statement | Type functions called | The resource is destroyed by |
|:--|:--|:--|
| [`CREATE EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/create_external_resource.md %}) | create, then status until `ready` | `DESTROY EXTERNAL RESOURCE` |
| [`REGISTER EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/register_external_resource.md %}) | status until `ready` | `DESTROY EXTERNAL RESOURCE` |
| [`ATTACH TO NEW TEMPORARY EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/attach.md %}#attach-to-external-resource), [`CONNECT TO NEW TEMPORARY EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/connect.md %}) | create, then status until `ready` | `DETACH`, `DISCONNECT` |
| `ATTACH TO EXTERNAL RESOURCE ⟨name⟩`, `CONNECT TO EXTERNAL RESOURCE ⟨name⟩` | none | not by this statement |
| [`DESTROY EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/destroy_external_resource.md %}) | destroy | |

* `CREATE EXTERNAL RESOURCE` creates a resource and records it.
* `REGISTER EXTERNAL RESOURCE` records a resource that already exists, from its handle, without calling the create function.
* `NEW TEMPORARY` creates a resource for one attachment or connection, without recording it; `DETACH` or `DISCONNECT` destroys it.
* `ATTACH TO EXTERNAL RESOURCE ⟨name⟩` and `CONNECT TO EXTERNAL RESOURCE ⟨name⟩` use a recorded resource without owning it: `DETACH` and `DISCONNECT` leave it in place.
* `DESTROY EXTERNAL RESOURCE` calls the destroy function of a recorded resource, removes its record and detaches the databases attached to it. This applies to resources recorded with `REGISTER EXTERNAL RESOURCE` as well.

If creating a resource fails after the create function was called, DuckDB destroys the resource it created. A resource given by its handle is never destroyed on a failure.

## Discovery

The list function of a type reports the resources of that type that exist outside DuckDB, including resources that no DuckDB instance has recorded. [`SHOW ALL EXTERNAL RESOURCES`]({% link docs/2.0/sql/statements/show.md %}#show-external-resources-statement) and `duckdb_external_resources(discover := true)` add them to the recorded resources, with `managed` set to `false`. A reported resource with the same type and handle as a recorded one is shown once, as the recorded resource. A reported resource can be recorded with `REGISTER EXTERNAL RESOURCE`, using its handle.

```sql
CREATE MACRO l_list(opts) AS TABLE
    SELECT * FROM (VALUES
        (MAP {'id': 'd1'}, 'dee-one', 'ext-1', 'running'),
        (MAP {'id': 'd2'}, 'dee-two', 'ext-2', 'stopped')
    ) t(handle, name, reference, state);
CALL register_external_resource_type(
    'mock@disc',
    kind := 'catalog',
    create_function := 'l_create',
    list_function := 'l_list'
);
SELECT name, type, managed, state, reference
FROM duckdb_external_resources(discover := true)
ORDER BY reference;
```

| name    | type      | managed | state   | reference |
|---------|-----------|---------|---------|-----------|
| dee-one | mock@disc | false   | running | ext-1     |
| dee-two | mock@disc | false   | stopped | ext-2     |

## Functions

The statements are built on the following table functions, which can also be called directly. Unlike the statements, `create_external_resource` and `destroy_external_resource` do not record a resource: the caller owns the resource they create.

### `create_external_resource`

`create_external_resource(⟨type⟩ [, params := ⟨map⟩] [, handle := ⟨map⟩] [, timeout_seconds := ⟨n⟩] [, poll_interval_seconds := ⟨n⟩])` creates a resource of a type: it calls the create function with `params`, then the status function until the state is `ready`. It returns the resource's `handle`, `uri` and `attached_db_type`, the full `result` of the status function, and a `deleter_function` and `deleter_payload` for [`destroy_external_resource`](#destroy_external_resource).

```sql
CREATE MACRO mock_create(p) AS TABLE SELECT MAP {'id': 'r1'} AS handle;
CREATE MACRO mock_status(h) AS TABLE
    SELECT
        'ready' AS state,
        MAP {'uri': 'quack:localhost:9494', 'attached_db_type': 'quack'} AS result;
CALL register_external_resource_type(
    'mock@local',
    kind := 'catalog',
    create_function := 'mock_create',
    status_function := 'mock_status'
);
SELECT handle, uri, attached_db_type FROM create_external_resource('mock@local');
```

| handle  | uri                  | attached_db_type |
|---------|----------------------|------------------|
| {id=r1} | quack:localhost:9494 | quack            |

With `handle :=`, the create function is not called; the status function resolves the given handle. The type's create function, `mock_create`, does not exist here:

```sql
CREATE MACRO mock_status(h) AS TABLE
    SELECT
        'ready' AS state,
        MAP {'uri': 'quack:localhost:9494', 'attached_db_type': 'quack'} AS result;
CALL register_external_resource_type(
    'mock@local',
    kind := 'catalog',
    create_function := 'mock_create',
    status_function := 'mock_status'
);
SELECT handle, uri FROM create_external_resource('mock@local', handle := MAP {'id': 'adopted'});
```

| handle       | uri                  |
|--------------|----------------------|
| {id=adopted} | quack:localhost:9494 |

`timeout_seconds` is between 0 and 2592000; `poll_interval_seconds` is between 1 and 2592000.

### `destroy_external_resource`

`destroy_external_resource(⟨deleter_function⟩, ⟨payload⟩)` destroys a resource created with [`create_external_resource`](#create_external_resource), using the `deleter_function` and `deleter_payload` it returned:

```sql
CREATE MACRO mock_create(p) AS TABLE SELECT MAP {'id': 'r1'} AS handle;
CREATE MACRO mock_status(h) AS TABLE
    SELECT
        'ready' AS state,
        MAP {'uri': 'quack:localhost:9494', 'attached_db_type': 'quack'} AS result;
CREATE MACRO mock_destroy(h) AS TABLE SELECT 'ok' AS status;
CALL register_external_resource_type(
    'mock@local',
    kind := 'catalog',
    create_function := 'mock_create',
    status_function := 'mock_status',
    destroy_function := 'mock_destroy'
);
SET VARIABLE resource = (
    SELECT {'fn': deleter_function, 'payload': deleter_payload}
    FROM create_external_resource('mock@local')
);
CALL destroy_external_resource(getvariable('resource').fn, getvariable('resource').payload);
```

| Success |
|---------|
| true    |

### `register_external_resource` and `deregister_external_resource`

`register_external_resource(⟨type⟩, ⟨name⟩, ⟨handle⟩ [, uri := ⟨uri⟩] [, attached_db_type := ⟨type⟩] [, deleter_function := ⟨function⟩])` records a resource under a name with the given handle and endpoint, without calling any type function. Unlike `REGISTER EXTERNAL RESOURCE`, it does not check the resource with its status function. `deregister_external_resource(⟨name⟩)` removes the record and leaves the resource itself in place:

```sql
CALL register_external_resource('mock@local', 'r1', MAP {'id': 'abc'});
CALL deregister_external_resource('r1');
SELECT count(*) AS resources FROM duckdb_external_resources();
```

| resources |
|-----------|
| 0         |

## Restrictions

When [`enable_external_access`]({% link docs/2.0/configuration/overview.md %}#configuration-reference) is `false`, the external resource statements are refused before any type function is called:

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
