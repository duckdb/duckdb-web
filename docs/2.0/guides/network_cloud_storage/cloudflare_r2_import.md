---
layout: docu
redirect_from:
- /docs/guides/import/cloudflare_r2_import
- /docs/guides/network_cloud_storage/cloudflare_r2_import
- /docs/stable/guides/network_cloud_storage/cloudflare_r2_import
- /docs/current/guides/network_cloud_storage/cloudflare_r2_import
- /docs/lts/guides/network_cloud_storage/cloudflare_r2_import
- /docs/preview/guides/network_cloud_storage/cloudflare_r2_import
title: Cloudflare R2 Import
how_to_topic: network-cloud-storage
---

## Prerequisites

For Cloudflare R2, the [S3 Compatibility API](https://developers.cloudflare.com/r2/api/s3/api/) allows you to use DuckDB's S3 support to read and write from R2 buckets.

This requires the [`httpfs` extension]({% link docs/2.0/core_extensions/httpfs/overview.md %}), which can be installed using the `INSTALL` SQL command. This only needs to be run once.

## Credentials and Configuration

You will need to [generate an S3 auth token](https://developers.cloudflare.com/r2/api/s3/tokens/) and create an `R2` secret in DuckDB:

```sql
CREATE SECRET (
    TYPE r2,
    KEY_ID '⟨AKIAIOSFODNN7EXAMPLE⟩',
    SECRET '⟨wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY⟩',
    ACCOUNT_ID '⟨your-32-character-hexadecimal-account-ID⟩'
);
```

## Querying

After setting up the R2 credentials, you can query the R2 data using DuckDB's built-in methods, such as `read_csv` or `read_parquet`:

```sql
SELECT * FROM read_parquet('r2://⟨r2-bucket-name⟩/⟨file⟩');
```
