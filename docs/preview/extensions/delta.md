---
github_repository: https://github.com/duckdb/duckdb-delta
layout: docu
title: Delta Extension
---

The `delta` extension adds support for the [Delta Lake open-source storage format](https://delta.io/). It is built using the [Delta Kernel](https://github.com/delta-incubator/delta-kernel-rs). The extension offers **read support** for Delta tables, both local and remote.

For implementation details, see the [announcement blog post]({% post_url 2024-06-10-delta %}).

> Warning The `delta` extension is currently experimental and is [only supported on given platforms](#supported-duckdb-versions-and-platforms).

## Installing and Loading

The `delta` extension will be transparently [autoloaded]({% link docs/preview/extensions/overview.md %}#autoloading-extensions) on first use from the official extension repository.
If you would like to install and load it manually, run:

```sql
INSTALL delta;
LOAD delta;
```

## Usage

To scan a local Delta table, run:

```sql
SELECT *
FROM delta_scan('file:///some/path/on/local/machine');
```

### Reading from an S3 Bucket

To scan a Delta table in an [S3 bucket]({% link docs/preview/extensions/httpfs/s3api.md %}), run:

```sql
SELECT *
FROM delta_scan('s3://some/delta/table');
```

For authenticating to S3 buckets, DuckDB [Secrets]({% link docs/preview/configuration/secrets_manager.md %}) are supported:

```sql
CREATE SECRET (
    TYPE s3,
    PROVIDER credential_chain
);
SELECT *
FROM delta_scan('s3://some/delta/table/with/auth');
```

To scan public buckets on S3, you may need to pass the correct region by creating a secret containing the region of your public S3 bucket:

```sql
CREATE SECRET (
    TYPE s3,
    REGION 'my-region'
);
SELECT *
FROM delta_scan('s3://some/public/table/in/my-region');
```

### Reading from Azure Blob Storage

To scan a Delta table in an [Azure Blob Storage bucket]({% link docs/preview/extensions/azure.md %}#azure-blob-storage), run:

```sql
SELECT *
FROM delta_scan('az://my-container/my-table');
```

For authenticating to Azure Blob Storage, DuckDB [Secrets]({% link docs/preview/configuration/secrets_manager.md %}) are supported:

```sql
CREATE SECRET (
    TYPE azure,
    PROVIDER credential_chain
);
SELECT *
FROM delta_scan('az://my-container/my-table-with-auth');
```

## Features

While the `delta` extension is still experimental, many (scanning) features and optimizations are already supported:

* multithreaded scans and Parquet metadata reading
* data skipping/filter pushdown
    * skipping row groups in file (based on Parquet metadata)
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

* Linux AMD64 (x86_64 and ARM64): `linux_amd64`, `linux_amd64_gcc4`, and `linux_arm64`
* macOS Intel and Apple Silicon: `osx_amd64` and `osx_arm64`
* Windows AMD64: `windows_amd64`

Support for the [other DuckDB platforms]({% link docs/preview/extensions/extension_distribution.md %}#platforms) is work-in-progress.
