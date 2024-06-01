---
layout: docu
title: S3 API Support
---

The `httpfs` extension supports reading/writing/globbing files on object storage servers using the S3 API. S3 offers a standard API to read and write to remote files (while regular http servers, predating S3, do not offer a common write API). DuckDB conforms to the S3 API, that is now common among industry storage providers.

## Platforms

The `httpfs` filesystem is tested with [AWS S3](https://aws.amazon.com/s3/), [Minio](https://min.io/), [Google Cloud](https://cloud.google.com/storage/docs/interoperability), and [lakeFS](https://docs.lakefs.io/integrations/duckdb.html). Other services that implement the S3 API (such as [Cloudflare R2](https://www.cloudflare.com/en-gb/developer-platform/r2/)) should also work, but not all features may be supported.

The following table shows which parts of the S3 API are required for each `httpfs` feature.

<div class="narrow_table"></div>

| Feature | Required S3 API features |
|:---|:---|
| Public file reads | HTTP Range requests |
| Private file reads | Secret key or session token authentication |
| File glob | [ListObjectV2](https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListObjectsV2.html) |
| File writes | [Multipart upload](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html) |

## Configuration and Authentication

The preferred way to configure and authenticate to S3 endpoints is to use [secrets](../../sql/statements/create_secret). Multiple secret providers are available.

> Deprecated Prior to version 0.10.0, DuckDB did not have a [Secrets manager](../../sql/statements/create_secret). Hence, the configuration of and authentication to S3 endpoints was handled via variables. See the [legacy authentication scheme for the S3 API](s3api_legacy_authentication).

### `CONFIG` Provider

The default provider, `CONFIG` (i.e., user-configured), allows access to the S3 bucket by manually providing a key. For example:

```sql
CREATE SECRET secret1 (
    TYPE S3,
    KEY_ID 'AKIAIOSFODNN7EXAMPLE',
    SECRET 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
    REGION 'us-east-1'
);
```

> Tip If you get an IO Error (`Connection error for HTTP HEAD`), configure the endpoint explicitly via `ENDPOINT 's3.⟨your-region⟩.amazonaws.com'`.

Now, to query using the above secret, simply query any `s3://` prefixed file:

```sql
SELECT *
FROM 's3://my-bucket/file.parquet';
```

### `CREDENTIAL_CHAIN` Provider

The `CREDENTIAL_CHAIN` provider allows automatically fetching credentials using mechanisms provided by the AWS SDK. For example, to use the AWS SDK default provider:

```sql
CREATE SECRET secret2 (
    TYPE S3,
    PROVIDER CREDENTIAL_CHAIN
);
```

Again, to query a file using the above secret, simply query any `s3://` prefixed file.

DuckDB also allows specifying a specific chain using the `CHAIN` keyword. This takes a semicolon-separated list (`a;b;c`) of providers that will be tried in order. For example:

```sql
CREATE SECRET secret3 (
    TYPE S3,
    PROVIDER CREDENTIAL_CHAIN,
    CHAIN 'env;config'
);
```

The possible values for `CHAIN` are the following:

* [`config`](https://sdk.amazonaws.com/cpp/api/LATEST/aws-cpp-sdk-core/html/class_aws_1_1_auth_1_1_profile_config_file_a_w_s_credentials_provider.html)
* [`sts`](https://sdk.amazonaws.com/cpp/api/LATEST/aws-cpp-sdk-core/html/class_aws_1_1_auth_1_1_s_t_s_assume_role_web_identity_credentials_provider.html)
* [`sso`](https://sdk.amazonaws.com/cpp/api/LATEST/aws-cpp-sdk-core/html/class_aws_1_1_auth_1_1_s_s_o_credentials_provider.html)
* [`env`](https://sdk.amazonaws.com/cpp/api/LATEST/aws-cpp-sdk-core/html/class_aws_1_1_auth_1_1_environment_a_w_s_credentials_provider.html)
* [`instance`](https://sdk.amazonaws.com/cpp/api/LATEST/aws-cpp-sdk-core/html/class_aws_1_1_auth_1_1_instance_profile_credentials_provider.html)
* [`process`](https://sdk.amazonaws.com/cpp/api/LATEST/aws-cpp-sdk-core/html/class_aws_1_1_auth_1_1_process_credentials_provider.html)

The `CREDENTIAL_CHAIN` provider also allows overriding the automatically fetched config. For example, to automatically load credentials, and then override the region, run:

```sql
CREATE SECRET secret4 (
    TYPE S3,
    PROVIDER CREDENTIAL_CHAIN,
    CHAIN 'config',
    REGION 'eu-west-1'
);
```

### Overview of S3 Secret Parameters

Below is a complete list of the supported parameters that can be used for both the `CONFIG` and `CREDENTIAL_CHAIN` providers:

| Name                          | Description                                                                           | Secret            | Type      | Default                                     |
|:------------------------------|:--------------------------------------------------------------------------------------|:------------------|:----------|:--------------------------------------------|
| `KEY_ID`                      | The ID of the key to use                                                              | `S3`, `GCS`, `R2` | `STRING`  | -                                           |
| `SECRET`                      | The secret of the key to use                                                          | `S3`, `GCS`, `R2` | `STRING`  | -                                           |
| `REGION`                      | The region for which to authenticate (should match the region of the bucket to query) | `S3`, `GCS`, `R2` | `STRING`  | `us-east-1`                                 |
| `SESSION_TOKEN`               | Optionally, a session token can be passed to use temporary credentials                | `S3`, `GCS`, `R2` | `STRING`  | -                                           |
| `ENDPOINT`                    | Specify a custom S3 endpoint                                                          | `S3`, `GCS`, `R2` | `STRING`  | `s3.amazonaws.com` for `S3`,                |
| `URL_STYLE`                   | Either `vhost` or `path`                                                              | `S3`, `GCS`, `R2` | `STRING`  | `vhost` for `S3`, `path` for `R2` and `GCS` |
| `USE_SSL`                     | Whether to use HTTPS or HTTP                                                          | `S3`, `GCS`, `R2` | `BOOLEAN` | `true`                                      |
| `URL_COMPATIBILITY_MODE`      | Can help when urls contain problematic characters.                                    | `S3`, `GCS`, `R2` | `BOOLEAN` | `true`                                      |
| `ACCOUNT_ID`                  | The R2 account ID to use for generating the endpoint url                              | `R2`              | `STRING`  | -                                           |

### Platform-Specific Secret Types

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
SELECT *
FROM read_parquet('r2://some/file/that/uses/r2/secret/file.parquet');
```

#### GCS Secrets

While [Google Cloud Storage](https://cloud.google.com/storage) is accessed by DuckDB using the S3 API, DuckDB has a special Secret type, `GCS`, to make configuring it a bit simpler:

```sql
CREATE SECRET secret6 (
    TYPE GCS,
    KEY_ID 'my_key',
    SECRET 'my_secret'
);
```

Note that the above secret, will automatically have the correct Google Cloud Storage endpoint configured. Also note that for `GCS` Secrets can also use both the `CONFIG` and `CREDENTIAL_CHAIN` providers. Finally, `GCS` secrets are only available when using urls starting with `gcs://` or `gs://`, for example:

```sql
SELECT *
FROM read_parquet('gcs://some/file/that/uses/gcs/secret/file.parquet');
```

## Reading

Reading files from S3 is now as simple as:

```sql
SELECT *
FROM 's3://bucket/file.extension';
```

Multiple files are also possible, for example:

```sql
SELECT *
FROM read_parquet([
    's3://bucket/file1.parquet',
    's3://bucket/file2.parquet'
]);
```

### Glob

File globbing is implemented using the ListObjectV2 API call and allows to use filesystem-like glob patterns to match multiple files, for example:

```sql
SELECT *
FROM read_parquet('s3://bucket/*.parquet');
```

This query matches all files in the root of the bucket with the [Parquet extension](../parquet).

Several features for matching are supported, such as `*` to match any number of any character, `?` for any single character or `[0-9]` for a single character in a range of characters:

```sql
SELECT count(*) FROM read_parquet('s3://bucket/folder*/100?/t[0-9].parquet');
```

A useful feature when using globs is the `filename` option, which adds a column named `filename` that encodes the file that a particular row originated from:

```sql
SELECT *
FROM read_parquet('s3://bucket/*.parquet', filename = true);
```

could for example result in:

<div class="narrow_table"></div>

| column_a | column_b | filename |
|:---|:---|:---|
| 1 | examplevalue1 | s3://bucket/file1.parquet |
| 2 | examplevalue1 | s3://bucket/file2.parquet |

### Hive Partitioning

DuckDB also offers support for the [Hive partitioning scheme](../../data/partitioning/hive_partitioning), which is available when using HTTP(S) and S3 endpoints.

## Writing

Writing to S3 uses the multipart upload API. This allows DuckDB to robustly upload files at high speed. Writing to S3 works for both CSV and Parquet:

```sql
COPY table_name TO 's3://bucket/file.extension';
```

Partitioned copy to S3 also works:

```sql
COPY table TO 's3://my-bucket/partitioned' (
    FORMAT PARQUET,
    PARTITION_BY (part_col_a, part_col_b)
);
```

An automatic check is performed for existing files/directories, which is currently quite conservative (and on S3 will add a bit of latency). To disable this check and force writing, an `OVERWRITE_OR_IGNORE` flag is added:

```sql
COPY table TO 's3://my-bucket/partitioned' (
    FORMAT PARQUET,
    PARTITION_BY (part_col_a, part_col_b),
    OVERWRITE_OR_IGNORE true
);
```

The naming scheme of the written files looks like this:

```text
s3://my-bucket/partitioned/part_col_a=⟨val⟩/part_col_b=⟨val⟩/data_⟨thread_number⟩.parquet
```

### Configuration

Some additional configuration options exist for the S3 upload, though the default values should suffice for most use cases.

<div class="narrow_table"></div>

| Name | Description |
|:---|:---|
| `s3_uploader_max_parts_per_file` | used for part size calculation, see [AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html) |
| `s3_uploader_max_filesize` | used for part size calculation, see [AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html) |
| `s3_uploader_thread_limit` | maximum number of uploader threads |
