---
github_repository: https://github.com/duckdb/duckdb-iceberg
layout: docu
title: Functions and Settings Reference
---

This page is a reference for all functions and settings provided by the [`iceberg` extension]({% link docs/current/core_extensions/iceberg/overview.md %}). For task-oriented documentation, see the [Overview]({% link docs/current/core_extensions/iceberg/overview.md %}) (reading), [Writing to Iceberg]({% link docs/current/core_extensions/iceberg/writing.md %}), and [Iceberg REST Catalogs]({% link docs/current/core_extensions/iceberg/iceberg_rest_catalogs.md %}) pages.

Functions that take a table accept either a path to a table's metadata (e.g., `'data/iceberg/lineitem_iceberg'`) or, when a [catalog is attached]({% link docs/current/core_extensions/iceberg/iceberg_rest_catalogs.md %}), a fully qualified table name (e.g., `my_catalog.default.my_table`).

## Common Parameters

The read and metadata table functions below accept the following named parameters:

| Parameter                    | Type        | Default                                    | Description                                                |
| ---------------------------- | ----------- | ------------------------------------------ | ---------------------------------------------------------- |
| `allow_moved_paths`          | `BOOLEAN`   | `false`                                    | Allows scanning Iceberg tables that are moved              |
| `metadata_compression_codec` | `VARCHAR`   | `''`                                       | Set to `'gzip'` to read gzip-compressed metadata files     |
| `snapshot_from_id`           | `UBIGINT`   | `NULL`                                     | Access the snapshot with a specific `id`                   |
| `snapshot_from_timestamp`    | `TIMESTAMP` | `NULL`                                     | Access the snapshot as of a specific `timestamp`           |
| `version`                    | `VARCHAR`   | `'?'`                                      | Explicit version string, hint file, or `'?'` for guessing  |
| `version_name_format`        | `VARCHAR`   | `'v%s%s.metadata.json,%s%s.metadata.json'` | Controls how versions are converted to metadata file names |

See [Selecting Metadata Versions]({% link docs/current/core_extensions/iceberg/overview.md %}#selecting-metadata-versions) for details.

## Read and Metadata Functions

| Function | Description |
| --- | --- |
| `iceberg_scan(table, ⟨options⟩)` | Reads the data of an Iceberg table. Returns the table's columns. |
| `iceberg_metadata(table, ⟨options⟩)` | Returns one row per manifest entry. Columns: `manifest_path`, `manifest_sequence_number`, `manifest_content`, `status`, `content`, `file_path`, `file_format`, `record_count`. |
| `iceberg_snapshots(table, ⟨options⟩)` | Returns one row per snapshot. Columns: `sequence_number`, `snapshot_id`, `timestamp_ms`, `manifest_list`. |
| `iceberg_column_stats(table, ⟨options⟩)` | Returns per-data-file, per-column statistics. Columns include `file_path`, `column_name`, `column_type`, `lower_bound`, `upper_bound`, `value_count`, `null_value_count`, `nan_value_count`. |
| `iceberg_partition_stats(table, ⟨options⟩)` | Returns per-partition-field statistics. Columns include `partition_field_name`, `partition_source_columns`, `partition_field_transform`, `lower_bound`, `upper_bound`. |
| `iceberg_load_table_response(table)` | Advanced, REST-catalog only. Returns the raw catalog `LoadTable` response: `metadata_location`, `metadata` (`VARIANT`), `config` (`MAP`), `storage_credentials`, `request_url`. |

```sql
SELECT * FROM iceberg_snapshots('data/iceberg/lineitem_iceberg');
SELECT * FROM iceberg_column_stats('my_catalog.default.events');
```

## Table and Schema Property Functions

These functions read and modify [Iceberg table properties](https://iceberg.apache.org/spec/#table-metadata-fields) and Iceberg schema (namespace) properties. They require an attached catalog. See [Writing to Iceberg]({% link docs/current/core_extensions/iceberg/writing.md %}#table-properties).

| Function | Description |
| --- | --- |
| `iceberg_table_properties(table)` | Returns all properties of the table. |
| `set_iceberg_table_properties(table, properties)` | Sets properties on the table. `properties` is a `MAP(VARCHAR, VARCHAR)`. |
| `remove_iceberg_table_properties(table, property_list)` | Removes the listed properties (`VARCHAR[]`) from the table. |
| `iceberg_schema_properties(schema)` | Returns all properties of the schema (namespace). |
| `set_iceberg_schema_properties(schema, properties)` | Sets properties on the schema. |
| `remove_iceberg_schema_properties(schema, property_list)` | Removes the listed properties from the schema. |

## DuckLake Interoperability

| Function | Description |
| --- | --- |
| `iceberg_to_ducklake(iceberg_catalog, ducklake_catalog, skip_tables := [...])` | Performs a metadata-only copy of an attached Iceberg catalog into a [DuckLake]({% link docs/current/core_extensions/ducklake.md %}) catalog. The optional `skip_tables` parameter (`VARCHAR[]`) excludes tables. |

See [Interoperability with DuckLake]({% link docs/current/core_extensions/iceberg/overview.md %}#interoperability-with-ducklake).

## Partition Transform Functions

These scalar functions implement the [Iceberg partition transforms](https://iceberg.apache.org/spec/#partition-transforms). They are most often used in a `PARTITIONED BY` clause (see [Partitioning]({% link docs/current/core_extensions/iceberg/writing.md %}#partitioning)), but can also be called directly.

| Function | Description |
| --- | --- |
| `iceberg_bucket(num_buckets, value)` | Returns the Iceberg bucket partition value (an `INTEGER`) for `value`. Supported `value` types: `INTEGER`, `BIGINT`, `DECIMAL`, `DATE`, `TIME`, `TIMESTAMP`, `TIMESTAMP WITH TIME ZONE`, `TIMESTAMP_NS`, `VARCHAR`, `BLOB`, `UUID`. |
| `iceberg_truncate(width, value)` | Returns the Iceberg truncate partition value for `value`, with the same type as `value`. Supported types: `INTEGER`, `BIGINT`, `DECIMAL`, `VARCHAR`, `BLOB`. |

```sql
SELECT iceberg_bucket(16, 'duckdb');
SELECT iceberg_truncate(10, 1234);
```

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| `unsafe_enable_version_guessing` | `BOOLEAN` | `false` | Enable globbing the filesystem (if possible) to find the latest metadata version. This may read an uncommitted version, so it is disabled by default. |
| `iceberg_use_metadata_log` | `BOOLEAN` | `true` | Use a table's optional `metadata-log` to preserve atomicity guarantees, at the cost of an additional metadata `GET` in rare cases. |
| `ignore_target_file_size_for_partitioned_tables` | `BOOLEAN` | `false` | Ignore the unsupported `write.target-file-size-bytes` table property on partitioned tables instead of raising an error. |
| `ignore_row_group_size_for_partitioned_tables` | `BOOLEAN` | `false` | Ignore the unsupported `write.parquet.row-group-size-bytes` table property on partitioned tables instead of raising an error. |
| `iceberg_via_aws_sdk_for_catalog_interactions` | `BOOLEAN` | `false` | Use the legacy AWS SDK code path to interact with AWS-based catalogs instead of DuckDB's HTTP client. |
