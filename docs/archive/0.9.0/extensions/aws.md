---
layout: docu
title: AWS Extension
---

The `aws` extension provides features that depend on the AWS SDK.

> This extension is currently in an experimental state. Feel free to try it out, but be aware some things may not work as expected.

## Features

| function | type | description | 
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
If autoinstall or autoload are disabled, you can always explicitly install and load httpfs and aws like:

```sql
INSTALL aws;
LOAD aws;
INSTALL httpfs;
LOAD httpfs;
```

See also the [S3 API capabilities of the `httpfs` extension](httpfs#s3).

## GitHub Repository

[<span class="github">GitHub</span>](https://github.com/duckdblabs/duckdb_aws)