---
github_repository: https://github.com/duckdb/duckdb-aws
layout: docu
title: AWS Extension
---

The `aws` extension adds functionality (e.g., authentication) on top of the `httpfs` extension's [S3 capabilities]({% link docs/preview/extensions/httpfs/overview.md %}#s3-api), using the AWS SDK.

## Installing and Loading

The `aws` extension will be transparently [autoloaded]({% link docs/preview/extensions/overview.md %}#autoloading-extensions) on first use from the official extension repository.
If you would like to install and load it manually, run:

```sql
INSTALL aws;
LOAD aws;
```

> In most cases, the `aws` extension works in conjunction with the [`httpfs` extension]({% link docs/preview/extensions/httpfs/overview.md %}.

## Configuration and Authentication

The preferred way to configure and authenticate to AWS S3 endpoints is to use [secrets]({% link docs/preview/sql/statements/create_secret.md %}).

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

> Tip If you get an IO Error (`Connection error for HTTP HEAD`), configure the endpoint explicitly via `ENDPOINT 's3.⟨your_region⟩.amazonaws.com'`{:.language-sql .highlight}.

Now, to query using the above secret, simply query any `s3://` prefixed file:

```sql
SELECT *
FROM 's3://⟨your_bucket⟩/⟨your_file⟩.parquet';
```

### `credential_chain` Provider

The `credential_chain` provider allows automatically fetching credentials using mechanisms provided by the AWS SDK. For example, to use the AWS SDK default provider:

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER credential_chain
);
```

Again, to query a file using the above secret, simply query any `s3://` prefixed file.

DuckDB also allows specifying a specific chain using the `CHAIN` keyword. This takes a semicolon-separated list (`a;b;c`) of providers that will be tried in order. For example:

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER credential_chain,
    CHAIN 'env;config'
);
```

The possible values for `CHAIN` are the following:

* [`config`](https://sdk.amazonaws.com/cpp/api/LATEST/aws-cpp-sdk-core/html/class_aws_1_1_auth_1_1_profile_config_file_a_w_s_credentials_provider.html)
* [`sts`](https://sdk.amazonaws.com/cpp/api/LATEST/aws-cpp-sdk-core/html/class_aws_1_1_auth_1_1_s_t_s_assume_role_web_identity_credentials_provider.html)
* [`sso`](https://aws.amazon.com/what-is/sso/)
* [`env`](https://sdk.amazonaws.com/cpp/api/LATEST/aws-cpp-sdk-core/html/class_aws_1_1_auth_1_1_environment_a_w_s_credentials_provider.html)
* [`instance`](https://sdk.amazonaws.com/cpp/api/LATEST/aws-cpp-sdk-core/html/class_aws_1_1_auth_1_1_instance_profile_credentials_provider.html)
* [`process`](https://sdk.amazonaws.com/cpp/api/LATEST/aws-cpp-sdk-core/html/class_aws_1_1_auth_1_1_process_credentials_provider.html)

The `credential_chain` provider also allows overriding the automatically fetched config. For example, to automatically load credentials, and then override the region, run:

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER credential_chain,
    CHAIN config,
    REGION '⟨eu-west-1⟩'
);
```

### Auto-Refresh

Some AWS endpoints require periodic refreshing of the credentials.
This can be specified with the `REFRESH auto` option:

```sql
CREATE SECRET env_test (
    TYPE s3,
    PROVIDER credential_chain,
    REFRESH auto
);
```

## Legacy Features

> Deprecated The `load_aws_credentials` function is deprecated.

Prior to version 0.10.0, DuckDB did not have a [Secrets manager]({% link docs/preview/sql/statements/create_secret.md %}), to load the credentials automatically, the AWS extension provided
a special function to load the AWS credentials in the [legacy authentication method]({% link docs/preview/extensions/httpfs/s3api_legacy_authentication.md %}).

| Function | Type | Description |
|---|---|-------|
| `load_aws_credentials` | `PRAGMA` function | Loads the AWS credentials through the [AWS Default Credentials Provider Chain](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials-chain.html) |

### Load AWS Credentials (Legacy)

To load the AWS credentials, run:

```sql
CALL load_aws_credentials();
```

<div class="monospace_table"></div>

| loaded_access_key_id | loaded_secret_access_key | loaded_session_token | loaded_region |
|----------------------|--------------------------|----------------------|---------------|
| AKIAIOSFODNN7EXAMPLE | `<redacted>`             | NULL                 | us-east-2     |

The function takes a string parameter to specify a specific profile:

```sql
CALL load_aws_credentials('minio-testing-2');
```

<div class="monospace_table"></div>

| loaded_access_key_id | loaded_secret_access_key | loaded_session_token | loaded_region |
|----------------------|--------------------------|----------------------|---------------|
| minio_duckdb_user_2  | `<redacted>`             | NULL                 | NULL          |

There are several parameters to tweak the behavior of the call:

```sql
CALL load_aws_credentials('minio-testing-2', set_region = false, redact_secret = false);
```

<div class="monospace_table"></div>

| loaded_access_key_id | loaded_secret_access_key     | loaded_session_token | loaded_region |
|----------------------|------------------------------|----------------------|---------------|
| minio_duckdb_user_2  | minio_duckdb_user_password_2 | NULL                 | NULL          |
