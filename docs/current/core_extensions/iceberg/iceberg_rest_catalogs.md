---
layout: docu
redirect_from:
- /docs/preview/core_extensions/iceberg/iceberg_rest_catalogs
- /docs/stable/core_extensions/iceberg/iceberg_rest_catalogs
title: Iceberg REST Catalogs
---

This page covers connecting to Iceberg REST Catalogs: authentication, the full set of `ATTACH` options, and setup instructions for specific catalogs. For the basics of attaching a catalog and querying it, see [Catalog Managed Tables]({% link docs/current/core_extensions/iceberg/overview.md %}#catalog-managed-tables); for write operations, see [Writing to Iceberg]({% link docs/current/core_extensions/iceberg/writing.md %}).

If you are attaching to an Iceberg REST Catalog managed by Amazon, please see the instructions for attaching to [Amazon S3 Tables]({% link docs/current/core_extensions/iceberg/amazon_s3_tables.md %}) or [Amazon SageMaker Lakehouse]({% link docs/current/core_extensions/iceberg/amazon_sagemaker_lakehouse.md %}).

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

You can attach the Iceberg catalog with the following [`ATTACH`]({% link docs/current/sql/statements/attach.md %}) statement.

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

A REST Catalog with OAuth2 authorization can also be attached with just an `ATTACH` statement. See the complete list of `ATTACH` options for a REST Catalog below.

| Parameter                            | Type       | Default              | Description                                                                                                                                                             |
| ------------------------------------ | ---------- | -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ENDPOINT_TYPE`                      | `VARCHAR`  | `NULL`               | Used for attaching S3 Tables or Glue catalogs. Allowed values are `GLUE` and `S3_TABLES`. Cannot be combined with `ENDPOINT` or `AUTHORIZATION_TYPE`.                  |
| `ENDPOINT`                           | `VARCHAR`  | `NULL`               | URL endpoint to communicate with the REST Catalog. Cannot be used in conjunction with `ENDPOINT_TYPE`.                                                                 |
| `SECRET`                             | `VARCHAR`  | `NULL`               | Name of the secret used to communicate with the REST Catalog.                                                                                                          |
| `CLIENT_ID`                          | `VARCHAR`  | `NULL`               | `CLIENT_ID` used for the secret.                                                                                                                                       |
| `CLIENT_SECRET`                      | `VARCHAR`  | `NULL`               | `CLIENT_SECRET` used for the secret.                                                                                                                                   |
| `DEFAULT_REGION`                     | `VARCHAR`  | `NULL`               | Default region to use when communicating with the storage layer.                                                                                                      |
| `DEFAULT_SCHEMA`                     | `VARCHAR`  | `NULL`               | The default schema (namespace) to use for the attached catalog.                                                                                                       |
| `OAUTH2_SERVER_URI`                  | `VARCHAR`  | `NULL`               | OAuth2 server URL for getting a Bearer token.                                                                                                                          |
| `AUTHORIZATION_TYPE`                 | `VARCHAR`  | `OAUTH2`             | Authorization scheme. Pass `SigV4` for catalogs that require SigV4 authorization, or `none` for catalogs that need no authentication. Cannot be combined with `ENDPOINT_TYPE`. |
| `ACCESS_DELEGATION_MODE`             | `VARCHAR`  | `vended_credentials` | Access delegation mode. Allowed values are `vended_credentials` and `none`.                                                                                            |
| `EXTRA_HTTP_HEADERS`                 | `MAP`      | `NULL`               | Additional HTTP headers to send with REST Catalog requests.                                                                                                            |
| `SUPPORT_NESTED_NAMESPACES`          | `BOOLEAN`  | `false`              | Set to `true` for catalogs that support nested namespaces.                                                                                                             |
| `STAGE_CREATE_TABLES`                | `BOOLEAN`  | `true`               | Controls whether DuckDB uses staged `CREATE TABLE`. Disable for catalogs that do not support staged table creation.                                                    |
| `DISABLE_MULTI_TABLE_COMMIT`         | `BOOLEAN`  | `false`              | Disables the multi-table transactions/commit endpoint. Enable for catalogs that reject this endpoint.                                                                  |
| `SKIP_CREATE_TABLE_METADATA_UPDATES` | `BOOLEAN`  | `false`              | Skips follow-up metadata updates after non-staged `CREATE TABLE`. Enable for catalogs that fully initialize metadata during table creation and reject subsequent updates. |
| `REMOVE_FILES_ON_DELETE`             | `BOOLEAN`  | `true`               | Controls whether DuckDB removes storage files when a table is dropped.                                                                                                 |
| `PURGE_REQUESTED`                    | `BOOLEAN`  | `false`              | Sends the [PurgeRequested](https://github.com/apache/iceberg/blob/4b4eb38cf6dda7b43faeb40eb00aa5db424d2ecb/open-api/rest-catalog-open-api.yaml#L1144) parameter when dropping a table. |
| `ENCODE_ENTIRE_PREFIX`               | `BOOLEAN`  | `false`              | URL-encode the entire path prefix when communicating with the catalog.                                                                                                 |
| `MAX_TABLE_STALENESS`                | `INTERVAL` | `NULL`               | Prevents unnecessary requests to the Iceberg REST Catalog. Accepts human-readable interval strings such as `10 minutes`, `30 seconds`, or `1 year`.                    |

> When attaching an AWS catalog with `ENDPOINT_TYPE` (`s3_tables` or `glue`), DuckDB applies AWS-appropriate defaults: `stage_create_tables` and `remove_files_on_delete` become `false` and `purge_requested` becomes `true`, unless you set them explicitly.

The following options can only be passed to a `CREATE SECRET` statement and they require `AUTHORIZATION_TYPE` to be `OAUTH2`:

| Parameter           | Type      | Default | Description                                          |
| ------------------- | --------- | ------- | ---------------------------------------------------- |
| `OAUTH2_GRANT_TYPE` | `VARCHAR` | `NULL`  | Grant Type when requesting an OAuth Token.           |
| `OAUTH2_SCOPE`      | `VARCHAR` | `NULL`  | Requested scope for the returned OAuth Access Token. |


## Working with an Attached Catalog

Once a catalog is attached, you can run the full set of read and write operations against its tables:

* **Reading and metadata**: `SELECT`, time travel with the `AT` clause, and the `iceberg_metadata`, `iceberg_snapshots`, and statistics functions. See the [Functions and Settings Reference]({% link docs/current/core_extensions/iceberg/reference.md %}).
* **Writing**: `CREATE`/`DROP SCHEMA` and `TABLE`, partitioning, `INSERT`, `UPDATE`, `DELETE`, `MERGE INTO`, `ALTER TABLE`, table properties, and `COPY FROM DATABASE`. See [Writing to Iceberg]({% link docs/current/core_extensions/iceberg/writing.md %}).

Metadata functions accept a fully qualified table name, e.g.:

```sql
SELECT * FROM iceberg_snapshots(my_catalog.default.t);
```

## Specific Catalog Examples

DuckDB can attach to a range of Iceberg REST Catalogs. The AWS-managed catalogs have dedicated setup pages because they require AWS credentials and SigV4 authorization:

* [Amazon S3 Tables]({% link docs/current/core_extensions/iceberg/amazon_s3_tables.md %})
* [Amazon SageMaker Lakehouse (AWS Glue)]({% link docs/current/core_extensions/iceberg/amazon_sagemaker_lakehouse.md %})

The remaining catalogs are configured directly on this page:

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

### Catalogs with Limited REST Spec Support

Some catalogs implement a subset of the Iceberg REST Catalog specification. Use the compatibility options below to adjust DuckDB's behavior for these catalogs.

| Catalog behavior | Option to set |
| --- | --- |
| Does not support staged CREATE TABLE | `STAGE_CREATE_TABLES false` |
| Rejects the multi-table transactions/commit endpoint | `DISABLE_MULTI_TABLE_COMMIT true` |
| Fully initializes metadata on CREATE TABLE and rejects follow-up metadata updates | `SKIP_CREATE_TABLE_METADATA_UPDATES true` |
| Does not allow DuckDB to remove storage files on DROP TABLE | `REMOVE_FILES_ON_DELETE false` |

For example, to attach a [Unity Catalog Horizon](https://docs.unitycatalog.io) endpoint that does not support staged creates, rejects the transactions/commit endpoint, and manages its own metadata and storage cleanup:

```sql
ATTACH '⟨warehouse⟩' AS horizon_catalog (
    TYPE iceberg,
    ENDPOINT '⟨catalog_endpoint⟩',
    STAGE_CREATE_TABLES false,
    DISABLE_MULTI_TABLE_COMMIT true,
    SKIP_CREATE_TABLE_METADATA_UPDATES true,
    REMOVE_FILES_ON_DELETE false
);
```

## Limitations

DuckDB supports Iceberg REST Catalogs backed by S3, S3 Tables, and Google Cloud Storage (GCS). Support for other storage backends is not yet available.
