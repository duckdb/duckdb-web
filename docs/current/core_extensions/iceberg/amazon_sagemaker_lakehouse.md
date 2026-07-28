---
layout: docu
redirect_from:
- /docs/stable/extensions/iceberg/amazon_sagemaker_lakehouse
- /docs/preview/core_extensions/iceberg/amazon_sagemaker_lakehouse
- /docs/stable/core_extensions/iceberg/amazon_sagemaker_lakehouse
title: Amazon SageMaker Lakehouse (AWS Glue)
---

> Support for Amazon SageMaker Lakehouse (AWS Glue) is currently experimental.

The `iceberg` extension supports reading Iceberg tables through the [Amazon SageMaker Lakehouse (a.k.a. AWS Glue)](https://aws.amazon.com/sagemaker/lakehouse/) catalog.

## Requirements

To use it, install the following extensions:

```sql
INSTALL aws;
INSTALL httpfs;
INSTALL iceberg;
```

> If you want to switch back to using extensions from the `core` repository,
> follow the [extension documentation]({% link docs/current/extensions/installing_extensions.md %}#force-installing-to-upgrade-extensions).

## Connecting to Amazon SageMaker Lakehouse (AWS Glue)

Create an S3 secret using the [Secrets Manager]({% link docs/current/configuration/secrets_manager.md %}):

```sql
CREATE SECRET (
    TYPE s3,
    PROVIDER credential_chain,
    CHAIN sts,
    ASSUME_ROLE_ARN 'arn:aws:iam::⟨account_id⟩:role/⟨role⟩',
    REGION 'us-east-2'
);
```

In this example we use an STS token, but [other authentication methods are supported]({% link docs/current/core_extensions/aws.md %}).

Then, connect to the catalog:

```sql
ATTACH '⟨account_id⟩' AS glue_catalog (
    TYPE iceberg,
    ENDPOINT 'glue.⟨REGION⟩.amazonaws.com/iceberg',
    AUTHORIZATION_TYPE 'sigv4'
);
```

Or alternatively:

```sql
ATTACH '⟨account_id⟩' AS glue_catalog (
    TYPE iceberg,
    ENDPOINT_TYPE 'glue'
);
```

> Warning As with [Amazon S3 Tables]({% link docs/current/core_extensions/iceberg/amazon_s3_tables.md %}), `ENDPOINT_TYPE glue` always builds an endpoint of the form `glue.⟨region⟩.amazonaws.com/iceberg`, which is incorrect for regions that do not use the plain `amazonaws.com` suffix (most notably the AWS China regions `cn-north-1` and `cn-northwest-1`, which use `amazonaws.com.cn`). For such regions, attach with an explicit `ENDPOINT` (with the correct host) together with `AUTHORIZATION_TYPE 'sigv4'` instead of using `ENDPOINT_TYPE`.

The warehouse identifier (the first argument to `ATTACH`) accepts the following forms:

| Warehouse | Meaning |
|---|---|
| `:` | The default catalog of the caller's account. |
| `⟨account_id⟩` | A 12-digit AWS account ID. |
| `⟨account_id⟩:⟨catalog⟩` | A named catalog in the given account. |
| `⟨catalog⟩/⟨sub_catalog⟩` | A nested (federated) catalog. |
| `⟨account_id⟩:⟨catalog⟩/⟨sub_catalog⟩` | A nested catalog in the given account. |

To check whether the attachment worked, list all tables:

```sql
SHOW ALL TABLES;
```

You can query a table as follows:

```sql
SELECT count(*)
FROM glue_catalog.⟨namespace_name⟩.⟨table_name⟩;
```

If you have an S3 Tables federated catalog, you can create a table using the standard `CREATE TABLE` syntax;

```sql
CREATE TABLE glue_catalog.⟨namespace_name⟩.⟨table_name⟩ (a INTEGER, b VARCHAR);
```

If the catalog is not federated by S3 Tables, you may need to create pass a `location` table property. You can do so using the `WITH` clause.

```sql
CREATE TABLE glue_catalog.⟨namespace_name⟩.⟨table_name⟩ (a INTEGER, b VARCHAR)
WITH (
    'location' = 's3://path/to/location'
);
```

You can learn more about the `WITH` clause at [Table Properties]({% link docs/current/core_extensions/iceberg/writing.md %}#table-properties).
