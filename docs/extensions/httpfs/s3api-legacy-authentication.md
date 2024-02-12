---
layout: docu
title: Legacy Authentication Scheme for S3 API
---

Prior to version 0.10.0, DuckDB did not have a [Secrets manager](../../sql/statements/create_secret). Hence, the configuration of and authentication to S3 endpoints was handled via variables. This page documents the legacy authentication scheme for the S3 API.

> The recommended way to configuration and authentication of S3 endpoints is to use [secrets](s3api#configuration-and-authentication).

## Legacy Authentication Scheme

To be able to read or write from S3, the correct region should be set:

```sql
SET s3_region = 'us-east-1';
```

Optionally, the endpoint can be configured in case a non-AWS object storage server is used:

```sql
SET s3_endpoint = '<domain>.<tld>:<port>';
```

If the endpoint is not SSL-enabled then run: 

```sql
SET s3_use_ssl = false;
```

Switching between [path-style](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-bucket-intro.html#path-style-url-ex) and [vhost-style](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-bucket-intro.html#virtual-host-style-url-ex) URLs is possible using:

```sql
SET s3_url_style = 'path';
```

However, note that this may also require updating the endpoint. For example for AWS S3 it is required to change the endpoint to `s3.<region>.amazonaws.com`.

After configuring the correct endpoint and region, public files can be read. To also read private files, authentication credentials can be added:

```sql
SET s3_access_key_id = '<AWS access key id>';
SET s3_secret_access_key = '<AWS secret access key>';
```

Alternatively, session tokens are also supported and can be used instead:

```sql
SET s3_session_token = '<AWS session token>';
```

The [`aws` extension](../aws) allows for loading AWS credentials.

## Per-Request Configuration

Aside from the global S3 configuration described above, specific configuration values can be used on a per-request basis. This allows for use of multiple sets of credentials, regions, etc. These are used by including them on the S3 URI as query parameters. All the individual configuration values listed above can be set as query parameters. For instance:

```sql
SELECT *
FROM 's3://bucket/file.parquet?s3_access_key_id=accessKey&s3_secret_access_key=secretKey';
```

Multiple configurations per query are also allowed:

```sql
SELECT *
FROM 's3://bucket/file.parquet?s3_region=region&s3_session_token=session_token' T1
INNER JOIN 's3://bucket/file.csv?s3_access_key_id=accessKey&s3_secret_access_key=secretKey' T2;
```

## Configuration

Some additional configuration options exist for the S3 upload, though the default values should suffice for most use cases.

Additionally, most of the configuration options can be set via environment variables:

<div class="narrow_table"></div>

| DuckDB setting         | Environment variable    | Note                                     |
|:-----------------------|:------------------------|:-----------------------------------------|
| `s3_region`            | `AWS_REGION`            | Takes priority over `AWS_DEFAULT_REGION` |
| `s3_region`            | `AWS_DEFAULT_REGION`    |                                          |
| `s3_access_key_id`     | `AWS_ACCESS_KEY_ID`     |                                          |
| `s3_secret_access_key` | `AWS_SECRET_ACCESS_KEY` |                                          |
| `s3_session_token`     | `AWS_SESSION_TOKEN`     |                                          |
| `s3_endpoint`          | `DUCKDB_S3_ENDPOINT`    |                                          |
| `s3_use_ssl`           | `DUCKDB_S3_USE_SSL`     |                                          |
