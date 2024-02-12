---
layout: docu
title: CREATE SECRET Statement
railroad: statements/secrets.js
---

The `CREATE SECRET` statement creates a new secret in the **Secrets Manager**, which provides unified user interface for secrets across all backends that use them. Secrets can be scoped, so different storage prefixes can have different secrets, allowing for example to join data across organizations in a single query. Secrets can also be persisted, so that they do not need to be specified every time DuckDB is launched.

> The Secrets Manager was introduced with DuckDB version 0.10.

> The Secrets Manager stored data in unencrypted binary format on the disk.

## Secrets Manager

### Types of Secrets

Secrets are typed, their type identifies which service they are for. Currently, the following cloud services are available:

* AWS S3 (`S3`), through the [`httpfs` extension](../../extensions/httpfs)
* Google Cloud Storage (`GCS`), through the [`httpfs` extension](../../extensions/httpfs)
* Cloudflare R2 (`R2`), through the [`httpfs` extension](../../extensions/httpfs)
* Azure Blob Storage (`AZURE`), through the [`azure` extension](../../extensions/azure)

For each type, there are one or more "secret providers" that specify how the secret is created. Secrets can also have an optional scope, which is a file path prefix that the secret applies to. When fetching a secret for a path, the secret scopes are compared to the path, returning the matching secret for the path. In the case of multiple matching secrets, the longest prefix is chosen.

### Creating a Secret

Secrets can be temporary or persistent. Temporary secrets are used by default – and are stored in-memory for the life span of the DuckDB instance similar to how settings worked previously. Persistent secrets are stored in **unencrypted binary format** in the `~/.duckdb/stored_secrets` directory. On startup of DuckDB, persistent secrets are read from this directory and automatically loaded.

#### Temporary Secrets

To create a temporary unscoped secret to access S3, we can now use the following:

```sql
CREATE SECRET (
    TYPE S3,
    KEY_ID 'mykey',
    SECRET 'mysecret',
    REGION 'myregion');
```

#### Persistent Secrets

In order to persist secrets between DuckDB database instances, we can now use the `CREATE PERSISTENT SECRET` command, e.g.:

```sql
CREATE PERSISTENT SECRET my_persistent_secret (
    TYPE S3,
    KEY_ID 'key',
    SECRET 'secret');
```

This will write the secret (unencrypted) to the `~/.duckdb/stored_secrets` directory.

### Deleting Secrets

Secrets can be deleted using the `DROP SECRET` statement, e.g.:

```sql
DROP PERSISTENT SECRET my_persistent_secret;
```

### Creating Multiple Secrets for the Same Service Type

If two secrets exist for a service type, the scope can be used to decide which one should be used. For example:

```sql
CREATE SECRET secret1 (
    TYPE S3,
    KEY_ID 'my_key1',
    SECRET 'my_secret1',
    SCOPE 's3://my-bucket');
```

```sql
CREATE SECRET secret2 (
    TYPE S3,
    KEY_ID 'my_key2',
    SECRET 'my_secret2',
    SCOPE 's3://my-other-bucket');
```

Now, if the user queries something from `s3://my-other-bucket/something`, secret `secret2` will be chosen automatically for that request.

### Listing Secrets

Secrets can be listed using the built-in table-producing function, e.g., by using the [`duckdb_secrets()` table function](../duckdb_table_functions#duckdb_secrets):

```sql
FROM duckdb_secrets();
```

Sensitive information will be redacted.

### Syntax for `CREATE SECRET`

<div id="rrdiagram1"></div>

### Syntax for `DROP SECRET`

<div id="rrdiagram2"></div>
