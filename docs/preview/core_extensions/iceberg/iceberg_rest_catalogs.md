---
layout: docu
title: Iceberg REST Catalogs
---

The `iceberg` extension supports attaching Iceberg REST Catalogs. Before attaching an Iceberg REST Catalog, you must install the `iceberg` extension by following the instructions located in the [overview]({% link docs/preview/core_extensions/iceberg/overview.md %}).

If you are attaching to an Iceberg REST Catalog managed by Amazon, please see the instructions for attaching to [Amazon S3 Tables]({% link docs/preview/core_extensions/iceberg/amazon_s3_tables.md %}) or [Amazon SageMaker Lakehouse]({% link docs/preview/core_extensions/iceberg/amazon_sagemaker_lakehouse.md %}).

For all other Iceberg REST Catalogs, you can follow the instructions below. Please see the [Examples](#specific-catalog-examples) section for questions about specific catalogs.

Most Iceberg REST Catalogs authenticate via OAuth2. You can use the existing DuckDB secret workflow to store login credentials for the OAuth2 service.

```sql
CREATE SECRET iceberg_secret (
    TYPE iceberg,
    CLIENT_ID '⟨admin⟩',
    CLIENT_SECRET '⟨password⟩',
    OAUTH2_SERVER_URI '⟨http://iceberg_rest_catalog_url.com/v1/oauth/tokens⟩'
);
```

If you already have a Bearer token, you can pass it directly to your `CREATE SECRET` statement

```sql
CREATE SECRET iceberg_secret (
    TYPE iceberg,
    TOKEN '⟨bearer_token⟩'
);
```

You can attach the Iceberg catalog with the following [`ATTACH`]({% link docs/preview/sql/statements/attach.md %}) statement.

```sql
LOAD httpfs;
ATTACH '⟨warehouse⟩' AS iceberg_catalog (
   TYPE iceberg,
   SECRET iceberg_secret, -- pass a specific secret name to prevent ambiguity
   ENDPOINT '⟨https://rest_endpoint.com⟩'
);
```

To see the available tables run
```sql
SHOW ALL TABLES;
```

## `ATTACH` Options

A REST Catalog with OAuth2 authorization can also be attached with just an `ATTACH` statement. See the complete list of `ATTACH` options for a REST catalog below. 

 
| Parameter                     | Type      | Default  | Description                                                                                           |
|-------------------------------|-----------|----------|-------------------------------------------------------------------------------------------------------|
| `ENDPOINT_TYPE`               | `VARCHAR` | `NULL`   | Used for attaching S3Tables or Glue catalogs. Allowed values are 'GLUE' and 'S3_TABLES'               |
| `ENDPOINT`                    | `VARCHAR` | `NULL`   | URL endpoint to communicate with the REST Catalog. Cannot be used in conjunction with `ENDPOINT_TYPE` |
| `SECRET`                      | `VARCHAR` | `NULL`   | Name of secret used to communicate with the REST Catalog                                              |
| `CLIENT_ID`                   | `VARCHAR` | `NULL`   | CLIENT_ID used for Secret                                                                             |
| `CLIENT_SECRET`               | `VARCHAR` | `NULL`   | CLIENT_SECRET needed for Secret                                                                       |
| `DEFAULT_REGION`              | `VARCHAR` | `NULL`   | A Default region to use when communicating with the storage layer                                     |
| `OAUTH2_SERVER_URI`           | `VARCHAR` | `NULL`   | OAuth2 server url for getting a Bearer Token                                                          |
| `AUTHORIZATION_TYPE`          | `VARCHAR` | `OAUTH2` | Pass `SigV4` for Catalogs the require SigV4 authorization, `none` for catalogs that don't need auth   |
| `ACCESS_DELEGATION_MODE`      | `VARCHAR` | `vended_credentials` | Access delegation mode. Allowed values are `vended_credentials` and `none`               |
| `EXTRA_HTTP_HEADERS`          | `MAP`     | `NULL`   | Additional HTTP headers to send with REST catalog requests                                            |
| `SUPPORT_NESTED_NAMESPACES` | `BOOLEAN` | `true`   | Option for catalogs that support nested namespaces.                                                   |
| `SUPPORT_STAGE_CREATE`        | `BOOLEAN` | `false`  | Option for catalogs that do not support stage create.                                                 |



The following options can only be passed to a `CREATE SECRET` statement, and they require `AUTHORIZATION_TYPE` to be `OAUTH2`

| Parameter           | Type      | Default | Description                                         |
|---------------------|-----------|---------|-----------------------------------------------------|
| `OAUTH2_GRANT_TYPE` | `VARCHAR` | `NULL`  | Grant Type when requesting an OAuth Token           |
| `OAUTH2_SCOPE`      | `VARCHAR` | `NULL`  | Requested scope for the returned OAuth Access Token |


### Supported Operations

The DuckDB Iceberg extension supports the following operations when used with a REST catalog attached:

* `CREATE/DROP SCHEMA`
* `CREATE/DROP TABLE`
* `INSERT INTO`
* `UPDATE`
* `DELETE`
* `SELECT`

Since these operations are supported, the following will also work:

```sql
COPY FROM DATABASE duckdb_db TO iceberg_datalake;
-- Or
COPY FROM DATABASE iceberg_datalake to duckdb_db;
```

This functionality enables deep copies between Iceberg and DuckDB storage.

#### Limitations for UPDATE and DELETE

The `UPDATE` and `DELETE` operations have the following limitations:

* They only work on tables that are **not partitioned** and **not sorted**. Attempting these operations on partitioned or sorted tables results in an error.
* DuckDB-Iceberg only writes **positional deletes**. Copy-on-write functionality is not yet supported.
* DuckDB-Iceberg only supports **merge-on-read semantics**. If a table has `write.update.mode` or `write.delete.mode` properties set to something other than `merge-on-read`, the operation fails.

### Metadata Operations

The functions `iceberg_metadata` and `iceberg_snapshots` are also available to use with an Iceberg REST catalog using a fully qualified path, e.g.

```sql
SELECT * FROM iceberg_metadata(my_datalake.default.t)

-- Or
SELECT * FROM iceberg_snapshots(my_datalake.default.t)
```

This functionality enables the user to do **time traveling**.

```sql
-- Using a snapshot id
SELECT * FROM my_datalake.default.t AT (VERSION => ⟨SNAPSHOT_ID⟩)

-- Or using a timestamp
SELECT * FROM my_datalake.default.t AT (TIMESTAMP => TIMESTAMP '2025-09-22 12:32:43.217')
```

### Interoperability with DuckLake

The DuckDB Iceberg extensions exposes a function to do metadata only copies of the Iceberg metadata to [DuckLake]({% link docs/preview/core_extensions/ducklake.md %}), which enables users to query Iceberg tables as if they were DuckLake tables.

```sql
-- Given that we have an Iceberg catalog attached aliased to iceberg_datalake
ATTACH 'ducklake:my_ducklake.ducklake' AS my_ducklake;

CALL iceberg_to_ducklake('iceberg_datalake', 'my_ducklake');
```

It is also possible to skip a set of tables provided the `skip_tables` parameter.

```sql
CALL iceberg_to_ducklake('iceberg_datalake', 'my_ducklake', skip_tables := ['table_to_skip']);
```

### Table Properties Functions

DuckDB provides functions to view and modify [Iceberg table properties](https://iceberg.apache.org/spec/#table-metadata-fields):

| Function | Description |
|----------|-------------|
| `iceberg_table_properties(table)` | Returns all properties of the specified table. |
| `set_iceberg_table_properties(table, properties)` | Sets properties on the specified table. |
| `remove_iceberg_table_properties(table, property_list)` | Removes properties from the specified table. |

```sql
-- View table properties
SELECT *
FROM iceberg_table_properties(iceberg_catalog.default.my_table);

-- Set table properties
CALL set_iceberg_table_properties(
    iceberg_catalog.default.my_table,
    {'write.update.mode': 'merge-on-read', 'write.delete.mode': 'merge-on-read'}
);

-- Remove table properties
CALL remove_iceberg_table_properties(
    iceberg_catalog.default.my_table,
    ['some.property']
);
```

### Unsupported Operations

The following operations are not supported by the DuckDB Iceberg extension:

* `MERGE INTO`
* `ALTER TABLE`

## Specific Catalog Examples

### Cloudflare R2 Catalog

To attach to an [R2 Cloudflare](https://developers.cloudflare.com/r2/data-catalog/) managed catalog follow the attach steps below. 

```sql
CREATE SECRET r2_secret (
    TYPE iceberg,
    TOKEN '⟨r2_token⟩'
);
```

You can create a token by following the [create an API token](https://developers.cloudflare.com/r2/data-catalog/get-started/#3-create-an-api-token) steps in getting started. Then, attach the catalog with the following commands.

```sql
ATTACH '⟨warehouse⟩' AS my_r2_catalog (
    TYPE iceberg,
    ENDPOINT '⟨catalog-uri⟩'
);
```

The variables for `warehouse` and `catalog-uri` are available under the settings of the R2 Object Storage Catalog (R2 Object Store, Catalog name, Settings).

Once you attached to the R2 Data Catalog, create a schema. You can set it as default with the `USE` command:

```sql
CREATE SCHEMA my_r2_catalog.my_schema;
USE my_r2_catalog.my_schema;
```

### Polaris

To attach to a [Polaris](https://polaris.apache.org) catalog, use the following commands:

```sql
CREATE SECRET polaris_secret (
    TYPE iceberg,
    CLIENT_ID '⟨admin⟩',
    CLIENT_SECRET '⟨password⟩',
);
```

```sql
ATTACH 'quickstart_catalog' AS polaris_catalog (
    TYPE iceberg,
    ENDPOINT '⟨polaris_rest_catalog_endpoint⟩',
    ACCESS_DELEGATION_MODE 'vended_credentials'
);
```

### Lakekeeper

To attach to a [Lakekeeper](https://docs.lakekeeper.io) catalog the following commands will work.

```sql
CREATE SECRET lakekeeper_secret (
    TYPE iceberg,
    CLIENT_ID '⟨admin⟩',
    CLIENT_SECRET '⟨password⟩',
    OAUTH2_SCOPE '⟨scope⟩',
    OAUTH2_SERVER_URI '⟨lakekeeper_oauth_url⟩'
);
```

```sql
ATTACH '⟨warehouse⟩' AS lakekeeper_catalog (
    TYPE iceberg,
    ENDPOINT '⟨lakekeeper_irc_url⟩',
    SECRET '⟨lakekeeper_secret⟩'
);
```

### Google Cloud BigLake

To attach to a [Google Cloud BigLake](https://cloud.google.com/biglake) catalog, you can use extra HTTP headers to specify the GCP project for billing purposes.

First, get your Google Cloud access token:

```bash
gcloud auth application-default print-access-token
```

Then create a secret with the token and extra headers:

```sql
CREATE SECRET biglake_secret (
    TYPE iceberg,
    TOKEN '⟨your_access_token⟩',
    EXTRA_HTTP_HEADERS MAP {
        'x-goog-user-project': '⟨your_gcp_project_id⟩'
    }
);
```

Attach to the BigLake catalog:

```sql
ATTACH '⟨gs://your-biglake-bucket⟩' AS biglake_catalog (
    TYPE iceberg,
    ENDPOINT 'https://biglake.googleapis.com/iceberg/v1/restcatalog',
    SECRET biglake_secret
);
```

Example using the [BigLake public dataset](https://opensource.googleblog.com/2026/01/explore-public-datasets-with-apache-iceberg-and-biglake.html):

```sql
CREATE SECRET biglake_public_secret (
    TYPE iceberg,
    TOKEN '⟨your_access_token⟩',
    EXTRA_HTTP_HEADERS MAP {
        'x-goog-user-project': '⟨your_gcp_project_id⟩'
    }
);

ATTACH 'gs://biglake-public-nyc-taxi-iceberg' AS biglake_public (
    TYPE iceberg,
    ENDPOINT 'https://biglake.googleapis.com/iceberg/v1/restcatalog',
    SECRET biglake_public_secret
);

-- Query the data
SELECT count(*) FROM biglake_public.public_data.nyc_taxicab;
```

> Note: Google Cloud access tokens expire after 1 hour. For long-running sessions, you'll need to refresh the token periodically.

## Limitations

DuckDB supports Iceberg REST Catalogs backed by S3, S3 Tables, and Google Cloud Storage (GCS). Support for other storage backends is not yet available.
