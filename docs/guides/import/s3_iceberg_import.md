---
layout: docu
title: S3 Iceberg Import
selected: S3 Iceberg Import
---

## Prerequisites

To load an Iceberg file from S3, both the [`httpfs`](../../extensions/httpfs) and [`iceberg`](../../extensions/iceberg) extensions are required. They can be installed use the `INSTALL` SQL command. The extensions only need to be installed once.

```sql
INSTALL httpfs;
INSTALL iceberg;
```

To load the extensions for usage, use the `LOAD` command:

```sql
LOAD httpfs;
LOAD iceberg;
```

## Credentials

After loading the extensions, set up the credentials and S3 region to read data. You may either use an access key and secret, or a token.

```sql
SET s3_region='us-east-1';
SET s3_access_key_id='<AWS access key id>';
SET s3_secret_access_key='<AWS secret access key>';
```

The alternative is to use a token:

```sql
SET s3_region='us-east-1';
SET s3_session_token='<AWS session token>';
```

ALternatively, use the [`aws` extension](../../extensions/aws) to retrieve the credentials from the aws config file. To load the credentials:

```sql
CALL load_aws_credentials();
```

## Loading Iceberg Tables from S3

After the extensions are set up and the S3 credentials are correctly configured, Iceberg table can be read from S3 using the following command:

```sql
SELECT *
FROM iceberg_scan('s3://<bucket>/<iceberg-table-folder>/metadata/<id>.metadata.json')
```

Note that you need to link directly to the manifest file. Otherwise you'll get an error like this:

```text
Error: IO Error: Cannot open file "s3://<bucket>/<iceberg-table-folder>/metadata/version-hint.text": No such file or directory
```
