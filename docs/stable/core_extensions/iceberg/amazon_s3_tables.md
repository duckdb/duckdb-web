---
layout: docu
title: Amazon S3 Tables
redirect_from:
- /docs/stable/extensions/iceberg/amazon_s3_tables
- /docs/stable/extensions/iceberg/amazon_s3_tables/
---

> Support for S3 Tables is currently experimental.

The `iceberg` extension supports reading Iceberg tables stored in [Amazon S3 Tables](https://aws.amazon.com/s3/features/tables/).

## Requirements

Install the following extensions:

```sql
INSTALL aws;
INSTALL httpfs;
INSTALL iceberg;
```

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
    KEY_ID '⟨AKIAIOSFODNN7EXAMPLE⟩',
    SECRET '⟨wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY⟩',
    REGION '⟨us-east-1⟩'
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
