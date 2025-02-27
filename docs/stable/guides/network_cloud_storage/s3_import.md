---
layout: docu
redirect_from:
- /docs/guides/import/s3_import
- /docs/guides/import/s3_import/
- /docs/guides/network_cloud_storage/s3_import
title: S3 Parquet Import
---

## Prerequisites

To load a Parquet file from S3, the [`httpfs` extension]({% link docs/stable/extensions/httpfs/overview.md %}) is required. This can be installed using the `INSTALL` SQL command. This only needs to be run once.

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
    TYPE s3,
    KEY_ID 'AKIAIOSFODNN7EXAMPLE',
    SECRET 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
    REGION 'us-east-1'
);
```

> Tip If you get an IO Error (`Connection error for HTTP HEAD`), configure the endpoint explicitly via `ENDPOINT 's3.⟨your-region⟩.amazonaws.com'`.

Alternatively, use the [`aws` extension]({% link docs/stable/extensions/aws.md %}) to retrieve the credentials automatically:

```sql
CREATE SECRET (
    TYPE s3,
    PROVIDER credential_chain
);
```

## Querying

After the `httpfs` extension is set up and the S3 configuration is set correctly, Parquet files can be read from S3 using the following command:

```sql
SELECT * FROM read_parquet('s3://⟨bucket⟩/⟨file⟩');
```

## Google Cloud Storage (GCS) and Cloudflare R2

DuckDB can also handle [Google Cloud Storage (GCS)]({% link docs/stable/guides/network_cloud_storage/gcs_import.md %}) and [Cloudflare R2]({% link docs/stable/guides/network_cloud_storage/cloudflare_r2_import.md %}) via the S3 API.
See the relevant guides for details.
