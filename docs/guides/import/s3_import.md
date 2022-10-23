---
layout: docu
title: S3 or GCS Parquet Import
selected: S3 or GCS Parquet Import
---

# How to load a Parquet file directly from S3 or GCS

To load a Parquet file from S3, the `HTTPFS` extension is required. This can be installed use the `INSTALL` SQL command. This only needs to be run once.

```sql
INSTALL httpfs;
```

To load the `HTTPFS` extension for usage, use the `LOAD` SQL command:

```sql
LOAD httpfs;
```

After loading the `HTTPFS` extension, set up the credentials and S3 region to read data. Firstly, the region where the data
resides needs to be configured:

```sql
SET s3_region='us-east-1';
```

With the only the region set, public S3 data can be queried. To query private S3 data, you need to either use an access key and secret:

```sql
SET s3_access_key_id='<AWS access key id>';
SET s3_secret_access_key='<AWS secret access key>';
```

or a session token:

```sql
SET s3_session_token='<AWS session token>';
```

After the `HTTPFS` extension is set up and the S3 configuration is set correctly, Parquet files can be read from S3 using the following command:

```sql
SELECT * FROM read_parquet('s3://<bucket>/<file>');
```

For GCS, the Interoperability API enables you to have access to it like an S3 connection.
You need to create [HMAC keys](https://console.cloud.google.com/storage/settings;tab=interoperability) and declare them:

```sql
SET s3_endpoint='storage.googleapis.com';
SET s3_access_key_id='key_id';
SET s3_secret_access_key='access_key';
```

Please note you will need to use the `s3://` URL to read your data.

```sql
SELECT * FROM read_parquet('s3://<gcs_bucket>/<file>');
```
