---
github_repository: https://github.com/duckdb/duckdb-iceberg
layout: docu
redirect_from:
- /docs/extensions/iceberg
- /docs/stable/extensions/iceberg
- /docs/stable/extensions/iceberg/overview
- /docs/stable/core_extensions/iceberg/overview
- /docs/current/core_extensions/iceberg/overview
- /docs/lts/core_extensions/iceberg/overview
- /docs/preview/core_extensions/iceberg/overview
title: Iceberg Extension
---

The `iceberg` extension implements support for the [Apache Iceberg open table format](https://iceberg.apache.org/). There are two ways to work with Iceberg in DuckDB:

* **[Individual tables](#querying-individual-tables)** are read directly from storage, by pointing at a table's metadata. This requires no catalog and is read-only.
* **[Catalog-managed tables](#catalog-managed-tables)** are accessed by attaching an Iceberg REST catalog. This unlocks the full feature set, including writing.

This page covers the basics of both. See also:

* [Writing to Iceberg]({% link docs/2.0/core_extensions/iceberg/writing_to_iceberg.md %}) describes the supported write operations, partitioning, and schema evolution.
* [Iceberg Functions]({% link docs/2.0/core_extensions/iceberg/iceberg_functions.md %}) documents the functions provided by the extension.
* [Iceberg Options]({% link docs/2.0/core_extensions/iceberg/iceberg_options.md %}) documents the scan parameters, `ATTACH` options, secret options, and settings.
* [Catalogs]({% link docs/2.0/core_extensions/iceberg/catalogs.md %}) explains how to attach an Iceberg REST Catalog, with instructions for specific catalogs.
* [Troubleshooting]({% link docs/2.0/core_extensions/iceberg/troubleshooting.md %}) lists common problems and their solutions.

## Installing and Loading

The `iceberg` extension is installed and loaded automatically on first use.
If you would like to install and load it manually, run:

```sql
INSTALL AND LOAD iceberg;
```

## Updating the Extension

The `iceberg` extension often receives updates between DuckDB releases.
To make sure that you have the latest version, [update your extensions]({% link docs/2.0/sql/statements/update_extensions.md %}):

```sql
UPDATE EXTENSIONS;
```

## Reading Iceberg Tables

Individual Iceberg tables can be read directly from storage with the `iceberg_scan` function, without attaching to a catalog. To test the examples, download the [`iceberg_data.zip`]({% link data/iceberg_data.zip %}) file and unzip it.

### Querying Individual Tables

Use the [`iceberg_scan` function]({% link docs/2.0/core_extensions/iceberg/iceberg_functions.md %}#iceberg_scan) to read an Iceberg table from a path:

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

For the full list of parameters accepted by `iceberg_scan`, see the [Iceberg Options]({% link docs/2.0/core_extensions/iceberg/iceberg_options.md %}#scan-options) page.

### Reading from Object Stores

The `iceberg` extension works together with the [`httpfs` extension]({% link docs/2.0/core_extensions/httpfs/overview.md %}) or the [`azure` extension]({% link docs/2.0/core_extensions/azure.md %}) to access Iceberg tables in object stores such as S3 or Azure Blob Storage.

```sql
SELECT count(*)
FROM iceberg_scan('s3://bucketname/lineitem_iceberg/metadata/v1.metadata.json');
```

### Metadata and Snapshots

To inspect the manifest entries and snapshots of a table, use the [`iceberg_metadata`]({% link docs/2.0/core_extensions/iceberg/iceberg_functions.md %}#iceberg_metadata) and [`iceberg_snapshots`]({% link docs/2.0/core_extensions/iceberg/iceberg_functions.md %}#iceberg_snapshots) functions.
To read tables without a `version-hint.text` file or with non-standard metadata file names, see [Selecting Metadata Versions]({% link docs/2.0/core_extensions/iceberg/iceberg_options.md %}#selecting-metadata-versions).

### Time Travel

To read a historical snapshot of a table, pass either `snapshot_from_id` or `snapshot_from_timestamp` (the two are mutually exclusive). Use [`iceberg_snapshots`]({% link docs/2.0/core_extensions/iceberg/iceberg_functions.md %}#iceberg_snapshots) to list the available snapshots:

```sql
-- Read a specific snapshot by id
SELECT count(*)
FROM iceberg_scan('data/iceberg/lineitem_iceberg', allow_moved_paths = true, snapshot_from_id = 7635660646343998149);

-- Read the snapshot that was current at a given time
SELECT count(*)
FROM iceberg_scan('data/iceberg/lineitem_iceberg', allow_moved_paths = true, snapshot_from_timestamp = TIMESTAMP '2023-02-15 15:08:00');
```

### Limitations of Direct Reads

* A version hint or explicit `version` is required to read a table, unless [version guessing]({% link docs/2.0/core_extensions/iceberg/iceberg_options.md %}#guessing-metadata-versions) is enabled.
* Only `gzip`-compressed metadata is supported (via `metadata_compression_codec = 'gzip'`).

## Catalog Managed Tables

For full read and write access — and to use Iceberg's catalog features — attach an Iceberg REST catalog. Most catalogs authenticate with OAuth2; store the credentials in a [secret]({% link docs/2.0/configuration/secrets_manager.md %}) and attach the catalog with `ATTACH ... (TYPE iceberg, ...)`:

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
    URI '⟨https://catalog.example.com⟩'
);
```

Once attached, the catalog behaves like any other DuckDB database: reference its tables as `⟨catalog⟩.⟨schema⟩.⟨table⟩` and query or modify them with regular SQL.

```sql
SHOW ALL TABLES;

SELECT count(*) FROM my_catalog.default.events;

INSERT INTO my_catalog.default.events VALUES (1, 'click', now());
```

The [metadata functions]({% link docs/2.0/core_extensions/iceberg/iceberg_functions.md %}#metadata-operations-on-attached-catalogs) also work on catalog tables when passed a fully qualified name, e.g., `iceberg_snapshots(my_catalog.default.events)`.

* For the full set of write operations — partitioning, `UPDATE`, `DELETE`, `MERGE INTO`, `ALTER TABLE`, and table properties — see [Writing to Iceberg]({% link docs/2.0/core_extensions/iceberg/writing_to_iceberg.md %}).
* For catalog-specific setup, see [Catalogs]({% link docs/2.0/core_extensions/iceberg/catalogs.md %}). For the complete list of `ATTACH` options and secret parameters, see [Iceberg Options]({% link docs/2.0/core_extensions/iceberg/iceberg_options.md %}#attach-options).

### Time Travel

On an attached catalog, time travel with the `AT` clause directly on the table:

```sql
-- Using a snapshot id
SELECT * FROM my_catalog.default.events AT (VERSION => ⟨snapshot_id⟩);

-- Using a timestamp
SELECT * FROM my_catalog.default.events AT (TIMESTAMP => TIMESTAMP '2025-09-22 12:32:43.217');
```

## Interoperability with DuckLake

The [`iceberg_to_ducklake` function]({% link docs/2.0/core_extensions/iceberg/iceberg_functions.md %}#iceberg_to_ducklake) performs a metadata-only copy of an attached Iceberg catalog into a [DuckLake]({% link docs/2.0/core_extensions/ducklake.md %}) catalog, letting you query Iceberg tables as if they were DuckLake tables.
