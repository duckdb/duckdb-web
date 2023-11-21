---
layout: docu
title: S3 Iceberg Import
selected: S3 Iceberg Import
---

# How to load an Iceberg table directly from S3

To load an Iceberg file from S3, both the `HTTPFS` and `iceberg` extensions are required. This can be installed use the `INSTALL` SQL command. This only needs to be run once.

```sql
INSTALL httpfs;
INSTALL iceberg;
```

To load the extensions for usage, use the `LOAD` SQL command:

```sql
LOAD httpfs;
LOAD iceberg;
```

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

Note: You can additionaly use the aws extension to retrieve the credentials from the aws config file. See [AWS Credentials](/docs/extensions/aws.html) for more information. To load the credentials:

```sql
CALL load_aws_credentials();
```

After the extensions are set up and the S3 credentials are correctly configured, Iceberg table can be read from S3 using the following command:

```sql
SELECT *
FROM
    iceberg_scan('s3://<bucket>/<iceberg-table-folder>/metadata/<id>.metadata.json')
```

Note: Note that you need to link directly to the manifest file. Otherwise you'll get an error like this:

```shell
Error: IO Error: Cannot open file "s3://<bucket>/<iceberg-table-folder>/metadata/version-hint.text": No such file or directory
```


