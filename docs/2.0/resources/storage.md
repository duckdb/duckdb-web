---
layout: docu
redirect_from:
- /docs/current/resources/storage
- /docs/lts/resources/storage
- /docs/preview/resources/storage
- /docs/stable/resources/storage
title: Storage Resources
---

<!-- ref: duckdb/duckdb#23731 duckdb/duckdb-web#7003 -->

A [resource type]({% link docs/2.0/resources/overview.md %}#resource-types) of kind `storage` represents storage, such as a storage bucket.

## Example

Register a storage type and list it:

```sql
CALL register_external_resource_type('scratch_bucket', kind := 'storage', create_function := 's3_bucket_create', destroy_function := 's3_bucket_destroy');
SELECT name, kind FROM (SHOW EXTERNAL RESOURCE TYPES);
```

| name           | kind    |
|----------------|---------|
| scratch_bucket | storage |
