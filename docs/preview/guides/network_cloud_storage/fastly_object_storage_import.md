---
layout: docu
title: Fastly Object Storage Import
---

## Prerequisites

For Fastly Object Storage, the [S3 Compatibility API](https://docs.fastly.com/products/object-storage) allows you to use DuckDB's S3 support to read and write from Fastly buckets.

This requires the [`httpfs` extension]({% link docs/preview/core_extensions/httpfs/overview.md %}), which can be installed using the `INSTALL` SQL command. This only needs to be run once.

## Credentials and Configuration

You will need to [generate an S3 auth token](https://docs.fastly.com/en/guides/working-with-object-storage#creating-an-object-storage-access-key) and create an `S3` secret in DuckDB:

```sql
CREATE SECRET my_secret (
    TYPE s3,
    KEY_ID '⟨AKIAIOSFODNN7EXAMPLE⟩',
    SECRET '⟨wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY⟩',
	URL_STYLE 'path',
    REGION '⟨us-east⟩',
    ENDPOINT '⟨us-east⟩.object.fastlystorage.app' -- see note below
);
```

* The `ENDPOINT` needs to point to the [Fastly endpoint for the region](https://docs.fastly.com/en/guides/working-with-object-storage#working-with-the-s3-compatible-api) you want to use (e.g., `eu-central.object.fastlystorage.app`).
* `REGION` must use the same region mentioned in `ENDPOINT`.
* `URL_STYLE` needs to use `path`.

## Querying

After setting up the Fastly Object Storage credentials, you can query the data there using DuckDB's built-in methods, such as `read_csv` or `read_parquet`:

```sql
SELECT * FROM 's3://⟨fastly-bucket-name⟩/(file).csv';
SELECT * FROM read_parquet('s3://⟨fastly-bucket-name⟩/⟨file⟩.parquet');
```
