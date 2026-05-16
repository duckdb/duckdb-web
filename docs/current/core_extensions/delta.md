---
github_repository: https://github.com/duckdb/duckdb-delta
layout: docu
redirect_from:
  - /docs/extensions/delta
  - /docs/stable/extensions/delta
  - /docs/preview/core_extensions/delta
  - /docs/stable/core_extensions/delta
title: Delta Extension
---

The `delta` extension adds support for the [Delta Lake open-source storage format](https://delta.io/). It is built using the [Delta Kernel](https://github.com/delta-incubator/delta-kernel-rs). The extension offers **read and write support** for Delta tables, both local and remote.

For implementation details, see the [announcement blog post]({% post_url 2024-06-10-delta %}).

> Warning We are aware of a regression in Azure Onelake which appears to be a consequence of a change in `delta-kernel-rs`. You can track the issue [on GitHub](https://github.com/duckdb/duckdb-delta/issues/307).

> To connect to Unity Catalog, DuckDB has the [`unity_catalog` extension]({% link docs/current/core_extensions/unity_catalog.md %}).

## Installing and Loading

The `delta` extension will be transparently [autoloaded]({% link docs/current/extensions/overview.md %}#autoloading-extensions) on first use from the official extension repository.
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

To scan a Delta table in an [S3 bucket]({% link docs/current/core_extensions/httpfs/s3api.md %}), run:

```sql
SELECT *
FROM delta_scan('s3://some/delta/table');
```

For authenticating to S3 buckets, DuckDB [Secrets]({% link docs/current/configuration/secrets_manager.md %}) are supported:

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

To scan a Delta table in an [Azure Blob Storage bucket]({% link docs/current/core_extensions/azure.md %}#azure-blob-storage), run:

```sql
SELECT *
FROM delta_scan('az://my-container/my-table');
```

For authenticating to Azure Blob Storage, DuckDB [Secrets]({% link docs/current/configuration/secrets_manager.md %}) are supported:

```sql
CREATE SECRET (
    TYPE azure,
    PROVIDER credential_chain
);
SELECT *
FROM delta_scan('az://my-container/my-table-with-auth');
```

### Reading from Google Cloud Storage

To scan a Delta table in a [GCS bucket]({% link docs/current/core_extensions/httpfs/s3api.md %}), use [HMAC keys](https://console.cloud.google.com/storage/settings;tab=interoperability) and create a secret:

```sql
CREATE SECRET (
    TYPE gcs,
    KEY_ID '⟨hmac-key-id⟩',
    SECRET '⟨hmac-secret⟩'
);
SELECT *
FROM delta_scan('gs://my-bucket/my-delta-table');
```

### Appending Data

To append rows to a Delta table, attach it and use `INSERT INTO`:

```sql
ATTACH 's3://my-bucket/my-delta-table' AS my_table (TYPE delta);
INSERT INTO my_table SELECT * FROM other_table;
```

### Time Travel

To read a specific version of a Delta table, attach it and use the `AT (VERSION => n)` clause:

```sql
ATTACH 's3://my-bucket/my-delta-table' AS my_table (TYPE delta);
SELECT * FROM my_table AT (VERSION => 5);
```

Alternatively, pin a version at attach time:

```sql
ATTACH 's3://my-bucket/my-delta-table' AS my_table (TYPE delta, VERSION 5);
```

### Checkpointing

To compact the Delta log of an attached table into a checkpoint file:

```sql
ATTACH 'path/to/my-delta-table' AS my_table (TYPE delta);
CHECKPOINT my_table;
```

### Credential Chains in Delta

DuckDB Delta uses `delta-kernel-rs` and `object_store` for some network operations.
These systems have a different ordering (and inclusion defaults) for credential
chains. If your system has multiple credential sources available, e.g., both
Service Principal via the environment and a CLI-based option, credential loading behavior
may be inconsistent.

To avoid ambiguities, we recommend that you configure exactly one available
credential type in your production chain secrets.

## Features

The `delta` extension supports:

- multithreaded scans and Parquet metadata reading
- data skipping/filter pushdown
  - skipping row groups in file (based on Parquet metadata)
  - skipping complete files (based on Delta partition information)
- projection pushdown
- scanning tables with deletion vectors
- all primitive types
- structs
- VARIANT type
- blind appends (`INSERT INTO`)
- cloud storage (AWS S3, Azure, GCS) with secrets

## Supported Platforms

The `delta` extension currently only supports the following platforms:

- Linux AMD64 (x86_64 and ARM64): `linux_amd64` and `linux_arm64`
- macOS Intel and Apple Silicon: `osx_amd64` and `osx_arm64`
- Windows AMD64: `windows_amd64`

Support for the [other DuckDB platforms]({% link docs/current/extensions/extension_distribution.md %}#platforms) is work-in-progress.

## Using delta-rs with DuckDB

In this example, we create a Delta table with the `delta-rs` Python binding, then we use the `delta` extension of DuckDB to read it. We also showcase how to do other read operations with DuckDB, like reading the change data feed using the Arrow zero-copy integration. This operation can also be lazy if reading bigger data by using [Arrow Datasets](https://delta-io.github.io/delta-rs/integrations/delta-lake-arrow/).

<!-- markdownlint-disable MD040 MD046 -->

<details markdown='1'>
<summary markdown='span'>
Click here to see the full example.
</summary>

```python
import deltalake as dl
import pyarrow as pa

# Create a delta table and read it with DuckDB Delta extension
dl.write_deltalake(
    "tmp/some_table",
    pa.table({
        "id": [1, 2, 3],
        "value": ["a", "b", "c"]
    })
)
with duckdb.connect() as conn:
    conn.execute("""
        INSTALL delta;
        LOAD delta;
    """)
    conn.sql("""
        SELECT * FROM delta_scan('tmp/some_table')
    """).show()

# Append some data and read the data change feed using the PyArrow integration
dl.write_deltalake(
    "tmp/some_table",
    pa.table({
        "id": [4, 5],
        "value": ["d", "e"]
    }),
    mode="append"
)
table = dl.DeltaTable("tmp/some_table").load_cdf(starting_version=1, ending_version=2)
with duckdb.connect() as conn:
    conn.register("t", table)
    conn.sql("SELECT * FROM t").show()
```

</details>

<!-- markdownlint-enable MD040 MD046 -->
