---
layout: post
title:  "Iceberg Writes in DuckDB-Iceberg"
author: "Tom Ebergen"
thumb: "/images/blog/thumbs/iceberg-writes.svg"
image: "/images/blog/thumbs/iceberg-writes.png"
excerpt: "We shipped a number of features and improvements to the DuckDB-Iceberg extension: insert, update, and delete statements are all supported now."
tags: ["deep dive"]
---

Over the past several months, the DuckDB Labs team has been hard at work on the [DuckDB-Iceberg extension]({% link docs/stable/core_extensions/iceberg/overview.md %}), with _full read support_ and _initial write support_ released in [v1.4.0]({% post_url 2025-09-16-announcing-duckdb-140 %}).
Today, we are happy to announce delete and update support for Iceberg v2 tables is available in [v1.4.2]({% post_url 2025-11-12-announcing-duckdb-142 %})!

The Iceberg open table format has become extremely popular in the past two years, with many databases announcing support for the open table format [originally developed at Netflix](https://softwareengineeringdaily.com/2024/03/07/iceberg-at-netflix-and-beyond-with-ryan-blue/). This past year the DuckDB team has made Iceberg integration a [priority]({% link roadmap.md %}) and today we are happy to announce another step in that direction. In this blog post we will describe the current feature set of DuckDB-Iceberg in DuckDB v1.4.2.

## Getting Started

To experiment with the new DuckDB-Iceberg features, you will need to connect to your favorite Iceberg REST Catalog. There are many ways to connect to an Iceberg REST Catalog: please have a look at the [Connecting to REST Catalogs]({% link docs/stable/core_extensions/iceberg/iceberg_rest_catalogs.md %}) for connecting to catalogs like [Apache Polaris](https://polaris.apache.org/) or [Lakekeeper](https://lakekeeper.io/) and the [Connecting to S3Tables]({% link docs/stable/core_extensions/iceberg/amazon_s3_tables.md %}) page if you would like to connect to [Amazon S3 Tables](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables.html).

```sql
ATTACH '⟨warehouse_name⟩' AS iceberg_catalog (
    TYPE iceberg,
    ⟨other options⟩
);
```

## Inserts, Deletes and Updates

Support for creating tables and inserting to tables was already added in DuckDB v1.4.0: you can use standard DuckDB SQL syntax to insert data into your Iceberg table.

```sql
CREATE TABLE iceberg_catalog.default.simple_table (
    col1 INTEGER,
    col2 VARCHAR
);
INSERT INTO iceberg_catalog.default.simple_table
    VALUES (1, 'hello'), (2, 'world'), (3, 'duckdb is great');
```

You can also use any DuckDB table scan function to insert data into an Iceberg table:

```sql
INSERT INTO iceberg_catalog.default.more_data
    SELECT * FROM read_parquet('path/to/parquet');
```

Starting with v1.4.2, the standard SQL syntax also works for deletes and updates:

```sql
DELETE FROM iceberg_catalog.default.simple_table WHERE col1 = 2;
UPDATE iceberg_catalog.default.simple_table SET col1 = col1 + 5 WHERE col1 = 1;
SELECT * FROM iceberg_catalog.default.simple_table;
```

```text
┌───────┬─────────────────┐
│ col1  │      col2       │
│ int32 │     varchar     │
├───────┼─────────────────┤
│     3 │ duckdb is great │
│     6 │ hello           │
└───────┴─────────────────┘
```

> The Iceberg write support current has two limitations:
> 
> The update support is limited to _tables that are not partitioned and not sorted._ Attempting to perform update, insert or delete operations on partitioned or sorted tables using DuckDB-Iceberg will result in an error.
>
> DuckDB-Iceberg only writes positional deletes for `DELETE` and `UPDATE` statements. Copy-on-write functionality is not yet supported.

## Functions for Table Properties

Currently, DuckDB-Iceberg only supports _merge-on-read semantics_. Within [Iceberg Table Metadata](https://iceberg.apache.org/spec/#table-metadata-fields), table properties can be used to describe what form of deletes or updates are allowed. DuckDB-Iceberg will respect `write.update.mode` and `write.delete.mode` table properties for updates and deletes. If a table has these properties and they are not `merge-on-read`, DuckDB will throw an error and the `UPDATE` or `DELETE` will not be committed. Version v1.4.2 introduces three new functions to add, remove, and view table properties for an Iceberg table:

* `set_iceberg_table_properties`
* `iceberg_table_properties`
* `remove_iceberg_table_properties`

You can use them as follows:

```sql
-- to set table properties
CALL set_iceberg_table_properties(iceberg_catalog.default.simple_table, {
    'write.update.mode': 'merge-on-read',
    'write.file.size': '100000kb'
});
-- to read table properties
SELECT * FROM iceberg_table_properties(iceberg_catalog.default.simple_table);
```

```text
┌───────────────────┬───────────────┐
│        key        │     value     │
│      varchar      │    varchar    │
├───────────────────┼───────────────┤
│ write.update.mode │ merge-on-read │
│ write.file.size   │ 100000kb      │
└───────────────────┴───────────────┘
```

```sql
-- to remove table properties
CALL remove_iceberg_table_properties(
    iceberg_catalog.default.simple_table,
    ['some.other.property']
);
```

## Iceberg Table Metadata

DuckDB-Iceberg also allows you to view the metadata of your Iceberg tables using the `iceberg_metadata()` and `iceberg_snapshots()` functions.

```sql
SELECT * FROM iceberg_metadata(iceberg_catalog.default.table_1);
```

```text
┌──────────────────────┬──────────────────────┬──────────────────┬─────────┬──────────────────┬─────────────────────────────────────────────────────────────┬─────────────┬──────────────┐
│    manifest_path     │ manifest_sequence_…  │ manifest_content │ status  │     content      │                         file_path                           │ file_format │ record_count │
│       varchar        │        int64         │     varchar      │ varchar │     varchar      │                          varchar                            │   varchar   │    int64     │
├──────────────────────┼──────────────────────┼──────────────────┼─────────┼──────────────────┼─────────────────────────────────────────────────────────────┼─────────────┼──────────────┤
│ s3://warehouse/def…  │                    1 │ DATA             │ ADDED   │ EXISTING         │ s3://<storage_location>/simple_table/data/019a6ecc-9e9e-7…  │ parquet     │            3 │
│ s3://warehouse/def…  │                    2 │ DELETE           │ ADDED   │ POSITION_DELETES │ s3://<storage_location>/simple_table/data/d65b1db8-9fa8-4…  │ parquet     │            1 │
│ s3://warehouse/def…  │                    3 │ DELETE           │ ADDED   │ POSITION_DELETES │ s3://<storage_location>/simple_table/data/8d1b92dc-5f6e-4…  │ parquet     │            1 │
│ s3://warehouse/def…  │                    3 │ DATA             │ ADDED   │ EXISTING         │ s3://<storage_location>/simple_table/data/019a6ecf-5261-7…  │ parquet     │            1 │
└──────────────────────┴──────────────────────┴──────────────────┴─────────┴──────────────────┴─────────────────────────────────────────────────────────────┴─────────────┴──────────────┘
```

```sql
SELECT * FROM iceberg_snapshots(iceberg_catalog.default.simple_table);
```

```text
┌─────────────────┬─────────────────────┬─────────────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ sequence_number │     snapshot_id     │      timestamp_ms       │                                                manifest_list                                                 │
│     uint64      │       uint64        │        timestamp        │                                                   varchar                                                    │
├─────────────────┼─────────────────────┼─────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│               1 │ 1790528822676766947 │ 2025-11-10 17:24:55.075 │ s3://<storage_location>/simple_table/data/snap-1790528822676766947-f09658c4-ca52-4305-943f-6a8073529fef.avro │
│               2 │ 6333537230056014119 │ 2025-11-10 17:27:35.602 │ s3://<storage_location>/simple_table/data/snap-6333537230056014119-316d09bc-549d-46bc-ae13-a9fab5cbf09b.avro │
│               3 │ 7452040077415501383 │ 2025-11-10 17:27:52.169 │ s3://<storage_location>/simple_table/data/snap-7452040077415501383-93dee94e-9ec1-45fa-aec2-13ef434e50eb.avro │
└─────────────────┴─────────────────────┴─────────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

```

## Time Travel

Time travel is also possible via snapshot ids or timestamps using the `AT (VERSION => ...)` or `AT (TIMESTAMP => ...)` syntax.

```sql
-- via snapshot id
SELECT *
FROM iceberg_catalog.default.simple_table AT (
	VERSION => ⟨snapshot_id⟩
);
```

```text
┌───────┬─────────────────┐
│ col1  │      col2       │
│ int32 │     varchar     │
├───────┼─────────────────┤
│     1 │ hello           │
│     3 │ duckdb is great │
└───────┴─────────────────┘
```

```sql
-- via timestamp
SELECT *
FROM iceberg_catalog.default.simple_table AT (
    TIMESTAMP => '2025-11-10 17:27:45.602'
);
```

```text
┌───────┬─────────────────┐
│ col1  │      col2       │
│ int32 │     varchar     │
├───────┼─────────────────┤
│     1 │ hello           │
│     3 │ duckdb is great │
└───────┴─────────────────┘
```

## Viewing Requests to the Iceberg REST Catalog

You may also be curious as to what requests DuckDB is making to the Iceberg REST Catalog.
To do so, enable HTTP [logging]({% link docs/stable/operations_manual/logging/overview.md %}), run your workload, then select from the `HTTP` logs.

```sql
CALL enable_logging('HTTP');
SELECT * FROM iceberg_catalog.default.simple_table;
SELECT request.type, request.url, response.status
FROM duckdb_logs_parsed('HTTP');
```

```text
┌─────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────┬────────────────────┐
│  type   │                                                                             url                          │       status       │
│ varchar │                                                                           varchar                        │      varchar       │
├─────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────────────────┤
│ GET     │ https://<catalog_endpoint>/iceberg/v1/<warehouse>/iceberg-testing/namespaces/default                     │ NULL               │
│ HEAD    │ https://<catalog_endpoint>/iceberg/v1/<warehouse>/iceberg-testing/namespaces/default/tables/simple_table │ NULL               │
│ GET     │ https://<catalog_endpoint>/iceberg/v1/<warehouse>/iceberg-testing/namespaces/default/tables/simple_table │ NULL               │
│ GET     │ https://<storage_endpoint>/data/snap-5943683398986255948-c2217dde-6036-4e07-88f2-…                       │ OK_200             │
│ GET     │ https://<storage_endpoint>/data/f8c95b93-7b6b-4a24-8557-b98b553723d4-m0.avro                             │ OK_200             │
│ GET     │ https://<storage_endpoint>/data/214a7988-da39-4dac-aa3a-4a73d3ead405-m0.avro                             │ OK_200             │
│ GET     │ https://<storage_endpoint>/data/019a7244-c6e8-7bc9-9dd4-7249fcb04959.parquet                             │ PartialContent_206 │
│ GET     │ https://<storage_endpoint>/data/019a7244-fcb5-7308-96ec-1c9e32509eab.parquet                             │ PartialContent_206 │
│ GET     │ https://<storage_endpoint>/data/7f14bb06-f57a-42b4-ba7f-053a65152759-m0.avro                             │ OK_200             │
│ GET     │ https://<storage_endpoint>/data/71f8b43d-51e7-40e7-be88-e8d869836ecd-deletes.parq…                       │ PartialContent_206 │
│ GET     │ https://<storage_endpoint>/data/64f6c6e2-2f54-470e-b990-b201bc615042-m0.avro                             │ OK_200             │
│ GET     │ https://<storage_endpoint>/data/4e54afed-6dd8-4ba0-88fb-16f972ac1d91-deletes.parq…                       │ PartialContent_206 │
├─────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────┴────────────────────┤
│ 12 rows                                                                                                                       3 columns │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Here we can see calls to the Iceberg REST Catalog, followed by calls to the storage endpoint. The first three calls to the Iceberg REST Catalog are to verify the schema still exists and to get the latest `metadata.json` of the DuckDB-Iceberg table. Next, it queries the manifest list, manifest files, and eventually the files with data and deletes. The data and delete files are stored locally in a cache to speed up subsequent reads.

## Transactions

DuckDB is an ACID-compliant database that supports [transactions]({% link docs/stable/sql/statements/transactions.md %}).
Work on DuckDB-Iceberg has been made with this in mind. Within a transaction, the following conditions will hold for Iceberg tables.

1. The first time a table is read in a transaction, its snapshot information is stored in the transaction and will remain consistent within that transaction.
2. Updates, inserts and deletes will only be committed to an Iceberg Table when the transaction is committed (i.e., `COMMIT`);

Point #1 is important for read performance. If you wish to do analytics on an Iceberg table and you do not need to get the latest version of the table every time, running your analytics in a transaction will prevent fetching the latest version for every query.

```sql
-- truncate the logs
CALL truncate_duckdb_logs();
CALL enable_logging('HTTP')
BEGIN;
-- first read gets latest snapshot information
SELECT * FROM iceberg_catalog.default.simple_table;
-- subsequent read reads from local cached data
SELECT * FROM iceberg_catalog.default.simple_table;
-- get logs
SELECT request.type, request.url, response.status
FROM duckdb_logs_parsed('HTTP');
```

```text
┌─────────┬─────────────────────────────────────────────────────────────────────────────────────────────────────────────┬────────────────────┐
│  type   │                                                  url                                                        │       status       │
│ varchar │                                                varchar                                                      │      varchar       │
├─────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────────────────┤
│ GET     │ https://<catalog_endpoint>/iceberg/v1/<warehouse>/iceberg-testing/namespaces/default                        │ NULL               │
│ HEAD    │ https://<catalog_endpoint>/iceberg/v1/<warehouse>/iceberg-testing/namespaces/default/tables/simple_table    │ NULL               │
│ GET     │ https://<catalog_endpoint>/iceberg/v1/<warehouse>/iceberg-testing/namespaces/default/tables/simple_table    │ NULL               │
│ GET     │ https://<storage_endpoint>/data/snap-5943683398986255948-c2217dde-6036-4e07-88f2-1…                         │ OK_200             │
│ GET     │ https://<storage_endpoint>/data/f8c95b93-7b6b-4a24-8557-b98b553723d4-m0.avro                                │ OK_200             │
│ GET     │ https://<storage_endpoint>/data/214a7988-da39-4dac-aa3a-4a73d3ead405-m0.avro                                │ OK_200             │
│ GET     │ https://<storage_endpoint>/data/019a7244-c6e8-7bc9-9dd4-7249fcb04959.parquet                                │ PartialContent_206 │
│ GET     │ https://<storage_endpoint>/data/019a7244-fcb5-7308-96ec-1c9e32509eab.parquet                                │ PartialContent_206 │
│ GET     │ https://<storage_endpoint>/data/7f14bb06-f57a-42b4-ba7f-053a65152759-m0.avro                                │ OK_200             │
│ GET     │ https://<storage_endpoint>/data/71f8b43d-51e7-40e7-be88-e8d869836ecd-deletes.parquet                        │ PartialContent_206 │
│ GET     │ https://<storage_endpoint>/data/64f6c6e2-2f54-470e-b990-b201bc615042-m0.avro                                │ OK_200             │
│ GET     │ https://<storage_endpoint>/data/4e54afed-6dd8-4ba0-88fb-16f972ac1d91-deletes.parquet                        │ PartialContent_206 │
├─────────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────┴────────────────────┤
│ 12 rows                                                                                                                          3 columns │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Here we see all the same requests we saw in the previous section. However, now we are in a transaction, which means the second time we read from `iceberg_catalog.default.simple_table`, we do not need to query the REST Catalog for table updates. This means DuckDB-Iceberg performs no extra requests when reading a table a second time, significantly improving performance.

## Conclusion and Future Work

With these features, DuckDB-Iceberg now has a strong base support for the Iceberg tables, which enables users to unlock the analytical powers of DuckDB on their Iceberg tables. There is still more work to come and the Iceberg table specification has many more features the DuckDB team would like to support in DuckDB-Iceberg. If you feel any feature is a priority for your analytical workloads, please reach out to us in the [DuckDB-Iceberg GitHub repository](https://github.com/duckdb/duckdb-iceberg) or [get in touch](https://duckdblabs.com/contact/) with our engineers.

Below is a list of improvements planned for the near future (in no particular order):

- Performance improvements
- Updates / deletes / inserts to partitioned tables
- Updates / deletes / inserts to sorted tables
- Schema evolution
- Support for Iceberg v3 tables, focusing on binary deletion vectors and row lineage tracking
