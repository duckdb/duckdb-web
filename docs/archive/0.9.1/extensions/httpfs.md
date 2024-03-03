---
layout: docu
title: httpfs Extension
---

The `httpfs` extension is an autoloadable extension implementing a file system that allows reading remote/writing remote files. For plain HTTP(S), only file reading is supported. For object storage using the S3 API, the `httpfs` extension supports reading/writing/globbing files.

The `httpfs` extension will be, by default, autoloaded on first use of any functionality exposed by this extension.
If you prefer to explicitly install and load this extension, you can always run `INSTALL httpfs` on first use and issue `LOAD httpfs` at the start of every session.

## Running Queries over HTTP(S)

With the `httpfs` extension, it is possible to directly query files over the HTTP(S) protocol. This works for all files supported by DuckDB or its various extensions, and provides read-only access.

```sql
SELECT * FROM 'https://domain.tld/file.extension';
```

For CSV files, files will be downloaded entirely in most cases, due to the row-based nature of the format. For Parquet files, DuckDB can use a combination of the Parquet metadata and HTTP range requests to only download the parts of the file that are actually required by the query. For example, the following query will only read the Parquet metadata and the data for the `column_a` column:

```sql
SELECT column_a FROM 'https://domain.tld/file.parquet';
```

In some cases even, no actual data needs to be read at all as they only require reading the metadata:

```sql
SELECT COUNT(*) FROM 'https://domain.tld/file.parquet';
```

Scanning multiple files over HTTP(S) is also supported:

```sql
SELECT * FROM read_parquet(['https://domain.tld/file1.parquet', 'https://domain.tld/file2.parquet']);

-- parquet_scan is an alias of read_parquet, so they are equivalent
SELECT * FROM parquet_scan(['https://domain.tld/file1.parquet', 'https://domain.tld/file2.parquet']);
```

## Running Queries over S3

The `httpfs` extension supports reading/writing/globbing files on object storage servers using the S3 API. S3 offers a standard API to read and write to remote files (while regular http servers, predating S3, do not offer a common write API). DuckDB conforms to the S3 API, that is now common among industry storage providers.

### Requirements

The `httpfs` filesystem is tested with [AWS S3](https://aws.amazon.com/s3/), [Minio](https://min.io/), [Google Cloud](https://cloud.google.com/storage/docs/interoperability), and [lakeFS](https://docs.lakefs.io/integrations/duckdb.html). Other services that implement the S3 API should also work, but not all features may be supported. Below is a list of which parts of the S3 API are required for each `httpfs` feature.

| Feature | Required S3 API features |
|:---|:---|
| Public file reads | HTTP Range requests |
| Private file reads | Secret key or session token authentication |
| File glob | [ListObjectV2](https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListObjectsV2.html)|
| File writes | [Multipart upload](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html)|

### Configuration

To be able to read or write from S3, the correct region should be set:

```sql
SET s3_region='us-east-1';
```

Optionally, the endpoint can be configured in case a non-AWS object storage server is used:

```sql
SET s3_endpoint='<domain>.<tld>:<port>';
```

If the endpoint is not SSL-enabled then run: 

```sql
SET s3_use_ssl=false;
```

Switching between [path-style](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-bucket-intro.html#path-style-url-ex) and [vhost-style](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-bucket-intro.html#virtual-host-style-url-ex) URLs is possible using:

```sql
SET s3_url_style='path';
```

However, note that this may also require updating the endpoint. For example for AWS S3 it is required to change the endpoint to `s3.<region>.amazonaws.com`.

After configuring the correct endpoint and region, public files can be read. To also read private files, authentication credentials can be added:

```sql
SET s3_access_key_id='<AWS access key id>';
SET s3_secret_access_key='<AWS secret access key>';
```

Alternatively, session tokens are also supported and can be used instead:

```sql
SET s3_session_token='<AWS session token>';
```

The [`aws` extension](aws) allows for loading AWS credentials.

#### Per-Request Configuration

Aside from the global S3 configuration described above, specific configuration values can be used on a per-request basis. This allows for use of multiple sets of credentials, regions, etc. These are used by including them on the S3 URI as query parameters. All the individual configuration values listed above can be set as query parameters. For instance:

```sql
SELECT *
FROM 's3://bucket/file.parquet?s3_access_key_id=accessKey&s3_secret_access_key=secretKey';
```

Multiple configurations per query are also allowed:

```sql
SELECT *
FROM 's3://bucket/file.parquet?s3_region=region&s3_session_token=session_token' T1
INNER JOIN 's3://bucket/file.csv?s3_access_key_id=accessKey&s3_secret_access_key=secretKey' T2;
```

### Reading

Reading files from S3 is now as simple as:

```sql
SELECT * FROM 's3://bucket/file.extension';
```

Multiple files are also possible, for example:

```sql
SELECT * FROM read_parquet(['s3://bucket/file1.parquet', 's3://bucket/file2.parquet']);
```

#### Glob

File globbing is implemented using the ListObjectV2 API call and allows to use filesystem-like glob patterns to match multiple files, for example:

```sql
SELECT * FROM read_parquet('s3://bucket/*.parquet');
```

This query matches all files in the root of the bucket with the parquet extension.

Several features for matching are supported, such as `*` to match any number of any character, `?` for any single character or `[0-9]` for a single character in a range of characters:

```sql
SELECT COUNT(*) FROM read_parquet('s3://bucket/folder*/100?/t[0-9].parquet');
```

A useful feature when using globs is the `filename` option which adds a column with the file that a row originated from:

```sql
SELECT * FROM read_parquet('s3://bucket/*.parquet', FILENAME = 1);
```

could for example result in:

| column_a | column_b | filename |
|:---|:---|:---|
| 1 | examplevalue1 | s3://bucket/file1.parquet |
| 2 | examplevalue1 | s3://bucket/file2.parquet |

#### Hive Partitioning

DuckDB also offers support for the Hive partitioning scheme. In the Hive partitioning scheme, data is partitioned in separate files. The columns by which the data is partitioned, are not actually in the files, but are encoded in the file path. So for example let us consider three parquet files Hive paritioned by year:

```text
s3://bucket/year=2012/file.parquet
s3://bucket/year=2013/file.parquet
s3://bucket/year=2014/file.parquet
```

If scanning these files with the `HIVE_PARTITIONING` option enabled:

```sql
SELECT * FROM read_parquet('s3://bucket/*/file.parquet', HIVE_PARTITIONING = 1);
```

could result in:

| column_a | column_b | year |
|:---|:---|:---|
| 1 | examplevalue1 | 2012 |
| 2 | examplevalue2 | 2013 |
| 3 | examplevalue3 | 2014 |

Note that the year column does not actually exist in the parquet files, it is parsed from the filenames. Within DuckDB however, these columns behave just like regular columns. For example, filters can be applied on Hive partition columns:

```sql
SELECT * FROM read_parquet('s3://bucket/*/file.parquet', HIVE_PARTITIONING = 1) where year=2013;
```

### Writing

Writing to S3 uses the multipart upload API. This allows DuckDB to robustly upload files at high speed. Writing to S3 works for both CSV and Parquet:

```sql
COPY table_name TO 's3://bucket/file.extension';
```

Partitioned copy to S3 also works:

```sql
COPY table TO 's3://my-bucket/partitioned' (FORMAT PARQUET, PARTITION_BY (part_col_a, part_col_b));
```

An automatic check is performed for existing files/directories, which is currently quite conservative (and on S3 will add a bit of latency). To disable this check and force writing, an `ALLOW_OVERWRITE` flag is added:

```sql
COPY table TO 's3://my-bucket/partitioned' (FORMAT PARQUET, PARTITION_BY (part_col_a, part_col_b), ALLOW_OVERWRITE true);
```

The naming scheme of the written files looks like this:

```text
s3://my-bucket/partitioned/part_col_a=<val>/part_col_b=<val>/data_<thread_number>.parquet
```

#### Configuration

Some additional configuration options exist for the S3 upload, though the default values should suffice for most use cases.

| setting | description |  
|:---|:---|
| `s3_uploader_max_parts_per_file` | used for part size calculation, see [AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html) |
| `s3_uploader_max_filesize` | used for part size calculation, see [AWS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html) |
| `s3_uploader_thread_limit` | maximum number of uploader threads |

Additionally, most of the configuration options can be set via environment variables:

| DuckDB setting         | Environment variable    | Note                                     |
|:-----------------------|:------------------------|:-----------------------------------------|
| `s3_region`            | `AWS_REGION`            | Takes priority over `AWS_DEFAULT_REGION` |
| `s3_region`            | `AWS_DEFAULT_REGION`    |                                          |
| `s3_access_key_id`     | `AWS_ACCESS_KEY_ID`     |                                          |
| `s3_secret_access_key` | `AWS_SECRET_ACCESS_KEY` |                                          |
| `s3_session_token`     | `AWS_SESSION_TOKEN`     |                                          |
| `s3_endpoint`          | `DUCKDB_S3_ENDPOINT`    |                                          |
| `s3_use_ssl`           | `DUCKDB_S3_USE_SSL`     |                                          |