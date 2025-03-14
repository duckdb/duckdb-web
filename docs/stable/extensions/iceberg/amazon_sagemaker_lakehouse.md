---
layout: docu
title: Amazon SageMaker Lakehouse (AWS Glue)
---

The `iceberg` extension supports reading Iceberg tables through the [Amazon SageMaker Lakehouse (a.k.a. AWS Glue)](https://aws.amazon.com/sagemaker/lakehouse/) catalog.
To do so, configure the role and region using the [Secrets Manager]({% link docs/stable/configuration/secrets_manager.md %}):

```sql
CREATE SECRET (
    TYPE s3,
    PROVIDER credential_chain,
    CHAIN sts,
    ASSUME_ROLE_ARN 'arn:aws:iam::⟨account_id⟩:role/⟨role⟩',
    REGION 'us-east-2'
);
```

Then, connect to the catalog using the `ENDPOINT_TYPE glue` option:

```sql
ATTACH '⟨account_id⟩:s3tablescatalog/⟨namespace_name⟩' AS glue_catalog (
    TYPE iceberg,
    ENDPOINT_TYPE glue
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
