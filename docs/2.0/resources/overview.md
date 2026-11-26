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

Some tasks need a resource outside DuckDB, such as a database server or a storage bucket. External resources let DuckDB create such a resource, use it, and dispose of it again. DuckDB also keeps track of the resources it manages, so that none is left behind and forgotten.

## Managing Resources Outside DuckDB

Managing a resource outside DuckDB means taking it through its lifecycle: it is created, it takes some time to become ready, it is used, and it is eventually disposed of. Checking the state of a resource is useful throughout. A newly created resource may still be starting. A resource may have been changed or removed by someone else. A resource may have been left behind by a run that failed. The resource is held by another system, so all of this happens through that system's API.

## External Resources in DuckDB

Extensions provide access to such APIs. The [`aws` extension]({% link docs/2.0/core_extensions/aws.md %}), for example, provides the functions `s3_create_bucket` and `s3_delete_bucket`, which create and delete buckets in Amazon S3. The external resources feature adds a layer on top of such functions. It defines one lifecycle for every kind of resource, gives the functions that implement it a fixed contract, and lets DuckDB's SQL statements create a resource, attach it as a database, and dispose of it through that contract. These functions can come from an extension, or be written in SQL as table macros.

## Terms

This page and the other pages about external resources use the following terms.

* **Underlying resource**: a resource outside DuckDB, such as a database server or a storage bucket.
* **Provider**: the system that holds underlying resources, such as a cloud service.
* **External resource type**: a named description of one class of underlying resources: its kind and its lifecycle callbacks. See [External Resource Types]({% link docs/2.0/resources/resource_types.md %}).
* **Lifecycle callback**: a table function or table macro that DuckDB calls at one step of the lifecycle of an underlying resource. An external resource type holds the names of its lifecycle callbacks. There are five kinds, named after their step:
    * **Create callback**: creates an underlying resource, and returns its handle.
    * **Status callback**: reports whether an underlying resource is ready, and its endpoint.
    * **Destroy callback**: disposes of an underlying resource.
    * **List callback**: reports the underlying resources that the provider holds.
    * **Resolve callback**: is recorded with the external resource type; DuckDB does not call it.

  See [Lifecycle Callbacks]({% link docs/2.0/resources/resource_types.md %}#lifecycle-callbacks).
* **Handle**: the value that identifies an underlying resource to the lifecycle callbacks of its external resource type. To DuckDB, a handle is opaque: DuckDB stores it and passes it to the lifecycle callbacks, without reading it. It is up to the author of the create callback to return a handle that the other lifecycle callbacks of the same external resource type can use to operate on the underlying resource.
* **Endpoint**: what DuckDB needs to attach an underlying resource as a database.
* **Resource registration**: the DuckDB object through which SQL statements refer to an underlying resource, under a name. See [Resource Registrations]({% link docs/2.0/resources/resource_registrations.md %}).
* **Deleter binding**: the destroy callback of an underlying resource together with its handle; running it tears down the underlying resource.
* **Provisioning**: creating an underlying resource: DuckDB calls the create callback, then calls the status callback to poll whether the underlying resource is ready.
* **Adoption**: taking an existing underlying resource by its handle: DuckDB calls the status callback to poll whether the underlying resource is ready, without calling the create callback.
* **Teardown**: running a deleter binding.
* **Discovery**: calling the list callbacks, to list the underlying resources that providers report, including those without a resource registration. See [Discovery]({% link docs/2.0/resources/resource_registrations.md %}#discovery).

What DuckDB knows about an underlying resource is what a lifecycle callback reported, when DuckDB called it.

## SQL Statements

In the SQL statements, `EXTERNAL RESOURCE` refers to a resource registration. `NEW TEMPORARY EXTERNAL RESOURCE`, in `ATTACH TO` and `CONNECT TO`, does not: it provisions an underlying resource for one attachment or connection, without a resource registration.

The SQL statements call the [external resource functions]({% link docs/2.0/resources/resource_registrations.md %}#external-resource-functions), or the deleter binding of a resource registration directly:

| Statement | What it runs | Lifecycle callbacks | Resource registration |
|:--|:--|:--|:--|
| [`CREATE EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/create_external_resource.md %}) | [`create_external_resource`]({% link docs/2.0/resources/resource_registrations.md %}#create_external_resource) with the statement's options as `params` | create, status | created |
| [`REGISTER EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/register_external_resource.md %}) | `create_external_resource` with the given `handle` | status | created |
| [`ATTACH TO NEW TEMPORARY EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/attach.md %}#attach-to-external-resource), [`CONNECT TO NEW TEMPORARY EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/connect.md %}) | `create_external_resource` with the statement's options as `params` | create, status; destroy at `DETACH` or `DISCONNECT` | none |
| `ATTACH TO EXTERNAL RESOURCE ⟨name⟩`, `CONNECT TO EXTERNAL RESOURCE ⟨name⟩` | `create_external_resource` with the handle of the resource registration | status | unchanged |
| [`DESTROY EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/destroy_external_resource.md %}) | the deleter binding of the resource registration | destroy | removed |
| [`SHOW [ALL] EXTERNAL RESOURCES`]({% link docs/2.0/sql/statements/show.md %}#show-external-resources-statement) | `duckdb_external_resources`, with `discover := true` for `ALL` | list, for `ALL` | none |

The SQL statements take no timeout or poll interval: they use the defaults of `create_external_resource`. All options of `CREATE EXTERNAL RESOURCE` are passed to the create callback.

## Restrictions

When [`enable_external_access`]({% link docs/2.0/configuration/overview.md %}#configuration-reference) is `false`, the statements that call lifecycle callbacks are refused before any lifecycle callback is called: `CREATE EXTERNAL RESOURCE`, `REGISTER EXTERNAL RESOURCE`, `DESTROY EXTERNAL RESOURCE`, and the `EXTERNAL RESOURCE` forms of `ATTACH TO` and `CONNECT TO`. They fail with a permission error, so that no underlying resource is provisioned, adopted or torn down.

`SHOW EXTERNAL RESOURCES` and `SHOW ALL EXTERNAL RESOURCES` are not refused. The external resource functions are not refused either: `create_external_resource` provisions an underlying resource, and `register_external_resource_type` and `register_external_resource` register, when [`enable_external_access`]({% link docs/2.0/configuration/overview.md %}#configuration-reference) is `false`.
