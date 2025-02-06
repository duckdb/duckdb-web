---
layout: docu
redirect_from:
- /docs/archive/1.1/guides/import/cloudflare_r2_import
title: Cloudflare R2 Import
---

## Prerequisites

For Cloudflare R2, the [S3 Compatibility API](https://developers.cloudflare.com/r2/api/s3/api/) allows you to use DuckDB's S3 support to read and write from R2 buckets.

This requires the [`httpfs` extension]({% link docs/archive/1.1/extensions/httpfs/overview.md %}), which can be installed using the `INSTALL` SQL command. This only needs to be run once.

## Credentials and Configuration

You will need to [generate an S3 auth token](https://developers.cloudflare.com/r2/api/s3/tokens/) and create an `R2` secret in DuckDB:

```sql
CREATE SECRET (
    TYPE R2,
    KEY_ID 'AKIAIOSFODNN7EXAMPLE',
    SECRET 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
    ACCOUNT_ID 'your-account-id-here' -- your 33 character hexadecimal account ID
);
```

## Querying

After setting up the R2 credentials, you can query the R2 data using DuckDB's built-in methods, such as `read_csv` or `read_parquet`:

```sql
SELECT * FROM read_parquet('r2://⟨r2_bucket_name⟩/⟨file⟩');
```