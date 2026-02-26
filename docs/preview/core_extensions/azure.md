---
github_repository: https://github.com/duckdb/duckdb-azure
layout: docu
title: Azure Extension
---

The `azure` extension is a loadable extension that adds a filesystem abstraction for [Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs) to DuckDB, enabling both reading and writing data.

## Installing and Loading

The `azure` extension will be transparently [autoloaded]({% link docs/preview/core_extensions/overview.md %}#autoloading-extensions) on first use from the official extension repository.
If you would like to install and load it manually, run:

```sql
INSTALL azure;
LOAD azure;
```

## Usage

Once the [authentication](#authentication) is set up, you can query Azure storage as follows:

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
TO 'abfss://⟨my_container⟩/⟨path⟩/output.csv';
```

You can also use fully qualified paths:

```sql
COPY my_table
TO 'az://⟨my_storage_account⟩.blob.core.windows.net/⟨my_container⟩/⟨path⟩/output.parquet';
```

## Configuration

Use the following [configuration options]({% link docs/preview/configuration/overview.md %}) to control how the extension reads remote files:

| Name | Description | Type | Default |
|:---|:---|:---|:---|
| `azure_http_stats` | Include HTTP info from Azure Storage in the [`EXPLAIN ANALYZE` statement]({% link docs/preview/dev/profiling.md %}). | `BOOLEAN` | `false` |
| `azure_read_transfer_concurrency` | Maximum number of threads the Azure client can use for a single parallel read. If `azure_read_transfer_chunk_size` is less than `azure_read_buffer_size` then setting this > 1 will allow the Azure client to do concurrent requests to fill the buffer. | `BIGINT` | `5` |
| `azure_read_transfer_chunk_size` | Maximum size in bytes that the Azure client will read in a single request. It is recommended that this is a factor of `azure_read_buffer_size`. | `BIGINT` | `1024*1024` |
| `azure_read_buffer_size` | Size of the read buffer. It is recommended that this is evenly divisible by `azure_read_transfer_chunk_size`. | `UBIGINT` | `1024*1024` |
| `azure_transport_option_type` | Underlying [adapter](https://github.com/Azure/azure-sdk-for-cpp/blob/main/doc/HttpTransportAdapter.md) to use in the Azure SDK. Valid values are: `default` or `curl`. | `VARCHAR` | `default` |
| `azure_context_caching` | Enable/disable the caching of the underlying Azure SDK HTTP connection in the DuckDB connection context when performing queries. If you suspect that this is causing some side effect, you can try to disable it by setting it to false (not recommended). | `BOOLEAN` | `true` |

> Setting `azure_transport_option_type` explicitly to `curl` will have the following effect:
> * On Linux, this may solve certificate issue (`Error: Invalid Error: Fail to get a new connection for: https://storage_account_name.blob.core.windows.net/. Problem with the SSL CA cert (path? access rights?)`) because when specifying the extension will try to find the bundle certificate in various paths (that is not done by *curl* by default and might be wrong due to static linking).
> * On Windows, this replaces the default adapter (*WinHTTP*) allowing you to use all *curl* capabilities (for example using a socks proxies).
> * On all operating systems, it will honor the following environment variables:
>   * `CURL_CA_INFO`: Path to a PEM encoded file containing the certificate authorities sent to libcurl. Note that this option is known to only work on Linux and might throw if set on other platforms.
>   * `CURL_CA_PATH`: Path to a directory which holds PEM encoded files, containing the certificate authorities sent to libcurl.

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

Multiple [Secret Providers]({% link docs/preview/configuration/secrets_manager.md %}#secret-providers) are available for the Azure extension:

* If you need to define different secrets for different storage accounts, use the [`SCOPE` configuration]({% link docs/preview/configuration/secrets_manager.md %}#creating-multiple-secrets-for-the-same-service-type). Note that the `SCOPE` requires a trailing slash (`SCOPE 'azure://some_container/'`).
* If you use fully qualified path then the `ACCOUNT_NAME` attribute is optional.

#### `CONFIG` Provider

The default provider, `CONFIG` (i.e., user-configured), allows access to the storage account using a connection string or anonymously. For example:

```sql
CREATE SECRET secret1 (
    TYPE azure,
    CONNECTION_STRING '⟨value⟩'
);
```

If you do not use authentication, you still need to specify the storage account name. For example:

```sql
CREATE SECRET secret2 (
    TYPE azure,
    PROVIDER config,
    ACCOUNT_NAME '⟨storage_account_name⟩'
);
```

The default `PROVIDER` is `CONFIG`.

#### `credential_chain` Provider

The `credential_chain` provider allows connecting using credentials automatically fetched by the Azure SDK via the Azure credential chain.
By default, the `DefaultAzureCredential` chain used, which tries credentials according to the order specified by the [Azure documentation](https://learn.microsoft.com/en-us/javascript/api/@azure/identity/defaultazurecredential?view=azure-node-latest#@azure-identity-defaultazurecredential-constructor).
For example:

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

The possible values are the following:
[`cli`](https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli);
[`managed_identity`](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview);
[`workload_identity`](https://learn.microsoft.com/en-us/entra/workload-id/workload-identities-overview);
[`env`](https://github.com/Azure/azure-sdk-for-cpp/blob/azure-identity_1.6.0/sdk/identity/azure-identity/README.md#environment-variables);
[`default`](https://github.com/Azure/azure-sdk-for-cpp/blob/azure-identity_1.6.0/sdk/identity/azure-identity/README.md#defaultazurecredential);

If no explicit `CHAIN` is provided, the default one will be [`default`](https://github.com/Azure/azure-sdk-for-cpp/blob/azure-identity_1.6.0/sdk/identity/azure-identity/README.md#defaultazurecredential)

#### Managed Identity

Managed Identity (MI) can be used gracefully and automatically via the `credential_chain`. In typical 
cases where the executor has a single MI available, no configuration is needed. 

If your execution environment has multiple Identities, use the `MANAGED_IDENTITY` provider and specify
which identity to use. This provider allows identity specification via one of 
`CLIENT_ID`, `OBJECT_ID` or `RESOURCE_ID`, e.g.:

```sql
CREATE SECRET secret1 (
    TYPE AZURE,
    PROVIDER MANAGED_IDENTITY,
    ACCOUNT_NAME '⟨storage account name⟩',
    CLIENT_ID '⟨used-assigned managed identity client id⟩'
);
```

The provider may be used without specifying an ID; if only a single ID is available this provider 
will function identically to the `credential_chain` provider, and use the single available ID. If 
multiple IDs are available, behavior is undefined (or more specifically, defined by the Azure SDK)
– therefore we recommend explicit Identity setting in this situation.


#### `SERVICE_PRINCIPAL` Provider

The `SERVICE_PRINCIPAL` provider allows connecting using a [Azure Service Principal (SPN)](https://learn.microsoft.com/en-us/entra/architecture/service-accounts-principal).

Either with a secret:

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

#### Configuring a Proxy

To configure proxy information when using secrets, you can add `HTTP_PROXY`, `PROXY_USER_NAME` and `PROXY_PASSWORD` in the secret definition. For example:

```sql
CREATE SECRET secret5 (
    TYPE azure,
    CONNECTION_STRING '⟨value⟩',
    HTTP_PROXY 'http://localhost:3128',
    PROXY_USER_NAME 'john',
    PROXY_PASSWORD 'doe'
);
```

> * When using secrets, the `HTTP_PROXY` environment variable will still be honored except if you provide an explicit value for it.
> * When using secrets, the `SET` variable of the *Authentication with variables* session will be ignored.
> * For the Azure `credential_chain` provider, the actual token is fetched at query time, not when the secret is created.

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
| `azure_credential_chain`| Ordered list of Azure credential providers, in string format separated by `;`. For example: `'cli;managed_identity;env'`. See the list of possible values in the [`credential_chain` provider section](#credential_chain-provider). Not used if you pass the connection string. | `STRING` | - |
| `azure_http_proxy` | Proxy to use when login & performing request to Azure. | `STRING` | `HTTP_PROXY` environment variable (if set). |
| `azure_proxy_user_name` | HTTP proxy username if needed. | `STRING` | - |
| `azure_proxy_password` | HTTP proxy password if needed. | `STRING` | - |

## Additional Information

### Logging

The Azure extension relies on the Azure SDK to connect to Azure Blob storage and supports printing the SDK logs to the console.
To control the log level, set the [`AZURE_LOG_LEVEL`](https://github.com/Azure/azure-sdk-for-cpp/blob/main/sdk/core/azure-core/README.md#sdk-log-messages) environment variable.

For instance, verbose logs can be enabled in Python as follows:

```python
import os
import duckdb

os.environ["AZURE_LOG_LEVEL"] = "verbose"

duckdb.sql("CREATE SECRET myaccount (TYPE azure, PROVIDER credential_chain, SCOPE 'az://myaccount.blob.core.windows.net/')")
duckdb.sql("SELECT count(*) FROM 'az://myaccount.blob.core.windows.net/path/to/blob.parquet'")
```

### Difference between ADLS and Blob Storage

Even though ADLS implements similar functionality as the Blob storage, there are some important performance benefits to using the ADLS endpoints for globbing, especially when using (complex) glob patterns.

To demonstrate, let's look at an example of how a glob is performed internally using the Blob and ADLS endpoints, respectively.

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

The following query is performed through the Blob endpoint:

```sql
SELECT count(*)
FROM 'az://root/l_receipmonth=1997-*/l_shipmode=SHIP/*.csv';
```

It will perform the following steps:

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

Meanwhile, the same query can be performed through the datalake endpoint as follows:

```sql
SELECT count(*)
FROM 'abfss://root/l_receipmonth=1997-*/l_shipmode=SHIP/*.csv';
```

This will perform the following steps:

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
