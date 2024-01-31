---
layout: docu
title: Azure Extension
---

The `azure` extension is a loadable extension that adds a filesystem abstraction for the [Azure Blob storage](https://azure.microsoft.com/en-us/products/storage/blobs) to DuckDB.

> This extension is currently in an experimental state. Feel free to try it out, but be aware some things may not work as expected.

## Installing and Loading

To install and load the `azure` extension, run:

```sql
INSTALL azure;
LOAD azure;
```

## Usage

Authentication is done by setting the connection string:

```sql
SET azure_storage_connection_string = '<your_connection_string>';
```

After setting the connection string, the Azure Blob Storage can be queried:

```sql
SELECT count(*) FROM 'azure://<my_container>/<my_file>.<parquet_or_csv>';
```

Blobs are also supported:

```sql
SELECT * FROM 'azure://<my_container>/*.csv';
```

## Configuration

Use the following [configuration options](../sql/configuration) how the extension reads remote files:

* `azure_http_stats` [type: `BOOLEAN`] (default: `false`)  
    Include http info from Azure Storage in the [`EXPLAIN ANALYZE` statement](/dev/profiling).
    Notice that the result may be incorrect for more than one active DuckDB connection and the calculation of total received and sent bytes is not yet implemented.
* `azure_read_transfer_concurrency` [type: `BIGINT`] (default: `5`)  
    Maximum number of threads the Azure client can use for a single parallel read. If `azure_read_transfer_chunk_size` is less than `azure_read_buffer_size` then setting this > 1 will allow the Azure client to do concurrent requests to fill the buffer.
* `azure_read_transfer_chunk_size` [type: `BIGINT`] (default: `1 * 1024 * 1024`)  
    Maximum size in bytes that the Azure client will read in a single request. It is recommended that this is a factor of `azure_read_buffer_size`.
* `azure_read_buffer_size` [type: `UBIGINT`] (default: `1 * 1024 * 1024`)  
    Size of the read buffer. It is recommended that this is evenly divisible by `azure_read_transfer_chunk_size`.

Example:

```sql
SET azure_http_stats = false;
SET azure_read_transfer_concurrency = 5;
SET azure_read_transfer_chunk_size = 1048576;
SET azure_read_buffer_size = 1048576;
```

## Authentication Configuration

The Azure extension has two ways to configure the authentication:

* with variables
* with secret

These are exclusive and cannot be mixed.

### Authentication with Variables

```sql
SET variable_name = variable_value;
```

Where `variable_name` can be one of the following:

* `azure_storage_connection_string` [type: `STRING`]  
    Azure connection string, used for authenticating and configuring azure requests.
* `azure_account_name` [type: `STRING`]  
    Azure account name, when set, the extension will attempt to automatically detect credentials (not used if you pass the connection string)
* `azure_endpoint` [type: `STRING`] (default: `blob.core.windows.net`)  
    Override the azure endpoint for when the Azure credential providers are used.
* `azure_credential_chain` [type: `STRING`] (default: `none`)  
    Ordered list of Azure credential providers, in string format separated by `;`. E.g., `'cli;managed_identity;env'` (not used if you pass the connection string).
  
    Possible values:
    [`cli`](https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli);
    [`managed_identity`](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview);
    [`env`](https://github.com/Azure/azure-sdk-for-cpp/blob/azure-identity_1.6.0/sdk/identity/azure-identity/README.md#environment-variables);
    [`default`](https://github.com/Azure/azure-sdk-for-cpp/blob/azure-identity_1.6.0/sdk/identity/azure-identity/README.md#defaultazurecredential);
    `none`. The latest will result in an exception (invalid input).

Additional variable to use a proxy:

* `azure_http_proxy` [type: `STRING`] (default: `HTTP_PROXY environment variable if set`)  
    Proxy to use when login & performing request to azure.
* `azure_proxy_user_name` [type: `STRING`]  
    Http proxy username if needed.
* `azure_proxy_password` [type: `STRING`]  
    Http proxy password if needed.

### Authentication with Secret

Two secret providers are available at the moment for the Azure extension:

1. The default one `CONFIG` allowing access to storage account using a connection string or anonymously.
   ```sql
   -- Note that PROVIDER CONFIG is optional as it is the default one
   CREATE SECRET s1 (
       TYPE AZURE,
       PROVIDER CONFIG,
       CONNECTION_STRING '<value>'
   )
   ```
   ```sql
   -- Note that PROVIDER CONFIG is optional as it is the default one
   CREATE SECRET s1 (
       TYPE AZURE,
       PROVIDER CONFIG,
       ACCOUNT_NAME '<storage account name>'
   )
   ```
2. The `CREDENTIAL_CHAIN` one allow to connect with an identity
   ```sql
   CREATE SECRET az1 (
       TYPE AZURE,
       PROVIDER CREDENTIAL_CHAIN,
       CHAIN 'cli;env',
       ACCOUNT_NAME '<storage account name>'
   )
   ```
   Check `azure_credential_chain` variable description for the `CHAIN` value. Also, note that when using `CREDENTIAL_CHAIN` provider the default chain value is `default`.

To configure proxy information when using secret, you can add `HTTP_PROXY`, `PROXY_USER_NAME` & `PROXY_PASSWORD` in the secret definition.

Example:

```sql
CREATE SECRET s1 (
    TYPE AZURE,
    CONNECTION_STRING '<value>',
    HTTP_PROXY        'http://localhost:3128',
    PROXY_USER_NAME   'john',
    PROXY_PASSWORD    'doe'
)
```

> * When using secret, the `HTTP_PROXY` env variable will still be honored except is you provide an explicit value for it.
> * When using secret, the `SET variable` of the *Authentication with variables* session will be ignore.
> * If you want to make your secrets persistent replace `CREATE SECRET` by `CREATE PERSISTENT SECRET`.

## GitHub Repository

[<span class="github">GitHub</span>](https://github.com/duckdb/duckdb_azure)
