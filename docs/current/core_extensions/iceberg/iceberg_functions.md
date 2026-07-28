---
layout: docu
title: Iceberg Functions
---

The `iceberg` extension provides the following functions:

| Function                                                  | Description                                                          |
| --------------------------------------------------------- | -------------------------------------------------------------------- |
| `iceberg_scan(source)`                                    | Reads an Iceberg table from a path.                                  |
| `iceberg_metadata(source)`                                | Returns the manifest entries of an Iceberg table.                    |
| `iceberg_snapshots(source)`                               | Returns the snapshots of an Iceberg table.                           |
| `iceberg_table_properties(table)`                         | Returns all properties of the specified table.                       |
| `set_iceberg_table_properties(table, properties)`         | Sets properties on the specified table.                              |
| `remove_iceberg_table_properties(table, property_list)`   | Removes properties from the specified table.                         |
| `iceberg_schema_properties(schema)`                       | Returns all properties of the specified schema.                      |
| `set_iceberg_schema_properties(schema, properties)`       | Sets properties on the specified schema.                             |
| `remove_iceberg_schema_properties(schema, property_list)` | Removes properties from the specified schema.                        |
| `iceberg_to_ducklake(iceberg_catalog, ducklake_catalog)`  | Copies the Iceberg metadata of a catalog to a DuckLake catalog.      |

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

The path can also point directly to a metadata file, or to an object store such as S3 or Azure Blob Storage. See the [Iceberg Options]({% link docs/current/core_extensions/iceberg/iceberg_options.md %}#scan-options) page for the parameters accepted by this function.

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

## Metadata Operations on Attached Catalogs

The functions `iceberg_metadata` and `iceberg_snapshots` are also available to use with an [attached Iceberg catalog]({% link docs/current/core_extensions/iceberg/catalogs.md %}) using a fully qualified path, e.g.:

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
 
You can use `ALTER TABLE ... SET` and `ALTER TABLE ... RESET` to modify table properties
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

## `iceberg_to_ducklake`

The DuckDB `iceberg` extension exposes a function to do metadata only copies of the Iceberg metadata to [DuckLake]({% link docs/current/core_extensions/ducklake.md %}), which enables users to query Iceberg tables as if they were DuckLake tables.

```sql
-- Given that we have an Iceberg catalog attached aliased to iceberg_datalake
ATTACH 'ducklake:my_ducklake.ducklake' AS my_ducklake;

CALL iceberg_to_ducklake('iceberg_datalake', 'my_ducklake');
```

It is also possible to skip a set of tables provided the `skip_tables` parameter.

```sql
CALL iceberg_to_ducklake('iceberg_datalake', 'my_ducklake', skip_tables := ['table_to_skip']);
```
