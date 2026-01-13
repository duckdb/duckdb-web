---
layout: docu
selected: S3 Iceberg Import
title: S3 Iceberg Import
---

## Prerequisites

Loading an Iceberg file from S3 requires both the [`httpfs`]({% link docs/preview/core_extensions/httpfs/overview.md %}) and [`iceberg`]({% link docs/preview/core_extensions/iceberg/overview.md %}) extensions. Install them using the `INSTALL` SQL command. You only need to install extensions once.

```sql
INSTALL httpfs;
INSTALL iceberg;
```

To load the extensions, use the `LOAD` command:

```sql
LOAD httpfs;
LOAD iceberg;
```

## Credentials

After loading the extensions, set up the credentials and S3 region to read data. You may either use an access key and secret, or a token.

```sql
CREATE SECRET (
    TYPE s3,
    KEY_ID '⟨AKIAIOSFODNN7EXAMPLE⟩',
    SECRET '⟨wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY⟩',
    REGION '⟨us-east-1⟩'
);
```

Alternatively, use the [`aws` extension]({% link docs/preview/core_extensions/aws.md %}) to retrieve the credentials automatically:

```sql
CREATE SECRET (
    TYPE s3,
    PROVIDER credential_chain
);
```

## Loading Iceberg Tables from S3

After the extensions are set up and the S3 credentials are correctly configured, Iceberg tables can be read from S3 using the following command:

```sql
SELECT *
FROM iceberg_scan('s3://⟨bucket⟩/⟨iceberg_table_folder⟩/metadata/⟨id⟩.metadata.json');
```

Note that you need to link directly to the manifest file. Otherwise, you'll get an error like this:

```console
IO Error:
Cannot open file "s3://bucket/iceberg_table_folder/metadata/version-hint.text": No such file or directory
```
