---
layout: docu
title: S3 and AWS Authentication
---

This page is the entry point for authenticating to S3 and other AWS services from DuckDB. Authentication is configured using [secrets]({% link docs/preview/sql/statements/create_secret.md %}), and the detailed reference material lives on the [S3 API Support]({% link docs/preview/core_extensions/httpfs/s3api.md %}) and [AWS Extension]({% link docs/preview/core_extensions/aws.md %}) pages. The sections below explain which method to use and link to the relevant reference.

## Choosing an Authentication Method

There are two S3 secret providers. Use the `config` provider when you have static credentials, and the `credential_chain` provider when you want DuckDB to fetch credentials automatically through the AWS SDK.

| Situation | Method | Reference |
|---|---|---|
| You have a static access key and secret | `config` provider | [`config` provider]({% link docs/preview/core_extensions/httpfs/s3api.md %}#config-provider) |
| Credentials come from `~/.aws/credentials` or `~/.aws/config` profiles | `credential_chain` with a profile | [Selecting a Profile]({% link docs/preview/core_extensions/aws.md %}#selecting-a-profile) |
| You sign in with AWS IAM Identity Center (SSO) | `credential_chain` with the `sso` chain | [Single Sign-On (SSO)]({% link docs/preview/core_extensions/aws.md %}#single-sign-on-sso) |
| You assume an IAM role via STS | `credential_chain` with the `sts` chain | [Assuming a Role (STS)]({% link docs/preview/core_extensions/aws.md %}#assuming-a-role-sts) |
| You run on Amazon EKS with IAM Roles for Service Accounts (IRSA) | `credential_chain` with the `web_identity` chain | [Web Identity (IRSA)]({% link docs/preview/core_extensions/aws.md %}#web-identity-irsa) |
| You run on an EC2 instance and want to use its instance profile | `credential_chain` with the `instance` chain | [`credential_chain` provider]({% link docs/preview/core_extensions/aws.md %}#credential_chain-provider) |
| You connect to Amazon RDS or Aurora with IAM authentication | `rds` secret | [Amazon RDS (IAM Authentication)]({% link docs/preview/core_extensions/aws.md %}#amazon-rds-iam-authentication) |

The `config` provider is part of the [`httpfs` extension]({% link docs/preview/core_extensions/httpfs/overview.md %}) and works with any S3-compatible storage. The `credential_chain` provider is AWS-specific and is provided by the [`aws` extension]({% link docs/preview/core_extensions/aws.md %}), which is autoloaded on first use.

## Static Credentials: the `config` Provider

Supply the key and secret directly:

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER config,
    KEY_ID '⟨AKIAIOSFODNN7EXAMPLE⟩',
    SECRET '⟨wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY⟩',
    REGION '⟨us-east-1⟩'
);
```

See the [`config` provider documentation]({% link docs/preview/core_extensions/httpfs/s3api.md %}#config-provider) for the full details, including how to set an explicit `ENDPOINT` for non-AWS storage.

## Automatic Credentials: the `credential_chain` Provider

The `credential_chain` provider fetches credentials automatically using the AWS SDK, covering profiles, SSO, assumed roles, web identities (IRSA), and instance metadata. To use the AWS SDK default provider:

```sql
CREATE OR REPLACE SECRET secret (
    TYPE s3,
    PROVIDER credential_chain
);
```

You can select a specific chain with the `CHAIN` keyword and refine the behavior for each method. The individual mechanisms are documented on the AWS Extension page:

* [Selecting a Profile]({% link docs/preview/core_extensions/aws.md %}#selecting-a-profile)
* [Assuming a Role (STS)]({% link docs/preview/core_extensions/aws.md %}#assuming-a-role-sts)
* [Web Identity (IRSA)]({% link docs/preview/core_extensions/aws.md %}#web-identity-irsa)
* [Single Sign-On (SSO)]({% link docs/preview/core_extensions/aws.md %}#single-sign-on-sso)

For behavior common to all `credential_chain` secrets, see [Region Resolution]({% link docs/preview/core_extensions/aws.md %}#region-resolution), [Validation]({% link docs/preview/core_extensions/aws.md %}#validation), and [Auto-Refresh]({% link docs/preview/core_extensions/aws.md %}#auto-refresh).

## Secret Parameters

The full list of S3 secret parameters that apply to both providers (`ENDPOINT`, `REGION`, `URL_STYLE`, `USE_SSL`, `KMS_KEY_ID`, `REQUESTER_PAYS`, and more) is documented in the [Overview of S3 Secret Parameters]({% link docs/preview/core_extensions/httpfs/s3api.md %}#overview-of-s3-secret-parameters). Platform-specific secret types for [Cloudflare R2 and Google Cloud Storage]({% link docs/preview/core_extensions/httpfs/s3api.md %}#platform-specific-secret-types) are also available.

## Legacy Authentication

Before DuckDB had a [Secrets manager]({% link docs/preview/sql/statements/create_secret.md %}), credentials were loaded through the `load_aws_credentials` function. This method is deprecated. See the [Legacy Authentication Scheme for S3 API]({% link docs/preview/core_extensions/httpfs/s3api_legacy_authentication.md %}) page if you are maintaining older setups.
