---
layout: docu
title: Secrets Manager
---

The **Secrets manager** provides a unified user interface for secrets across all backends that use them. Secrets can be scoped, so different storage prefixes can have different secrets, allowing for example to join data across organizations in a single query. Secrets can also be persisted, so that they do not need to be specified every time DuckDB is launched.

> Warning Persistent secrets are stored in unencrypted binary format on the disk.

## Secrets

### Types of Secrets

Secrets are typed, their type identifies which service they are for. Currently, the following cloud services are available:

* AWS S3 (`S3`), through the [`httpfs` extension](../extensions/httpfs/s3api)
* Azure Blob Storage (`AZURE`), through the [`azure` extension](../extensions/azure)
* Cloudflare R2 (`R2`), through the [`httpfs` extension](../extensions/httpfs/s3api)
* Google Cloud Storage (`GCS`), through the [`httpfs` extension](../extensions/httpfs/s3api)
* Hugging Face (`HUGGINGFACE`), through the [`httpfs` extension](../extensions/httpfs/hugging_face)

For each type, there are one or more "secret providers" that specify how the secret is created. Secrets can also have an optional scope, which is a file path prefix that the secret applies to. When fetching a secret for a path, the secret scopes are compared to the path, returning the matching secret for the path. In the case of multiple matching secrets, the longest prefix is chosen.

### Creating a Secret

Secrets can be created using the [`CREATE SECRET` SQL statement](../sql/statements/create_secret).
Secrets can be **temporary** or **persistent**. Temporary secrets are used by default – and are stored in-memory for the life span of the DuckDB instance similar to how settings worked previously. Persistent secrets are stored in **unencrypted binary format** in the `~/.duckdb/stored_secrets` directory. On startup of DuckDB, persistent secrets are read from this directory and automatically loaded.

#### Secret Providers

To create a secret, a **Secret Provider** needs to be used. A Secret Provider is a mechanism through which a secret is generated. To illustrate this, for the `S3`, `GCS`, `R2`, and `AZURE` secret types, DuckDB currently supports two providers: `CONFIG` and `CREDENTIAL_CHAIN`. The `CONFIG` provider requires the user to pass all configuration information into the `CREATE SECRET`, whereas the `CREDENTIAL_CHAIN` provider will automatically try to fetch credentials. When no Secret Provider is specified, the `CONFIG` provider is used. For more details on how to create secrets using different providers check out the respective pages on [httpfs](../extensions/httpfs#configuration-and-authentication-using-secrets) and [azure](../extensions/azure#authentication-with-secret).

#### Temporary Secrets

To create a temporary unscoped secret to access S3, we can now use the following:

```sql
CREATE SECRET my_secret (
    TYPE S3,
    KEY_ID 'my_secret_key',
    SECRET 'my_secret_value',
    REGION 'my_region'
);
```

Note that we implicitly use the default `CONFIG` secret provider here.

#### Persistent Secrets

In order to persist secrets between DuckDB database instances, we can now use the `CREATE PERSISTENT SECRET` command, e.g.:

```sql
CREATE PERSISTENT SECRET my_persistent_secret (
    TYPE S3,
    KEY_ID 'my_secret_key',
    SECRET 'my_secret_value'
);
```

This will write the secret (unencrypted) to the `~/.duckdb/stored_secrets` directory.

### Deleting Secrets

Secrets can be deleted using the [`DROP SECRET` statement](../sql/statements/create_secret#syntax-for-drop-secret), e.g.:

```sql
DROP PERSISTENT SECRET my_persistent_secret;
```

### Creating Multiple Secrets for the Same Service Type

If two secrets exist for a service type, the scope can be used to decide which one should be used. For example:

```sql
CREATE SECRET secret1 (
    TYPE S3,
    KEY_ID 'my_secret_key1',
    SECRET 'my_secret_value1',
    SCOPE 's3://my-bucket'
);
```

```sql
CREATE SECRET secret2 (
    TYPE S3,
    KEY_ID 'my_secret_key2',
    SECRET 'my_secret_value2',
    SCOPE 's3://my-other-bucket'
);
```

Now, if the user queries something from `s3://my-other-bucket/something`, secret `secret2` will be chosen automatically for that request. To see which secret is being used, the `which_secret` scalar function can be used, which takes a path and a secret type as parameters:

```sql
FROM which_secret('s3://my-other-bucket/file.parquet', 's3');
```

### Listing Secrets

Secrets can be listed using the built-in table-producing function, e.g., by using the [`duckdb_secrets()` table function](../sql/duckdb_table_functions#duckdb_secrets):

```sql
FROM duckdb_secrets();
```

Sensitive information will be redacted.
