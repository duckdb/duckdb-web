---
layout: docu
title: httpfs Extension for HTTP and S3 Support
---

The `httpfs` extension is an autoloadable extension implementing a file system that allows reading remote/writing remote files.
For plain HTTP(S), only file reading is supported. For object storage using the S3 API, the `httpfs` extension supports reading/writing/globbing files.

## Installation and Loading

The `httpfs` extension will be, by default, autoloaded on first use of any functionality exposed by this extension.

To manually install and load the `httpfs` extension, run:

```sql
INSTALL httpfs;
LOAD httpfs;
```

## HTTP(S)

With the `httpfs` extension, it is possible to directly query files over the HTTP(S) protocol. This works for all files supported by DuckDB or its various extensions, and provides read-only access.

```sql
SELECT * FROM 'https://domain.tld/file.extension';
```

For CSV files, files will be downloaded entirely in most cases, due to the row-based nature of the format. For Parquet files, DuckDB can use a combination of the Parquet metadata and HTTP range requests to only download the parts of the file that are actually required by the query. For example, the following query will only read the Parquet metadata and the data for the `column_a` column:

```sql
SELECT column_a FROM 'https://domain.tld/file.parquet';
```

In some cases even, no actual data needs to be read at all as they only require reading the metadata:

```sql
SELECT count(*) FROM 'https://domain.tld/file.parquet';
```

Scanning multiple files over HTTP(S) is also supported:

```sql
SELECT * FROM read_parquet([
    'https://domain.tld/file1.parquet',
    'https://domain.tld/file2.parquet'
]);
```

## S3 API

The `httpfs` extension supports reading/writing/globbing files on object storage servers using the S3 API. S3 offers a standard API to read and write to remote files (while regular http servers, predating S3, do not offer a common write API). DuckDB conforms to the S3 API, that is now common among industry storage providers.

### Platforms

The `httpfs` filesystem is tested with [AWS S3](https://aws.amazon.com/s3/), [Minio](https://min.io/), [Google Cloud](https://cloud.google.com/storage/docs/interoperability), and [lakeFS](https://docs.lakefs.io/integrations/duckdb.html). Other services that implement the S3 API (such as [Cloudflare R2](https://www.cloudflare.com/en-gb/developer-platform/r2/)) should also work, but not all features may be supported.

The following table shows which parts of the S3 API are required for each `httpfs` feature.

<div class="narrow_table"></div>

| Feature | Required S3 API features |
|:---|:---|
| Public file reads | HTTP Range requests |
| Private file reads | Secret key or session token authentication |
| File glob | [ListObjectV2](https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListObjectsV2.html) |
| File writes | [Multipart upload](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html) |

### Configuration and Authentication using Secrets

The preferred way to configure and authenticate to S3 endpoints is to use [secrets](../sql/statements/create_secret).
Multiple secret providers are available.

#### `CONFIG` Provider
The default provider, `CONFIG` (i.e., user-configured), allows access to the S3 bucket by manually providing a key. For example:

```sql
CREATE SECRET secret1 (
    TYPE S3,
    KEY_ID 'AKIAIOSFODNN7EXAMPLE',
    SECRET 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
    REGION 'us-east-1'
);
```

Now, to query using the above secret, simply query any `s3://` prefixed file:

```sql
SELECT * FROM 's3://my-bucket/file.parquet'
```

#### `CREDENTIAL_CHAIN` Provider
The `CREDENTIAL_CHAIN` provider allows automatically fetching credentials using mechanisms provided by the AWS SDK. For example, to use the AWS SDK default provider:

```sql
CREATE SECRET secret2 (
    TYPE S3,
    PROVIDER CREDENTIAL_CHAIN
);
```

Again, to query a file using the above secret, simply query any `s3://` prefixed file.

DuckDB also allows specifying a specific chain using the `CHAIN` keyword. This takes a `;` separated list of providers that will be tried in order. For example:

```sql
CREATE SECRET secret3 (
    TYPE S3,
    PROVIDER CREDENTIAL_CHAIN,
    CHAIN 'env;config',
);
```

The possible values for CHAIN are the following:
[`config`](https://sdk.amazonaws.com/cpp/api/LATEST/aws-cpp-sdk-core/html/class_aws_1_1_auth_1_1_profile_config_file_a_w_s_credentials_provider.html);
[`sts`](https://sdk.amazonaws.com/cpp/api/LATEST/aws-cpp-sdk-core/html/class_aws_1_1_auth_1_1_s_t_s_assume_role_web_identity_credentials_provider.html);
[`sso`](https://sdk.amazonaws.com/cpp/api/LATEST/aws-cpp-sdk-core/html/class_aws_1_1_auth_1_1_s_s_o_credentials_provider.html);
[`env`](https://sdk.amazonaws.com/cpp/api/LATEST/aws-cpp-sdk-core/html/class_aws_1_1_auth_1_1_environment_a_w_s_credentials_provider.html);
[`instance`](https://sdk.amazonaws.com/cpp/api/LATEST/aws-cpp-sdk-core/html/class_aws_1_1_auth_1_1_instance_profile_credentials_provider.html);
[`process`](https://sdk.amazonaws.com/cpp/api/LATEST/aws-cpp-sdk-core/html/class_aws_1_1_auth_1_1_process_credentials_provider.html);
[`task_role`](https://sdk.amazonaws.com/cpp/api/LATEST/aws-cpp-sdk-core/html/namespace_aws_1_1_auth.html#a9515ae0d50cc264d79bd772e9b84bb09)

The CREDENTIAL_CHAIN provider also allows overriding the automatically fetched config. For example, to automatically load credentials, and then override the region, run:

```sql
CREATE SECRET secret4 (
    TYPE AZURE,
    PROVIDER CREDENTIAL_CHAIN,
    CHAIN 'config',
    REGION 'eu-west-1'
);
```

#### R2 Secrets
While [Cloudflare R2](https://www.cloudflare.com/developer-platform/r2) uses the regular S3 API, DuckDB has a special Secret type, `R2`, to make configuring it a bit simpler:
```sql
CREATE SECRET secret5 (
    TYPE R2,
    KEY_ID 'AKIAIOSFODNN7EXAMPLE',
    SECRET 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
    ACCOUNT_ID 'my_account_id'
);
```
Note the addition of the `ACCOUNT_ID` which is used to generate to correct endpoint url for you. Also note that for `R2` Secrets can also use both the `CONFIG` and `CREDENTIAL_CHAIN` providers. Finally, `R2` secrets are only available when using urls starting with `r2://`, for example:

```sql
SELECT * FROM read_parquet('r2://some/file/that/uses/r2/secret/file.parquet')
```

#### GCS Secrets
While [Google Cloud Storage](https://cloud.google.com/storage) is accessed by DuckDB using the S3 API, DuckDB has a special Secret type, `GCS`, to make configuring it a bit simpler:
```sql
CREATE SECRET secret6 (
    TYPE GCS,
    KEY_ID 'my_key',
    SECRET 'my_secret'
)
```
Note that the above secret, will automatically have the correct Google Cloud Storage endpoint configured. Also note that for `GCS` Secrets can also use both the `CONFIG` and `CREDENTIAL_CHAIN` providers. Finally, `GCS` secrets are only available when using urls starting with `gcs://` or `gs://`, for example:

```sql
SELECT * FROM read_parquet('gcs://some/file/that/uses/gcs/secret/file.parquet')
```

#### Overview of S3 Secret parameters

Below is a complete list of the supported parameters that can be used for both the `CONFIG` and `CREDENTIAL_CHAIN` providers: 

| Name                          | Description                                                                           | Secret      | Type      | Default                                     |
|:------------------------------|:--------------------------------------------------------------------------------------|:------------------|:----------|:--------------------------------------------|
| `KEY_ID`                      | The ID of the key to use                                                              | `S3`, `GCS`, `R2` | `STRING`  | -                                           |
| `SECRET`                      | The secret of the key to use                                                          | `S3`, `GCS`, `R2` | `STRING`  | -                                           |
| `REGION`                      | The region for which to authenticate (should match the region of the bucket to query) | `S3`, `GCS`, `R2` | `STRING`  | `us-east-1`                                 |
| `SESSION_TOKEN`               | Optionally, a session token can be passed to use temporary credentials                | `S3`, `GCS`, `R2` | `STRING`  | -                                           |
| `ENDPOINT`                    | Specify a custom S3 endpoint                                                          | `S3`, `GCS`, `R2` | `STRING`  | `s3.amazonaws.com` for `S3`,                |
| `URL_STYLE`                   | Either `vhost` or `path`                                                              | `S3`, `GCS`, `R2` | `STRING`  | `vhost` for `S3`, `path` for `R2` and `GCS` |
| `USE_SSL`                     | Whether to use HTTPS or HTTP                                                          | `S3`, `GCS`, `R2` | `BOOLEAN` | `TRUE`                                      |
| `URL_COMPATIBILITY_MODE`      | Can help when urls contain problematic characters.                                    | `S3`, `GCS`, `R2` | `BOOLEAN` | `TRUE`                                      |
| `ACCOUNT_ID`                  | The R2 account ID to use for generating the endpoint url                              | `R2`              | `STRING`  | -                                           |

### Configuration and Authentication using `SET` Variables (Deprecated)

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

The [`aws` extension](aws) allows for loading AWS credentials.

#### Per-Request Configuration

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

### Reading

Reading files from S3 is now as simple as:

```sql
SELECT * FROM 's3://bucket/file.extension';
```

Multiple files are also possible, for example:

```sql
SELECT * FROM read_parquet(['s3://bucket/file1.parquet', 's3://bucket/file2.parquet']);
```

#### Glob

File globbing is implemented using the ListObjectV2 API call and allows to use filesystem-like glob patterns to match multiple files, for example:

```sql
SELECT * FROM read_parquet('s3://bucket/*.parquet');
```

This query matches all files in the root of the bucket with the [Parquet extension](parquet).

Several features for matching are supported, such as `*` to match any number of any character, `?` for any single character or `[0-9]` for a single character in a range of characters:

```sql
SELECT count(*) FROM read_parquet('s3://bucket/folder*/100?/t[0-9].parquet');
```

A useful feature when using globs is the `filename` option which adds a column with the file that a row originated from:

```sql
SELECT * FROM read_parquet('s3://bucket/*.parquet', FILENAME = 1);
```

could for example result in:

<div class="narrow_table"></div>

| column_a | column_b | filename |
|:---|:---|:---|
| 1 | examplevalue1 | s3://bucket/file1.parquet |
| 2 | examplevalue1 | s3://bucket/file2.parquet |

#### Hive Partitioning

DuckDB also offers support for the Hive partitioning scheme. In the Hive partitioning scheme, data is partitioned in separate files. The columns by which the data is partitioned, are not actually in the files, but are encoded in the file path. So for example let us consider three Parquet files Hive paritioned by year:

```text
s3://bucket/year=2012/file.parquet
s3://bucket/year=2013/file.parquet
s3://bucket/year=2014/file.parquet
```

If scanning these files with the `HIVE_PARTITIONING` option enabled:

```sql
SELECT * FROM read_parquet('s3://bucket/*/file.parquet', HIVE_PARTITIONING = 1);
```

could result in:

<div class="narrow_table"></div>

| column_a | column_b | year |
|:---|:---|:---|
| 1 | examplevalue1 | 2012 |
| 2 | examplevalue2 | 2013 |
| 3 | examplevalue3 | 2014 |

Note that the year column does not actually exist in the Parquet files, it is parsed from the filenames. Within DuckDB however, these columns behave just like regular columns. For example, filters can be applied on Hive partition columns:

```sql
SELECT * FROM read_parquet('s3://bucket/*/file.parquet', HIVE_PARTITIONING = 1) WHERE year = 2013;
```

### Writing

Writing to S3 uses the multipart upload API. This allows DuckDB to robustly upload files at high speed. Writing to S3 works for both CSV and Parquet:

```sql
COPY table_name TO 's3://bucket/file.extension';
```

Partitioned copy to S3 also works:

```sql
COPY table TO 's3://my-bucket/partitioned' (FORMAT PARQUET, PARTITION_BY (part_col_a, part_col_b));
```

An automatic check is performed for existing files/directories, which is currently quite conservative (and on S3 will add a bit of latency). To disable this check and force writing, an `OVERWRITE_OR_IGNORE` flag is added:

```sql
COPY table TO 's3://my-bucket/partitioned' (FORMAT PARQUET, PARTITION_BY (part_col_a, part_col_b), OVERWRITE_OR_IGNORE true);
```

The naming scheme of the written files looks like this:

```text
s3://my-bucket/partitioned/part_col_a=<val>/part_col_b=<val>/data_<thread_number>.parquet
```

#### Configuration

Some additional configuration options exist for the S3 upload, though the default values should suffice for most use cases.

<div class="narrow_table"></div>

| setting | description |  
|:---|:---|
| `s3_uploader_max_parts_per_file` | used for part size calculation, see [AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html) |
| `s3_uploader_max_filesize` | used for part size calculation, see [AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html) |
| `s3_uploader_thread_limit` | maximum number of uploader threads |

Additionally, most of the configuration options can be set via environment variables:

| DuckDB setting         | Environment variable    | Note                                     |
|:-----------------------|:------------------------|:-----------------------------------------|
| `s3_region`            | `AWS_REGION`            | Takes priority over `AWS_DEFAULT_REGION` |
| `s3_region`            | `AWS_DEFAULT_REGION`    |                                          |
| `s3_access_key_id`     | `AWS_ACCESS_KEY_ID`     |                                          |
| `s3_secret_access_key` | `AWS_SECRET_ACCESS_KEY` |                                          |
| `s3_session_token`     | `AWS_SESSION_TOKEN`     |                                          |
| `s3_endpoint`          | `DUCKDB_S3_ENDPOINT`    |                                          |
| `s3_use_ssl`           | `DUCKDB_S3_USE_SSL`     |                                          |

## GitHub

The `httpfs` extension is part of the [main DuckDB repository](https://github.com/duckdb/duckdb/tree/main/extension/httpfs).
