---
github_repository: https://github.com/duckdb/duckdb-aws
layout: docu
redirect_from:
- /docs/extensions/aws
- /docs/stable/extensions/aws
- /docs/preview/core_extensions/aws
- /docs/stable/core_extensions/aws
title: AWS Extension
---

The `aws` extension adds functionality, e.g., authentication, on top of the `httpfs` extension's [S3 capabilities]({% link docs/current/core_extensions/httpfs/overview.md %}#s3-api), using the AWS SDK.

## Installing and Loading

The `aws` extension will be transparently [autoloaded]({% link docs/current/core_extensions/overview.md %}#autoloading-extensions) on first use from the official extension repository.
If you would like to install and load it manually, run:

```sql
INSTALL aws;
LOAD aws;
```

> In most cases, the `aws` extension works in conjunction with the [`httpfs` extension]({% link docs/current/core_extensions/httpfs/overview.md %}).

## Configuration and Authentication

The preferred way to configure and authenticate to AWS S3 endpoints is to use [secrets]({% link docs/current/sql/statements/create_secret.md %}).
There are two S3 secret providers:

* The `config` provider, where you supply the access key and secret manually. It is part of the `httpfs` extension and is documented in the [S3 API page]({% link docs/current/core_extensions/httpfs/s3api.md %}#config-provider). Use it when you already have static credentials.
* The `credential_chain` provider, described below, which fetches credentials automatically using the AWS SDK. It is provided by the `aws` extension and supports profiles, SSO, assumed roles, web identities (IRSA), and instance metadata.

The full list of S3 secret parameters that apply to *both* providers (`ENDPOINT`, `REGION`, `URL_STYLE`, `USE_SSL`, `KMS_KEY_ID`, `REQUESTER_PAYS`, …) is documented in the [S3 API page]({% link docs/current/core_extensions/httpfs/s3api.md %}#overview-of-s3-secret-parameters).

## `credential_chain` Provider

The `credential_chain` provider allows automatically fetching credentials using mechanisms provided by the AWS SDK. For example, to use the AWS SDK default provider:

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER credential_chain
);
```

To query a file using the above secret, simply query any `s3://` prefixed file.

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
* `web_identity` (for [IAM Roles for Service Accounts (IRSA)](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html); see [Web Identity (IRSA)](#web-identity-irsa))

The `credential_chain` provider also allows overriding the automatically fetched config. For example, to automatically load credentials, and then override the region, run:

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER credential_chain,
    CHAIN config,
    REGION '⟨eu-west-1⟩'
);
```

### Selecting a Profile

To load credentials based on a named profile which is not the default (from the `AWS_PROFILE` environment variable or the default profile based on AWS SDK precedence), use the `PROFILE` parameter:

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER credential_chain,
    CHAIN config,
    PROFILE '⟨my_profile⟩'
);
```

This approach is equivalent to the [deprecated S3 API]({% link docs/current/core_extensions/httpfs/s3api_legacy_authentication.md %})'s method `load_aws_credentials('⟨my_profile⟩')`.

### Assuming a Role (STS)

To assume an IAM role, pass its ARN via `ASSUME_ROLE_ARN`. An `EXTERNAL_ID` can be supplied for the role's trust policy:

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER credential_chain,
    CHAIN 'sts',
    ASSUME_ROLE_ARN 'arn:aws:iam::⟨account_id⟩:role/⟨role⟩',
    EXTERNAL_ID '⟨external_id⟩',
    REGION '⟨us-east-1⟩'
);
```

> The `sts` chain value requires an `ASSUME_ROLE_ARN` value. If the selected profile itself uses STS, use `CHAIN 'config'` instead.

### Web Identity (IRSA)

For [IAM Roles for Service Accounts (IRSA)](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html) — commonly used on Amazon EKS — use the `web_identity` chain together with a role ARN and a token file. A `SESSION_NAME` can optionally be set:

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER credential_chain,
    CHAIN 'web_identity',
    ASSUME_ROLE_ARN 'arn:aws:iam::⟨account_id⟩:role/⟨role⟩',
    WEB_IDENTITY_TOKEN_FILE '⟨/var/run/secrets/eks.amazonaws.com/serviceaccount/token⟩'
);
```

### Single Sign-On (SSO)

DuckDB can use credentials obtained through [AWS IAM Identity Center (SSO)](https://aws.amazon.com/what-is/sso/). First authenticate on the command line (`aws sso login --profile ⟨my-sso-profile⟩`), then create a secret using the `sso` chain:

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER credential_chain,
    CHAIN 'sso',
    PROFILE '⟨my-sso-profile⟩'
);
```

### HTTP Proxy

When credentials must be fetched through an HTTP proxy, configure it on the secret:

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER credential_chain,
    HTTP_PROXY '⟨proxy.example.com:8080⟩',
    HTTP_PROXY_USERNAME '⟨username⟩',
    HTTP_PROXY_PASSWORD '⟨password⟩'
);
```

### Region Resolution

If no region is provided explicitly, DuckDB resolves it from the following sources, in order:

1. The `REGION` secret parameter.
2. The `s3_region` [setting]({% link docs/current/configuration/overview.md %}) (`SET s3_region = '⟨region⟩'`).
3. The `AWS_REGION` environment variable.
4. The `AWS_DEFAULT_REGION` environment variable.
5. The `region` of the profile in `~/.aws/config`.

If none of these resolve, `CREATE SECRET` still succeeds, but DuckDB logs a warning:

```console
Set region explicitly using REGION 'us-east-1' in your CREATE SECRET statement, adding a region to your profile in ~/.aws/config or configure the AWS_REGION or AWS_DEFAULT_REGION environment variables.
```

### Validation

The AWS `credential_chain` provider will look for any required credentials during `CREATE SECRET` time, failing if absent/unavailable.

This behavior may be configured via the `VALIDATION` option as follows:

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER credential_chain,
    VALIDATION 'exists'
);
```

Two validation modes are supported:

* `exists` (default) requires present credentials.
* `none` allows `CREATE SECRET` to succeed for `credential_chains` with no available credentials.

> `VALIDATION 'exists'` validates only the __presence__ of a credential, __not its operational readiness__. Thus, no attempt is made to
> convert into an access token, or perform a read, write, etc.

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

> When `CHAIN` is `sts` or `web_identity`, `REFRESH auto` is enabled automatically, since these credentials are short-lived.

## Amazon RDS (IAM Authentication)

The `aws` extension can generate short-lived [IAM authentication tokens](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html) for connecting to Amazon RDS and Aurora databases, exposed through a secret of type `rds`. It accepts the same [`credential_chain`](#credential_chain-provider) options as an `s3` secret, plus the required `RDS_USER`, `RDS_HOST`, `RDS_PORT`, and `REGION` parameters. Unlike an `s3` secret, an `rds` secret also requires an explicit `CHAIN`:

```sql
CREATE SECRET aws_rds_secret (
    TYPE rds,
    PROVIDER credential_chain,
    REGION '⟨eu-west-1⟩',
    RDS_USER '⟨db_user⟩',
    RDS_HOST '⟨instance⟩.⟨identifier⟩.⟨region⟩.rds.amazonaws.com',
    RDS_PORT '5432'
);
```

> The `rds` secret _type_ is registered by the [`postgres` extension]({% link docs/current/core_extensions/postgres/overview.md %}), not by `aws`, so the `postgres` extension must be installed and loaded before the statement above will run. For the complete end-to-end setup — passing the secret to a connection via `AWS_RDS_SECRET`, attaching, and querying — see the [Amazon RDS with IAM authentication guide]({% link docs/current/guides/database_integration/rds_iam.md %}) or the [Postgres secrets documentation]({% link docs/current/core_extensions/postgres/secrets.md %}#aws-rds-iam-authentication).

## Legacy Features

> Deprecated The `load_aws_credentials` function is deprecated and is removed in later releases. Use a [secret]({% link docs/current/sql/statements/create_secret.md %}) with the [`credential_chain` provider](#credential_chain-provider) instead.

Prior to version 0.10.0, DuckDB did not have a [Secrets manager]({% link docs/current/sql/statements/create_secret.md %}), to load the credentials automatically, the AWS extension provided
a special function to load the AWS credentials in the [legacy authentication method]({% link docs/current/core_extensions/httpfs/s3api_legacy_authentication.md %}).

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
