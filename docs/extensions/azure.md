---
layout: docu
title: Azure Extension
---

The `azure` extension is a loadable extension that adds a filesystem abstraction for the [Azure Blob storage](https://azure.microsoft.com/en-us/products/storage/blobs) to DuckDB.

## Installing and Loading

To install and load the `azure` extension, run:

```sql
INSTALL azure;
LOAD azure;
```

## Usage

Once the [authentication](#authentication) is set up, the Azure Blob Storage can be queried as follows:

```sql
SELECT count(*) FROM 'az://<my_container>/<my_file>.<parquet_or_csv>';
```

Globs are also supported:

```sql
SELECT * FROM 'az://<my_container>/*.csv';
```

## Configuration

Use the following [configuration options](../sql/configuration) how the extension reads remote files:

| Name | Description | Type | Default |
|:---|:---|:---|:---|
| `azure_http_stats` | Include http info from Azure Storage in the [`EXPLAIN ANALYZE` statement](/dev/profiling). Notice that the result may be incorrect for more than one active DuckDB connection and the calculation of total received and sent bytes is not yet implemented. | `BOOLEAN` | `false` |
| `azure_read_transfer_concurrency` | Maximum number of threads the Azure client can use for a single parallel read. If `azure_read_transfer_chunk_size` is less than `azure_read_buffer_size` then setting this > 1 will allow the Azure client to do concurrent requests to fill the buffer. | `BIGINT` | `5` |
| `azure_read_transfer_chunk_size` | Maximum size in bytes that the Azure client will read in a single request. It is recommended that this is a factor of `azure_read_buffer_size`. | `BIGINT` | `1024*1024` |
| `azure_read_buffer_size` | Size of the read buffer. It is recommended that this is evenly divisible by `azure_read_transfer_chunk_size`. | `UBIGINT` | `1024*1024` |

Example:

```sql
SET azure_http_stats = false;
SET azure_read_transfer_concurrency = 5;
SET azure_read_transfer_chunk_size = 1048576;
SET azure_read_buffer_size = 1048576;
```

## Authentication

The Azure extension has two ways to configure the authentication. The preferred way is to use Secrets.

### Authentication with Secret

Multiple secret providers are available for the Azure extension:

#### `CONFIG` Provider

The default provider, `CONFIG` (i.e., user-configured), allows access to the storage account using a connection string or anonymously. For example:

```sql
CREATE SECRET secret1 (
    TYPE AZURE,
    CONNECTION_STRING '<value>'
);
```

If you do not use authentication, you still need to specify the storage account name. For example:

```sql
-- Note that PROVIDER CONFIG is optional as it is the default one
CREATE SECRET secret2 (
    TYPE AZURE,
    PROVIDER CONFIG,
    ACCOUNT_NAME '<storage account name>'
);
```

#### `CREDENTIAL_CHAIN` Provider

The `CREDENTIAL_CHAIN` provider allows connecting using credentials automatically fetched by the Azure SDK via the Azure credential chain.
By default, the `DefaultAzureCredential` chain used, which tries credentials according to the order specified by the [Azure documentation](https://learn.microsoft.com/en-us/javascript/api/@azure/identity/defaultazurecredential?view=azure-node-latest#@azure-identity-defaultazurecredential-constructor).
For example:

```sql
CREATE SECRET secret3 (
    TYPE AZURE,
    PROVIDER CREDENTIAL_CHAIN,
    ACCOUNT_NAME '<storage account name>'
);
```

DuckDB also allows specifying a specific chain using the `CHAIN` keyword. For example:

```sql
CREATE SECRET secret4 (
    TYPE AZURE,
    PROVIDER CREDENTIAL_CHAIN,
    CHAIN 'cli;env;managed_identity',
    ACCOUNT_NAME '<storage account name>'
);
```

#### Configuring a Proxy

To configure proxy information when using secrets, you can add `HTTP_PROXY`, `PROXY_USER_NAME`, and `PROXY_PASSWORD` in the secret definition. For example:

```sql
CREATE SECRET secret5 (
    TYPE AZURE,
    CONNECTION_STRING '<value>',
    HTTP_PROXY 'http://localhost:3128',
    PROXY_USER_NAME 'john',
    PROXY_PASSWORD 'doe'
);
```

> * When using secrets, the `HTTP_PROXY` environment variable will still be honored except is you provide an explicit value for it.
> * When using secrets, the `SET` variable of the *Authentication with variables* session will be ignore.
> * The Azure `CREDENTIAL_CHAIN` provider, the actual token is fetched at query time, not at the time of creating the secret.

### Authentication with Variables (Deprecated)

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

## GitHub Repository

[<span class="github">GitHub</span>](https://github.com/duckdb/duckdb_azure)
