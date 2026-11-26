---
layout: docu
redirect_from:
- /docs/current/resources/resource_types
- /docs/lts/resources/resource_types
- /docs/preview/resources/resource_types
- /docs/stable/resources/resource_types
title: External Resource Types
---

<!-- ref: duckdb/duckdb#23731 duckdb/duckdb-web#7003 duckdb/duckdb#23736 duckdb/duckdb-web#7004 -->

> New External resources were introduced in DuckDB 2.0.0.

This page describes [external resource types]({% link docs/2.0/resources/overview.md %}#terms): what they consist of, how they are registered, and the contract of their lifecycle callbacks. See [External Resources]({% link docs/2.0/resources/overview.md %}) for the terms used on this page.

An external resource type consists of a name, a [kind](#external-resource-type-kinds), and the names of its [lifecycle callbacks](#lifecycle-callbacks). It is registered by calling the [`register_external_resource_type`](#register_external_resource_type) function. The registered external resource types are listed by [`SHOW EXTERNAL RESOURCE TYPES`]({% link docs/2.0/sql/statements/show.md %}#show-external-resource-types-statement) and [`duckdb_external_resource_types()`]({% link docs/2.0/sql/meta/duckdb_table_functions.md %}#duckdb_external_resource_types).

External resource types belong to the DuckDB instance: they are shared by all its connections and are kept in memory. An external resource type name is registered only once, and a registered external resource type cannot be changed or removed. Registering a name that is already registered fails, so that an external resource type that is in use is never replaced.

## External Resource Type Names

<!-- ref: duckdb/duckdb#29056 duckdb/duckdb-web#7856 -->

In the SQL statements, an external resource type name is written unquoted, in double quotes, or as a string literal. The form decides which characters the name can contain, and whether its case is kept:

| Form | Characters | Case |
|:--|:--|:--|
| Unquoted | letters, digits, `_`; with parts, also `.` and `-` (see below) | folded to lowercase |
| Double quotes: `"⟨name⟩"` | any; `""` stands for one `"` | folded to lowercase |
| String literal: `'⟨name⟩'` | any; `''` stands for one `'`; a backslash is an ordinary character | kept as written |

Backticks work like double quotes, and dollar-quoted strings work like string literals. Folding to lowercase applies to the letters `A` to `Z`; other letters are kept as written.

An unquoted name without dots is an identifier: it starts with a letter or `_`, and is not a reserved keyword such as `select`. Since DuckDB 2.0.1, an unquoted name can also consist of two or more parts separated by dots, as in `aws.s3.bucket`. Each part consists of letters, digits and `_`, and can contain a `-` between two of these characters, as in `quack-on-ec2`. A part can start with a digit and can be a keyword. Each dot has a part directly on both sides, without spaces. A `-` is allowed only in a name with parts.

The name that DuckDB looks up for some written forms:

| Written | Name looked up |
|:--|:--|
| `Nobody.Provides.THIS` | `nobody.provides.this` |
| `"Nobody.Provides.THIS"` | `nobody.provides.this` |
| `'Nobody.Provides.THIS'` | `Nobody.Provides.THIS` |
| `'aws:cloudformation:stack'` | `aws:cloudformation:stack` |

An external resource type whose name contains an uppercase letter can therefore only be referred to by a string literal. These rules apply to every SQL statement that takes an external resource type name: [`CREATE EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/create_external_resource.md %}), [`REGISTER EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/register_external_resource.md %}), `ATTACH TO NEW TEMPORARY EXTERNAL RESOURCE`, `CONNECT TO NEW TEMPORARY EXTERNAL RESOURCE` and `SHOW EXTERNAL RESOURCES WITH TYPE`. The external resource functions take the name as a `VARCHAR`, which is kept as written.

## External Resource Types Provided by Extensions

An extension can register external resource types when it is loaded; their `origin` is `extension`, and that of an external resource type registered by calling `register_external_resource_type` is `user`. If an external resource type is not registered but a known extension provides it, DuckDB autoloads that extension. With autoloading disabled, the error names the extension and the statements to install and load it.

## External Resource Type Kinds

The `kind` of an external resource type is a label, chosen when the external resource type is registered and shown in the listings of external resource types. The external resource types of the [`aws` extension]({% link docs/2.0/core_extensions/aws.md %}), for example, have the following kinds:

| External resource type | Kind |
|:--|:--|
| `aws.cloudformation.stack` | `storage` |
| `aws.s3.bucket` | `storage` |
| `aws.s3tables.bucket` | `catalog` |
| `aws.system-table` | `catalog` |

The kind `catalog` marks an external resource type whose underlying resources are databases. For a `catalog` external resource type, the `result` of the status callback must contain the endpoint, `uri` and `attached_db_type`, when an underlying resource is provisioned or adopted; otherwise provisioning or adoption fails, since the underlying resource could not be attached. Every other kind is treated alike.

## Lifecycle Callbacks

DuckDB calls the lifecycle callbacks of an external resource type at the steps of the lifecycle of an underlying resource. A lifecycle callback is a table function or table macro, and has to follow a contract: what DuckDB passes to it, and which columns and values DuckDB reads from its result. The names of these columns are part of the contract.

DuckDB calls a lifecycle callback on an internal connection of its own. A lifecycle callback must therefore be visible to every connection: a `TEMP` macro cannot be a lifecycle callback. An unqualified name of a lifecycle callback is resolved in the search path that was in effect when the external resource type was registered.

| Lifecycle callback | Called for | Argument | Result |
|:--|:--|:--|:--|
| create | provisioning | the options of the statement, or `params` of `create_external_resource`, as a `MAP(VARCHAR, VARCHAR)` with lowercase keys | one row, with the column `handle`: a `MAP(VARCHAR, VARCHAR)`, not `NULL` |
| status | provisioning, adoption, and `ATTACH`/`CONNECT TO EXTERNAL RESOURCE ⟨name⟩` | the handle | one row, with the columns `state` (`VARCHAR`) and `result` (`MAP(VARCHAR, VARCHAR)`) |
| destroy | teardown | the handle | DuckDB reads no column; an error means that the teardown failed |
| list | discovery | an empty `MAP(VARCHAR, VARCHAR)` | one row per underlying resource, with the columns `handle`, `name`, `reference` and `state` |
| resolve | | | DuckDB does not call it |

The create callback is required; the other lifecycle callbacks are optional. A handle is a `MAP(VARCHAR, VARCHAR)`; DuckDB passes it to the lifecycle callbacks unchanged, without reading it. Provisioning and adoption require a status callback, since DuckDB polls it to learn whether the underlying resource is ready; without one, they fail.

The `state` that the status callback reports controls polling: `ready` ends it successfully, `failed` ends it with an error, and any other value makes DuckDB call the status callback again after the poll interval. The `result` holds the endpoint, as the keys `uri` and `attached_db_type`. Its other keys are passed to `ATTACH` as options of the attached database.

The list callback reports each underlying resource with the handle that the create callback would return for it, the provider's own `name` and `reference` for it, and its `state` as the provider reports it.

An example of an external resource type, with all its lifecycle callbacks written as table macros, is [Example: Scratch Databases for CI Runs]({% link docs/2.0/resources/resource_type_example.md %}).

## `register_external_resource_type`

The `register_external_resource_type` function registers an external resource type. It calls no lifecycle callback; the names of the lifecycle callbacks are resolved when DuckDB first calls them. `name` is given by position; the other parameters are given by name, as in `kind := 'catalog'`.

| Parameter | Description | Mandatory |
|:--|:--|:--|
| `name` | The name of the external resource type, a `VARCHAR`, kept as written. | true |
| `kind` | The [kind](#external-resource-type-kinds) of the external resource type, a `VARCHAR`. | true |
| `create_function` | The name of the create callback, a `VARCHAR`. | true |
| `status_function` | The name of the status callback, a `VARCHAR`. | |
| `destroy_function` | The name of the destroy callback, a `VARCHAR`. | |
| `list_function` | The name of the list callback, a `VARCHAR`. | |
| `resolve_function` | The name of the resolve callback, a `VARCHAR`. | |

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
```

| Success |
|---------|
| true    |
