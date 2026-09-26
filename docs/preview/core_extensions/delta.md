---
github_repository: https://github.com/duckdb/duckdb-delta
layout: docu
title: Delta Extension
---

The `delta` extension adds support for the [Delta Lake open-source storage format](https://delta.io/). It is built using the [Delta Kernel](https://github.com/delta-incubator/delta-kernel-rs). The extension offers **read and write support** for Delta tables, both local and remote.

For implementation details, see the [announcement blog post]({% post_url 2024-06-10-delta %}).

> Warning We are aware of a regression in Azure Onelake which appears to be a consequence of a change in `delta-kernel-rs`. You can track the issue [on GitHub](https://github.com/duckdb/duckdb-delta/issues/307).

> To connect to Unity Catalog, DuckDB has the [`unity_catalog` extension]({% link docs/preview/core_extensions/unity_catalog.md %}).

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

To scan a Delta table in an [S3 bucket]({% link docs/preview/core_extensions/httpfs/s3api.md %}), run:

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

To scan a Delta table in an [Azure Blob Storage bucket]({% link docs/preview/core_extensions/azure.md %}#azure-blob-storage), run:

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

### Reading from Google Cloud Storage

To scan a Delta table in a [GCS bucket]({% link docs/preview/core_extensions/httpfs/s3api.md %}), use [HMAC keys](https://console.cloud.google.com/storage/settings;tab=interoperability) and create a secret:

```sql
CREATE SECRET (
    TYPE gcs,
    KEY_ID '⟨hmac-key-id⟩',
    SECRET '⟨hmac-secret⟩'
);
SELECT *
FROM delta_scan('gs://my-bucket/my-delta-table');
```

### Creating Tables

To create a new Delta table, attach the location where it should live and create a table with the same name as the attached database:

```sql
ATTACH 's3://my-bucket/my-new-table' AS my_new_table (TYPE delta);
CREATE TABLE my_new_table.my_new_table (id BIGINT, region VARCHAR)
PARTITIONED BY (region);
INSERT INTO my_new_table VALUES (1, 'eu');
```

The new table can be read and written right away, without attaching it again. `CREATE TABLE ... IF NOT EXISTS` leaves an existing table untouched.

The following are not supported:

* `CREATE OR REPLACE TABLE` and `CREATE TABLE ... AS SELECT`. To fill a new table, create it and then `INSERT` into it.
* `NOT NULL` and other constraints, and `SORTED BY`.
* Column types that Delta has no equivalent for, such as unsigned integers.
* A table whose columns are all partition columns.

#### Table Properties

Options in a `WITH` clause become Delta table properties:

```sql
ATTACH 's3://my-bucket/my-new-table' AS my_new_table (TYPE delta);
CREATE TABLE my_new_table.my_new_table (id BIGINT, name VARCHAR)
WITH ('delta.enableDeletionVectors' = 'true', 'delta.appendOnly' = 'true');
```

The [Delta Kernel](https://github.com/delta-incubator/delta-kernel-rs) validates each property and enables the table features it requires, so the table's protocol follows from its properties. Values can be any constant expression; `NULL` is not allowed. The only option that is not a table property is `location`, which may repeat the attached path but cannot name a different one.

To create a table with [column mapping](#column-mapping), set `'delta.columnMapping.mode'` to `'name'` or `'id'`. A column-mapped table cannot have nested columns (`STRUCT`, `LIST` or `MAP`) or partition columns, because DuckDB cannot write to such tables yet. The same applies to properties that imply column mapping, such as `'delta.enableIcebergCompatV3'`.

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

A table attached at a version or a [timestamp](#time-travel-by-timestamp) is read-only: an `INSERT` into it fails.

`delta_scan` takes the version as a named parameter:

```sql
SELECT * FROM delta_scan('s3://my-bucket/my-delta-table', version => 5);
```

#### Time Travel by Timestamp

To read a table as it was at a point in time, give a timestamp instead of a version, in any of the same three places:

```sql
SELECT * FROM my_table AT (TIMESTAMP => TIMESTAMPTZ '2026-09-01 12:00:00+00');
```

```sql
ATTACH 's3://my-bucket/my-delta-table' AS my_table_then (
    TYPE delta,
    TIMESTAMP TIMESTAMPTZ '2026-09-01 12:00:00+00'
);
```

```sql
SELECT *
FROM delta_scan('s3://my-bucket/my-delta-table', timestamp => TIMESTAMPTZ '2026-09-01 12:00:00+00');
```

* A timestamp reads the latest version committed at or before it. A timestamp before the table's first commit is an error.
* A timestamp without a time zone is interpreted in the session's `TimeZone`.
* A timestamp later than `now()` is refused.
* A version and a timestamp cannot both be given.
* Within a transaction, a timestamp resolves once: every later read of the same instant sees the same version, even if the table receives new commits in the meantime.
* A version or timestamp given to `ATTACH` is the default for queries on that table. An `AT` clause overrides it, in either unit.

### Checkpointing

To compact the Delta log of an attached table into a checkpoint file:

```sql
ATTACH 'path/to/my-delta-table' AS my_table (TYPE delta);
CHECKPOINT my_table;
```

### Idempotent Appends

The `delta` extension exposes an idempotent-append API that uses Delta's per-application transaction versions to give exactly-once semantics: an append tagged with an `app_id` and a version is only committed if the table's currently recorded version for that `app_id` matches the expected previous version. This lets a producer safely retry a batch without duplicating it.

Within a transaction, tag the append with `delta_set_transaction_version(⟨table⟩, ⟨app_id⟩, ⟨new_version⟩, ⟨expected_previous_version⟩)`:

```sql
ATTACH 'path/to/my-delta-table' AS my_table (TYPE delta);

BEGIN TRANSACTION;
CALL delta_set_transaction_version('my_table', 'my_app_id', 1::UBIGINT, NULL::UBIGINT);
INSERT INTO my_table VALUES (1);
COMMIT;
```

On `COMMIT`, the version is compared-and-swapped: if another process advanced the version for `my_app_id` in the meantime, the commit fails. Aborting the transaction leaves the version unchanged. Read the current version with `delta_get_transaction_version(⟨table⟩, ⟨app_id⟩)`, which returns `NULL` if no version has been recorded yet.

### Attach Options

When attaching a Delta table you can pass the following options to `ATTACH`:

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `VERSION` | `UBIGINT` | latest | Pin the attached table to a specific [table version](#time-travel). The attached table is read-only. |
| `TIMESTAMP` | `TIMESTAMP WITH TIME ZONE` | latest | Pin the attached table to the version current at a [point in time](#time-travel-by-timestamp). Cannot be combined with `VERSION`. The attached table is read-only. |
| `PIN_SNAPSHOT` | `BOOLEAN` | `false` | Resolve the table snapshot once at attach time and reuse it, rather than re-resolving the latest version per query. |
| `PUSHDOWN_PARTITION_INFO` | `BOOLEAN` | `true` | Push down partition information so that whole files can be skipped based on partition values. |
| `PUSHDOWN_FILTERS` | `VARCHAR` | `all` | Filter pushdown mode for file skipping. One of `none`, `all`, `constant_only`, `dynamic_only`. |

```sql
ATTACH 's3://my-bucket/my-delta-table' AS my_table (
    TYPE delta,
    PIN_SNAPSHOT true,
    PUSHDOWN_FILTERS 'constant_only'
);
```

### Inspecting Scanned Files

`delta_list_files` returns the data files a scan would read for a table, together with their cardinality, partition values, and whether they carry deletion vectors. This is useful for understanding the effect of [data skipping](#features):

```sql
SELECT * FROM delta_list_files('file:///some/path/on/local/machine');
```

| Column | Type | Description |
| --- | --- | --- |
| `data_file` | `VARCHAR` | Path to the Parquet data file. |
| `cardinality` | `UBIGINT` | Number of rows in the file. |
| `partitions` | `MAP(VARCHAR, VARCHAR)` | Partition column values for the file. |
| `have_deletes` | `BOOLEAN` | Whether the file has an associated deletion vector. |

### Column Mapping

Delta tables with [column mapping](https://github.com/delta-io/delta/blob/master/PROTOCOL.md#column-mapping) enabled are read as the Delta protocol specifies for each mode: in `id` mode, columns are matched by Parquet field ID; in `name` mode, by physical column name.

The protocol requires every data file of an `id`-mode table to carry Parquet field IDs, but some writers, including older DuckDB versions, wrote files without them. The `delta_column_mapping_policy` setting decides how such files are read:

* `strict`: refuse the file with an error that names it.
* `lenient`: match the file's columns by physical name, or failing that by logical name, and log a warning under the `delta.ColumnMapping` log type. The names have to cover every column in the file, otherwise the read fails.

> Warning The default changed in DuckDB 2.0. It is now `strict`, so a table whose `id`-mode files lack field IDs, which DuckDB 1.5 read by name under its `lenient` default, fails to read. To read such a table, opt in to the old behavior:

```sql
SET delta_column_mapping_policy = 'lenient';
```

### Credential Chains in Delta

DuckDB Delta uses `delta-kernel-rs` and `object_store` for some network operations.
These systems have a different ordering (and inclusion defaults) for credential
chains. If your system has multiple credential sources available, e.g., both
Service Principal via the environment and a CLI-based option, credential loading behavior
may be inconsistent.

To avoid ambiguities, we recommend that you configure exactly one available
credential type in your production chain secrets.

## Settings

The `delta` extension adds the following settings:

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| `delta_column_mapping_policy` | `VARCHAR` | `strict` | How to read a data file of a column-mapped table that does not conform to the Delta protocol, such as an `id`-mode file without Parquet field IDs: `strict` refuses the file, `lenient` matches its columns by name and logs a warning. See [Column Mapping](#column-mapping). |
| `delta_kernel_logging` | `BOOLEAN` | `false` | Forward the internal logging of the [Delta Kernel](https://github.com/delta-incubator/delta-kernel-rs) to the DuckDB logger. May impact performance even when DuckDB logging is disabled. |
| `delta_scan_explain_files_filtered` | `BOOLEAN` | `true` | Add the filtered files to the `EXPLAIN` output. May impact the performance of `delta_scan` during `EXPLAIN ANALYZE` queries. |

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
- creating tables (`CREATE TABLE`)
- blind appends (`INSERT INTO`)
- cloud storage (AWS S3, Azure, GCS) with secrets

## Limitations

* Tables with a column of one of Delta's interval types (`interval year to month` or `interval day to second`), or of type `geometry` or `geography`, cannot be read. The scan fails with an error rather than leaving the column out.
* Writes to a table that declares column defaults are refused, because DuckDB does not fill in the defaults.

## Supported Platforms

The `delta` extension currently only supports the following platforms:

- Linux AMD64 (x86_64 and ARM64): `linux_amd64` and `linux_arm64`
- macOS Intel and Apple Silicon: `osx_amd64` and `osx_arm64`
- Windows AMD64: `windows_amd64`

Support for the [other DuckDB platforms]({% link docs/preview/extensions/extension_distribution.md %}#platforms) is work-in-progress.

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
