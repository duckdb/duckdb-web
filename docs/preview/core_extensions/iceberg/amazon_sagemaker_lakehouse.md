---
layout: docu
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
> follow the [extension documentation]({% link docs/preview/extensions/installing_extensions.md %}#force-installing-to-upgrade-extensions).

## Connecting to Amazon SageMaker Lakehouse (AWS Glue)

Create an S3 secret using the [Secrets Manager]({% link docs/preview/configuration/secrets_manager.md %}):

```sql
CREATE SECRET (
    TYPE s3,
    PROVIDER credential_chain,
    CHAIN sts,
    ASSUME_ROLE_ARN 'arn:aws:iam::⟨account_id⟩:role/⟨role⟩',
    REGION 'us-east-2'
);
```

In this example we use an STS token, but [other authentication methods are supported]({% link docs/preview/core_extensions/aws.md %}).

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

To check whether the attachment worked, list all tables:

```sql
SHOW ALL TABLES;
```

You can query a table as follows:

```sql
SELECT count(*)
FROM glue_catalog.⟨namespace_name⟩.⟨table_name⟩;
```

If you have an S3Tables federated catalog, you can create a table using the standard `CREATE TABLE` syntax;

```sql
CREATE TABLE glue_catalog.⟨namespace_name⟩.⟨table_name⟩ (a int, b varchar);
```

If the catalog is not federated by S3Tables, you may need to create pass a `location` table property. You can do so using the `WITH` clause.

```sql
CREATE TABLE glue_catalog.⟨namespace_name⟩.⟨table_name⟩ (a int, b varchar)
WITH (
    'location'='s3://path/to/location'
);
```

You can learn more about the `WITH` clause at [Table Properties]({% link docs/preview/core_extensions/iceberg/iceberg_rest_catalogs.md %}#table-properties-functions).
