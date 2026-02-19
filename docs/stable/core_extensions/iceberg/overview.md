---
github_repository: https://github.com/duckdb/duckdb-iceberg
layout: docu
redirect_from:
- /docs/stable/extensions/iceberg
- /docs/stable/extensions/iceberg/overview
- /docs/extensions/iceberg
title: Iceberg Extension
---

The `iceberg` extension implements support for the [Apache Iceberg open table format](https://iceberg.apache.org/). 
In this page we will go over the basic usage of the extension without the need to attach to an Iceberg catalog. For full support – including write support – see [how to attach Iceberg REST catalogs]({% link docs/stable/core_extensions/iceberg/iceberg_rest_catalogs.md %}).

## Installing and Loading

The `iceberg` extension is installed and loaded automatically on first use.
If you would like to install and load it manually, run:

```sql
INSTALL iceberg;
LOAD iceberg;
```

## Updating the Extension

The `iceberg` extension often receives updates between DuckDB releases.
To make sure that you have the latest version, [update your extensions]({% link docs/stable/sql/statements/update_extensions.md %}):

```sql
UPDATE EXTENSIONS;
```

## Usage

To test the examples, download the [`iceberg_data.zip`]({% link data/iceberg_data.zip %}) file and unzip it.

### Common Parameters

| Parameter                    | Type        | Default                                    | Description                                                |
| ---------------------------- | ----------- | ------------------------------------------ | ---------------------------------------------------------- |
| `allow_moved_paths`          | `BOOLEAN`   | `false`                                    | Allows scanning Iceberg tables that are moved              |
| `metadata_compression_codec` | `VARCHAR`   | `''`                                       | Treats metadata files as when set to `'gzip'`              |
| `snapshot_from_id`           | `UBIGINT`   | `NULL`                                     | Access snapshot with a specific `id`                       |
| `snapshot_from_timestamp`    | `TIMESTAMP` | `NULL`                                     | Access snapshot with a specific `timestamp`                |
| `version`                    | `VARCHAR`   | `'?'`                                      | Provides an explicit version string, hint file or guessing |
| `version_name_format`        | `VARCHAR`   | `'v%s%s.metadata.json,%s%s.metadata.json'` | Controls how versions are converted to metadata file names |

### Querying Individual Tables

```sql
SELECT count(*)
FROM iceberg_scan('data/iceberg/lineitem_iceberg', allow_moved_paths = true);
```

| count_star() |
|-------------:|
| 51793        |

> The `allow_moved_paths` option ensures that some path resolution is performed, 
> which allows scanning Iceberg tables that are moved.

You can also directly specify the current manifest in the query, this may be resolved from the catalog prior to the query, in this example the manifest version is a UUID.
To do so, navigate to the `data/iceberg` directory and run:

```sql
SELECT count(*)
FROM iceberg_scan('lineitem_iceberg/metadata/v1.metadata.json');
```

| count_star() |
|-------------:|
| 60175        |

The `iceberg` extension works together with the [`httpfs` extension]({% link docs/stable/core_extensions/httpfs/overview.md %}) or the [`azure` extension]({% link docs/stable/core_extensions/azure.md %}) to access Iceberg tables in object stores such as S3 or Azure Blob Storage.

```sql
SELECT count(*)
FROM iceberg_scan('s3://bucketname/lineitem_iceberg/metadata/v1.metadata.json');
```

### Access Iceberg Metadata

To access Iceberg Metadata, you can use the `iceberg_metadata` function:

```sql
SELECT *
FROM iceberg_metadata('data/iceberg/lineitem_iceberg', allow_moved_paths = true);
```

<div class="monospace_table"></div>

|                             manifest_path                              | manifest_sequence_number | manifest_content | status  | content  |                                     file_path                                      | file_format | record_count |
|------------------------------------------------------------------------|--------------------------|------------------|---------|----------|------------------------------------------------------------------------------------|-------------|--------------|
| lineitem_iceberg/metadata/10eaca8a-1e1c-421e-ad6d-b232e5ee23d3-m1.avro | 2                        | DATA             | ADDED   | EXISTING | lineitem_iceberg/data/00041-414-f3c73457-bbd6-4b92-9c15-17b241171b16-00001.parquet | PARQUET     | 51793        |
| lineitem_iceberg/metadata/10eaca8a-1e1c-421e-ad6d-b232e5ee23d3-m0.avro | 2                        | DATA             | DELETED | EXISTING | lineitem_iceberg/data/00000-411-0792dcfe-4e25-4ca3-8ada-175286069a47-00001.parquet | PARQUET     | 60175        |

### Visualizing Snapshots

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

### Selecting Metadata Versions

By default, the `iceberg` extension will look for a `version-hint.text` file to identify the proper metadata version to use. This can be overridden by explicitly supplying a version number via the `version` parameter to the functions of the `iceberg` extension:

```sql
SELECT *
FROM iceberg_snapshots(
    'data/iceberg/lineitem_iceberg',
    version = '1'
);
```

By default, `iceberg` functions will look for both `v{version}.metadata.json` and `{version}.metadata.json` files, or `v{version}.gz.metadata.json` and `{version}.gz.metadata.json` when `metadata_compression_codec = 'gzip'` is specified.
Other compression codecs are not supported.

If any text file is provided through the `version` parameter, it is opened and treated as a version hint file:

```sql
SELECT *
FROM iceberg_snapshots(
    'data/iceberg/lineitem_iceberg',
    version = 'version-hint.txt'
);
```

The `iceberg` extension will open this file and use the **entire content** of the file as a provided version number.
Note that the entire content of the `version-hint.txt` file will be treated as a literal version name, with no encoding, escaping or trimming. This includes any whitespace, or unsafe characters  which will be explicitly passed formatted into filenames in the logic described below.

### Working with Alternative Metadata Naming Conventions

The `iceberg` extension can handle different metadata naming conventions by specifying them as a comma-delimited list of format strings via the `version_name_format` parameter. Each format string must contain two `%s` parameters. The first is the location of the version number in the metadata filename and the second is the location of the filename extension specified by the `metadata_compression_codec`. The behavior described above is provided by the default value of `"v%s%s.metadata.gz,%s%smetadata.gz`.
If you had an alternatively named metadata file, e.g., `rev-2.metadata.json.gz`, the table can be read via the follow statement:

```sql
SELECT *
FROM iceberg_snapshots(
    'data/iceberg/alternative_metadata_gz_naming',
    version = '2',
    version_name_format = 'rev-%s.metadata.json%s',
    metadata_compression_codec = 'gzip'
);
```

### “Guessing” Metadata Versions

By default, either a table version number or a `version-hint.text` **must** be provided for the `iceberg` extension to read a table. This is typically provided by an external data catalog. In the event neither is present, the `iceberg` extension can attempt to guess the latest version by passing `?` as the `version` parameter:

```sql
SELECT count(*)
FROM iceberg_scan(
    'data/iceberg/lineitem_iceberg_no_hint',
    version = '?',
    allow_moved_paths = true
);
```

The “latest” version is assumed to be the filename that is lexicographically largest when sorting the filenames. Collations are not considered. This behavior is not enabled by default as it may potentially violate ACID constraints. It can be enabled by setting `unsafe_enable_version_guessing` to `true`. When this is set, `iceberg` functions will attempt to guess the latest version by default before failing.

```sql
SET unsafe_enable_version_guessing = true;
SELECT count(*)
FROM iceberg_scan(
    'data/iceberg/lineitem_iceberg_no_hint',
    allow_moved_paths = true
);
```

## Limitations

* Inserts into v3 Iceberg specification tables.
* Reads from v3 tables with v2 data types.
* Geometry data type.

For a set of unsupported operations when attaching to an Iceberg catalog, see [Unsupported Operations]({% link docs/stable/core_extensions/iceberg/iceberg_rest_catalogs.md %}#unsupported-operations).
