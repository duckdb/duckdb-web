---
layout: docu
title: GCS Import
---

## Prerequisites

For Google Cloud Storage (GCS), the Interoperability API enables you to have access to it like an S3 connection using the [`httpfs` extension](../../extensions/httpfs).
This can be installed with the `INSTALL` SQL command. This only needs to be run once.

## Credentials and Configuration

You need to create [HMAC keys](https://console.cloud.google.com/storage/settings;tab=interoperability) and declare them:

```sql
CREATE SECRET (
    TYPE GCS,
    KEY_ID 'AKIAIOSFODNN7EXAMPLE',
    SECRET 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
);
```

## Querying

After setting up the GCS credentials, you can query the GCS data using:

```sql
SELECT *
FROM read_parquet('gs://⟨gcs_bucket⟩/⟨file⟩');
```
