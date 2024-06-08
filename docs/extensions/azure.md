---
layout: docu
title: Azure Extension
github_repository: https://github.com/duckdb/duckdb_azure
---

The `azure` extension is a loadable extension that adds a filesystem abstraction for the [Azure Blob storage](https://azure.microsoft.com/en-us/products/storage/blobs) to DuckDB.

## Installing and Loading

To install and load the `azure` extension, run:

```sql
INSTALL azure;
LOAD azure;
```

## Usage

Once the [authentication](#authentication) is set up, you can query Azure storage as follows:

### For Azure Blob Storage

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

### For Azure Data Lake Storage (ADLS)

Allowed URI schemes: `abfss`

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

## Configuration

Use the following [configuration options](../configuration/overview) how the extension reads remote files:

| Name | Description | Type | Default |
|:---|:---|:---|:---|
| `azure_http_stats` | Include http info from Azure Storage in the [`EXPLAIN ANALYZE` statement](/dev/profiling). | `BOOLEAN` | `false` |
| `azure_read_transfer_concurrency` | Maximum number of threads the Azure client can use for a single parallel read. If `azure_read_transfer_chunk_size` is less than `azure_read_buffer_size` then setting this > 1 will allow the Azure client to do concurrent requests to fill the buffer. | `BIGINT` | `5` |
| `azure_read_transfer_chunk_size` | Maximum size in bytes that the Azure client will read in a single request. It is recommended that this is a factor of `azure_read_buffer_size`. | `BIGINT` | `1024*1024` |
| `azure_read_buffer_size` | Size of the read buffer. It is recommended that this is evenly divisible by `azure_read_transfer_chunk_size`. | `UBIGINT` | `1024*1024` |
| `azure_transport_option_type` | Underlying [adapter](https://github.com/Azure/azure-sdk-for-cpp/blob/main/doc/HttpTransportAdapter.md) to use in the Azure SDK. Valid values are: `default` or `curl`. | `VARCHAR` | `default` |
| `azure_context_caching` | Enable/disable the caching of the underlying Azure SDK HTTP connection in the DuckDB connection context when performing queries. If you suspect that this is causing some side effect, you can try to disable it by setting it to false (not recommended). | `BOOLEAN` | `true` |

> Setting `azure_transport_option_type` explicitly to `curl` with have the following effect:
> * On Linux, this may solve certificates issue (`Error: Invalid Error: Fail to get a new connection for: https://⟨storage account name⟩.blob.core.windows.net/. Problem with the SSL CA cert (path? access rights?)`) because when specifying the extension will try to find the bundle certificate in various paths (that is not done by *curl* by default and might be wrong due to static linking).
> * On Windows, this replaces the default adapter (*WinHTTP*) allowing you to use all *curl* capabilities (for example using a socks proxies).
> * On all operating systems, it will honor the following environment variables:
>   * `CURL_CA_INFO`: Path to a PEM encoded file containing the certificate authorities sent to libcurl. Note that this option is known to only work on Linux and might throw if set on other platforms.
>   * `CURL_CA_PATH`: Path to a directory which holds PEM encoded file, containing the certificate authorities sent to libcurl.

Example:

```sql
SET azure_http_stats = false;
SET azure_read_transfer_concurrency = 5;
SET azure_read_transfer_chunk_size = 1_048_576;
SET azure_read_buffer_size = 1_048_576;
```

## Authentication

The Azure extension has two ways to configure the authentication. The preferred way is to use Secrets.

### Authentication with Secret

Multiple [Secret Providers](../configuration/secrets_manager#secret-providers) are available for the Azure extension:

> * If you need to define different secrets for different storage accounts you can use [the `SCOPE` configuration](../configuration/secrets_manager#creating-multiple-secrets-for-the-same-service-type).
> * If you use fully qualified path then the `ACCOUNT_NAME` attribute is optional.

#### `CONFIG` Provider

The default provider, `CONFIG` (i.e., user-configured), allows access to the storage account using a connection string or anonymously. For example:

```sql
CREATE SECRET secret1 (
    TYPE AZURE,
    CONNECTION_STRING '⟨value⟩'
);
```

If you do not use authentication, you still need to specify the storage account name. For example:

```sql
CREATE SECRET secret2 (
    TYPE AZURE,
    PROVIDER CONFIG,
    ACCOUNT_NAME '⟨storage account name⟩'
);
```

The default `PROVIDER` is `CONFIG`.

#### `CREDENTIAL_CHAIN` Provider

The `CREDENTIAL_CHAIN` provider allows connecting using credentials automatically fetched by the Azure SDK via the Azure credential chain.
By default, the `DefaultAzureCredential` chain used, which tries credentials according to the order specified by the [Azure documentation](https://learn.microsoft.com/en-us/javascript/api/@azure/identity/defaultazurecredential?view=azure-node-latest#@azure-identity-defaultazurecredential-constructor).
For example:

```sql
CREATE SECRET secret3 (
    TYPE AZURE,
    PROVIDER CREDENTIAL_CHAIN,
    ACCOUNT_NAME '⟨storage account name⟩'
);
```

DuckDB also allows specifying a specific chain using the `CHAIN` keyword. This takes a semicolon-separated list (`a;b;c`) of providers that will be tried in order. For example:

```sql
CREATE SECRET secret4 (
    TYPE AZURE,
    PROVIDER CREDENTIAL_CHAIN,
    CHAIN 'cli;env',
    ACCOUNT_NAME '⟨storage account name⟩'
);
```

The possible values are the following:
[`cli`](https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli);
[`managed_identity`](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview);
[`env`](https://github.com/Azure/azure-sdk-for-cpp/blob/azure-identity_1.6.0/sdk/identity/azure-identity/README.md#environment-variables);
[`default`](https://github.com/Azure/azure-sdk-for-cpp/blob/azure-identity_1.6.0/sdk/identity/azure-identity/README.md#defaultazurecredential);

If no explicit `CHAIN` is provided, the default one will be [`default`](https://github.com/Azure/azure-sdk-for-cpp/blob/azure-identity_1.6.0/sdk/identity/azure-identity/README.md#defaultazurecredential)

#### `SERVICE_PRINCIPAL` Provider

The `SERVICE_PRINCIPAL` provider allows connecting using a [Azure Service Principal (SPN)](https://learn.microsoft.com/en-us/entra/architecture/service-accounts-principal).

Either with a secret:

```sql
CREATE SECRET azure_spn (
    TYPE AZURE,
    PROVIDER SERVICE_PRINCIPAL,
    TENANT_ID '⟨tenant id⟩',
    CLIENT_ID '⟨client id⟩',
    CLIENT_SECRET '⟨client secret⟩',
    ACCOUNT_NAME '⟨storage account name⟩'
);
```

Or with a certificate:

```sql
CREATE SECRET azure_spn_cert (
    TYPE AZURE,
    PROVIDER SERVICE_PRINCIPAL,
    TENANT_ID '⟨tenant id⟩',
    CLIENT_ID '⟨client id⟩',
    CLIENT_CERTIFICATE_PATH '⟨client cert path⟩',
    ACCOUNT_NAME '⟨storage account name⟩'
);
```

#### Configuring a Proxy

To configure proxy information when using secrets, you can add `HTTP_PROXY`, `PROXY_USER_NAME`, and `PROXY_PASSWORD` in the secret definition. For example:

```sql
CREATE SECRET secret5 (
    TYPE AZURE,
    CONNECTION_STRING '⟨value⟩',
    HTTP_PROXY 'http://localhost:3128',
    PROXY_USER_NAME 'john',
    PROXY_PASSWORD 'doe'
);
```

> * When using secrets, the `HTTP_PROXY` environment variable will still be honored except if you provide an explicit value for it.
> * When using secrets, the `SET` variable of the *Authentication with variables* session will be ignored.
> * The Azure `CREDENTIAL_CHAIN` provider, the actual token is fetched at query time, not at the time of creating the secret.

### Authentication with Variables (Deprecated)

```sql
SET variable_name = variable_value;
```

Where `variable_name` can be one of the following:

| Name | Description | Type | Default |
|:---|:---|:---|:---|
| `azure_storage_connection_string` | Azure connection string, used for authenticating and configuring Azure requests. | `STRING` | - |
| `azure_account_name` | Azure account name, when set, the extension will attempt to automatically detect credentials (not used if you pass the connection string). | `STRING` | - |
| `azure_endpoint` | Override the Azure endpoint for when the Azure credential providers are used. | `STRING` | `blob.core.windows.net` |
| `azure_credential_chain`| Ordered list of Azure credential providers, in string format separated by `;`. For example: `'cli;managed_identity;env'`. See the list of possible values in the [`CREDENTIAL_CHAIN` provider section](#credential_chain-provider). Not used if you pass the connection string. | `STRING` | - |
| `azure_http_proxy`| Proxy to use when login & performing request to Azure. | `STRING` | `HTTP_PROXY` environment variable (if set). |
| `azure_proxy_user_name`| Http proxy username if needed. | `STRING` | - |
| `azure_proxy_password`| Http proxy password if needed. | `STRING` | - |

## Additional Information

### Difference between ADLS and Blob Storage

Even though ADLS implements similar functionality as the Blob storage, there are some important performance benefits to using the ADLS endpoints for globbing, especially when using (complex) glob patterns.

To demonstrate, lets look at an example of how the a glob is performed internally using respectively the Glob and ADLS endpoints.

Using the following filesystem:

```text
root
├── l_receipmonth=1997-10
│   ├── l_shipmode=AIR
│   │   └── data_0.csv
│   ├── l_shipmode=SHIP
│   │   └── data_0.csv
│   └── l_shipmode=TRUCK
│       └── data_0.csv
├── l_receipmonth=1997-11
│   ├── l_shipmode=AIR
│   │   └── data_0.csv
│   ├── l_shipmode=SHIP
│   │   └── data_0.csv
│   └── l_shipmode=TRUCK
│       └── data_0.csv
└── l_receipmonth=1997-12
    ├── l_shipmode=AIR
    │   └── data_0.csv
    ├── l_shipmode=SHIP
    │   └── data_0.csv
    └── l_shipmode=TRUCK
        └── data_0.csv
```

The following query performed through the blob endpoint

```sql
SELECT count(*)
FROM 'az://root/l_receipmonth=1997-*/l_shipmode=SHIP/*.csv';
```

will perform the following steps:

* List all the files with the prefix `root/l_receipmonth=1997-`
    * `root/l_receipmonth=1997-10/l_shipmode=SHIP/data_0.csv`
    * `root/l_receipmonth=1997-10/l_shipmode=AIR/data_0.csv`
    * `root/l_receipmonth=1997-10/l_shipmode=TRUCK/data_0.csv`
    * `root/l_receipmonth=1997-11/l_shipmode=SHIP/data_0.csv`
    * `root/l_receipmonth=1997-11/l_shipmode=AIR/data_0.csv`
    * `root/l_receipmonth=1997-11/l_shipmode=TRUCK/data_0.csv`
    * `root/l_receipmonth=1997-12/l_shipmode=SHIP/data_0.csv`
    * `root/l_receipmonth=1997-12/l_shipmode=AIR/data_0.csv`
    * `root/l_receipmonth=1997-12/l_shipmode=TRUCK/data_0.csv`
* Filter the result with the requested pattern `root/l_receipmonth=1997-*/l_shipmode=SHIP/*.csv`
    * `root/l_receipmonth=1997-10/l_shipmode=SHIP/data_0.csv`
    * `root/l_receipmonth=1997-11/l_shipmode=SHIP/data_0.csv`
    * `root/l_receipmonth=1997-12/l_shipmode=SHIP/data_0.csv`

Meanwhile, the same query performed through the datalake endpoint,

```sql
SELECT count(*)
FROM 'abfss://root/l_receipmonth=1997-*/l_shipmode=SHIP/*.csv';
```

will perform the following steps:

* List all directories in `root/`
    * `root/l_receipmonth=1997-10`
    * `root/l_receipmonth=1997-11`
    * `root/l_receipmonth=1997-12`
* Filter and list subdirectories: `root/l_receipmonth=1997-10`, `root/l_receipmonth=1997-11`, `root/l_receipmonth=1997-12`
    * `root/l_receipmonth=1997-10/l_shipmode=SHIP`
    * `root/l_receipmonth=1997-10/l_shipmode=AIR`
    * `root/l_receipmonth=1997-10/l_shipmode=TRUCK`
    * `root/l_receipmonth=1997-11/l_shipmode=SHIP`
    * `root/l_receipmonth=1997-11/l_shipmode=AIR`
    * `root/l_receipmonth=1997-11/l_shipmode=TRUCK`
    * `root/l_receipmonth=1997-12/l_shipmode=SHIP`
    * `root/l_receipmonth=1997-12/l_shipmode=AIR`
    * `root/l_receipmonth=1997-12/l_shipmode=TRUCK`
* Filter and list subdirectories: `root/l_receipmonth=1997-10/l_shipmode=SHIP`, `root/l_receipmonth=1997-11/l_shipmode=SHIP`, `root/l_receipmonth=1997-12/l_shipmode=SHIP`
    * `root/l_receipmonth=1997-10/l_shipmode=SHIP/data_0.csv`
    * `root/l_receipmonth=1997-11/l_shipmode=SHIP/data_0.csv`
    * `root/l_receipmonth=1997-12/l_shipmode=SHIP/data_0.csv`

As you can see because the Blob endpoint does not support the notion of directories, the filter can only be performed after the listing, whereas the ADLS endpoint will list files recursively. Especially with higher partition/directory counts, the performance difference can be very significant.
