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

An external resource is a resource outside DuckDB, such as a database server or a storage bucket, that DuckDB records under a name. Each resource has a type, which defines the functions that create, inspect, and destroy resources of that type.

## Resource Types

A resource type is registered with the `register_external_resource_type` function. Extensions register their own types; a type can also be defined in SQL, with table macros as its functions. See [Resource Types]({% link docs/2.0/sql/statements/create_external_resource.md %}#resource-types) for the functions a type can have.

The `kind` of a type classifies it:

* [`catalog`]({% link docs/2.0/resources/catalog.md %})
* [`storage`]({% link docs/2.0/resources/storage.md %})
* [`compute`]({% link docs/2.0/resources/compute.md %})

## Lifecycle

* [`CREATE EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/create_external_resource.md %}) creates a resource and records it under a name.
* [`REGISTER EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/register_external_resource.md %}) records a resource that already exists.
* [`ATTACH TO EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/attach.md %}#attach-to-external-resource) and [`CONNECT TO EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/connect.md %}) use the database of a resource.
* [`SHOW EXTERNAL RESOURCES`]({% link docs/2.0/sql/statements/show.md %}#show-external-resources-statement) and [`SHOW EXTERNAL RESOURCE TYPES`]({% link docs/2.0/sql/statements/show.md %}#show-external-resource-types-statement) list the recorded resources and the registered types.
* [`DESTROY EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/destroy_external_resource.md %}) removes a resource.

## Functions

* [`create_external_resource`, `destroy_external_resource`, `register_external_resource`, and `deregister_external_resource`]({% link docs/2.0/sql/statements/create_external_resource.md %}#functions) work with external resources directly.
* [`duckdb_external_resource_types()`]({% link docs/2.0/sql/meta/duckdb_table_functions.md %}#duckdb_external_resource_types) and [`duckdb_external_resources()`]({% link docs/2.0/sql/meta/duckdb_table_functions.md %}#duckdb_external_resources) list the registered types and resources.

## Restrictions

When [`enable_external_access`]({% link docs/2.0/configuration/overview.md %}#configuration-reference) is `false`, the external resource statements are refused. See [Restrictions]({% link docs/2.0/sql/statements/create_external_resource.md %}#restrictions).
