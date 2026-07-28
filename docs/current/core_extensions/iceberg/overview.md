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

The `iceberg` extension implements support for the [Apache Iceberg open table format](https://iceberg.apache.org/).
This page describes how to install the extension and how to read Iceberg tables straight from storage, without attaching to a catalog.
For full support – including write support – [attach an Iceberg catalog]({% link docs/current/core_extensions/iceberg/catalogs.md %}).

The documentation of the `iceberg` extension is split over the following pages:

* [Writing to Iceberg]({% link docs/current/core_extensions/iceberg/writing_to_iceberg.md %}) describes the supported write operations, partitioning and schema evolution.
* [Iceberg Functions]({% link docs/current/core_extensions/iceberg/iceberg_functions.md %}) documents the functions provided by the extension.
* [Iceberg Options]({% link docs/current/core_extensions/iceberg/iceberg_options.md %}) documents the scan parameters, `ATTACH` options, secret options and settings.
* [Catalogs]({% link docs/current/core_extensions/iceberg/catalogs.md %}) explains how to attach an Iceberg REST Catalog, with instructions for specific catalogs.
* [Troubleshooting]({% link docs/current/core_extensions/iceberg/troubleshooting.md %}) lists common problems and their solutions.

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

## Reading Iceberg Tables

To test the examples, download the [`iceberg_data.zip`]({% link data/iceberg_data.zip %}) file and unzip it.

### Querying Individual Tables

Use the [`iceberg_scan` function]({% link docs/current/core_extensions/iceberg/iceberg_functions.md %}#iceberg_scan) to read an Iceberg table from a path:

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

For the full list of parameters accepted by `iceberg_scan`, see the [Iceberg Options]({% link docs/current/core_extensions/iceberg/iceberg_options.md %}#scan-options) page.

### Reading from Object Stores

The `iceberg` extension works together with the [`httpfs` extension]({% link docs/current/core_extensions/httpfs/overview.md %}) or the [`azure` extension]({% link docs/current/core_extensions/azure.md %}) to access Iceberg tables in object stores such as S3 or Azure Blob Storage.

```sql
SELECT count(*)
FROM iceberg_scan('s3://bucketname/lineitem_iceberg/metadata/v1.metadata.json');
```

## Limitations

* Some v3 types (Geography, timestamptz_ns)

For a set of unsupported operations when attaching to an Iceberg catalog, see [Unsupported Operations]({% link docs/current/core_extensions/iceberg/writing_to_iceberg.md %}#unsupported-operations).
