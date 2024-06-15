---
layout: docu
title: AWS Extension
github_repository: https://github.com/duckdb/duckdb_aws
---

The `aws` extension adds functionality (e.g., authentication) on top of the `httpfs` extension's [S3 capabilities](httpfs/overview#s3-api), using the AWS SDK.

## Installing and Loading

The `aws` extension will be transparently [autoloaded](overview#autoloading-extensions) on first use from the official extension repository.
If you would like to install and load it manually, run:

```sql
INSTALL aws;
LOAD aws;
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

In most cases, you will not need to explicitly interact with the `aws` extension. It will automatically be invoked
whenever you use DuckDB's [S3 Secret functionality](../sql/statements/create_secret). See the [httpfs extension's S3 capabilities](httpfs/overview#s3) for instructions.

## Legacy Features

Prior to version 0.10.0, DuckDB did not have a [Secrets manager](../sql/statements/create_secret), to load the credentials automatically, the AWS extension provided
a special function to load the AWS credentials in the [legacy authentication method](httpfs/s3api_legacy_authentication).

| Function | Type | Description |
|---|---|-------|
| `load_aws_credentials` | `PRAGMA` function | Loads the AWS credentials through the [AWS Default Credentials Provider Chain](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials-chain.html). |

### Load AWS Credentials (Legacy)

To load the AWS credentials, run:

```sql
CALL load_aws_credentials();
```

| loaded_access_key_id | loaded_secret_access_key | loaded_session_token | loaded_region |
|----------------------|--------------------------|----------------------|---------------|
| AKIAIOSFODNN7EXAMPLE | <redacted>               | NULL                 | us-east-2     |

The function takes a string parameter to specify a specific profile:

```sql
CALL load_aws_credentials('minio-testing-2');
```

| loaded_access_key_id | loaded_secret_access_key | loaded_session_token | loaded_region |
|----------------------|--------------------------|----------------------|---------------|
| minio_duckdb_user_2  | <redacted>               | NULL                 | NULL          |

There are several parameters to tweak the behavior of the call:

```sql
CALL load_aws_credentials('minio-testing-2', set_region = false, redact_secret = false);
```

| loaded_access_key_id | loaded_secret_access_key     | loaded_session_token | loaded_region |
|----------------------|------------------------------|----------------------|---------------|
| minio_duckdb_user_2  | minio_duckdb_user_password_2 | NULL                 | NULL          |
