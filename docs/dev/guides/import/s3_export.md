---
layout: docu
redirect_from:
- /docs/guides/import/s3_export
title: S3 Parquet Export
---

To write a Parquet file to S3, the [`httpfs` extension](../../extensions/httpfs) is required. This can be installed use the `INSTALL` SQL command. This only needs to be run once.

```sql
INSTALL httpfs;
```

To load the `httpfs` extension for usage, use the `LOAD` SQL command:

```sql
LOAD httpfs;
```

After loading the `httpfs` extension, set up the credentials and S3 region to write data. You may either use an access key and secret, or a token.

```sql
SET s3_region = 'us-east-1';
SET s3_access_key_id = '<AWS access key id>';
SET s3_secret_access_key = '<AWS secret access key>';
```

The alternative is to use a token:

```sql
SET s3_region = 'us-east-1';
SET s3_session_token = '<AWS session token>';
```

After the `httpfs` extension is set up and the S3 credentials are correctly configured, Parquet files can be written to S3 using the following command:

```sql
COPY <table_name> TO 's3://bucket/file.parquet';
```

Similarly, Google Cloud Storage (GCS) is supported through the Interoperability API. You need to create [HMAC keys](https://console.cloud.google.com/storage/settings;tab=interoperability) and declare them:

```sql
SET s3_endpoint = 'storage.googleapis.com';
SET s3_access_key_id = 'key_id';
SET s3_secret_access_key = 'access_key';
```

Please note you will need to use the `s3://` URL to write your files.

```sql
COPY <table_name> TO 's3://gcs_bucket/file.parquet';
```
