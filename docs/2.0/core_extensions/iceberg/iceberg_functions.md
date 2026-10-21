---
layout: docu
redirect_from:
- /docs/preview/core_extensions/iceberg/reference
- /docs/current/core_extensions/iceberg/reference
- /docs/current/core_extensions/iceberg/iceberg_functions
- /docs/lts/core_extensions/iceberg/iceberg_functions
- /docs/preview/core_extensions/iceberg/iceberg_functions
title: Iceberg Functions
---

The `iceberg` extension provides the following functions:

| Function                                                  | Description                                                          |
| --------------------------------------------------------- | -------------------------------------------------------------------- |
| `iceberg_scan(source)`                                    | Reads an Iceberg table from a path.                                  |
| `iceberg_metadata(source)`                                | Returns the manifest entries of an Iceberg table.                    |
| `iceberg_snapshots(source)`                               | Returns the snapshots of an Iceberg table.                           |
| `iceberg_column_stats(source)`                            | Returns per-data-file, per-column statistics of an Iceberg table.    |
| `iceberg_partition_stats(source)`                         | Returns per-partition-field statistics of an Iceberg table.          |
| `iceberg_load_table_response(table)`                      | Returns the raw `LoadTable` response of the REST Catalog.            |
| `iceberg_files(source)`                                   | Returns the data and delete files of an Iceberg table snapshot.      |
| `iceberg_manifests(source)`                               | Returns the manifest files of an Iceberg table snapshot.             |
| `iceberg_history(source)`                                 | Returns the history of the table's current snapshot.                 |
| `iceberg_refs(source)`                                    | Returns the branches and tags of an Iceberg table.                   |
| `iceberg_partition_specs(source)`                         | Returns the partition specs of an Iceberg table.                     |
| `iceberg_scan_plan(table)`                                | Returns the scan tasks (files to read) planned for an Iceberg table. |
| `iceberg_view_metadata(view)`                             | Returns the raw `LoadView` response of the REST Catalog.             |
| `iceberg_table_properties(table)`                         | Returns all properties of the specified table.                       |
| `set_iceberg_table_properties(table, properties)`         | Sets properties on the specified table.                              |
| `remove_iceberg_table_properties(table, property_names)`  | Removes properties from the specified table.                         |
| `iceberg_schema_properties(schema)`                       | Returns all properties of the specified schema.                      |
| `set_iceberg_schema_properties(schema, properties)`       | Sets properties on the specified schema.                             |
| `remove_iceberg_schema_properties(schema, property_list)` | Removes properties from the specified schema.                        |
| `iceberg_rollback_to_snapshot(table, snapshot_id)`        | Rolls back an Iceberg table to an earlier snapshot.                  |
| `iceberg_rewrite_data_files(table)`                       | Compacts the data files of an Iceberg table.                         |
| `iceberg_to_ducklake(iceberg_catalog, ducklake_catalog)`  | Copies the Iceberg metadata of a catalog to a DuckLake catalog.      |
| `iceberg_bucket(num_buckets, value)`                      | Computes the Iceberg `bucket` partition transform of a value.        |
| `iceberg_truncate(width, value)`                          | Computes the Iceberg `truncate` partition transform of a value.      |

The examples on this page use the [`iceberg_data.zip`]({% link data/iceberg_data.zip %}) file; download and unzip it to run them.

## `iceberg_scan`

The `iceberg_scan` function reads an Iceberg table from a path, without requiring an attached catalog:

```sql
SELECT count(*)
FROM iceberg_scan('data/iceberg/lineitem_iceberg', allow_moved_paths = true);
```

| count_star() |
|-------------:|
| 51793        |

The path can also point directly to a metadata file, or to an object store such as S3 or Azure Blob Storage. See the [Iceberg Options]({% link docs/2.0/core_extensions/iceberg/iceberg_options.md %}#scan-options) page for the parameters accepted by this function.

## `iceberg_metadata`

To access Iceberg metadata, you can use the `iceberg_metadata` function:

```sql
SELECT *
FROM iceberg_metadata('data/iceberg/lineitem_iceberg', allow_moved_paths = true);
```

<div class="monospace_table"></div>

|                             manifest_path                              | manifest_sequence_number | manifest_content | status  | content  |                                     file_path                                      | file_format | record_count |
|------------------------------------------------------------------------|--------------------------|------------------|---------|----------|------------------------------------------------------------------------------------|-------------|--------------|
| lineitem_iceberg/metadata/10eaca8a-1e1c-421e-ad6d-b232e5ee23d3-m1.avro | 2                        | DATA             | ADDED   | EXISTING | lineitem_iceberg/data/00041-414-f3c73457-bbd6-4b92-9c15-17b241171b16-00001.parquet | PARQUET     | 51793        |
| lineitem_iceberg/metadata/10eaca8a-1e1c-421e-ad6d-b232e5ee23d3-m0.avro | 2                        | DATA             | DELETED | EXISTING | lineitem_iceberg/data/00000-411-0792dcfe-4e25-4ca3-8ada-175286069a47-00001.parquet | PARQUET     | 60175        |

## `iceberg_snapshots`

To visualize the snapshots in an Iceberg table, use the `iceberg_snapshots` function:

```sql
SELECT *
FROM iceberg_snapshots('data/iceberg/lineitem_iceberg');
```

<div class="monospace_table"></div>

| sequence_number |     snapshot_id     |      timestamp_ms       |                                         manifest_list                                          |
|-----------------|---------------------|-------------------------|------------------------------------------------------------------------------------------------|
| 1               | 3776207205136740581 | 2023-02-15 15:07:54.504 | lineitem_iceberg/metadata/snap-3776207205136740581-1-cf3d0be5-cf70-453d-ad8f-48fdc412e608.avro |
| 2               | 7635660646343998149 | 2023-02-15 15:08:14.73  | lineitem_iceberg/metadata/snap-7635660646343998149-1-10eaca8a-1e1c-421e-ad6d-b232e5ee23d3.avro |

> `iceberg_snapshots` does not take `allow_moved_paths`, `snapshot_from_id` or `snapshot_from_timestamp` as parameters.

## `iceberg_column_stats`

The `iceberg_column_stats` function returns the statistics stored in the manifests for every data file and column.
Its columns include `file_path`, `column_name`, `column_type`, `lower_bound`, `upper_bound`, `value_count`, `null_value_count` and `nan_value_count`.

```sql
SELECT *
FROM iceberg_column_stats('data/iceberg/lineitem_iceberg', allow_moved_paths = true);
```

## `iceberg_partition_stats`

The `iceberg_partition_stats` function returns statistics per partition field.
Its columns include `partition_field_name`, `partition_source_columns`, `partition_field_transform`, `lower_bound` and `upper_bound`.

```sql
SELECT *
FROM iceberg_partition_stats(my_datalake.default.t);
```

## `iceberg_load_table_response`

The `iceberg_load_table_response` function is an advanced function that only works with an [attached Iceberg REST Catalog]({% link docs/2.0/core_extensions/iceberg/catalogs.md %}).
It returns the raw `LoadTable` response of the catalog with the columns `metadata_location`, `metadata` (`VARIANT`), `config` (`MAP`), `storage_credentials` and `request_url`.

```sql
SELECT *
FROM iceberg_load_table_response(my_datalake.default.t);
```

## Metadata Operations on Attached Catalogs

The functions `iceberg_metadata` and `iceberg_snapshots` are also available to use with an [attached Iceberg catalog]({% link docs/2.0/core_extensions/iceberg/catalogs.md %}) using a fully qualified path, e.g.:

```sql
SELECT * FROM iceberg_metadata(my_datalake.default.t)

-- Or
SELECT * FROM iceberg_snapshots(my_datalake.default.t)
```

This functionality enables the user to do **time traveling**.

```sql
-- Using a snapshot id
SELECT * FROM my_datalake.default.t AT (VERSION => ⟨SNAPSHOT_ID⟩)

-- Or using a timestamp
SELECT * FROM my_datalake.default.t AT (TIMESTAMP => TIMESTAMP '2025-09-22 12:32:43.217')
```

## Table Properties Functions

DuckDB provides functions to view and modify [Iceberg table properties](https://iceberg.apache.org/spec/#table-metadata-fields):

| Function                                                | Description                                    |
| ------------------------------------------------------- | ---------------------------------------------- |
| `iceberg_table_properties(table)`                       | Returns all properties of the specified table. |
| `set_iceberg_table_properties(table, properties)`       | Sets properties on the specified table.        |
| `remove_iceberg_table_properties(table, property_names)` | Removes properties from the specified table.   |

You can also use `ALTER TABLE ... SET` and `ALTER TABLE ... RESET` to modify table properties:

```sql
-- View table properties
SELECT *
FROM iceberg_table_properties(iceberg_catalog.default.my_table);

-- Set table properties
ALTER TABLE iceberg_catalog.default.my_table SET (
    'write.update.mode'='merge-on-read', 
    'write.delete.mode'='merge-on-read',
    'format-version'=3
);

-- Remove table properties
ALTER TABLE iceberg_catalog.default.my_table RESET (
    'write.update.mode',
    'owner'
);
```

The `set_iceberg_table_properties` and `remove_iceberg_table_properties` functions take the table name as a string and cannot change reserved Iceberg table properties. In particular, `format-version` can only be changed with `ALTER TABLE ... SET`.

```sql
CALL set_iceberg_table_properties('iceberg_catalog.default.my_table', {
    'write.update.mode': 'merge-on-read'
});

CALL remove_iceberg_table_properties(
    'iceberg_catalog.default.my_table',
    ['write.update.mode']
);
```

## Schema Properties Functions

Iceberg catalogs allow arbitrary key-value [properties](https://iceberg.apache.org/spec/#namespaces) to be attached at the schema (namespace) level. These properties are typically used to record ownership, descriptions, default storage locations, or any other metadata that applies to every table in a schema.

| Function                                                  | Description                                            |
| --------------------------------------------------------- | ------------------------------------------------------ |
| `iceberg_schema_properties(schema)`                       | Returns all properties of the specified schema.        |
| `set_iceberg_schema_properties(schema, properties)`       | Sets properties on the specified schema.               |
| `remove_iceberg_schema_properties(schema, property_list)` | Removes properties from the specified schema.          |

```sql
-- Set schema properties
CALL set_iceberg_schema_properties(iceberg_catalog.default, {
    'owner': 'analytics-team',
    'description': 'Default analytics schema'
});

-- Read schema properties
SELECT * FROM iceberg_schema_properties(iceberg_catalog.default);

-- Remove schema properties
CALL remove_iceberg_schema_properties(
    iceberg_catalog.default,
    ['description']
);
```

Schema properties are written through the Iceberg REST Catalog, so any other Iceberg-aware engine attached to the same catalog will see the updates immediately. `remove_iceberg_schema_properties` returns the number of remaining schema properties.

## Metadata Table Functions

The following functions expose the [Iceberg metadata tables](https://iceberg.apache.org/docs/latest/spark-queries/#inspecting-tables). Like `iceberg_metadata` and `iceberg_snapshots`, they accept either a table path (along with the [scan options]({% link docs/2.0/core_extensions/iceberg/iceberg_options.md %}#scan-options) `metadata_compression_codec`, `version` and `version_name_format`) or a table in an attached catalog.

| Function | Additional parameters | Description |
| --- | --- | --- |
| `iceberg_files(source)` | `allow_moved_paths`, `snapshot_from_id`, `snapshot_from_timestamp` | Returns one row per data file and delete file of the snapshot, including the file path, format, partition, record count, file size and column-level statistics (`column_sizes`, `value_counts`, `null_value_counts`, `lower_bounds`, `upper_bounds`, `readable_metrics`, etc.). |
| `iceberg_manifests(source)` | `allow_moved_paths`, `snapshot_from_id`, `snapshot_from_timestamp` | Returns one row per manifest file of the snapshot, with the manifest path and length, partition spec ID, the snapshot that added it, counts of added/existing/deleted data and delete files, and partition summaries. |
| `iceberg_history(source)` | | Returns the snapshot log of the table with the columns `made_current_at`, `snapshot_id`, `parent_id` and `is_current_ancestor`. |
| `iceberg_refs(source)` | | Returns the branches and tags of the table with the columns `name`, `type`, `snapshot_id`, `max_reference_age_in_ms`, `min_snapshots_to_keep` and `max_snapshot_age_in_ms`. |
| `iceberg_partition_specs(source)` | | Returns one row per partition field of each partition spec with the columns `spec_id`, `is_default`, `field_id`, `name`, `transform`, `source_id` and `source_column`. |

```sql
SELECT file_path, record_count, file_size_in_bytes
FROM iceberg_files(my_datalake.default.t);

SELECT *
FROM iceberg_partition_specs(my_datalake.default.t);
```

## `iceberg_scan_plan`

The `iceberg_scan_plan(table)` function is an advanced function that returns the scan tasks DuckDB would read for a table, i.e., one row per data file together with its partition values and the delete files that apply to it. The `table` argument is the fully qualified name of a table in an attached Iceberg REST Catalog as a string (e.g., `'my_datalake.default.t'`), or a table location. It accepts the following named parameters:

| Parameter | Type | Description |
| --- | --- | --- |
| `row_filter` | `VARCHAR` | A filter expression used to prune the files to scan. |
| `produce_sequence_number` | `BOOLEAN` | Include the data sequence number of each file in the output. |
| `snapshot_from_id` | `UBIGINT` | Plan the scan for the snapshot with the given ID. |
| `snapshot_from_timestamp` | `TIMESTAMP_MS` | Plan the scan for the snapshot that was current at the given timestamp. |
| `allow_moved_paths`, `metadata_compression_codec`, `version`, `version_name_format` | | The [scan options]({% link docs/2.0/core_extensions/iceberg/iceberg_options.md %}#scan-options), for tables given by their location. |

If the [`iceberg_use_server_side_scan_planning` setting]({% link docs/2.0/core_extensions/iceberg/iceberg_options.md %}#settings) is enabled and the catalog supports it, the planning is performed by the REST Catalog.

## `iceberg_view_metadata`

The `iceberg_view_metadata(view)` function is the counterpart of [`iceberg_load_table_response`](#iceberg_load_table_response) for views: it returns the raw `LoadView` response of an [attached Iceberg REST Catalog]({% link docs/2.0/core_extensions/iceberg/catalogs.md %}) with the columns `metadata_location`, `metadata` (`VARIANT`), `config` (`MAP`) and `request_url`. This is useful for inspecting views, including views defined in a SQL dialect DuckDB cannot parse.

```sql
SELECT *
FROM iceberg_view_metadata('my_datalake.default.my_view');
```

## Table Maintenance Functions

### `iceberg_rollback_to_snapshot`

The `iceberg_rollback_to_snapshot(table, snapshot_id)` function sets the current snapshot of a table in an attached Iceberg catalog to an earlier snapshot. The table name is passed as a string and the snapshot ID can be taken from [`iceberg_snapshots`](#iceberg_snapshots). The function returns the `previous_snapshot_id` and the new `current_snapshot_id`.

```sql
CALL iceberg_rollback_to_snapshot('my_datalake.default.t', ⟨snapshot_id⟩);
```

### `iceberg_rewrite_data_files`

The `iceberg_rewrite_data_files(table)` function compacts the data files of a table in an attached Iceberg catalog: it rewrites small (and overly large) data files into files close to the target file size, applying any pending position and equality deletes. It returns the columns `rewritten_data_files_count`, `added_data_files_count`, `rewritten_bytes_count`, `failed_data_files_count` and `removed_delete_files_count`.

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `target_file_size_bytes` | `VARCHAR` or integer | The table's `write.target-file-size-bytes` property, or 512 MiB | The target size of the rewritten files. |
| `min_file_size_bytes` | `VARCHAR` or integer | 75% of the target file size | Files smaller than this are candidates for rewriting. |
| `max_file_size_bytes` | `VARCHAR` or integer | 180% of the target file size | Files larger than this are candidates for rewriting. |
| `min_input_files` | `BIGINT` | `5` | The minimum number of candidate files (per partition) required to perform a rewrite. |
| `max_files_to_rewrite` | `BIGINT` | `NULL` (no limit) | The maximum number of files to rewrite. |
| `rewrite_all` | `BOOLEAN` | `false` | Rewrite all data files regardless of their size. |
| `output_spec_id` | `INTEGER` | The table's default partition spec | The partition spec to rewrite the files into. |

```sql
CALL iceberg_rewrite_data_files('my_datalake.default.t', min_input_files => 2);
```

## `iceberg_to_ducklake`

The DuckDB `iceberg` extension exposes a function to do metadata only copies of the Iceberg metadata to [DuckLake]({% link docs/2.0/core_extensions/ducklake.md %}), which enables users to query Iceberg tables as if they were DuckLake tables.

```sql
-- Given that we have an Iceberg catalog attached aliased to iceberg_datalake
ATTACH 'ducklake:my_ducklake.ducklake' AS my_ducklake;

CALL iceberg_to_ducklake('iceberg_datalake', 'my_ducklake');
```

It is also possible to skip a set of tables provided the `skip_tables` parameter.

```sql
CALL iceberg_to_ducklake('iceberg_datalake', 'my_ducklake', skip_tables := ['table_to_skip']);
```

## Partition Transform Functions

The `iceberg_bucket` and `iceberg_truncate` scalar functions implement the [Iceberg partition transforms](https://iceberg.apache.org/spec/#partition-transforms) of the same name.
They are most often used implicitly through the `PARTITIONED BY` clause (see [Partitioning]({% link docs/2.0/core_extensions/iceberg/writing_to_iceberg.md %}#partitioning)), but they can also be called directly:

| Function | Description |
| --- | --- |
| `iceberg_bucket(num_buckets, value)` | Returns the Iceberg bucket partition value (an `INTEGER`) for `value`. Supported `value` types: `INTEGER`, `BIGINT`, `DECIMAL`, `DATE`, `TIME`, `TIMESTAMP`, `TIMESTAMP WITH TIME ZONE`, `TIMESTAMP_NS`, `VARCHAR`, `BLOB`, `UUID`. |
| `iceberg_truncate(width, value)` | Returns the Iceberg truncate partition value for `value`, with the same type as `value`. Supported `value` types: `INTEGER`, `BIGINT`, `DECIMAL`, `VARCHAR`, `BLOB`. |

```sql
SELECT iceberg_bucket(16, 'duckdb');
SELECT iceberg_truncate(10, 1234);
```
