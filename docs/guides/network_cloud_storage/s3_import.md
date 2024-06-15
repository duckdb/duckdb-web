---
layout: docu
title: S3 Parquet Import
redirect_from:
  - /docs/guides/import/s3_import
---

## Prerequisites

To load a Parquet file from S3, the [`httpfs` extension]({% link docs/extensions/httpfs/overview.md %}) is required. This can be installed use the `INSTALL` SQL command. This only needs to be run once.

```sql
INSTALL httpfs;
```

To load the `httpfs` extension for usage, use the `LOAD` SQL command:

```sql
LOAD httpfs;
```

## Credentials and Configuration

After loading the `httpfs` extension, set up the credentials and S3 region to read data:

```sql
CREATE SECRET (
    TYPE S3,
    KEY_ID 'AKIAIOSFODNN7EXAMPLE',
    SECRET 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
    REGION 'us-east-1'
);
```

> Tip If you get an IO Error (`Connection error for HTTP HEAD`), configure the endpoint explicitly via `ENDPOINT 's3.⟨your-region⟩.amazonaws.com'`.

Alternatively, use the [`aws` extension]({% link docs/extensions/aws.md %}) to retrieve the credentials automatically:

```sql
CREATE SECRET (
    TYPE S3,
    PROVIDER CREDENTIAL_CHAIN
);
```

## Querying

After the `httpfs` extension is set up and the S3 configuration is set correctly, Parquet files can be read from S3 using the following command:

```sql
SELECT * FROM read_parquet('s3://⟨bucket⟩/⟨file⟩');
```

## Google Cloud Storage (GCS) and Cloudflare R2

DuckDB can also handle [Google Cloud Storage (GCS)]({% link docs/guides/network_cloud_storage/gcs_import.md %}) and [Cloudflare R2]({% link docs/guides/network_cloud_storage/cloudflare_r2_import.md %}) via the S3 API.
See the relevant guides for details.
