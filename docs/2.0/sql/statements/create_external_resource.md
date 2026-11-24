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

The `CREATE EXTERNAL RESOURCE` statement creates a resource of a registered type, such as a database server or a storage bucket, and records it under a name. A registered resource can be attached with [`ATTACH TO EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/attach.md %}#attach-to-external-resource) and is removed with [`DESTROY EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/destroy_external_resource.md %}). A resource that already exists is recorded with [`REGISTER EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/register_external_resource.md %}), and [`SHOW EXTERNAL RESOURCES`]({% link docs/2.0/sql/statements/show.md %}#show-external-resources-statement) lists the recorded resources.

## Syntax

```sql
CREATE EXTERNAL RESOURCE ⟨type⟩ AS ⟨name⟩ [(⟨option⟩ [⟨value⟩], ...)];
```

The options are passed to the create function of the type. The name is required: a `CREATE EXTERNAL RESOURCE` statement without `AS ⟨name⟩` is an error, and so is a second one with a name that is already registered.

## Resource Types

A resource type is registered with the `register_external_resource_type` function. Extensions register their own types; a type can also be defined in SQL, with table macros as its functions:

* `create_function` creates the resource and returns its handle, a `MAP`.
* `status_function` returns the state of the resource; when it is `ready`, it also returns the endpoint to attach: its `uri` and `attached_db_type`.
* `destroy_function` removes the resource.

`kind` classifies the type, e.g., `catalog`, `storage` or `compute`. For a `catalog` type, the status function must return a `uri`. A type can also have a `resolve_function`, and a `list_function`, which reports resources for [`SHOW ALL EXTERNAL RESOURCES`]({% link docs/2.0/sql/statements/show.md %}#show-external-resources-statement). A type name can be registered only once.

```sql
CREATE MACRO dt_create(p) AS TABLE SELECT MAP {'id': 'd1'} AS handle;
CREATE MACRO dt_status(h) AS TABLE SELECT 'ready' AS state, MAP {'uri': ':memory:', 'attached_db_type': 'duckdb'} AS result;
CREATE MACRO dt_destroy(h) AS TABLE SELECT 'gone' AS status;
CALL register_external_resource_type('test.dotted.type', kind := 'catalog', create_function := 'dt_create', status_function := 'dt_status', destroy_function := 'dt_destroy');
CREATE EXTERNAL RESOURCE test.dotted.type AS created;
SELECT name, type FROM (SHOW EXTERNAL RESOURCES);
```

| name    | type             |
|---------|------------------|
| created | test.dotted.type |

### Writing a Type Name

Since DuckDB 2.0.1, a type name can be written without quotes as a dotted name, as in the example above. A dotted name is folded to lowercase like an identifier; a quoted type name is taken as written:

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

### Types Provided by Extensions

If a type is not registered but a known extension provides it, DuckDB autoloads that extension. With autoloading disabled, the error names the extension and the statements to install and load it.

## Functions

The following table functions work with external resources directly.

### `create_external_resource`

`create_external_resource(⟨type⟩ [, params := ⟨map⟩] [, handle := ⟨map⟩] [, timeout_seconds := ⟨n⟩] [, poll_interval_seconds := ⟨n⟩])` creates a resource of a type: it calls the create function, then the status function until the state is `ready`. It returns the resource's `handle`, `uri` and `attached_db_type`, the full `result` of the status function, and a `deleter_function` and `deleter_payload` for [`destroy_external_resource`](#destroy_external_resource).

```sql
CREATE MACRO mock_create(p) AS TABLE SELECT MAP {'id': 'r1'} AS handle;
CREATE MACRO mock_status(h) AS TABLE SELECT 'ready' AS state, MAP {'uri': 'quack:localhost:9494', 'attached_db_type': 'quack'} AS result;
CALL register_external_resource_type('mock@local', kind := 'catalog', create_function := 'mock_create', status_function := 'mock_status');
SELECT handle, uri, attached_db_type FROM create_external_resource('mock@local');
```

| handle  | uri                  | attached_db_type |
|---------|----------------------|------------------|
| {id=r1} | quack:localhost:9494 | quack            |

With `handle :=`, the create function is not called; the status function resolves the given handle. The type's create function, `mock_create`, does not exist here:

```sql
CREATE MACRO mock_status(h) AS TABLE SELECT 'ready' AS state, MAP {'uri': 'quack:localhost:9494', 'attached_db_type': 'quack'} AS result;
CALL register_external_resource_type('mock@local', kind := 'catalog', create_function := 'mock_create', status_function := 'mock_status');
SELECT handle, uri FROM create_external_resource('mock@local', handle := MAP {'id': 'adopted'});
```

| handle       | uri                  |
|--------------|----------------------|
| {id=adopted} | quack:localhost:9494 |

A status of `failed` is an error, and so is a type without a status function. `timeout_seconds` is between 0 and 2592000; `poll_interval_seconds` is between 1 and 2592000.

### `destroy_external_resource`

`destroy_external_resource(⟨deleter_function⟩, ⟨payload⟩)` destroys a resource created with [`create_external_resource`](#create_external_resource), using the `deleter_function` and `deleter_payload` it returned:

```sql
CREATE MACRO mock_create(p) AS TABLE SELECT MAP {'id': 'r1'} AS handle;
CREATE MACRO mock_status(h) AS TABLE SELECT 'ready' AS state, MAP {'uri': 'quack:localhost:9494', 'attached_db_type': 'quack'} AS result;
CREATE MACRO mock_destroy(h) AS TABLE SELECT 'ok' AS status;
CALL register_external_resource_type('mock@local', kind := 'catalog', create_function := 'mock_create', status_function := 'mock_status', destroy_function := 'mock_destroy');
SET VARIABLE resource = (SELECT {'fn': deleter_function, 'payload': deleter_payload} FROM create_external_resource('mock@local'));
CALL destroy_external_resource(getvariable('resource').fn, getvariable('resource').payload);
```

| Success |
|---------|
| true    |

### `register_external_resource` and `deregister_external_resource`

`register_external_resource(⟨type⟩, ⟨name⟩, ⟨handle⟩ [, uri := ⟨uri⟩] [, attached_db_type := ⟨type⟩] [, deleter_function := ⟨function⟩])` records a resource under a name without calling any function of its type. A registration is kept when the transaction that made it is rolled back, because the resource exists outside DuckDB. `deregister_external_resource(⟨name⟩)` removes the record and leaves the resource itself in place:

```sql
CALL register_external_resource('mock@local', 'r1', MAP {'id': 'abc'});
CALL deregister_external_resource('r1');
SELECT count(*) AS resources FROM duckdb_external_resources();
```

| resources |
|-----------|
| 0         |

## Restrictions

When [`enable_external_access`]({% link docs/2.0/configuration/overview.md %}#configuration-reference) is `false`, `CREATE EXTERNAL RESOURCE` and the other external resource statements are refused, before anything is created:

```sql
CREATE MACRO mock_create(p) AS TABLE SELECT MAP {'id': 'r1'} AS handle;
CALL register_external_resource_type('mock@local', kind := 'catalog', create_function := 'mock_create');
SET enable_external_access = false;
CREATE EXTERNAL RESOURCE 'mock@local' AS res;
```

```console
Permission Error: External resources are disabled through configuration
```
