---
layout: post
title: "Managing External Resources in DuckDB"
authors:
  - Geertjan Wielenga
thumb: "/images/blog/thumbs/external-resources.svg"
image: "/images/blog/thumbs/external-resources.png"
excerpt: "DuckDB 2.0 introduces external resources: a framework for creating, tracking, and destroying resources outside DuckDB—like database servers or cloud storage—through SQL. Extensions can register new resource types, and applications can manage their lifecycle through simple SQL statements."
tag: release
---

DuckDB 2.0 introduces a framework for managing resources that live outside the database: external resources. An external resource might be a database server, a cloud storage bucket, or a temporary compute cluster. Extensions can manually manage these resources, defining creation and cleanup logic. DuckDB's external resource framework adds a coordination layer: applications can express the entire lifecycle through SQL, and this DuckDB process ensures resources are created, checked for readiness, and cleaned up.

## The Problem External Resources Solve

In applications that work with multiple systems, coordinating the lifecycle of temporary infrastructure can become messy. You might need to:

* Create a temporary database server for a job
* Check if it's ready before using it
* Attach to it and run queries
* Ensure it gets cleaned up when you're done

Without a unified framework, this work spreads across different tools and languages. The chance of leaving a resource behind—and the bill that comes with it—grows with every manual step. DuckDB's external resources let you express the entire lifecycle as SQL, with this DuckDB process responsible for checking readiness and cleanup.

## How External Resources Work

An external resource is defined by its type. A resource type is a named set of lifecycle callbacks that DuckDB calls at key events in the resource's lifecycle. The three main lifecycle callbacks are:

* **create callback**: Called to create the resource. Returns a handle that identifies it.
* **status callback**: Called repeatedly until the resource is ready. Returns a state and, when ready, the resource's endpoint (its URI and database type).
* **destroy callback**: Called to clean up the resource.

Additional lifecycle callbacks include list and resolve, though these three are the most commonly used.

Extensions register their own resource types when they load, particularly if they primarily communicate with external resources. For example, the `aws` extension registers types for CloudFormation stacks and S3 buckets. Resource types can also be defined in SQL using table macros as their lifecycle callbacks.

## Creating and Using Resources

The simplest way to work with external resources is through SQL:

```sql
CREATE EXTERNAL RESOURCE resource_type_name AS resource_name;
```

DuckDB calls the resource type's create lifecycle callback, then polls the status callback until the resource is ready. Once ready, the resource is registered under its name and can be attached or connected to:

```sql
ATTACH TO EXTERNAL RESOURCE resource_name AS alias;
```

Here's a complete example using a resource type defined with table macros:

```sql
-- Define a resource type using table macros as its lifecycle callbacks
CREATE MACRO dt_create(p) AS TABLE SELECT MAP {'id': 'd1'} AS handle;
CREATE MACRO dt_status(h) AS TABLE
    SELECT 'ready' AS state, MAP {'uri': ':memory:', 'attached_db_type': 'duckdb'} AS result;
CREATE MACRO dt_destroy(h) AS TABLE SELECT 'gone' AS status;

-- Register the resource type
CALL register_external_resource_type(
    'test.dotted.type',
    kind := 'catalog',
    create_function := 'dt_create',
    status_function := 'dt_status',
    destroy_function := 'dt_destroy'
);

-- Create a resource of that resource type
CREATE EXTERNAL RESOURCE test.dotted.type AS created;

-- List the resource
SELECT name, type FROM (SHOW EXTERNAL RESOURCES);
```

The result:

| name    | type             |
|---------|------------------|
| created | test.dotted.type |

## Resource Lifecycle Patterns

DuckDB supports several ways to work with external resources, each with different ownership models:

| Pattern | Use | Lifetime |
|:--|:--|:--|
| `CREATE EXTERNAL RESOURCE` | Register a resource for reuse | Until explicitly destroyed |
| `REGISTER EXTERNAL RESOURCE` | Register a resource that already exists | Until explicitly destroyed |
| `ATTACH TO NEW TEMPORARY EXTERNAL RESOURCE` | Create and use in one statement | Until detached |
| `ATTACH TO EXTERNAL RESOURCE ⟨name⟩` | Use a registered resource | Use only |

The `NEW TEMPORARY` pattern is useful for short-lived work: DuckDB creates the resource, uses it, and destroys it when you detach. Registered resources persist across statements and must be explicitly destroyed with `DESTROY EXTERNAL RESOURCE`.

## The Problem This Solves

Before external resources, the `aws` extension had to store state outside DuckDB—managing credentials, tracking provisioned instances, and remembering which resources belonged to which database session. Extensions that work with remote services faced the same problem: prior to the external resource framework, DuckDB was unaware of the resource's lifecycle. As a result, cleanup happened outside the SQL context, or didn't happen at all.

External resources move that responsibility into DuckDB. When you write `CREATE EXTERNAL RESOURCE aws.s3tables.bucket AS my_data`, DuckDB calls the AWS extension's creation logic, waits for the bucket to be ready, and then registers it. When you detach, DuckDB calls the cleanup logic. The entire flow is under SQL's control, with this DuckDB process responsible for ensuring nothing leaks.

## Examples in the Wild

The DuckDB 2.0 source includes test resources built with table macros as lifecycle callbacks, and the `quack` extension uses external resources to manage temporary Quack database servers. The `aws` extension registers resource types for CloudFormation stacks, S3 buckets, and S3 tables. More extensions will follow as the pattern proves useful.

If you've built a resource type or used external resources in your application, let us know. Email [geertjan@ducklabs.com](mailto:geertjan@ducklabs.com).

## Further Reading

- [External Resources Documentation]({% link docs/2.0/resources/overview.md %})
- [External Resource Types Reference]({% link docs/2.0/resources/resource_types.md %})
- [Resource Registrations]({% link docs/2.0/resources/resource_registrations.md %})
- [Example: Scratch Databases for CI Runs]({% link docs/2.0/resources/resource_type_example.md %})
