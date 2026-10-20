---
layout: docu
redirect_from:
- /docs/current/quack/troubleshooting
- /docs/lts/quack/troubleshooting
- /docs/preview/quack/troubleshooting
title: Troubleshooting Quack
---

Quack was released as a stable extension in [DuckDB 2.0]({% link release_calendar.md %}), having previously been available as a preview since DuckDB 1.5.3.
The protocol continues to be refined as the team works toward full production readiness.
If you experience any issues with Quack, try upgrading all your DuckDB clients to the latest version of the `quack` extension:

```sql
FORCE INSTALL quack;
```

## `ATTACH` Fails to Bind a Remote Table Definition

When a Quack client runs `ATTACH 'quack:⟨host⟩'`, it loads the server's table definitions up front and binds them locally. A single definition that cannot be bound fails the entire attachment, even when you only intend to query unrelated, ordinary tables on the server. The attachment does not silently skip the problematic table.

A common cause is an [Iceberg]({% link docs/2.0/core_extensions/iceberg/overview.md %}) catalog attached on the server with the default [`TABLE_RESOLUTION 'lazy'`]({% link docs/2.0/core_extensions/iceberg/iceberg_options.md %}#attach-options). Lazily resolved tables are listed with a placeholder column of type `UNKNOWN`, which the client receives through `duckdb_tables()` and cannot bind:

```console
Catalog Error: Type with name UNKNOWN does not exist!
```

The `UNKNOWN` type here is not the table's real type, and it does not mean the client must install the `iceberg` extension. It means the server has not yet resolved the table's schema.

### Resolving Tables Eagerly on the Server

Attach the Iceberg catalog on the server with `TABLE_RESOLUTION 'eager'` so that schemas are resolved while tables are enumerated, which lets Quack import their real definitions:

{:.codebox-server}
```sql
-- Server: substitute your own warehouse, URI, and secret.
LOAD iceberg;
LOAD quack;

ATTACH 'warehouse' AS ice (
    TYPE iceberg,
    URI 'https://catalog.example.com/api/catalog',
    SECRET iceberg_catalog_secret,
    TABLE_RESOLUTION 'eager'
);

CREATE TABLE local_data AS SELECT 42 AS i;
CALL quack_serve('quack:localhost', token = 'example-token');
```

The client can then attach and query as usual:

{:.codebox-client}
```sql
-- Client, in a separate DuckDB instance.
LOAD quack;
ATTACH 'quack:localhost' AS remote (TOKEN 'example-token');
FROM remote.local_data;
```

Eager resolution adds metadata-loading work and can increase catalog enumeration time for large catalogs. It does not fix unrelated binding errors or failures to load Iceberg metadata.

Resolving only some tables before attaching is not enough: if any other unresolved table remains, the attachment still fails. Warming every table individually is a workaround, but restarting the server or adding new unresolved tables brings the problem back, so eager server-side resolution is the more reliable fix.

### Querying Without Attaching

If you want to keep lazy resolution, use `quack_query()`, which runs SQL directly on the server without importing its catalog:

{:.codebox-client}
```sql
FROM quack_query(
    'quack:localhost',
    'SELECT count(*) FROM ice.demo.orders',
    token = 'example-token'
);
```
