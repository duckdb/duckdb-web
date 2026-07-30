---
layout: docu
redirect_from:
- /docs/extensions/httpfs/s3api
- /docs/stable/extensions/httpfs/s3api
- /docs/preview/core_extensions/httpfs/s3api
- /docs/stable/core_extensions/httpfs/s3api
- /docs/stable/extensions/httpfs/s3api
title: S3 API Support
---

The `httpfs` extension supports reading/writing/[globbing](#globbing) files on object storage servers using the S3 API. S3 offers a standard API to read and write to remote files (while regular http servers, predating S3, do not offer a common write API). DuckDB conforms to the S3 API, that is now common among industry storage providers.

## Platforms

The `httpfs` filesystem is tested with [AWS S3](https://aws.amazon.com/s3/), [Minio](https://min.io/), [Google Cloud](https://cloud.google.com/storage/docs/interoperability) and [lakeFS](https://docs.lakefs.io/integrations/duckdb.html). Other services that implement the S3 API (such as [Cloudflare R2](https://www.cloudflare.com/en-gb/developer-platform/r2/) and [Tigris](https://www.tigrisdata.com/)) should also work, but not all features may be supported.

The following table shows which parts of the S3 API are required for each `httpfs` feature.

| Feature | Required S3 API features |
|:---|:---|
| Public file reads | HTTP Range requests |
| Private file reads | Secret key or session token authentication |
| File glob | [ListObjectsV2](https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListObjectsV2.html) |
| File writes | [Multipart upload](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html) |

## Configuration and Authentication

The preferred way to configure and authenticate to S3 endpoints is to use [secrets]({% link docs/current/sql/statements/create_secret.md %}). Multiple secret providers are available.

To migrate from the [deprecated S3 API]({% link docs/current/core_extensions/httpfs/s3api_legacy_authentication.md %}), use a defined secret with a profile.
See [Selecting a Profile]({% link docs/current/core_extensions/aws.md %}#selecting-a-profile).

### `config` Provider

The default provider, `config` (i.e., user-configured), allows access to the S3 bucket by manually providing a key. For example:

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER config,
    KEY_ID '⟨AKIAIOSFODNN7EXAMPLE⟩',
    SECRET '⟨wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY⟩',
    REGION '⟨us-east-1⟩'
);
```

> Tip If you get an IO Error (`Connection error for HTTP HEAD`), configure the endpoint explicitly via `ENDPOINT 's3.⟨your-region⟩.amazonaws.com'`{:.language-sql .highlight}.

Now, to query using the above secret, simply query any `s3://` prefixed file:

```sql
SELECT *
FROM 's3://⟨your-bucket⟩/⟨your_file⟩.parquet';
```

### `credential_chain` Provider

The `credential_chain` provider automatically fetches credentials using the AWS SDK (profiles, SSO, assumed roles, web identities, instance metadata, and more). It is provided by the [`aws` extension]({% link docs/current/core_extensions/aws.md %}). For example, to use the AWS SDK default provider:

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER credential_chain
);
```

For the full set of `credential_chain` options — `CHAIN` values, profile selection, assuming roles, SSO, web identity (IRSA), region resolution, validation, and auto-refresh — see the [AWS extension page]({% link docs/current/core_extensions/aws.md %}#credential_chain-provider).

### Overview of S3 Secret Parameters

Below is a complete list of the supported parameters that can be used for both the `config` and `credential_chain` providers:

| Name                          | Description                                                                           | Secret            | Type      | Default                                     |
|:------------------------------|:--------------------------------------------------------------------------------------|:------------------|:----------|:--------------------------------------------|
| `ENDPOINT`                    | Specify a custom S3 endpoint                                                          | `S3`, `GCS`, `R2` | `STRING`  | `s3.amazonaws.com` for `S3`,                |
| `KEY_ID`                      | The ID of the key to use                                                              | `S3`, `GCS`, `R2` | `STRING`  | -                                           |
| `REGION`                      | The region for which to authenticate (should match the region of the bucket to query) | `S3`, `GCS`, `R2` | `STRING`  | `us-east-1`                                 |
| `SECRET`                      | The secret of the key to use                                                          | `S3`, `GCS`, `R2` | `STRING`  | -                                           |
| `SESSION_TOKEN`               | Optionally, a session token can be passed to use temporary credentials                | `S3`, `GCS`, `R2` | `STRING`  | -                                           |
| `URL_COMPATIBILITY_MODE`      | Can help when URLs contain problematic characters                                     | `S3`, `GCS`, `R2` | `BOOLEAN` | `true`                                      |
| `URL_STYLE`                   | Either `vhost` (alias `virtual`) or `path`                                            | `S3`, `GCS`, `R2` | `STRING`  | `vhost` for `S3`, `path` for `R2` and `GCS` |
| `USE_SSL`                     | Whether to use HTTPS or HTTP                                                          | `S3`, `GCS`, `R2` | `BOOLEAN` | `true`                                      |
| `VERIFY_SSL`                  | Whether to verify the SSL certificate of the server                                   | `S3`, `GCS`, `R2` | `BOOLEAN` | `true`                                      |
| `ACCOUNT_ID`                  | The R2 account ID to use for generating the endpoint URL                              | `R2`              | `STRING`  | -                                           |
| `KMS_KEY_ID`                  | AWS KMS (Key Management Service) key for Server Side Encryption S3                    | `S3`              | `STRING`  | -                                           |
| `REQUESTER_PAYS`              | Allows use of "requester pays" S3 buckets                                             | `S3`              | `BOOLEAN` | `false`                                     |
| `REFRESH`                     | Set to `auto` to periodically refresh credentials (see the [`aws` extension]({% link docs/current/core_extensions/aws.md %}#auto-refresh)) | `S3`, `GCS`, `R2` | `STRING`  | -                                           |

### Automatic Credential Refresh

Independently of the `REFRESH` secret parameter, DuckDB automatically refreshes S3 credentials when a request fails with an HTTP `401` or `403` status (for example, when temporary credentials have expired), then retries the request. This behavior is controlled by the `httpfs_enable_credential_refresh` setting (`BOOLEAN`, default `true`):

```sql
SET httpfs_enable_credential_refresh = false;
```

### Platform-Specific Secret Types

#### S3 Secrets

The httpfs extension supports [Server Side Encryption via the AWS Key Management Service (KMS) on S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html) using the `KMS_KEY_ID` option:

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER credential_chain,
    CHAIN config,
    REGION '⟨eu-west-1⟩',
    KMS_KEY_ID 'arn:aws:kms:⟨region⟩:⟨account_id⟩:⟨key⟩/⟨key_id⟩',
    SCOPE 's3://⟨bucket-sub-path⟩'
);
```

#### R2 Secrets

While [Cloudflare R2](https://www.cloudflare.com/developer-platform/r2) uses the regular S3 API, DuckDB has a special Secret type, `R2`, to make configuring it a bit simpler:

```sql
CREATE OR REPLACE SECRET secret (
    TYPE r2,
    KEY_ID '⟨AKIAIOSFODNN7EXAMPLE⟩',
    SECRET '⟨wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY⟩',
    ACCOUNT_ID '⟨my_account_id⟩'
);
```

Note the addition of the `ACCOUNT_ID` which is used to generate the correct endpoint URL for you. Also note that `R2` Secrets can also use both the `CONFIG` and `credential_chain` providers. However, since DuckDB uses an AWS client internally, when using `credential_chain`, the client will search for AWS credentials in the standard AWS credential locations (environment variables, credential files, etc.). Therefore, your R2 credentials must be made available as AWS environment variables (`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`) for the credential chain to work properly. Finally, `R2` secrets are only available when using URLs starting with `r2://`, for example:

```sql
SELECT *
FROM read_parquet('r2://⟨some-file-that-uses-an-r2-secret⟩.parquet');
```

#### GCS Secrets

While [Google Cloud Storage](https://cloud.google.com/storage) is accessed by DuckDB using the S3 API, DuckDB has a special Secret type, `GCS`, to make configuring it a bit simpler:

```sql
CREATE OR REPLACE SECRET secret (
    TYPE gcs,
    KEY_ID '⟨my_hmac_access_id⟩',
    SECRET '⟨my_hmac_secret_key⟩'
);
```


**Important**: The `KEY_ID` and `SECRET` values must be HMAC keys generated specifically for Google Cloud Storage interoperability. These are not the same as regular GCP service account keys or access tokens. You can create HMAC keys by following the [Google Cloud documentation for managing HMAC keys](https://cloud.google.com/storage/docs/authentication/managing-hmackeys).

Note that the above secret will automatically have the correct Google Cloud Storage endpoint configured. Also note that `GCS` Secrets can also use both the `CONFIG` and `credential_chain` providers. However, since DuckDB uses an AWS client internally, when using `credential_chain`, the client will search for AWS credentials in the standard AWS credential locations (environment variables, credential files, etc.). Therefore, your GCS HMAC keys must be made available as AWS environment variables (`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`) for the credential chain to work properly. Finally, `GCS` secrets are only available when using URLs starting with `gcs://` or `gs://`, for example:

```sql
SELECT *
FROM read_parquet('gcs://⟨some/file/that/uses/a/gcs/secret⟩.parquet');
```

## Reading

Reading files from S3 is now as simple as:

```sql
SELECT *
FROM 's3://⟨your-bucket⟩/⟨filename⟩.⟨extension⟩';
```

### Partial Reading

The `httpfs` extension supports [partial reading]({% link docs/current/core_extensions/httpfs/https.md %}#partial-reading) from S3 buckets.

### Pinning Object Versions

By default, a long-running query re-reads an object at whatever version is current at read time, which can change if the object is overwritten. Set `s3_version_id_pinning` (`BOOLEAN`, default `false`) to pin reads to the object version captured on the first `HEAD` request, so a query sees a consistent version even if the object is overwritten mid-query. This requires the HTTP metadata cache:

```sql
SET enable_http_metadata_cache = true;
SET s3_version_id_pinning = true;
```

### Reading Multiple Files

Multiple files are also possible, for example:

```sql
SELECT *
FROM read_parquet([
    's3://⟨your-bucket⟩/⟨filename-1⟩.parquet',
    's3://⟨your-bucket⟩/⟨filename-2⟩.parquet'
]);
```

### Globbing

File [globbing]({% link docs/current/sql/functions/pattern_matching.md %}#globbing) is implemented using the ListObjectsV2 API call and allows using filesystem-like glob patterns to match multiple files, for example:

```sql
SELECT *
FROM read_parquet('s3://⟨your-bucket⟩/*.parquet');
```

This query matches all files in the root of the bucket with the [Parquet extension]({% link docs/current/data/parquet/overview.md %}).

Several features for matching are supported, such as `*` to match any number of any character, `?` for any single character or `[0-9]` for a single character in a range of characters:

```sql
SELECT count(*) FROM read_parquet('s3://⟨your-bucket⟩/folder*/100?/t[0-9].parquet');
```

A useful feature when using globs is the `filename` option, which adds a column named `filename` that encodes the file that a particular row originated from:

```sql
SELECT *
FROM read_parquet('s3://⟨your-bucket⟩/*.parquet', filename = true);
```

This could for example result in:

| column_a | column_b | filename |
|:---|:---|:---|
| 1 | examplevalue1 | s3://bucket-name/file1.parquet |
| 2 | examplevalue1 | s3://bucket-name/file2.parquet |

### Hive Partitioning

DuckDB also offers support for the [Hive partitioning scheme]({% link docs/current/data/partitioning/hive_partitioning.md %}), which is available when using HTTP(S) and S3 endpoints.

## Writing

Writing to S3 uses the multipart upload API. This allows DuckDB to robustly upload files at high speed. Writing to S3 works for both CSV and Parquet:

```sql
COPY table_name TO 's3://⟨your-bucket⟩/⟨filename⟩.⟨extension⟩';
```

Partitioned copy to S3 also works:

```sql
COPY table TO 's3://⟨your-bucket⟩/partitioned' (
    FORMAT parquet,
    PARTITION_BY (⟨part_col_a⟩, ⟨part_col_b⟩)
);
```

An automatic check is performed for existing files/directories, which is currently quite conservative (and on S3 will add a bit of latency). To disable this check and force writing, an `OVERWRITE_OR_IGNORE` flag is added:

```sql
COPY table TO 's3://⟨your-bucket⟩/partitioned' (
    FORMAT parquet,
    PARTITION_BY (⟨part_col_a⟩, ⟨part_col_b⟩),
    OVERWRITE_OR_IGNORE true
);
```

The naming scheme of the written files looks like this:

```sql
s3://⟨your-bucket⟩/partitioned/part_col_a=⟨val⟩/part_col_b=⟨val⟩/data_⟨thread_number⟩.parquet
```

### Configuration

Some additional configuration options exist for the S3 upload, though the default values should suffice for most use cases.

| Name | Description | Default |
|:---|:---|:---|
| `s3_uploader_max_parts_per_file` | Used for part size calculation, see [AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html) | `10000` |
| `s3_uploader_max_filesize` | Used for part size calculation, see [AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html) | `800GB` |
| `s3_uploader_thread_limit` | Maximum number of uploader threads | `50` |

Further S3-related settings are available and documented in the [configuration reference]({% link docs/current/configuration/overview.md %}), including `enable_global_s3_configuration`, `merge_http_secret_into_s3_request`, `s3_allow_recursive_globbing`, `httpfs_enable_credential_refresh`, `s3_version_id_pinning`, and `unsafe_disable_etag_checks`.
