---
github_repository: https://github.com/duckdb/duckdb-iceberg
layout: docu
redirect_from:
- /docs/extensions/iceberg
- /docs/stable/extensions/iceberg
- /docs/stable/extensions/iceberg/overview
- /docs/preview/core_extensions/iceberg/overview
- /docs/stable/core_extensions/iceberg/overview
title: Iceberg Extension
---

The `iceberg` extension implements support for the [Apache Iceberg open table format](https://iceberg.apache.org/). There are two ways to work with Iceberg in DuckDB:

* **[Individual tables](#individual-tables)** are read directly from storage, by pointing at a table's metadata. This requires no catalog and is read-only.
* **[Catalog-managed tables](#catalog-managed-tables)** are accessed by attaching an Iceberg REST catalog. This unlocks the full feature set, including writing.

This page covers the basics of both. See also:

* [Iceberg REST Catalogs]({% link docs/current/core_extensions/iceberg/iceberg_rest_catalogs.md %}) – connecting to specific catalogs (Amazon S3 Tables, AWS Glue, Cloudflare R2, Polaris, Lakekeeper, BigLake).
* [Writing to Iceberg]({% link docs/current/core_extensions/iceberg/writing.md %}) – create tables, insert, update, delete, merge, and evolve schemas.
* [Functions and Settings Reference]({% link docs/current/core_extensions/iceberg/reference.md %}) – all table functions, scalar functions, and settings.

## Installing and Loading

The `iceberg` extension is installed and loaded automatically on first use.
If you would like to install and load it manually, run:

```sql
INSTALL iceberg;
LOAD iceberg;
```

## Updating the Extension

The `iceberg` extension often receives updates between DuckDB releases.
To make sure that you have the latest version, [update your extensions]({% link docs/current/sql/statements/update_extensions.md %}):

```sql
UPDATE EXTENSIONS;
```

## Individual Tables

Individual Iceberg tables can be read directly from storage with the `iceberg_scan` function, without attaching to a catalog. To test the examples, download the [`iceberg_data.zip`]({% link data/iceberg_data.zip %}) file and unzip it.

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

The `iceberg` extension works together with the [`httpfs` extension]({% link docs/current/core_extensions/httpfs/overview.md %}) or the [`azure` extension]({% link docs/current/core_extensions/azure.md %}) to access Iceberg tables in object stores such as S3 or Azure Blob Storage.

```sql
SELECT count(*)
FROM iceberg_scan('s3://bucketname/lineitem_iceberg/metadata/v1.metadata.json');
```

### Accessing Iceberg Metadata

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

### Time Travel

To read a historical snapshot of a table, pass either `snapshot_from_id` or `snapshot_from_timestamp` (the two are mutually exclusive). Use [`iceberg_snapshots`](#visualizing-snapshots) to list the available snapshots:

```sql
-- Read a specific snapshot by id
SELECT count(*)
FROM iceberg_scan('data/iceberg/lineitem_iceberg', snapshot_from_id = 7635660646343998149);

-- Read the snapshot that was current at a given time
SELECT count(*)
FROM iceberg_scan('data/iceberg/lineitem_iceberg', snapshot_from_timestamp = TIMESTAMP '2023-02-15 15:08:00');
```

### Limitations of Direct Reads

* A version hint or explicit `version` is required to read a table, unless [version guessing](#guessing-metadata-versions) is enabled.
* Only `gzip`-compressed metadata is supported (via `metadata_compression_codec = 'gzip'`).

## Catalog Managed Tables

For full read and write access — and to use Iceberg's catalog features — attach an Iceberg REST catalog. Most catalogs authenticate with OAuth2; store the credentials in a [secret]({% link docs/current/configuration/secrets_manager.md %}) and attach the catalog with `ATTACH ... (TYPE iceberg, ...)`:

```sql
CREATE SECRET iceberg_secret (
    TYPE iceberg,
    CLIENT_ID '⟨admin⟩',
    CLIENT_SECRET '⟨password⟩',
    OAUTH2_SERVER_URI '⟨https://catalog.example.com/v1/oauth/tokens⟩'
);

ATTACH '⟨warehouse⟩' AS my_catalog (
    TYPE iceberg,
    SECRET iceberg_secret,
    ENDPOINT '⟨https://catalog.example.com⟩'
);
```

Once attached, the catalog behaves like any other DuckDB database: reference its tables as `⟨catalog⟩.⟨schema⟩.⟨table⟩` and query or modify them with regular SQL.

```sql
SHOW ALL TABLES;

SELECT count(*) FROM my_catalog.default.events;

INSERT INTO my_catalog.default.events VALUES (1, 'click', now());
```

The [metadata functions]({% link docs/current/core_extensions/iceberg/reference.md %}#read-and-metadata-functions) also work on catalog tables when passed a fully qualified name, e.g., `iceberg_snapshots(my_catalog.default.events)`.

* For the full set of write operations — partitioning, `UPDATE`, `DELETE`, `MERGE INTO`, `ALTER TABLE`, and table properties — see [Writing to Iceberg]({% link docs/current/core_extensions/iceberg/writing.md %}).
* For catalog-specific setup and the complete list of `ATTACH` options and secret parameters, see [Iceberg REST Catalogs]({% link docs/current/core_extensions/iceberg/iceberg_rest_catalogs.md %}).

### Time Travel

On an attached catalog, time travel with the `AT` clause directly on the table:

```sql
-- Using a snapshot id
SELECT * FROM my_catalog.default.events AT (VERSION => ⟨snapshot_id⟩);

-- Using a timestamp
SELECT * FROM my_catalog.default.events AT (TIMESTAMP => TIMESTAMP '2025-09-22 12:32:43.217');
```

## Interoperability with DuckLake

The `iceberg_to_ducklake` function performs a metadata-only copy of an attached Iceberg catalog into a [DuckLake]({% link docs/current/core_extensions/ducklake.md %}) catalog, letting you query Iceberg tables as if they were DuckLake tables:

```sql
-- With an Iceberg catalog attached as my_catalog
ATTACH 'ducklake:my_ducklake.ducklake' AS my_ducklake;
CALL iceberg_to_ducklake('my_catalog', 'my_ducklake');

-- Skip specific tables
CALL iceberg_to_ducklake('my_catalog', 'my_ducklake', skip_tables := ['table_to_skip']);
```
