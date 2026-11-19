---
github_repository: https://github.com/duckdb/duckdb-delta
layout: docu
redirect_from:
- /docs/extensions/delta
- /docs/stable/extensions/delta
- /docs/stable/core_extensions/delta
- /docs/current/core_extensions/delta
- /docs/lts/core_extensions/delta
- /docs/preview/core_extensions/delta
title: Delta Extension
---

The `delta` extension adds support for the [Delta Lake open-source storage format](https://delta.io/). It is built using the [Delta Kernel](https://github.com/delta-io/delta-kernel-rs). The extension reads Delta tables, local and remote, and writes them: it can create tables and append to them.

For implementation details, see the [“Native Delta Lake Support in DuckDB” blog post]({% post_url 2024-06-10-delta %}).

> To connect to Unity Catalog, DuckDB has the [`unity_catalog` extension]({% link docs/2.0/core_extensions/unity_catalog.md %}).

## Installing and Loading

The `delta` extension will be transparently [autoloaded]({% link docs/2.0/extensions/overview.md %}#autoloading-extensions) on first use from the official extension repository.
If you would like to install and load it manually, run:

```sql
INSTALL AND LOAD delta;
```

## Usage

To scan a local Delta table, run:

```sql
SELECT *
FROM delta_scan('file:///⟨path⟩');
```

### Attaching Tables

A Delta table can also be attached as a database. The database holds exactly one table, with the same name as the database, so `my_table` and `my_table.my_table` refer to the same table:

```sql
ATTACH 'file:///⟨path⟩' AS my_table (TYPE delta);
SELECT * FROM my_table;
```

### Reading from an S3 Bucket

To scan a Delta table in an [S3 bucket]({% link docs/2.0/core_extensions/httpfs/s3api.md %}), run:

```sql
SELECT *
FROM delta_scan('s3://⟨my_bucket⟩/⟨path⟩');
```

To authenticate, create a [secret]({% link docs/2.0/configuration/secrets_manager.md %}):

```sql
CREATE SECRET (
    TYPE s3,
    PROVIDER credential_chain
);
SELECT *
FROM delta_scan('s3://⟨my_bucket⟩/⟨path⟩');
```

For a public bucket, you may need to set its region in a secret:

```sql
CREATE SECRET (
    TYPE s3,
    REGION '⟨my_region⟩'
);
SELECT *
FROM delta_scan('s3://⟨my_bucket⟩/⟨path⟩');
```

### Reading from Azure Blob Storage

To scan a Delta table in an [Azure Blob Storage container]({% link docs/2.0/core_extensions/azure.md %}#azure-blob-storage), run:

```sql
SELECT *
FROM delta_scan('az://⟨my_container⟩/⟨path⟩');
```

To authenticate, create a [secret]({% link docs/2.0/configuration/secrets_manager.md %}):

```sql
CREATE SECRET (
    TYPE azure,
    PROVIDER credential_chain,
    ACCOUNT_NAME '⟨storage_account_name⟩'
);
SELECT *
FROM delta_scan('az://⟨my_container⟩/⟨path⟩');
```

### Reading from Google Cloud Storage

To scan a Delta table in a GCS bucket (`gs://` or `gcs://`), create a GCS [secret]({% link docs/2.0/configuration/secrets_manager.md %}). Two kinds of credentials work.

With [HMAC keys](https://console.cloud.google.com/storage/settings;tab=interoperability), DuckDB reads the table through GCS's [S3 API compatibility]({% link docs/2.0/core_extensions/httpfs/s3api.md %}):

```sql
CREATE SECRET (
    TYPE gcs,
    KEY_ID '⟨hmac_key_id⟩',
    SECRET '⟨hmac_secret⟩'
);
SELECT *
FROM delta_scan('gs://⟨my_bucket⟩/⟨path⟩');
```

Since v2.0.1, an OAuth bearer token also works, such as one that Unity Catalog vends for a table on GCS. DuckDB then reads the table through the native GCS API:

```sql
CREATE SECRET (
    TYPE gcs,
    BEARER_TOKEN '⟨oauth_token⟩'
);
SELECT *
FROM delta_scan('gs://⟨my_bucket⟩/⟨path⟩');
```

* If the GCS secret that matches the path has a `BEARER_TOKEN`, the token is used and `KEY_ID` and `SECRET` are ignored.
* With a bearer token, `ENDPOINT` sets the base URL of the GCS API, e.g., for an emulator. Without a scheme, it uses HTTPS, or HTTP if `USE_SSL` is `false`. `REGION` and `URL_STYLE` are ignored.
* DuckDB does not refresh the token. When it expires, replace the secret.
* Without a secret, the scan fails.

### Creating Tables

> New This feature was introduced in DuckDB 2.0.

To create a Delta table, attach the location for it and create a table named after the attached database:

```sql
ATTACH 's3://⟨my_bucket⟩/⟨path⟩' AS events (TYPE delta);
CREATE TABLE events.events (id BIGINT, region VARCHAR)
PARTITIONED BY (region);
INSERT INTO events VALUES (1, 'eu');
```

A partition key matches its column in any case, and the column's own spelling is recorded; this also holds for `CREATE TABLE ... AS SELECT` and for `COPY`'s `PARTITION_BY`.

Only `CREATE TABLE` needs the full `events.events` name: without the database name, it creates the table in the default database.

The table can be read and written without attaching it again.

> Warning `ATTACH` does not check that the path holds a Delta table. A mistyped path attaches as an empty database and only fails on the first read.

#### Table Properties

Options in a `WITH` clause are stored as Delta table properties, except `location`, which must match the attached path:

```sql
ATTACH 's3://⟨my_bucket⟩/⟨other_path⟩' AS audit (TYPE delta);
CREATE TABLE audit.audit (id BIGINT, name VARCHAR)
WITH ('delta.enableDeletionVectors' = 'true', 'delta.appendOnly' = 'true');
```

Properties that enable a Delta feature, such as deletion vectors, also upgrade the table's protocol as needed. Values can be any constant expression except `NULL`. Some properties cannot be set at creation, such as `'delta.enableVariantShredding'`.

To create a table with [column mapping](#column-mapping), set `'delta.columnMapping.mode'` to `'name'` or `'id'`.

### Creating Tables from a Query

> New This feature was introduced in DuckDB 2.0.1.

To create a Delta table from a query, attach its location and use `CREATE TABLE ... AS SELECT`:

```sql
ATTACH 's3://⟨my_bucket⟩/⟨path⟩' AS sales (TYPE delta);
CREATE TABLE sales.sales PARTITIONED BY (region)
WITH ('delta.columnMapping.mode' = 'name') AS
    SELECT * FROM read_parquet('sales/*.parquet');
```

The column names and types are the query's. `PARTITIONED BY` and `WITH` work as for [`CREATE TABLE`](#creating-tables), column mapping in `name` and `id` mode included, with nested columns too.

To write a query's result as a new Delta table without attaching it, use `COPY` with `FORMAT delta`, then read the table with `delta_scan` or `ATTACH`:

```sql
COPY (SELECT * FROM read_parquet('sales/*.parquet'))
TO 's3://⟨my_bucket⟩/⟨other_path⟩' (FORMAT delta, PARTITION_BY (region));
SELECT count(*) FROM delta_scan('s3://⟨my_bucket⟩/⟨other_path⟩');
```

`COPY` takes table properties in `WITH_PROPERTIES`, a struct or a map whose keys keep their case. A known `delta.` property can also be given as an option of its own, in double quotes:

```sql
COPY (SELECT 1 AS id, 'x' AS name) TO 'audit_copy' (FORMAT delta,
    WITH_PROPERTIES {'delta.appendOnly': 'true', 'owner': 'data-team'});
COPY (SELECT 1 AS id) TO 'mapped_copy' (FORMAT delta, "delta.columnMapping.mode" 'id');
```

A `delta.` key must name a known Delta property. In `WITH` and in `WITH_PROPERTIES`, it must be spelled with its exact case: `'delta.columnmapping.mode'` fails and suggests `'delta.columnMapping.mode'`. As a `COPY` option of its own, its case does not matter, since DuckDB lowercases option names: it is stored under the property's own spelling. A key outside `delta.` is stored as given. A property can be given only once, either as an option or in `WITH_PROPERTIES`. In `WITH_PROPERTIES`, `'location'` must name the `COPY` target and `'path'` is refused, as in `CREATE TABLE`.

Both statements write the new table in a single commit: version 0 holds the table's protocol and metadata together with every data file, with file statistics, as Spark writes it. If the statement fails before it commits, for example because the query fails partway through, it creates no table and removes the files it wrote, on a best-effort basis. An empty query result creates an empty table.

The table is created when the statement ends, not when the transaction commits, as for `CREATE TABLE`. A `ROLLBACK` does not remove it:

```sql
BEGIN;
CREATE TABLE sales.sales AS SELECT 1 AS id;
ROLLBACK;
-- sales.sales exists, with its row
```

The following are not supported:

* Columns whose type Delta cannot store, such as `UHUGEINT`, `TIME`, intervals, or an untyped `NULL`: the statement fails before anything is written, naming the column. Cast the column in the query, e.g., `SELECT x::BIGINT AS x`, `SELECT x::VARCHAR AS x` for `UHUGEINT` values beyond the 38 digits of `DECIMAL(38, 0)`, or `SELECT NULL::INTEGER AS n`.
* Writing to a path that already holds a Delta table: `COPY` does not append or overwrite, and `CREATE TABLE ... AS SELECT` fails as `CREATE TABLE` does. With `IF NOT EXISTS`, an existing table is left as it is and the query does not run, unless a column or partition column is refused (see [Limitations](#limitations)): that fails first.
* `CREATE OR REPLACE TABLE ... AS SELECT`.
* `COPY` options for files, such as `OVERWRITE` or `PER_THREAD_OUTPUT`, and options outside `delta.` given on their own: put the latter in `WITH_PROPERTIES`.

In a [Unity Catalog]({% link docs/2.0/core_extensions/unity_catalog.md %}#creating-tables) catalog, `CREATE TABLE ... AS SELECT` goes through the `unity_catalog` extension, which also registers the table.

Readers see two differences from a table Spark creates. Its history records the operation as `CREATE TABLE`, not `CREATE TABLE AS SELECT`. And in a column-mapped, partitioned table, the data files of the create leave the partition columns out (their values are in the log, as the Delta protocol allows); files that later `INSERT`s write include them. A table whose features require the partition columns in its files (`materializePartitionColumns`, `icebergCompatV2`, or `icebergCompatV3`) gets them in every file.

### Appending Data

To append rows to a Delta table, attach it and use `INSERT INTO`:

```sql
ATTACH 's3://⟨my_bucket⟩/⟨path⟩' AS my_table (TYPE delta);
INSERT INTO my_table SELECT * FROM other_table;
```

Since v1.5.6, if the table schema declares `CHAR(n)` or `VARCHAR(n)` (Spark writes these), a write with a value longer than `n` characters fails as a whole.

### Time Travel

> New Time travel by timestamp was introduced in DuckDB 2.0.

To read a table as it was at an earlier version or point in time, use the `AT` clause, an `ATTACH` option, or a `delta_scan` parameter:

```sql
-- Query an attached table
SELECT * FROM my_table AT (VERSION => 5);
SELECT * FROM my_table AT (TIMESTAMP => TIMESTAMPTZ '2026-09-01 12:00:00+00');

-- Attach the table at a version or point in time
ATTACH 's3://⟨my_bucket⟩/⟨path⟩' AS my_table_v5 (TYPE delta, VERSION 5);
ATTACH 's3://⟨my_bucket⟩/⟨path⟩' AS my_table_then (TYPE delta, TIMESTAMP TIMESTAMPTZ '2026-09-01 12:00:00+00');

-- Scan without attaching
SELECT * FROM delta_scan('s3://⟨my_bucket⟩/⟨path⟩', version => 5); -- since v1.5.4
SELECT * FROM delta_scan('s3://⟨my_bucket⟩/⟨path⟩', timestamp => TIMESTAMPTZ '2026-09-01 12:00:00+00');
```

* A table attached at a version or timestamp is read-only.
* A version or timestamp given to `ATTACH` is the default for queries on that table; an `AT` clause overrides it.
* A version and a timestamp cannot be given together.
* A timestamp reads the latest version committed at or before it. One later than `now()` or earlier than the table's first commit fails.
* A timestamp without a time zone uses the session's `TimeZone`.
* Within a transaction, a timestamp always reads the same version.

### Checkpointing

Since v1.5.1, [`CHECKPOINT`]({% link docs/2.0/sql/statements/checkpoint.md %}) compacts the Delta log of an attached table into a checkpoint file, which speeds up reads of tables with long logs:

```sql
ATTACH '⟨path⟩' AS my_table (TYPE delta);
CHECKPOINT my_table;
```

### Idempotent Appends

To retry a batch without writing it twice, tag the append with an application ID and a version. DuckDB commits the append only if the table's last recorded version for that ID is the one you expect. This uses Delta's per-application transaction versions.

Within a transaction, tag the append with `delta_set_transaction_version(⟨table⟩, ⟨app_id⟩, ⟨new_version⟩, ⟨expected_previous_version⟩)`{:.language-sql .highlight}:

```sql
ATTACH '⟨path⟩' AS my_table (TYPE delta);

BEGIN TRANSACTION;
CALL delta_set_transaction_version('my_table', 'my_app_id', 1::UBIGINT, NULL::UBIGINT);
INSERT INTO my_table VALUES (1);
COMMIT;
```

If another process committed a different version for `my_app_id` first, `COMMIT` fails. A rolled-back transaction leaves the version unchanged. Read the current version with `delta_get_transaction_version(⟨table⟩, ⟨app_id⟩)`{:.language-sql .highlight}, which returns `NULL` if no version has been recorded yet.

### Attach Options

When attaching a Delta table you can pass the following options to `ATTACH`:

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `VERSION` | `UBIGINT` | latest | Attach the table at a specific [table version](#time-travel). |
| `TIMESTAMP` | `TIMESTAMP WITH TIME ZONE` | latest | Attach the table at the version current at a [point in time](#time-travel). |
| `PIN_SNAPSHOT` | `BOOLEAN` | `false` | Resolve the latest table snapshot once, on first use, and reuse it for every later query. Without it, each transaction reads the latest version; since v1.5.3, it loads only the log entries committed since the previous read. |
| `PUSHDOWN_PARTITION_INFO` | `BOOLEAN` | `true` | Push down partition information so that whole files can be skipped based on partition values. |
| `PUSHDOWN_FILTERS` | `VARCHAR` | `all` | Filter pushdown mode for file skipping. One of `none`, `all`, `constant_only`, `dynamic_only`. |

```sql
ATTACH 's3://⟨my_bucket⟩/⟨path⟩' AS my_table (
    TYPE delta,
    PIN_SNAPSHOT true,
    PUSHDOWN_FILTERS 'constant_only'
);
```

Since v2.0.1, an option that the `delta` extension does not know, e.g., a misspelled one, fails with `Unrecognized option for Delta attach`. Before, it was ignored.

### Inspecting Scanned Files

`delta_list_files` returns the data files a scan would read for a table, together with their cardinality, partition values, and whether they carry deletion vectors. This is useful for understanding the effect of [data skipping](#features):

```sql
SELECT * FROM delta_list_files('file:///⟨path⟩');
```

| Column | Type | Description |
| --- | --- | --- |
| `data_file` | `VARCHAR` | Path to the Parquet data file. |
| `cardinality` | `UBIGINT` | Number of rows in the file. |
| `partitions` | `MAP(VARCHAR, VARCHAR)` | Partition column values for the file. |
| `have_deletes` | `BOOLEAN` | Whether the file has an associated deletion vector. |

To list the files of an earlier table version, pass `version => ⟨version⟩`{:.language-sql .highlight}. To add a `delete_count` column with the number of rows each file's deletion vector removes, pass `delete_count => true`:

```sql
SELECT data_file, cardinality, delete_count
FROM delta_list_files('file:///⟨path⟩', version => 3, delete_count => true);
```

### Reading Domain Metadata

Since v1.5.1, `delta_domain_metadata` returns one row per [domain](https://github.com/delta-io/delta/blob/master/PROTOCOL.md#domain-metadata) of a table, with the `VARCHAR` columns `domain` and `configuration`. Pass `version => ⟨version⟩`{:.language-sql .highlight} for an earlier version:

```sql
SELECT domain, configuration
FROM delta_domain_metadata('file:///⟨path⟩');
```

For an attached table, `duckdb_tables()` shows the same pairs in its `tags` column.

### Column Mapping

Delta tables with [column mapping](https://github.com/delta-io/delta/blob/master/PROTOCOL.md#column-mapping) enabled are read as the Delta protocol specifies for each mode: in `id` mode, columns are matched by Parquet field ID; in `name` mode, by physical column name.

The protocol requires every data file of an `id`-mode table to carry Parquet field IDs, but some writers omit them, including DuckDB 1.5.5 and earlier. Since v1.5.6, the `delta_column_mapping_policy` setting decides how such files are read:

* `strict`: fail with an error that names the file.
* `lenient`: match the file's columns by physical name, or failing that by logical name, and log a warning under the `delta.ColumnMapping` log type. The names must cover every column in the file, otherwise the read fails.

> Warning The default changed from `lenient` in DuckDB 1.5 to `strict` in v2.0. To read such files as v1.5 did, run `SET delta_column_mapping_policy = 'lenient';`{:.language-sql .highlight}.

Since v2.0.1, DuckDB writes to column-mapped tables with partition columns or nested (struct, list, and map) columns, in both modes: `INSERT` into such a table works, whoever created it, and `CREATE TABLE` and `CREATE TABLE ... AS SELECT` can create one. Spark reads and appends to the files that DuckDB writes. Each partition of a column-mapped table goes to a directory named `part-` followed by a hash of the partition values, not to a Hive-style `⟨column⟩=⟨value⟩` directory: readers take the partition values from the Delta log.

> Warning Before v2.0.1, the partition columns of a column-mapped table read as `NULL` in every row, without an error.

### VARIANT Columns

Delta `variant` columns are read as DuckDB [`VARIANT`]({% link docs/2.0/sql/data_types/variant.md %}), whether their files are shredded or not, and top-level `VARIANT` columns can be appended to.

> New The following were introduced in DuckDB 2.0.

* A query that reads one field of a `VARIANT` or `STRUCT` column, such as `SELECT v.a`, reads only that field from the Parquet files, so on a shredded table it skips the columns of the other fields. This does not apply to a column with a `TIMESTAMP WITH TIME ZONE` field at any depth: DuckDB reads all of it.
* `CREATE TABLE` accepts top-level `VARIANT` columns. Since v2.0.1, it refuses a `VARIANT` inside a struct, list, or map, which DuckDB cannot write.
* When writing, DuckDB shreds `VARIANT` values only if the table sets `'delta.enableVariantShredding'` to `'true'`, as the Delta protocol requires; otherwise it writes them unshredded. Because `CREATE TABLE` cannot set this property, a table created by DuckDB holds unshredded files.

### Catalog-Managed Tables

A Delta table with the `catalogManaged` feature, such as a Unity Catalog managed table, has commits that only its catalog tracks. Reading or writing such a table straight from storage, with `delta_scan` or `ATTACH ... (TYPE delta)`, fails with an error. Attach its catalog instead, for example with the [`unity_catalog` extension]({% link docs/2.0/core_extensions/unity_catalog.md %}), and query the table through it.

### Credential Chains in Delta

For some network operations, the `delta` extension uses `delta-kernel-rs` and `object_store`, which try credential sources in a different order than DuckDB and include different ones by default. If more than one source is available, e.g., a service principal in the environment and the Azure CLI, credential loading may be inconsistent. Configure exactly one credential type in the chain of your secret.

Since v1.5.6, the `delta` extension supports [Azure workload identity](https://learn.microsoft.com/en-us/entra/workload-id/workload-identities-overview) (for example on AKS): name `workload_identity` in the `CHAIN` of an [Azure `credential_chain` secret]({% link docs/2.0/core_extensions/azure.md %}#credential_chain-provider), and set the `AZURE_FEDERATED_TOKEN_FILE`, `AZURE_CLIENT_ID`, and `AZURE_TENANT_ID` environment variables.

## Settings

The `delta` extension adds the following settings:

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| `delta_column_mapping_policy` | `VARCHAR` | `strict` | How to read an `id`-mode data file without Parquet field IDs: `strict` raises an error, `lenient` matches its columns by name. See [Column Mapping](#column-mapping). |
| `delta_kernel_logging` | `BOOLEAN` | `false` | Forward the internal logging of the [Delta Kernel](https://github.com/delta-io/delta-kernel-rs) to the DuckDB logger. May impact performance even when DuckDB logging is disabled. |
| `delta_scan_explain_files_filtered` | `BOOLEAN` | `true` | Add the filtered files to the `EXPLAIN` output. May impact the performance of `delta_scan` during `EXPLAIN ANALYZE` queries. |

## Features

The `delta` extension supports:

* multithreaded scans and Parquet metadata reading
* data skipping/filter pushdown
    * skipping row groups in file (based on Parquet metadata)
    * skipping complete files (based on Delta partition information and file statistics)
* projection pushdown, down to single fields of struct and [`VARIANT`](#variant-columns) columns
* scanning tables with deletion vectors
* [column mapping](#column-mapping) in `name` and `id` mode
* [time travel](#time-travel) by version or timestamp
* all primitive types except intervals
* nested types (structs, lists, and maps)
* creating tables (`CREATE TABLE`, and since v2.0.1 [`CREATE TABLE ... AS SELECT` and `COPY ... TO ... (FORMAT delta)`](#creating-tables-from-a-query))
* blind appends (`INSERT INTO`), with file statistics for data skipping
* [idempotent appends](#idempotent-appends)
* [checkpoints](#checkpointing) (`CHECKPOINT`)
* cloud storage (AWS S3, Azure, GCS) with secrets

## Limitations

* `CREATE OR REPLACE TABLE` is not supported. Before v2.0.1, `CREATE TABLE ... AS SELECT` is not supported either: create the table, then `INSERT` into it.
* `UPDATE`, `DELETE`, [`MERGE INTO`]({% link docs/2.0/sql/statements/merge_into.md %}), `ALTER TABLE`, and `DROP TABLE` are not supported, nor are `RETURNING` and `ON CONFLICT` clauses on `INSERT`.
* `CREATE TABLE` does not support:
    * constraints, including `NOT NULL`
    * `DEFAULT` values and generated columns
    * `SORTED BY`
    * column types without a Delta equivalent, such as `TIME` or unsigned integers
    * a table whose columns are all partition columns
    * since v2.0.1, a `VARIANT` inside a struct, list, or map; before, `CREATE TABLE` accepted it and the first `INSERT` failed
    * a `MAP` with a `LIST` key, at any depth
    * since v2.0.1, a `VARCHAR` column with a collation (`COLLATE`), at any depth: Delta has no collations. A cast or a string function keeps the collation, so write the column from an uncollated source.
    * a partition column of a struct, list, map, array, or `VARIANT` type, and since v2.0.1 of type `BLOB`: a Delta partition column must have a primitive type
* `CREATE TABLE ... AS SELECT` and `COPY ... TO ... (FORMAT delta)` refuse the same columns and partition columns, before anything is written.
* Since v2.0.1, the column and partition-column checks above (types, `VARIANT`, `MAP`, collations) run before `IF NOT EXISTS` is considered: `CREATE TABLE IF NOT EXISTS` with such a column fails even if the table exists, with or without `AS SELECT`.
* Before v2.0.1, DuckDB cannot write to a table with [column mapping](#column-mapping) that has nested or partition columns, nor create one.
* Writing to a column-mapped table with a struct field whose physical name is `__duckdb_field_id` (in any case) fails before anything is written.
* Tables with an interval (`interval year to month` or `interval day to second`), `geometry`, or `geography` column cannot be read.
* Writing to a table with the `allowColumnDefaults` writer feature fails, even if no column has a default yet: DuckDB cannot fill in Delta defaults and does not write `NULL` instead. Reading works.
* Writing to a table that declares a `CHAR(n)` or `VARCHAR(n)` width on a nested field, such as `ARRAY<VARCHAR(5)>`, is not supported.
* Writing to a table with a `VARIANT` inside a struct, list, or map is not supported.

## Supported Platforms

The `delta` extension currently only supports the following platforms:

* Linux (x86_64 and ARM64): `linux_amd64` and `linux_arm64`
* macOS Intel and Apple Silicon: `osx_amd64` and `osx_arm64`
* Windows AMD64: `windows_amd64`

Support for the [other DuckDB platforms]({% link docs/2.0/extensions/extension_distribution.md %}#platforms) is work-in-progress.

## Using delta-rs with DuckDB

This example writes a Delta table with the `delta-rs` Python package and reads it with DuckDB. It then reads the table's change data feed through the Arrow zero-copy integration. For larger data, use [Arrow Datasets](https://delta-io.github.io/delta-rs/latest/integrations/delta-lake-arrow/) to read it lazily.

The example needs `deltalake`, the Python package of `delta-rs`, with its `pyarrow` extra:

```batch
pip install duckdb "deltalake[pyarrow]"
```

<!-- markdownlint-disable MD040 MD046 -->

<details markdown='1'>
<summary markdown='span'>
Full example
</summary>

```python
import deltalake as dl
import duckdb
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
    conn.sql("""
        SELECT * FROM delta_scan('tmp/some_table')
    """).show()

# Append some data and read the change data feed, an Arrow record batch reader
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
