---
github_repository: https://github.com/duckdb/duckdb_iceberg
layout: docu
title: Iceberg Extension
---

The `iceberg` extension is a loadable extension that implements support for the [Apache Iceberg format](https://iceberg.apache.org/).

## Installing and Loading

To install and load the `iceberg` extension, run:

```sql
INSTALL iceberg;
LOAD iceberg;
```

## Usage

To test the examples, download the [`iceberg_data.zip`](/data/iceberg_data.zip) file and unzip it.

### Querying Individual Tables

```sql
SELECT count(*)
FROM iceberg_scan('data/iceberg/lineitem_iceberg', allow_moved_paths = true);
```

| count_star() |
|--------------|
| 51793        |

> The `allow_moved_paths` option ensures that some path resolution is performed, which allows scanning Iceberg tables that are moved.

You can also address specify the current manifest directly in the query, this may be resolved from the catalog prior to the query, in this example the manifest version is a UUID.

```sql
SELECT count(*)
FROM iceberg_scan('data/iceberg/lineitem_iceberg/metadata/02701-1e474dc7-4723-4f8d-a8b3-b5f0454eb7ce.metadata.json');
```

This extension can be paired with the [`httpfs` extension](/docs/extensions/httpfs) to access Iceberg tables in object stores such as S3.

```sql
SELECT count(*)
FROM iceberg_scan('s3://bucketname/lineitem_iceberg/metadata/02701-1e474dc7-4723-4f8d-a8b3-b5f0454eb7ce.metadata.json', allow_moved_paths = true);
```

### Access Iceberg Metadata

```sql
SELECT *
FROM iceberg_metadata('data/iceberg/lineitem_iceberg', allow_moved_paths = true);
```

|                             manifest_path                              | manifest_sequence_number | manifest_content | status  | content  |                                     file_path                                      | file_format | record_count |
|------------------------------------------------------------------------|--------------------------|------------------|---------|----------|------------------------------------------------------------------------------------|-------------|--------------|
| lineitem_iceberg/metadata/10eaca8a-1e1c-421e-ad6d-b232e5ee23d3-m1.avro | 2                        | DATA             | ADDED   | EXISTING | lineitem_iceberg/data/00041-414-f3c73457-bbd6-4b92-9c15-17b241171b16-00001.parquet | PARQUET     | 51793        |
| lineitem_iceberg/metadata/10eaca8a-1e1c-421e-ad6d-b232e5ee23d3-m0.avro | 2                        | DATA             | DELETED | EXISTING | lineitem_iceberg/data/00000-411-0792dcfe-4e25-4ca3-8ada-175286069a47-00001.parquet | PARQUET     | 60175        |

### Visualizing Snapshots

```sql
SELECT *
FROM iceberg_snapshots('data/iceberg/lineitem_iceberg');
```

| sequence_number |     snapshot_id     |      timestamp_ms       |                                         manifest_list                                          |
|-----------------|---------------------|-------------------------|------------------------------------------------------------------------------------------------|
| 1               | 3776207205136740581 | 2023-02-15 15:07:54.504 | lineitem_iceberg/metadata/snap-3776207205136740581-1-cf3d0be5-cf70-453d-ad8f-48fdc412e608.avro |
| 2               | 7635660646343998149 | 2023-02-15 15:08:14.73  | lineitem_iceberg/metadata/snap-7635660646343998149-1-10eaca8a-1e1c-421e-ad6d-b232e5ee23d3.avro |

## Limitations

Writing (i.e., exporting to) Iceberg files is currently not supported.