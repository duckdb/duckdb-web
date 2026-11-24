---
layout: docu
redirect_from:
- /docs/current/resources/catalog
- /docs/lts/resources/catalog
- /docs/preview/resources/catalog
- /docs/stable/resources/catalog
title: Catalog Resources
---

<!-- ref: duckdb/duckdb#23731 duckdb/duckdb-web#7003 duckdb/duckdb#23736 duckdb/duckdb-web#7004 -->

A [resource type]({% link docs/2.0/resources/overview.md %}#resource-types) of kind `catalog` provides a database. Its status function must return a `uri`, together with the `attached_db_type` of the endpoint. A catalog resource can be attached with [`ATTACH TO EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/attach.md %}#attach-to-external-resource) or connected to with [`CONNECT TO EXTERNAL RESOURCE`]({% link docs/2.0/sql/statements/connect.md %}).

## Example

Register a catalog type defined with table macros, create a resource, and attach it:

```sql
CREATE MACRO b_create(p) AS TABLE SELECT MAP {'id': 'b1'} AS handle;
CREATE MACRO b_status(h) AS TABLE SELECT 'ready' AS state, MAP {'uri': ':memory:', 'attached_db_type': 'duckdb'} AS result;
CREATE MACRO b_destroy(h) AS TABLE SELECT 'gone' AS status;
CALL register_external_resource_type('mem@local', kind := 'catalog', create_function := 'b_create', status_function := 'b_status', destroy_function := 'b_destroy');
CREATE EXTERNAL RESOURCE 'mem@local' AS shared;
ATTACH TO EXTERNAL RESOURCE shared AS db;
```
