---
layout: docu
redirect_from:
- /docs/stable/extensions/iceberg/amazon_s3_tables
- /docs/preview/core_extensions/iceberg/amazon_s3_tables
- /docs/stable/core_extensions/iceberg/amazon_s3_tables
- /docs/current/core_extensions/iceberg/amazon_s3_tables
- /docs/stable/extensions/iceberg/amazon_sagemaker_lakehouse
- /docs/preview/core_extensions/iceberg/amazon_sagemaker_lakehouse
- /docs/stable/core_extensions/iceberg/amazon_sagemaker_lakehouse
- /docs/current/core_extensions/iceberg/amazon_sagemaker_lakehouse
- /docs/preview/core_extensions/iceberg/iceberg_rest_catalogs
- /docs/stable/core_extensions/iceberg/iceberg_rest_catalogs
- /docs/current/core_extensions/iceberg/iceberg_rest_catalogs
title: Catalogs
---

The `iceberg` extension supports attaching Iceberg REST Catalogs. Attaching a catalog is required for [writing to Iceberg]({% link docs/current/core_extensions/iceberg/writing_to_iceberg.md %}). Before attaching an Iceberg REST Catalog, you must install the `iceberg` extension by following the instructions located in the [overview]({% link docs/current/core_extensions/iceberg/overview.md %}).

The section below describes the generic way of attaching an Iceberg REST Catalog. For instructions specific to a catalog implementation, see [Amazon S3 Tables](#amazon-s3-tables), [AWS Glue](#aws-glue-amazon-sagemaker-lakehouse), [Cloudflare R2 Data Catalog](#cloudflare-r2-data-catalog), [Apache Polaris](#apache-polaris), [Lakekeeper](#lakekeeper) and [Google Cloud BigLake](#google-cloud-biglake).

## Attaching an Iceberg REST Catalog

Most Iceberg REST Catalogs authenticate via OAuth2. You can use the existing DuckDB secret workflow to store login credentials for the OAuth2 service.

```sql
CREATE SECRET iceberg_secret (
    TYPE ICEBERG,
    CLIENT_ID '⟨admin⟩',
    CLIENT_SECRET '⟨password⟩',
    OAUTH2_SERVER_URI '⟨http://iceberg_rest_catalog_url.com/v1/oauth/tokens⟩'
);
```

If you already have a Bearer token, you can pass it directly to your `CREATE SECRET` statement

```sql
CREATE SECRET iceberg_secret (
    TYPE ICEBERG,
    TOKEN '⟨bearer_token⟩'
);
```

You can attach the Iceberg catalog with the following [`ATTACH`]({% link docs/current/sql/statements/attach.md %}) statement.

```sql
LOAD httpfs;
ATTACH '⟨warehouse⟩' AS iceberg_catalog (
   TYPE ICEBERG,
   SECRET iceberg_secret, -- pass a specific secret name to prevent ambiguity
   ENDPOINT '⟨https://rest_endpoint.com⟩'
);
```

To see the available tables run

```sql
SHOW ALL TABLES;
```

A REST Catalog with OAuth2 authorization can also be attached with just an `ATTACH` statement. For the complete list of `ATTACH` and `CREATE SECRET` options, see the [Iceberg Options]({% link docs/current/core_extensions/iceberg/iceberg_options.md %}#attach-options) page.

## Amazon S3 Tables

The `iceberg` extension supports reading Iceberg tables stored in [Amazon S3 Tables](https://aws.amazon.com/s3/features/tables/).

To use it, install the following extensions:

You can let DuckDB detect your AWS credentials and configuration based on the default profile in your `~/.aws` directory by creating the following secret using the [Secrets Manager]({% link docs/current/configuration/secrets_manager.md %}):

```sql
CREATE SECRET (
    TYPE s3,
    PROVIDER credential_chain
);
```

Alternatively, you can set the values manually:

```sql
CREATE SECRET (
    TYPE s3,
    KEY_ID '⟨key_id⟩',
    SECRET '⟨secret⟩',
    REGION '⟨region⟩'
);
```

Then, connect to the catalog using your S3 Tables ARN (available in the AWS Management Console) and the `ENDPOINT_TYPE s3_tables` option:

```sql
ATTACH '⟨s3_tables_arn⟩' AS my_s3_tables_catalog (
   TYPE ICEBERG,
   ENDPOINT_TYPE s3_tables
);
```

To check whether the attachment worked, list all tables:

```sql
SHOW ALL TABLES;
```

You can query a table as follows:

```sql
SELECT count(*)
FROM my_s3_tables_catalog.⟨namespace_name⟩.⟨table_name⟩;
```

## AWS Glue (Amazon SageMaker Lakehouse)

The `iceberg` extension supports reading Iceberg tables through the [Amazon SageMaker Lakehouse (a.k.a. AWS Glue)](https://aws.amazon.com/sagemaker/lakehouse/) catalog.

Create an S3 secret using the [Secrets Manager]({% link docs/current/configuration/secrets_manager.md %}):

```sql
CREATE SECRET (
    TYPE s3,
    PROVIDER credential_chain,
    REGION '<region>'
);
```

In this example we use an STS token, but [other authentication methods are supported]({% link docs/current/core_extensions/aws.md %}).

Then, connect to the catalog:

```sql
ATTACH '⟨account_id⟩' AS glue_catalog (
    TYPE ICEBERG,
    ENDPOINT 'glue.⟨REGION⟩.amazonaws.com/iceberg',
    AUTHORIZATION_TYPE 'sigv4'
);
```

Or alternatively:

```sql
ATTACH '⟨account_id⟩' AS glue_catalog (
    TYPE ICEBERG,
    ENDPOINT_TYPE 'glue'
);
```

To check whether the attachment worked, list all tables:

```sql
SHOW ALL TABLES;
```

You can query a table as follows:

```sql
SELECT count(*)
FROM glue_catalog.⟨namespace_name⟩.⟨table_name⟩;
```

If you have an S3 Tables federated catalog, you can create a table using the standard `CREATE TABLE` syntax;

```sql
CREATE TABLE glue_catalog.⟨namespace_name⟩.⟨table_name⟩ (a INTEGER, b VARCHAR);
```

If the catalog is not federated by S3 Tables, you may need to create pass a `location` table property. You can do so using the `WITH` clause.

```sql
CREATE TABLE glue_catalog.⟨namespace_name⟩.⟨table_name⟩ (a INTEGER, b VARCHAR)
WITH (
    'location' = 's3://path/to/location'
);
```

You can learn more about the `WITH` clause at [Creating Tables]({% link docs/current/core_extensions/iceberg/writing_to_iceberg.md %}#creating-tables).

## Cloudflare R2 Data Catalog

To attach to an [R2 Cloudflare](https://developers.cloudflare.com/r2/data-catalog/) managed catalog follow the attach steps below.

```sql
CREATE SECRET r2_secret (
    TYPE ICEBERG,
    TOKEN '⟨r2_token⟩'
);
```

You can create a token by following the [create an API token](https://developers.cloudflare.com/r2/data-catalog/get-started/#3-create-an-api-token) steps in getting started. Then, attach the catalog with the following commands.

```sql
ATTACH '⟨warehouse⟩' AS my_r2_catalog (
    TYPE ICEBERG,
    ENDPOINT '⟨catalog-uri⟩'
);
```

The variables for `warehouse` and `catalog-uri` are available under the settings of the R2 Object Storage Catalog (R2 Object Store, Catalog name, Settings).

Once you attached to the R2 Data Catalog, create a schema. You can set it as default with the `USE` command:

```sql
CREATE SCHEMA my_r2_catalog.my_schema;
USE my_r2_catalog.my_schema;
```

## Apache Polaris

To attach to a [Polaris](https://polaris.apache.org) catalog, use the following commands:

```sql
CREATE SECRET polaris_secret (
    TYPE ICEBERG,
    CLIENT_ID '⟨admin⟩',
    CLIENT_SECRET '⟨password⟩',
);
```

```sql
ATTACH 'quickstart_catalog' AS polaris_catalog (
    TYPE ICEBERG,
    ENDPOINT '⟨polaris_rest_catalog_endpoint⟩',
    ACCESS_DELEGATION_MODE 'vended_credentials'
);
```

## Lakekeeper

To attach to a [Lakekeeper](https://docs.lakekeeper.io) catalog the following commands will work.

```sql
CREATE SECRET lakekeeper_secret (
    TYPE ICEBERG,
    CLIENT_ID '⟨admin⟩',
    CLIENT_SECRET '⟨password⟩',
    OAUTH2_SCOPE '⟨scope⟩',
    OAUTH2_SERVER_URI '⟨lakekeeper_oauth_url⟩'
);
```

```sql
ATTACH '⟨warehouse⟩' AS lakekeeper_catalog (
    TYPE ICEBERG,
    ENDPOINT '⟨lakekeeper_irc_url⟩',
    SECRET '⟨lakekeeper_secret⟩'
);
```

## Google Cloud BigLake

To attach to a [Google Cloud BigLake](https://cloud.google.com/biglake) catalog, you can use extra HTTP headers to specify the GCP project for billing purposes.

First, get your Google Cloud access token:

```bash
gcloud auth application-default print-access-token
```

Then create a secret with the token and extra headers:

```sql
CREATE SECRET biglake_secret (
    TYPE ICEBERG,
    TOKEN '⟨your_access_token⟩',
    EXTRA_HTTP_HEADERS MAP {
        'x-goog-user-project': '⟨your_gcp_project_id⟩'
    }
);
```

Attach to the BigLake catalog:

```sql
ATTACH '⟨gs://your-biglake-bucket⟩' AS biglake_catalog (
    TYPE ICEBERG,
    ENDPOINT 'https://biglake.googleapis.com/iceberg/v1/restcatalog',
    SECRET biglake_secret
);
```

Example using the [BigLake public dataset](https://opensource.googleblog.com/2026/01/explore-public-datasets-with-apache-iceberg-and-biglake.html):

```sql
CREATE SECRET biglake_public_secret (
    TYPE ICEBERG,
    TOKEN '⟨your_access_token⟩',
    EXTRA_HTTP_HEADERS MAP {
        'x-goog-user-project': '⟨your_gcp_project_id⟩'
    }
);

ATTACH 'gs://biglake-public-nyc-taxi-iceberg' AS biglake_public (
    TYPE ICEBERG,
    ENDPOINT 'https://biglake.googleapis.com/iceberg/v1/restcatalog',
    SECRET biglake_public_secret
);

-- Query the data
SELECT count(*) FROM biglake_public.public_data.nyc_taxicab;
```

> Note: Google Cloud access tokens expire after 1 hour. For long-running sessions, you'll need to refresh the token periodically.

## Limitations

DuckDB supports Iceberg REST Catalogs backed by S3, S3 Tables, and Google Cloud Storage (GCS). Support for other storage backends is not yet available.
