---
layout: docu
title: S3 Parquet Export
selected: S3 Parquet Export
---

# How to write a Parquet file directly to S3

To write a Parquet file to S3, the `HTTPFS` extension is required. This can be installed use the `INSTALL` SQL command. This only needs to be run once.

```sql
INSTALL httpfs;
```

To load the `HTTPFS` extension for usage, use the `LOAD` SQL command:

```sql
LOAD httpfs;
```

After loading the `HTTPFS` extension, set up the credentials and S3 region to write data. You may either use an access key and secret, or a token.

```sql
SET s3_region='us-east-1';
SET s3_access_key_id='<AWS access key id>';
SET s3_secret_access_key='<AWS secret access key>';
```
The alternative is to use a token:
```sql
SET s3_region='us-east-1';
SET s3_session_token='<AWS session token>';
```

After the `HTTPFS` extension is set up and the S3 credentials are correctly configured, Parquet files can be written to S3 using the following command:

```sql
COPY <table_name> TO 's3://bucket/file.extension';
```
