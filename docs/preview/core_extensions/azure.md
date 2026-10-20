---
github_repository: https://github.com/duckdb/duckdb-azure
layout: docu
title: Azure Extension
---

The `azure` extension lets DuckDB read and write files in [Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs) and Azure Data Lake Storage (ADLS) Gen2.

## Installing and Loading

The `azure` extension will be transparently [autoloaded]({% link docs/preview/extensions/overview.md %}#autoloading-extensions) on first use from the official extension repository.
If you would like to install and load it manually, run:

```sql
INSTALL AND LOAD azure;
```

## Usage

Queries need a [secret](#authentication-with-secret); for a public container, a secret with the storage account name is enough (see the [`CONFIG` provider](#config-provider)). Then you can query Azure storage as follows:

### Azure Blob Storage

Allowed URI schemes: `az` or `azure`

```sql
SELECT count(*)
FROM 'az://⟨my_container⟩/⟨path⟩/⟨my_file⟩.⟨parquet_or_csv⟩';
```

Globs are also supported:

```sql
SELECT *
FROM 'az://⟨my_container⟩/⟨path⟩/*.csv';
```

```sql
SELECT *
FROM 'az://⟨my_container⟩/⟨path⟩/**';
```

Or with a fully qualified path syntax:

```sql
SELECT count(*)
FROM 'az://⟨my_storage_account⟩.blob.core.windows.net/⟨my_container⟩/⟨path⟩/⟨my_file⟩.⟨parquet_or_csv⟩';
```

```sql
SELECT *
FROM 'az://⟨my_storage_account⟩.blob.core.windows.net/⟨my_container⟩/⟨path⟩/*.csv';
```

### Azure Data Lake Storage (ADLS)

Allowed URI schemes: `abfss` or `abfs` (both connect over HTTPS)

```sql
SELECT count(*)
FROM 'abfss://⟨my_filesystem⟩/⟨path⟩/⟨my_file⟩.⟨parquet_or_csv⟩';
```

Globs are also supported:

```sql
SELECT *
FROM 'abfss://⟨my_filesystem⟩/⟨path⟩/*.csv';
```

```sql
SELECT *
FROM 'abfss://⟨my_filesystem⟩/⟨path⟩/**';
```

Or with a fully qualified path syntax:

```sql
SELECT count(*)
FROM 'abfss://⟨my_storage_account⟩.dfs.core.windows.net/⟨my_filesystem⟩/⟨path⟩/⟨my_file⟩.⟨parquet_or_csv⟩';
```

```sql
SELECT *
FROM 'abfss://⟨my_storage_account⟩.dfs.core.windows.net/⟨my_filesystem⟩/⟨path⟩/*.csv';
```

The fully qualified path can also use the `⟨my_filesystem⟩@⟨my_storage_account⟩`{:.language-sql .highlight} form:

```sql
SELECT count(*)
FROM 'abfss://⟨my_filesystem⟩@⟨my_storage_account⟩.dfs.core.windows.net/⟨path⟩/⟨my_file⟩.⟨parquet_or_csv⟩';
```

## Writing to Azure Blob Storage

You can write data directly to Azure Blob or ADLSv2 Storage using the [`COPY` statement]({% link docs/preview/sql/statements/copy.md %}).

```sql
-- Write query results to a Parquet file on Blob Storage
COPY (SELECT * FROM my_table)
TO 'az://⟨my_container⟩/⟨path⟩/output.parquet';
```

```sql
-- Write a table to a CSV file on ADLSv2 Storage
COPY my_table
TO 'abfss://⟨my_filesystem⟩/⟨path⟩/output.csv';
```

You can also use fully qualified paths:

```sql
COPY my_table
TO 'az://⟨my_storage_account⟩.blob.core.windows.net/⟨my_container⟩/⟨path⟩/output.parquet';
```

Since v1.5.4, the extension buffers written data locally and uploads it in blocks of `azure_write_block_size` bytes (default: 8 MiB).
By default, the uploaded blocks are committed when the file is closed, so other readers see the new content only after the write completes.
To commit earlier, set `azure_write_staged_blocks_per_commit` to the number of blocks after which an intermediate commit happens.

> Warning An intermediate commit makes an incomplete file visible to readers. A Parquet file cannot be read until its footer is written at the end, so keep the default `0` for Parquet files and for Delta, Iceberg or DuckLake tables.

### Writing Large Files

Azure limits a blob to 50,000 blocks.
With the default block size of 8 MiB, the largest file you can write is about 390 GiB.
To write larger files, increase `azure_write_block_size` (maximum: 4000 MiB, about 3.9 GiB). For example, to write files up to about 3 TiB:

```sql
SET azure_write_block_size = 64 * 1024 * 1024;
```

## Configuration

Use the following [configuration options]({% link docs/preview/configuration/overview.md %}) to control how the extension reads and writes remote files:

| Name | Description | Type | Default |
|:---|:---|:---|:---|
| `azure_http_stats` | Include HTTP info from Azure Storage in the [`EXPLAIN ANALYZE` statement]({% link docs/preview/dev/profiling.md %}). | `BOOLEAN` | `false` |
| `azure_http_logging` | Write Azure HTTP requests to the DuckDB `HTTP` log when it is enabled. See [Logging](#logging). | `BOOLEAN` | `true` |
| `azure_http_logging_redact_query_params` | Semicolon-separated list of URL query parameter names (case-sensitive) whose values are redacted in the HTTP log. | `VARCHAR` | `sig` |
| `azure_http_logging_redact_headers` | Semicolon-separated list of header names (case-insensitive) whose values are redacted in the HTTP log, for both requests and responses. | `VARCHAR` | `Authorization` |
| `azure_read_transfer_concurrency` | Maximum number of threads the Azure client can use for a single parallel read. Values above 1 let the client fill one buffer with parallel requests, when the chunk size is smaller than the buffer. | `INTEGER` | `5` |
| `azure_read_transfer_chunk_size` | Maximum size in bytes that the Azure client will read in a single request. Should be a divisor of `azure_read_buffer_size`. | `BIGINT` | `8*1024*1024` |
| `azure_read_buffer_size` | Size of the read buffer. Should be a multiple of `azure_read_transfer_chunk_size`. | `UBIGINT` | `8*1024*1024` |
| `azure_write_block_size` | Size in bytes of each block for Blob and ADLS writes. Setting it to `0` restores the default. The maximum is 4000 MiB (about 3.9 GiB). See [Writing Large Files](#writing-large-files). | `UBIGINT` | `8*1024*1024` |
| `azure_write_staged_blocks_per_commit` | Number of uploaded blocks after which an intermediate commit happens. With `0`, all blocks are committed when the file is closed. Non-zero values make partial writes visible sooner, at the cost of extra requests. This option does not change the 50,000-block limit. | `UBIGINT` | `0` |
| `azure_transport_option_type` | Underlying [adapter](https://github.com/Azure/azure-sdk-for-cpp/blob/main/doc/HttpTransportAdapter.md) to use in the Azure SDK. Valid values are: `default` or `curl`. | `VARCHAR` | `default` |
| `azure_context_caching` | Enable/disable the caching of the underlying Azure SDK HTTP connection in the DuckDB connection context when performing queries. If you suspect that this is causing some side effect, you can try to disable it by setting it to false (not recommended). | `BOOLEAN` | `true` |

Since v1.5.4, `azure_read_transfer_chunk_size` and `azure_read_buffer_size` default to 8 MiB (previously 1 MiB).

> Tip Setting `azure_transport_option_type` to `curl` has the following effects:
>
> * On Linux, it may fix certificate errors such as `Problem with the SSL CA cert (path? access rights?)`: the extension then looks for the CA bundle in the usual paths, which *curl* does not do by default and which static linking may get wrong.
> * On Windows, it replaces the default adapter (*WinHTTP*), so you can use all *curl* features, e.g., SOCKS proxies.
> * On all operating systems, it honors these environment variables:
>     * `CURL_CA_INFO`: path to a PEM encoded file with the certificate authorities for libcurl. It is known to work only on Linux and may fail on other platforms.
>     * `CURL_CA_PATH`: path to a directory of PEM encoded files with the certificate authorities for libcurl.

Example:

```sql
SET azure_http_stats = false;
SET azure_read_transfer_concurrency = 5;
SET azure_read_transfer_chunk_size = 8_388_608;
SET azure_read_buffer_size = 8_388_608;
```

## Authentication

Authenticate with a [secret](#authentication-with-secret). The `SET` variables in [Authentication with Variables](#authentication-with-variables) still work but are deprecated.

### Authentication with Secret

Several [Secret Providers]({% link docs/preview/configuration/secrets_manager.md %}#secret-providers) are available, described below. These rules apply to every provider:

* If you need to define different secrets for different storage accounts, use the [`SCOPE` configuration]({% link docs/preview/configuration/secrets_manager.md %}#creating-multiple-secrets-for-the-same-service-type). Note that the `SCOPE` requires a trailing slash (`SCOPE 'az://⟨my_storage_account⟩.blob.core.windows.net/'`{:.language-sql .highlight}).
* With fully qualified paths, `ACCOUNT_NAME` is optional.
* For paths that are not fully qualified, the `ENDPOINT` attribute overrides the default endpoint (`blob.core.windows.net` for `az://` and `azure://`, `dfs.core.windows.net` for `abfss://` and `abfs://`).

#### `CONFIG` Provider

The default provider, `CONFIG` (i.e., user-configured), allows access to the storage account using a connection string or anonymously. For example:

```sql
CREATE SECRET secret1 (
    TYPE azure,
    CONNECTION_STRING '⟨connection_string⟩'
);
```

For anonymous access, give the storage account name:

```sql
CREATE SECRET secret2 (
    TYPE azure,
    PROVIDER config,
    ACCOUNT_NAME '⟨storage_account_name⟩'
);
```

#### `credential_chain` Provider

The `credential_chain` provider allows connecting using credentials automatically fetched by the Azure SDK via the Azure credential chain.
By default, the provider uses the Azure SDK's [`DefaultAzureCredential`](https://github.com/Azure/azure-sdk-for-cpp/blob/azure-identity_1.6.0/sdk/identity/azure-identity/README.md#defaultazurecredential) chain. The token is fetched at query time, not when the secret is created. For example:

```sql
CREATE SECRET secret3 (
    TYPE azure,
    PROVIDER credential_chain,
    ACCOUNT_NAME '⟨storage_account_name⟩'
);
```

DuckDB also allows specifying a specific chain using the `CHAIN` keyword. This takes a semicolon-separated list (`a;b;c`) of providers that will be tried in order. For example:

```sql
CREATE SECRET secret4 (
    TYPE azure,
    PROVIDER credential_chain,
    CHAIN 'cli;env',
    ACCOUNT_NAME '⟨storage_account_name⟩'
);
```

The possible values are:

* [`cli`](https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli): the Azure CLI login
* [`managed_identity`](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview)
* [`workload_identity`](https://learn.microsoft.com/en-us/entra/workload-id/workload-identities-overview), e.g., on AKS
* [`env`](https://github.com/Azure/azure-sdk-for-cpp/blob/azure-identity_1.6.0/sdk/identity/azure-identity/README.md#environment-variables): environment variables
* [`default`](https://github.com/Azure/azure-sdk-for-cpp/blob/azure-identity_1.6.0/sdk/identity/azure-identity/README.md#defaultazurecredential): the full default chain, used when no `CHAIN` is given

#### `MANAGED_IDENTITY` Provider

If the machine has one managed identity, the `credential_chain` provider uses it with no extra options. If it has several, use the `MANAGED_IDENTITY` provider and pick one with `CLIENT_ID`, `OBJECT_ID` or `RESOURCE_ID`:

```sql
CREATE SECRET azure_mi (
    TYPE azure,
    PROVIDER managed_identity,
    ACCOUNT_NAME '⟨storage_account_name⟩',
    CLIENT_ID '⟨client_id⟩'
);
```

Without an ID, the provider works like `credential_chain`. With several identities and no ID, the Azure SDK decides which one is used, so set an ID.

#### `SERVICE_PRINCIPAL` Provider

The `SERVICE_PRINCIPAL` provider allows connecting using an [Azure Service Principal (SPN)](https://learn.microsoft.com/en-us/entra/architecture/service-accounts-principal).

With a client secret:

```sql
CREATE SECRET azure_spn (
    TYPE azure,
    PROVIDER service_principal,
    TENANT_ID '⟨tenant_id⟩',
    CLIENT_ID '⟨client_id⟩',
    CLIENT_SECRET '⟨client_secret⟩',
    ACCOUNT_NAME '⟨storage_account_name⟩'
);
```

Or with a certificate:

```sql
CREATE SECRET azure_spn_cert (
    TYPE azure,
    PROVIDER service_principal,
    TENANT_ID '⟨tenant_id⟩',
    CLIENT_ID '⟨client_id⟩',
    CLIENT_CERTIFICATE_PATH '⟨client_cert_path⟩',
    ACCOUNT_NAME '⟨storage_account_name⟩'
);
```

#### `ACCESS_TOKEN` Provider

The `ACCESS_TOKEN` provider allows connecting with an OAuth access token (bearer token) that you obtained outside of DuckDB:

```sql
CREATE SECRET azure_token (
    TYPE azure,
    PROVIDER access_token,
    ACCESS_TOKEN '⟨access_token⟩',
    ACCOUNT_NAME '⟨storage_account_name⟩'
);
```

> Warning The extension does not refresh the token. When it expires, run `CREATE OR REPLACE SECRET` with a new token; it takes effect on the next query.

#### Configuring a Proxy

To configure proxy information when using secrets, you can add `HTTP_PROXY`, `PROXY_USER_NAME` and `PROXY_PASSWORD` in the secret definition. For example:

```sql
CREATE SECRET secret5 (
    TYPE azure,
    CONNECTION_STRING '⟨connection_string⟩',
    HTTP_PROXY 'http://localhost:3128',
    PROXY_USER_NAME '⟨proxy_user_name⟩',
    PROXY_PASSWORD '⟨proxy_password⟩'
);
```

> Note When you use secrets:
>
> * The `HTTP_PROXY` environment variable is still honored, unless the secret sets `HTTP_PROXY`.
> * The `SET` variables of [Authentication with Variables](#authentication-with-variables) are ignored.

### Authentication with Variables

> Deprecated Use [secrets](#authentication-with-secret) instead.

```sql
SET ⟨variable_name⟩ = ⟨value⟩;
```

Where `variable_name` can be one of the following:

| Name | Description | Type | Default |
|:---|:---|:---|:---|
| `azure_storage_connection_string` | Azure connection string, used for authenticating and configuring Azure requests. | `VARCHAR` | - |
| `azure_account_name` | Azure account name, when set, the extension will attempt to automatically detect credentials (not used if you pass the connection string). | `VARCHAR` | - |
| `azure_endpoint` | Override the Azure endpoint for when the Azure credential providers are used. | `VARCHAR` | `blob.core.windows.net` |
| `azure_credential_chain`| Ordered list of Azure credential providers, in string format separated by `;`. For example: `'cli;managed_identity;env'`. See the list of possible values in the [`credential_chain` provider section](#credential_chain-provider). Not used if you pass the connection string. | `VARCHAR` | - |
| `azure_http_proxy` | Proxy for login and for requests to Azure. | `VARCHAR` | `HTTP_PROXY` environment variable (if set). |
| `azure_proxy_user_name` | HTTP proxy username if needed. | `VARCHAR` | - |
| `azure_proxy_password` | HTTP proxy password if needed. | `VARCHAR` | - |

## Additional Information

### Logging

Since v1.5.2, the Azure extension writes its HTTP requests to the DuckDB [`HTTP` log]({% link docs/preview/operations_manual/logging/overview.md %}). To inspect them:

```sql
CALL enable_logging('HTTP');
SELECT * FROM 'az://⟨my_container⟩/⟨path⟩/⟨my_file⟩.parquet';
SELECT request.type, request.url, response.status FROM duckdb_logs_parsed('HTTP');
```

Logged requests show the DuckDB `User-Agent` header.
The values of the `sig` query parameter and the `Authorization` header are replaced by `REDACTED`.
To change what is redacted, set `azure_http_logging_redact_query_params` and `azure_http_logging_redact_headers`.
A new value replaces the default list, so include `sig` or `Authorization` if you still want them redacted:

```sql
SET azure_http_logging_redact_headers = 'Authorization;x-ms-date';
```

> Warning The Azure extension applies only these settings, not DuckDB's `redact_http_logs` setting. To keep Azure requests out of the `HTTP` log, run `SET azure_http_logging = false;`.

The Azure extension relies on the Azure SDK to connect to Azure Blob storage and supports printing the SDK logs to the console.
To control the log level, set the [`AZURE_LOG_LEVEL`](https://github.com/Azure/azure-sdk-for-cpp/blob/main/sdk/core/azure-core/README.md#sdk-log-messages) environment variable.

For instance, to start the DuckDB CLI with verbose logs:

```batch
AZURE_LOG_LEVEL=verbose duckdb
```

```sql
CREATE SECRET myaccount (
    TYPE azure,
    PROVIDER credential_chain,
    SCOPE 'az://⟨my_storage_account⟩.blob.core.windows.net/'
);
SELECT count(*) FROM 'az://⟨my_storage_account⟩.blob.core.windows.net/⟨my_container⟩/⟨path⟩/⟨my_file⟩.parquet';
```

### Difference between ADLS and Blob Storage

For glob patterns over many directories, prefer `abfss://`: the ADLS endpoint lists only the directories that match, while the Blob endpoint lists every file under the prefix and filters afterwards. The following example shows how a glob is performed through each endpoint.

Using the following filesystem:

```text
root
├── l_receiptmonth=1997-10
│   ├── l_shipmode=AIR
│   │   └── data_0.csv
│   ├── l_shipmode=SHIP
│   │   └── data_0.csv
│   └── l_shipmode=TRUCK
│       └── data_0.csv
├── l_receiptmonth=1997-11
│   ├── l_shipmode=AIR
│   │   └── data_0.csv
│   ├── l_shipmode=SHIP
│   │   └── data_0.csv
│   └── l_shipmode=TRUCK
│       └── data_0.csv
└── l_receiptmonth=1997-12
    ├── l_shipmode=AIR
    │   └── data_0.csv
    ├── l_shipmode=SHIP
    │   └── data_0.csv
    └── l_shipmode=TRUCK
        └── data_0.csv
```

The following query is performed through the Blob endpoint:

```sql
SELECT count(*)
FROM 'az://root/l_receiptmonth=1997-*/l_shipmode=SHIP/*.csv';
```

It will perform the following steps:

* List all the files with the prefix `root/l_receiptmonth=1997-`
    * `root/l_receiptmonth=1997-10/l_shipmode=SHIP/data_0.csv`
    * `root/l_receiptmonth=1997-10/l_shipmode=AIR/data_0.csv`
    * `root/l_receiptmonth=1997-10/l_shipmode=TRUCK/data_0.csv`
    * `root/l_receiptmonth=1997-11/l_shipmode=SHIP/data_0.csv`
    * `root/l_receiptmonth=1997-11/l_shipmode=AIR/data_0.csv`
    * `root/l_receiptmonth=1997-11/l_shipmode=TRUCK/data_0.csv`
    * `root/l_receiptmonth=1997-12/l_shipmode=SHIP/data_0.csv`
    * `root/l_receiptmonth=1997-12/l_shipmode=AIR/data_0.csv`
    * `root/l_receiptmonth=1997-12/l_shipmode=TRUCK/data_0.csv`
* Filter the result with the requested pattern `root/l_receiptmonth=1997-*/l_shipmode=SHIP/*.csv`
    * `root/l_receiptmonth=1997-10/l_shipmode=SHIP/data_0.csv`
    * `root/l_receiptmonth=1997-11/l_shipmode=SHIP/data_0.csv`
    * `root/l_receiptmonth=1997-12/l_shipmode=SHIP/data_0.csv`

Meanwhile, the same query can be performed through the datalake endpoint as follows:

```sql
SELECT count(*)
FROM 'abfss://root/l_receiptmonth=1997-*/l_shipmode=SHIP/*.csv';
```

This will perform the following steps:

* List all directories in `root/`
    * `root/l_receiptmonth=1997-10`
    * `root/l_receiptmonth=1997-11`
    * `root/l_receiptmonth=1997-12`
* Filter and list subdirectories: `root/l_receiptmonth=1997-10`, `root/l_receiptmonth=1997-11`, `root/l_receiptmonth=1997-12`
    * `root/l_receiptmonth=1997-10/l_shipmode=SHIP`
    * `root/l_receiptmonth=1997-10/l_shipmode=AIR`
    * `root/l_receiptmonth=1997-10/l_shipmode=TRUCK`
    * `root/l_receiptmonth=1997-11/l_shipmode=SHIP`
    * `root/l_receiptmonth=1997-11/l_shipmode=AIR`
    * `root/l_receiptmonth=1997-11/l_shipmode=TRUCK`
    * `root/l_receiptmonth=1997-12/l_shipmode=SHIP`
    * `root/l_receiptmonth=1997-12/l_shipmode=AIR`
    * `root/l_receiptmonth=1997-12/l_shipmode=TRUCK`
* Filter and list subdirectories: `root/l_receiptmonth=1997-10/l_shipmode=SHIP`, `root/l_receiptmonth=1997-11/l_shipmode=SHIP`, `root/l_receiptmonth=1997-12/l_shipmode=SHIP`
    * `root/l_receiptmonth=1997-10/l_shipmode=SHIP/data_0.csv`
    * `root/l_receiptmonth=1997-11/l_shipmode=SHIP/data_0.csv`
    * `root/l_receiptmonth=1997-12/l_shipmode=SHIP/data_0.csv`

Because the Blob endpoint does not support the notion of directories, the filter can only be performed after the listing, whereas the ADLS endpoint will list files recursively. Especially with higher partition/directory counts, the performance difference can be very significant.
