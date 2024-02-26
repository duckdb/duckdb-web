---
layout: docu
title: AWS Extension
github_repository: https://github.com/duckdb/duckdb_aws
---

The `aws` extension adds functionality (e.g., authentication) on top of the `httpfs` extension's [S3 capabilities](httpfs#s3), using the AWS SDK.

## Installing and Loading

To install and load the `aws` extension, run:

```sql
INSTALL aws;
LOAD aws;
```

## Features

| Function | Type | Description |
|---|---|-------|
| `load_aws_credentials` | `PRAGMA` function | Automatically loads the AWS credentials through the [AWS Default Credentials Provider Chain](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials-chain.html) |

## Usage

### Load AWS Credentials

To load the AWS credentials, run:

```sql
CALL load_aws_credentials();
```

```text
┌─────────────────────────┬──────────────────────────┬──────────────────────┬───────────────┐
│ loaded_access_key_id    │ loaded_secret_access_key │ loaded_session_token │ loaded_region │
│       varchar           │         varchar          │       varchar        │    varchar    │
├─────────────────────────┼──────────────────────────┼──────────────────────┼───────────────┤
│ AKIAIOSFODNN7EXAMPLE    │ <redacted>               │                      │ eu-west-1     │
└─────────────────────────┴──────────────────────────┴──────────────────────┴───────────────┘
```

The function takes a string parameter to specify a specific profile:

```sql
CALL load_aws_credentials('minio-testing-2');
```

```text
┌──────────────────────┬──────────────────────────┬──────────────────────┬───────────────┐
│ loaded_access_key_id │ loaded_secret_access_key │ loaded_session_token │ loaded_region │
│       varchar        │         varchar          │       varchar        │    varchar    │
├──────────────────────┼──────────────────────────┼──────────────────────┼───────────────┤
│ minio_duckdb_user_2  │ <redacted>               │                      │ eu-west-2     │
└──────────────────────┴──────────────────────────┴──────────────────────┴───────────────┘
```

There are several parameters to tweak the behavior of the call:

```sql
CALL load_aws_credentials('minio-testing-2', set_region=false, redact_secret=false);
```

```text
┌──────────────────────┬──────────────────────────────┬──────────────────────┬───────────────┐
│ loaded_access_key_id │   loaded_secret_access_key   │ loaded_session_token │ loaded_region │
│       varchar        │           varchar            │       varchar        │    varchar    │
├──────────────────────┼──────────────────────────────┼──────────────────────┼───────────────┤
│ minio_duckdb_user_2  │ minio_duckdb_user_password_2 │                      │               │
└──────────────────────┴──────────────────────────────┴──────────────────────┴───────────────┘
```

## Related Extensions

`aws` depends on `httpfs` extension capablities, and both will be autoloaded on the first call to `load_aws_credentials`.
If autoinstall or autoload are disabled, you can always explicitly install and load them as follows:

```sql
INSTALL aws;
INSTALL httpfs;
LOAD aws;
LOAD httpfs;
```

## Usage

See the [httpfs extension's S3 capabilities](httpfs/overview#s3) for instructions.
