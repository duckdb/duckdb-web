---
layout: docu
title: Amazon S3 Tables
---

The `iceberg` extension supports reading Iceberg tables stored in [Amazon S3 Tables](https://aws.amazon.com/s3/features/tables/).

## Requirements

The S3 Tables support is currently experimental.
To use it, install the following extensions:

```sql
FORCE INSTALL aws FROM core_nightly;
FORCE INSTALL httpfs FROM core_nightly;
FORCE INSTALL iceberg FROM core_nightly;
```

> If you want to switch back to using extensions from the `core` repository,
> follow the [extension documentation]({% link docs/stable/extensions/installing_extensions.md %}#force-installing-to-upgrade-extensions).

## Connecting to Amazon S3 Tables

You can let DuckDB detect your AWS credentials and configuration based on the default profile in your `~/.aws` directory by creating the following secret using the [Secrets Manager]({% link docs/stable/configuration/secrets_manager.md %}):

```sql
CREATE SECRET (
    TYPE s3,
    PROVIDER credential_chain
);
```

Alternatively, you can set the values manually:

```sql
CREATE SECRET (
    TYPE s3,
    KEY_ID '⟨YOUR_ACCESS_KEY_ID⟩',
    SECRET '⟨YOUR_SECRET_ACCESS_KEY⟩',
    REGION '⟨YOUR_DEFAULT_REGION⟩'
);
```

Then, connect to the catalog using you S3 Tables ARN (available in the AWS Management Console) and the `ENDPOINT_TYPE s3_tables` option:

```sql
ATTACH '⟨s3_tables_arn⟩' AS s3_tables (
   TYPE iceberg,
   ENDPOINT_TYPE s3_tables
);
```

To check whether the attachment worked, list all tables:

```sql
SHOW ALL TABLES;
```

You can query a table as follows:

```sql
SELECT count(*)
FROM s3_tables.⟨namespace_name⟩.⟨table_name⟩;
```
