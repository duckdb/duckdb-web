---
layout: post
title: "Managing External Resources in DuckDB"
authors:
  - Geertjan Wielenga
excerpt: "DuckDB 2.0 introduces external resources: a framework for creating, tracking, and destroying resources outside DuckDB—like database servers or cloud storage—through SQL. Extensions can register new resource types, and applications can manage their lifecycle through simple SQL statements."
tag: release
---

DuckDB 2.0 introduces a framework for managing resources that live outside the database: external resources. An external resource might be a database server, a cloud storage bucket, or a temporary compute cluster. DuckDB can create it, track its readiness, and ensure it gets cleaned up—all expressed in SQL. Extensions define what kinds of resources can exist and how they're managed; DuckDB handles the coordination.

## The Problem External Resources Solve

In applications that work with multiple systems, coordinating the lifecycle of temporary infrastructure can become messy. You might need to:

* Create a temporary database server for a job
* Check if it's ready before using it
* Attach to it and run queries
* Ensure it gets cleaned up when you're done

Without a unified framework, this work spreads across different tools and languages. The chance of leaving a resource behind—and the bill that comes with it—grows with every manual step. DuckDB's external resources let you express the entire lifecycle as SQL, with the database itself responsible for checking readiness and cleanup.

## How External Resources Work

An external resource is defined by its type. A resource type is a named set of functions that DuckDB calls at key points in the resource's lifecycle:

* **create function**: Called to create the resource. Returns a handle that identifies it.
* **status function**: Called repeatedly until the resource is ready. Returns a state and, when ready, the resource's endpoint (its URI and database type).
* **destroy function**: Called to clean up the resource.

Extensions register their own resource types when they load. For example, the `aws` extension registers types for CloudFormation stacks and S3 buckets. Types can also be defined in SQL using table macros.

## Creating and Using Resources

The simplest way to work with external resources is through SQL:

```sql
CREATE EXTERNAL RESOURCE type_name AS resource_name;
```

DuckDB calls the type's create function, then polls the status function until the resource is ready. Once ready, the resource is recorded under its name and can be attached or connected to:

```sql
ATTACH TO EXTERNAL RESOURCE resource_name AS alias;
```

Here's a complete example using a resource type defined with table macros:

```sql
-- Define a resource type with table macros as its functions
CREATE MACRO dt_create(p) AS TABLE SELECT MAP {'id': 'd1'} AS handle;
CREATE MACRO dt_status(h) AS TABLE
    SELECT 'ready' AS state, MAP {'uri': ':memory:', 'attached_db_type': 'duckdb'} AS result;
CREATE MACRO dt_destroy(h) AS TABLE SELECT 'gone' AS status;

-- Register the type
CALL register_external_resource_type(
    'test.dotted.type',
    kind := 'catalog',
    create_function := 'dt_create',
    status_function := 'dt_status',
    destroy_function := 'dt_destroy'
);

-- Create a resource of that type
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
| `CREATE EXTERNAL RESOURCE` | Record a resource for reuse | Until explicitly destroyed |
| `REGISTER EXTERNAL RESOURCE` | Record a resource that already exists | Until explicitly destroyed |
| `ATTACH TO NEW TEMPORARY EXTERNAL RESOURCE` | Create and use in one statement | Until detached |
| `ATTACH TO EXTERNAL RESOURCE ⟨name⟩` | Use a recorded resource | Use only |

The `NEW TEMPORARY` pattern is useful for short-lived work: DuckDB creates the resource, uses it, and destroys it when you detach. Recorded resources persist across statements and must be explicitly destroyed with `DESTROY EXTERNAL RESOURCE`.

## The Problem This Solves

Before external resources, the `aws` extension had to store state outside DuckDB—managing credentials, tracking provisioned instances, and remembering which resources belonged to which database session. Extensions that work with remote services faced the same problem: without DuckDB aware of their lifecycle, cleanup happened outside the SQL context, or didn't happen at all.

External resources move that responsibility into DuckDB. When you write `CREATE EXTERNAL RESOURCE aws.s3tables.bucket AS my_data`, DuckDB calls the AWS extension's creation logic, waits for the bucket to be ready, and then records it. When you detach, DuckDB calls the cleanup logic. The entire flow is under SQL's control, with DuckDB responsible for ensuring nothing leaks.

## Examples in the Wild

The DuckDB 2.0 source includes test resources built with table macros, and the `quack` extension uses external resources to manage temporary Quack database servers. The `aws` extension registers resource types for CloudFormation stacks, S3 buckets, and S3 tables. More extensions will follow as the pattern proves useful.

If you've built a resource type or used external resources in your application, let us know. Email [geertjan@ducklabs.com](mailto:geertjan@ducklabs.com).
