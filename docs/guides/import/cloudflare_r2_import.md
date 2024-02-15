---
layout: docu
title: Cloudflare R2 Import
---

## Prerequisites

For Cloudflare R2, the [S3 Compatibility API](https://developers.cloudflare.com/r2/api/s3/api/) allows you to use DuckDB's S3 support to read and write from R2 buckets.
This requires the [`httpfs` extension](../../extensions/httpfs), which can be installed use the `INSTALL` SQL command. This only needs to be run once.

## Credentials and Configuration

You will need to [generate an S3 auth token](https://developers.cloudflare.com/r2/api/s3/tokens/) and create an `R2` secret in DuckDB:

```sql
CREATE SECRET (
    TYPE R2,
    KEY_ID 'AKIAIOSFODNN7EXAMPLE',
    SECRET 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
    ACCOUNT_ID 'my_account_id'
);
```

## Querying

After setting up the R2 credentials, you can query the R2 data using:

```sql
SELECT * FROM read_parquet('r2://<r2_bucket_name>/<file>');
```
