---
layout: docu
title: Google Cloud Storage Import
redirect_from:
  - /docs/guides/import/gcs_import
---

## Prerequisites

The Google Cloud Storage (GCS) can be used via the [`httpfs` extension](../../extensions/httpfs).
This can be installed with the `INSTALL httpfs` SQL command. This only needs to be run once.

## Credentials and Configuration

You need to create [HMAC keys](https://console.cloud.google.com/storage/settings;tab=interoperability) and declare them:

```sql
CREATE SECRET (
    TYPE GCS,
    KEY_ID 'AKIAIOSFODNN7EXAMPLE',
    SECRET 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
);
```

## Querying

After setting up the GCS credentials, you can query the GCS data using:

```sql
SELECT *
FROM read_parquet('gs://⟨gcs_bucket⟩/⟨file.parquet⟩');
```

## Attaching to Database

You can [attach to a database file](duckdb_over_https_or_s3) in read-only mode:

```sql
ATTACH 'gs://⟨gcs_bucket⟩/⟨file.duckdb⟩' AS ⟨duckdb_database⟩ (READ_ONLY);
```
