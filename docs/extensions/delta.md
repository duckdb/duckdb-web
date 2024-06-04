---
layout: docu
title: Delta Extension
github_repository: https://github.com/duckdb/duckdb_delta
---

The `delta` extension adds support for the [Delta Lake open-source storage format](https://delta.io/). It is built using the [Delta Kernel](https://github.com/delta-incubator/delta-kernel-rs). The extension offers **read support** for delta tables, both local and remote.

> Warning The `delta` extension is currently experimental and is [only supported on given platforms](#supported-duckdb-versions-and-platforms).

## Installing and Loading

The `delta` extension is installed and loaded automatically upon first use. If you prefer to install and load it manually, run:

```sql
INSTALL delta;
LOAD delta;
```

## Usage

To scan a local delta table, run:

```sql
SELECT *
FROM delta_scan('file:///some/path/on/local/machine');
```

To scan a delta table in an S3 bucket, run:

```sql
SELECT *
FROM delta_scan('s3://some/delta/table');
```

For authenticating to S3 buckets, DuckDB [Secrets](../configuration/secrets_manager) are supported:

```sql
CREATE SECRET (
    TYPE S3,
    PROVIDER CREDENTIAL_CHAIN
);
SELECT *
FROM delta_scan('s3://some/delta/table/with/auth');
```

## Features

While the `delta` extension is still experimental, many (scanning) features and optimizations are already supported:

* multithreaded scans and Parquet metadata reading
* data skipping/filter pushdown
    * skipping row-groups in file (based on Parquet metadata)
    * skipping complete files (based on Delta partition information)
* projection pushdown
* scanning tables with deletion vectors
* all primitive types
* structs
* S3 support with secrets

More optimizations are going to be released in the future.

## Supported DuckDB Versions and Platforms

The `delta` extension requires DuckDB version 0.10.3 or newer.

The `delta` extension currently only supports the following platforms:

* Linux AMD64 (x86_64): `linux_amd64` and `linux_amd64_gcc4`
* macOS Intel and Apple Silicon: `osx_amd64` and `osx_arm64`

Support for the [other DuckDB platforms](working_with_extensions#platforms) is work-in-progress.
