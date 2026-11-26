---
layout: docu
redirect_from:
- /docs/current/resources/resource_registrations
- /docs/lts/resources/resource_registrations
- /docs/preview/resources/resource_registrations
- /docs/stable/resources/resource_registrations
title: Resource Registrations
---

<!-- ref: duckdb/duckdb#23731 duckdb/duckdb-web#7003 duckdb/duckdb#23736 duckdb/duckdb-web#7004 -->

> New External resources were introduced in DuckDB 2.0.0.

This page describes [resource registrations]({% link docs/2.0/resources/overview.md %}#terms) and the external resource functions that provision, register and tear down underlying resources. See [External Resources]({% link docs/2.0/resources/overview.md %}) for the terms used on this page, and [External Resource Types]({% link docs/2.0/resources/resource_types.md %}) for the lifecycle callbacks that these functions call.

A resource registration consists of:

* a name, given with `AS ⟨name⟩`, unique within the DuckDB instance
* the name of its external resource type
* the handle of its underlying resource
* the endpoint that the status callback reported when the resource registration was created
* its deleter binding

Resource registrations belong to the DuckDB instance: they are shared by all its connections. They are kept in memory, not in a database file, and end with the DuckDB instance; to manage an underlying resource again after a restart, a resource registration has to be created again with `REGISTER EXTERNAL RESOURCE` from its handle. Resource registrations are not transactional: a resource registration is kept when the transaction that created it is rolled back.

Creating a resource registration with a name that is already registered fails, so that a name always refers to one underlying resource.

A resource registration holds what the lifecycle callbacks reported when it was created. Later calls of the status callback, by `ATTACH TO EXTERNAL RESOURCE ⟨name⟩` and `CONNECT TO EXTERNAL RESOURCE ⟨name⟩`, are used by the statement that makes them, and do not change the resource registration: the attachment or connection uses the endpoint that the status callback reports then, and the resource registration keeps the endpoint it was created with. When the status callback reports `failed`, the attachment or connection is refused, and the resource registration is kept.

`DESTROY EXTERNAL RESOURCE` runs the deleter binding first, and removes the resource registration only when the destroy callback raises no error. When it raises one, the resource registration is kept, and the error message contains the query that retries the teardown. With an empty deleter binding, no lifecycle callback is called, and the resource registration is removed. After the teardown, the databases attached with `ATTACH TO EXTERNAL RESOURCE ⟨name⟩` are detached.

## Discovery

Discovery calls the list callback of each external resource type that has one, and adds the underlying resources it reports to the listing of the resource registrations. [`SHOW ALL EXTERNAL RESOURCES`]({% link docs/2.0/sql/statements/show.md %}#show-external-resources-statement) and `duckdb_external_resources(discover := true)` use discovery. In the listing, `managed` is `true` for a resource registration and `false` for an underlying resource that a list callback reported. An underlying resource with the same external resource type and handle as a resource registration is shown once, as the resource registration. Because the list callback asks the provider, discovery also reports underlying resources that no resource registration refers to, such as ones left behind by a run that failed; `REGISTER EXTERNAL RESOURCE` can create a resource registration for such an underlying resource from its handle.

## Listing Resource Registrations

[`SHOW EXTERNAL RESOURCES`]({% link docs/2.0/sql/statements/show.md %}#show-external-resources-statement) and [`duckdb_external_resources()`]({% link docs/2.0/sql/meta/duckdb_table_functions.md %}#duckdb_external_resources) list the resource registrations and, with `ALL` or `discover := true`, the underlying resources that [discovery](#discovery) reports.

## External Resource Functions

The external resource functions are table functions. Most SQL statements are built on them (see [SQL Statements]({% link docs/2.0/resources/overview.md %}#sql-statements)); they can also be called directly. [`register_external_resource_type`]({% link docs/2.0/resources/resource_types.md %}#register_external_resource_type) is described on the page about external resource types.

### `create_external_resource`

The `create_external_resource` function provisions an underlying resource of an external resource type, or, with `handle`, adopts one. It creates no resource registration: the caller is responsible for the teardown of what it provisions. `type` is given by position; the other parameters are given by name, as in `params := MAP {'name': 'db1'}`.

| Parameter | Description | Mandatory |
|:--|:--|:--|
| `type` | The name of the external resource type, a `VARCHAR`. | true |
| `params` | The argument for the create callback, a `MAP(VARCHAR, VARCHAR)`. | |
| `handle` | A handle, a `MAP(VARCHAR, VARCHAR)`. When given, the create callback is not called: the underlying resource is adopted. | |
| `resource_name` | A label for the `ExternalResource` log entries of the call, a `VARCHAR`. | |
| `teardown_on_failure` | Whether DuckDB tears down an underlying resource that it provisioned when the call fails afterwards, for example at the timeout, a `BOOLEAN`. Defaults to `true`. An adopted underlying resource is never torn down on a failure. | |
| `timeout_seconds` | How long to call the status callback until it reports `ready`, a `BIGINT`. Defaults to 300; `0` means no timeout. At most 2592000. | |
| `poll_interval_seconds` | How long to wait between two calls of the status callback, a `BIGINT`. Defaults to 5; between 1 and 2592000. | |

It returns one row, with the columns `handle`, `uri` and `attached_db_type`; `result`, the full `result` of the status callback; and `deleter_function` and `deleter_payload`, the deleter binding for [`destroy_external_resource`](#destroy_external_resource):

```sql
CREATE MACRO demo_create(params) AS TABLE
    SELECT MAP {'id': map_extract_value(params, 'name')} AS handle;
CREATE MACRO demo_status(handle) AS TABLE
    SELECT 'ready' AS state, MAP {'uri': ':memory:', 'attached_db_type': 'duckdb'} AS result;
CREATE MACRO demo_destroy(handle) AS TABLE
    SELECT map_extract_value(handle, 'id') AS destroyed;
CALL register_external_resource_type(
    'demo',
    kind := 'catalog',
    create_function := 'demo_create',
    status_function := 'demo_status',
    destroy_function := 'demo_destroy'
);
SELECT handle, uri, attached_db_type, deleter_function, deleter_payload
FROM create_external_resource('demo', params := MAP {'name': 'db1'});
```

| handle | uri | attached_db_type | deleter_function | deleter_payload |
|---|---|---|---|---|
| {id=db1} | :memory: | duckdb | demo_destroy | {id=db1} |

With `handle`, only the status callback is called. The external resource type's create callback, `demo_create`, does not exist here:

```sql
CREATE MACRO demo_status(handle) AS TABLE
    SELECT 'ready' AS state, MAP {'uri': ':memory:', 'attached_db_type': 'duckdb'} AS result;
CALL register_external_resource_type(
    'demo',
    kind := 'catalog',
    create_function := 'demo_create',
    status_function := 'demo_status'
);
SELECT handle, uri FROM create_external_resource('demo', handle := MAP {'id': 'existing'});
```

| handle | uri |
|---|---|
| {id=existing} | :memory: |

### `destroy_external_resource`

The `destroy_external_resource` function runs a deleter binding: it calls the destroy callback `deleter_function` with the handle `payload`. It is used with the `deleter_function` and `deleter_payload` that [`create_external_resource`](#create_external_resource) returns. Both parameters are given by position.

| Parameter | Description | Mandatory |
|:--|:--|:--|
| `deleter_function` | The name of the destroy callback, a `VARCHAR`. | true |
| `payload` | The handle to pass to the destroy callback. | true |

It returns one row, with the column `Success`:

```sql
CREATE MACRO demo_create(params) AS TABLE
    SELECT MAP {'id': map_extract_value(params, 'name')} AS handle;
CREATE MACRO demo_status(handle) AS TABLE
    SELECT 'ready' AS state, MAP {'uri': ':memory:', 'attached_db_type': 'duckdb'} AS result;
CREATE MACRO demo_destroy(handle) AS TABLE
    SELECT map_extract_value(handle, 'id') AS destroyed;
CALL register_external_resource_type(
    'demo',
    kind := 'catalog',
    create_function := 'demo_create',
    status_function := 'demo_status',
    destroy_function := 'demo_destroy'
);
SET VARIABLE resource = (
    SELECT {'deleter_function': deleter_function, 'deleter_payload': deleter_payload}
    FROM create_external_resource('demo', params := MAP {'name': 'db1'})
);
SELECT * FROM destroy_external_resource(
    getvariable('resource').deleter_function,
    getvariable('resource').deleter_payload
);
```

| Success |
|---------|
| true    |

### `register_external_resource`

The `register_external_resource` function creates a resource registration from the given values. It calls no lifecycle callback, and does not check that the external resource type is registered. `type`, `name` and `handle` are given by position; the other parameters are given by name, as in `uri := ':memory:'`.

| Parameter | Description | Mandatory |
|:--|:--|:--|
| `type` | The name of the external resource type, a `VARCHAR`. | true |
| `name` | The name of the resource registration, a `VARCHAR`. | true |
| `handle` | The handle of the underlying resource, a `MAP(VARCHAR, VARCHAR)`. | true |
| `uri` | The `uri` of the endpoint, a `VARCHAR`. | |
| `attached_db_type` | The `attached_db_type` of the endpoint, a `VARCHAR`. | |
| `deleter_function` | The name of the destroy callback of the deleter binding, a `VARCHAR`. Without it, the deleter binding is empty. | |

It returns one row, with the column `Success`:

```sql
CALL register_external_resource(
    'demo',
    'db1',
    MAP {'id': 'db1'},
    uri := ':memory:',
    attached_db_type := 'duckdb'
);
SELECT name, type, managed, handle, uri, attached_db_type FROM duckdb_external_resources();
```

| name | type | managed | handle | uri | attached_db_type |
|---|---|---|---|---|---|
| db1 | demo | true | {id=db1} | :memory: | duckdb |

### `deregister_external_resource`

The `deregister_external_resource` function removes a resource registration. It calls no lifecycle callback, so the underlying resource is not torn down. The parameter is given by position.

| Parameter | Description | Mandatory |
|:--|:--|:--|
| `name` | The name of the resource registration, a `VARCHAR`. | true |

It returns one row, with the column `Success`:

```sql
CALL register_external_resource('demo', 'db1', MAP {'id': 'db1'});
CALL deregister_external_resource('db1');
SELECT count(*) AS registrations FROM duckdb_external_resources();
```

| registrations |
|---------------|
| 0             |

Deregistering a name without a resource registration fails.
