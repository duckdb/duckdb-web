---
layout: docu
title: AWS Extension
github_repository: https://github.com/duckdb/duckdb_aws
---

The `aws` extension adds functionality (e.g., authentication) on top of the `httpfs` extension's [S3 capabilities](httpfs#s3), using the AWS SDK.

## Installing and Loading

To install and load the `aws` extension, run:

```sql
INSTALL aws;
LOAD aws;
```

## Usage

See the [httpfs extension's S3 capabilities](httpfs#s3) for instructions.
