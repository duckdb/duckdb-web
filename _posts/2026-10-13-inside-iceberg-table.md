---
layout: post
title: "What Is Inside an Iceberg Table?"
authors:
  - The DuckDB team
thumb: "/images/blog/thumbs/iceberg-writes.svg"
image: "/images/blog/thumbs/iceberg-writes.png"
excerpt: "An Iceberg table is a tree of JSON, Avro and Parquet files. DuckDB can read every one of them, so you can walk the tree yourself with SQL: from the metadata file, through the manifest list and manifests, down to the data files and delete files."
tag: deep-dive
---

An [Apache Iceberg](https://iceberg.apache.org/) table looks like a regular table when you query it, but underneath it is a small tree of files: one JSON file at the top, a few layers of Avro files in the middle, and Parquet files at the bottom. When something is slow or looks wrong, it helps to know what is in that tree.

DuckDB can read all three formats, so you can inspect every layer with plain SQL. In this post, we create a small Iceberg table, change it a few times, and then walk through the files from the top down.

## Getting Started

You need DuckDB with the [`iceberg` extension]({% link docs/current/core_extensions/iceberg/overview.md %}) and an [Iceberg REST catalog](https://iceberg.apache.org/) to attach to. The [catalogs page]({% link docs/current/core_extensions/iceberg/catalogs.md %}) has instructions for catalogs such as [Apache Polaris](https://polaris.apache.org/), [Lakekeeper](https://lakekeeper.io/) and Amazon S3 Tables.

A catalog is needed because the files on their own cannot tell you which version of the table is current. An Iceberg table writes a new `metadata.json` on every change and never overwrites the old one. The catalog holds the one piece of mutable state: a pointer to the current metadata file. When you query the table, DuckDB asks the catalog for that pointer first, then follows the tree of files down from there.

For this post, we run a catalog locally with the [Iceberg REST catalog fixture](https://iceberg.apache.org/), a small reference catalog that the Iceberg project publishes as a Docker image. It is the quickest catalog to set up: it runs from a single image, needs no Cloud account and no authentication, and keeps everything on local disk where you can open the files yourself.

We start it like this:

```bash
docker run -p 8181:8181 \
    -v /data/lake:/data/lake \
    -e CATALOG_WAREHOUSE=/data/lake \
    apache/iceberg-rest-fixture
```

Each part of that command maps to something DuckDB relies on later:

* `-p 8181:8181` publishes the catalog's REST API on `localhost:8181`, the address DuckDB connects to.
* `-v /data/lake:/data/lake` mounts a host directory into the container, so the metadata, manifest and Parquet files survive after the container stops and you can read them directly.
* `-e CATALOG_WAREHOUSE=/data/lake` tells the catalog where to write those files, which is why every path in the output below begins with `/data/lake`.

> Note Run the examples below in the local DuckDB [CLI]({% link docs/current/clients/cli/overview.md %}), not in the browser-based [DuckDB Shell](https://shell.duckdb.org/), because a page served from the web cannot reach a catalog on your own `localhost`.

With the fixture running, attach it like this:

```sql
ATTACH 'warehouse' AS lake (
    TYPE iceberg,
    ENDPOINT 'http://localhost:8181',
    AUTHORIZATION_TYPE 'none'
);
```

This opens a catalog connection named `lake` that you query like any attached database.

* `TYPE iceberg` tells DuckDB to speak the Iceberg REST protocol.
* `ENDPOINT` is the address published by the `-p` flag above.
* `AUTHORIZATION_TYPE 'none'` matches the fixture, which expects no credentials.
* The first argument is the warehouse name. The fixture serves a single warehouse, so any name works.
* With object storage, the paths in the output below start with [`s3://`]({% link docs/current/core_extensions/httpfs/s3api.md %}) instead of `/data/lake`, but everything else is the same.

## A Table with History

We create a table of train services, partitioned by date, and change it three times: an insert of three days of data, an insert of a fourth day, and a delete.

```sql
CREATE SCHEMA lake.demo;
CREATE TABLE lake.demo.services (
    service_id BIGINT,
    service_date DATE,
    station VARCHAR,
    delay_min INTEGER
)
PARTITIONED BY (service_date);

INSERT INTO lake.demo.services
    SELECT
        i,
        DATE '2026-10-01' + (i % 3)::INTEGER,
        ['Utrecht Centraal', 'Delft', 'Leiden Centraal'][1 + (i % 3)::INTEGER],
        (i % 9)::INTEGER
    FROM range(1, 9_001) t(i);

INSERT INTO lake.demo.services
    SELECT i, DATE '2026-10-04', 'Den Haag HS', (i % 5)::INTEGER
    FROM range(9_001, 12_001) t(i);

DELETE FROM lake.demo.services
WHERE service_date = DATE '2026-10-02' AND delay_min = 4;
```

Each of the two inserts and the delete commits on its own. A write does not change the table in place: DuckDB reads the current snapshot, writes new data and metadata files alongside the old ones, and then asks the catalog to move the table pointer from that snapshot to the new one. That move is the commit.

The commit names the snapshot it expects to replace, so two writers that start from the same snapshot cannot both succeed. The first commit moves the pointer, and the second is rejected, because the snapshot it meant to replace is no longer current. The rejected write then retries on top of the new snapshot. When run in sequence from a single session, the three statements here never conflict, because each one starts from the snapshot the previous one committed.

The table now has 11,000 rows: the first insert added 9,000, the second added 3,000, and the delete removed the 1,000 rows of October 2 that had a delay of 4 minutes. Each of the three statements created a new [snapshot](https://iceberg.apache.org/spec/#snapshots), which [`iceberg_snapshots`]({% link docs/current/core_extensions/iceberg/iceberg_functions.md %}#iceberg_snapshots) lists as follows:

```sql
SELECT sequence_number, snapshot_id, operation
FROM iceberg_snapshots(lake.demo.services)
ORDER BY sequence_number;
```

```text
┌─────────────────┬─────────────────────┬───────────┐
│ sequence_number │     snapshot_id     │ operation │
│     uint64      │       uint64        │  varchar  │
├─────────────────┼─────────────────────┼───────────┤
│               1 │ 7523747767380427861 │ append    │
│               2 │ 3062515218093523051 │ append    │
│               3 │ 6456433563311493009 │ delete    │
└─────────────────┴─────────────────────┴───────────┘
```

## The Tree

Before going through the layers one by one, here is the whole structure. Each layer points to the files in the layer below it:

```text
metadata.json                    one per table version
└── manifest list (Avro)         one per snapshot
    └── manifests (Avro)         one per write (for simplicity)
        ├── data files (Parquet)
        └── delete files (Parquet)
```

All of these files are immutable. Every change writes new files and a new `metadata.json`, then commits by moving the catalog pointer to it.

## Layer 1: The Metadata File

The catalog stores a single pointer per table: the location of the current metadata file. `iceberg_load_table_response` returns what the catalog sent back when DuckDB loaded the table, including that location:

```sql
SELECT metadata_location
FROM iceberg_load_table_response(lake.demo.services);
```

```text
┌────────────────────────────────────────────────────────────────────────────────────────────┐
│                                     metadata_location                                      │
│                                          varchar                                           │
├────────────────────────────────────────────────────────────────────────────────────────────┤
│ /data/lake/demo/services/metadata/00003-b79b5ffd-f118-44fd-9d8e-3551c147ef3b.metadata.json │
└────────────────────────────────────────────────────────────────────────────────────────────┘
```

The file name starts with `00003` because this is the fourth version of the metadata, counting from `00000` when the table was created.

It is a JSON document, so [`read_json`]({% link docs/current/data/json/loading_json.md %}) can read it. We store the location in a [variable]({% link docs/current/sql/statements/set_variable.md %}) to keep the queries short:

```sql
SET VARIABLE metadata_file = (
    SELECT metadata_location FROM iceberg_load_table_response(lake.demo.services)
);

SELECT
    "format-version",
    "current-snapshot-id",
    len(snapshots) AS snapshots,
    len("metadata-log") AS previous_metadata_files
FROM read_json(getvariable('metadata_file'));
```

```text
┌────────────────┬─────────────────────┬───────────┬─────────────────────────┐
│ format-version │ current-snapshot-id │ snapshots │ previous_metadata_files │
│     int64      │        int64        │   int64   │          int64          │
├────────────────┼─────────────────────┼───────────┼─────────────────────────┤
│              2 │ 6456433563311493009 │         3 │                       3 │
└────────────────┴─────────────────────┴───────────┴─────────────────────────┘
```

Besides the schema and partition spec, the metadata file holds the list of all snapshots that are still around, and each snapshot has a `summary` with counters. These counters are a cheap way to see what each change did, without reading any data:

```sql
SELECT
    s."sequence-number" AS seq,
    s.summary.operation,
    s.summary."added-records",
    s.summary."added-position-deletes",
    s.summary."total-records",
    s.summary."total-data-files",
    s.summary."total-delete-files"
FROM (SELECT unnest(snapshots) AS s FROM read_json(getvariable('metadata_file')))
ORDER BY seq;
```

```text
┌───────┬───────────┬───────────────┬────────────────────────┬───────────────┬──────────────────┬────────────────────┐
│  seq  │ operation │ added-records │ added-position-deletes │ total-records │ total-data-files │ total-delete-files │
│ int64 │  varchar  │    varchar    │        varchar         │    varchar    │     varchar      │      varchar       │
├───────┼───────────┼───────────────┼────────────────────────┼───────────────┼──────────────────┼────────────────────┤
│     1 │ append    │ 9000          │ NULL                   │ 9000          │ 3                │ 0                  │
│     2 │ append    │ 3000          │ NULL                   │ 12000         │ 4                │ 0                  │
│     3 │ delete    │ NULL          │ 1000                   │ 12000         │ 4                │ 1                  │
└───────┴───────────┴───────────────┴────────────────────────┴───────────────┴──────────────────┴────────────────────┘
```

In the last row, after the delete, `total-records` is still 12,000 and there are still four data files. The delete did not touch the data files. It added one *delete file* with 1,000 entries. We will get to that file in a moment.

> Note The Iceberg spec treats these `summary` fields as optional, so an engine is free to leave any of them out. The counters above are populated by DuckDB, but a table written by another engine may be missing some of them, in which case the field reads as `NULL`. Treat them as a convenient hint rather than a guarantee.

> Tip The metadata file grows with every commit, because it keeps the snapshot list and a log of previous metadata files. On a table that receives thousands of small commits, it can become large enough to slow down loading the table. Expiring old snapshots, which most catalogs and engines can do, keeps it in check.

## Layer 2: The Manifest List

Each snapshot points to a *manifest list*, an Avro file that lists the manifests making up that snapshot. The [`avro` extension]({% link docs/current/core_extensions/avro.md %}) reads it with `read_avro`. We take the manifest list of the latest snapshot:

```sql
SET VARIABLE manifest_list = (
    SELECT manifest_list
    FROM iceberg_snapshots(lake.demo.services)
    ORDER BY sequence_number DESC
    LIMIT 1
);

SELECT
    regexp_replace(manifest_path, '.*/metadata/', '') AS manifest,
    content,
    sequence_number,
    added_files_count,
    added_rows_count
FROM read_avro(getvariable('manifest_list'));
```

```text
┌──────────────────────────────────────────────┬─────────┬─────────────────┬───────────────────┬──────────────────┐
│                   manifest                   │ content │ sequence_number │ added_files_count │ added_rows_count │
│                   varchar                    │  int32  │      int64      │       int32       │      int64       │
├──────────────────────────────────────────────┼─────────┼─────────────────┼───────────────────┼──────────────────┤
│ ffbf7076-8d36-46f0-aaa2-76e7d95442f0-m0.avro │       0 │               1 │                 3 │             9000 │
│ 74fa5b1f-0908-4e34-964a-504d946671de-m0.avro │       0 │               2 │                 1 │             3000 │
│ 5282235d-42b4-4b5d-a190-147a867994b7-m0.avro │       1 │               3 │                 1 │             1000 │
└──────────────────────────────────────────────┴─────────┴─────────────────┴───────────────────┴──────────────────┘
```

We created one manifest with every write. `content` is 0 for manifests that track data files and 1 for manifests that track delete files. The manifest list also stores the range of partition values in each manifest (not shown here), so a reader can skip entire manifests when a query filters on the partition column.

The latest snapshot still includes the manifests written by the two earlier snapshots. To make a commit cheap to write, an engine can add a new manifest for every write, as happened here. This comes at the cost of read performance, because of the rapidly accumulating small manifests. An alternative method merges new additions into an existing manifest, which is more expensive for the writer but more optimized for the reader.

## Layer 3: The Manifests

The manifests list the actual files, one entry per file, with the partition values, the row count and per-column statistics. They are Avro too:

```sql
SELECT
    status,
    data_file.content,
    regexp_replace(data_file.file_path, '.*/data/', '') AS file,
    data_file.record_count,
    data_file.partition
FROM read_avro('/data/lake/demo/services/metadata/*-m*.avro')
ORDER BY file;
```

```text
┌────────┬─────────┬──────────────────────────────────────────────────────────────────────────────┬──────────────┬─────────────────────────────────────────┐
│ status │ content │                                     file                                     │ record_count │                partition                │
│ int32  │  int32  │                                   varchar                                    │    int64     │  struct(identity_service_date_2 date)   │
├────────┼─────────┼──────────────────────────────────────────────────────────────────────────────┼──────────────┼─────────────────────────────────────────┤
│      1 │       0 │ service_date=2026-10-01/01a12bb2-ad80-7cf4-8f63-beee9619f7c0.parquet         │         3000 │ {'identity_service_date_2': 2026-10-01} │
│      1 │       0 │ service_date=2026-10-02/01a12bb2-ad7f-7690-bda8-690b622b119a.parquet         │         3000 │ {'identity_service_date_2': 2026-10-02} │
│      1 │       1 │ service_date=2026-10-02/58a752c7-9925-4add-99ca-785505e17589-deletes.parquet │         1000 │ {'identity_service_date_2': 2026-10-02} │
│      1 │       0 │ service_date=2026-10-03/01a12bb2-ad80-71f7-b4cd-58684f05b129.parquet         │         3000 │ {'identity_service_date_2': 2026-10-03} │
│      1 │       0 │ service_date=2026-10-04/01a12bb2-adbe-790f-bde9-50db3acba4b2.parquet         │         3000 │ {'identity_service_date_2': 2026-10-04} │
└────────┴─────────┴──────────────────────────────────────────────────────────────────────────────┴──────────────┴─────────────────────────────────────────┘
```

`status = 1` means the file was added in the snapshot that wrote the manifest. `content` is 0 for a data file and 1 for a position delete file. The partition value is stored per file, which is what lets a reader skip files without opening them.

The extension has a function that does this for you. [`iceberg_metadata`]({% link docs/current/core_extensions/iceberg/iceberg_functions.md %}#iceberg_metadata) follows the current snapshot through the manifest list and the manifests and returns one row per file:

```sql
SELECT
    manifest_content,
    regexp_replace(file_path, '.*/data/', '') AS file,
    record_count
FROM iceberg_metadata(lake.demo.services)
ORDER BY file;
```

```text
┌──────────────────┬──────────────────────────────────────────────────────────────────────────────┬──────────────┐
│ manifest_content │                                     file                                     │ record_count │
│     varchar      │                                   varchar                                    │    int64     │
├──────────────────┼──────────────────────────────────────────────────────────────────────────────┼──────────────┤
│ DATA             │ service_date=2026-10-01/01a12bb2-ad80-7cf4-8f63-beee9619f7c0.parquet         │         3000 │
│ DATA             │ service_date=2026-10-02/01a12bb2-ad7f-7690-bda8-690b622b119a.parquet         │         3000 │
│ DELETE           │ service_date=2026-10-02/58a752c7-9925-4add-99ca-785505e17589-deletes.parquet │         1000 │
│ DATA             │ service_date=2026-10-03/01a12bb2-ad80-71f7-b4cd-58684f05b129.parquet         │         3000 │
│ DATA             │ service_date=2026-10-04/01a12bb2-adbe-790f-bde9-50db3acba4b2.parquet         │         3000 │
└──────────────────┴──────────────────────────────────────────────────────────────────────────────┴──────────────┘
```

Reading the Avro files directly is useful when you want to see fields that the function does not return, or when you are looking at an older snapshot or a table that is not in a catalog.

## Column Statistics

The manifests also store, for every data file, the lower and upper bound of each column. [`iceberg_column_stats`]({% link docs/current/core_extensions/iceberg/reference.md %}) returns them in a readable form:

```sql
SELECT
    column_name,
    regexp_replace(file_path, '.*/data/', '') AS file,
    lower_bound,
    upper_bound
FROM iceberg_column_stats(lake.demo.services)
WHERE column_name = 'service_id'
ORDER BY file;
```

```text
┌─────────────┬──────────────────────────────────────────────────────────────────────────────┬─────────────┬─────────────┐
│ column_name │                                     file                                     │ lower_bound │ upper_bound │
│   varchar   │                                   varchar                                    │   varchar   │   varchar   │
├─────────────┼──────────────────────────────────────────────────────────────────────────────┼─────────────┼─────────────┤
│ service_id  │ service_date=2026-10-01/01a12bb2-ad80-7cf4-8f63-beee9619f7c0.parquet         │ 3           │ 9000        │
│ service_id  │ service_date=2026-10-02/01a12bb2-ad7f-7690-bda8-690b622b119a.parquet         │ 1           │ 8998        │
│ service_id  │ service_date=2026-10-02/58a752c7-9925-4add-99ca-785505e17589-deletes.parquet │ NULL        │ NULL        │
│ service_id  │ service_date=2026-10-03/01a12bb2-ad80-71f7-b4cd-58684f05b129.parquet         │ 2           │ 8999        │
│ service_id  │ service_date=2026-10-04/01a12bb2-adbe-790f-bde9-50db3acba4b2.parquet         │ 9001        │ 12000       │
└─────────────┴──────────────────────────────────────────────────────────────────────────────┴─────────────┴─────────────┘
```

These bounds are what DuckDB uses to skip files when you filter on a column that is not the partition column. A query with `WHERE service_id > 10000` only has to open the file for October 4, because the bounds of the other three files rule them out.

The ranges for the first three days overlap almost completely, because the rows were spread over the days round-robin. Data that is written in the order of a commonly filtered column gets narrower bounds and more skipping.

## Partition Statistics

The bounds above are per column, per data file. For the partition column there is a coarser view, one row per manifest, that the manifest list keeps so a reader can skip an entire manifest before opening any of its files. [`iceberg_partition_stats`]({% link docs/current/core_extensions/iceberg/reference.md %}) returns it:

```sql
SELECT
    partition_field_name,
    partition_field_transform,
    lower_bound,
    upper_bound
FROM iceberg_partition_stats(lake.demo.services)
ORDER BY lower_bound;
```

```text
┌─────────────────────────┬───────────────────────────┬─────────────┬─────────────┐
│  partition_field_name   │ partition_field_transform │ lower_bound │ upper_bound │
│         varchar         │          varchar          │   varchar   │   varchar   │
├─────────────────────────┼───────────────────────────┼─────────────┼─────────────┤
│ identity_service_date_2 │ identity                  │ 2026-10-01  │ 2026-10-03  │
│ identity_service_date_2 │ identity                  │ 2026-10-02  │ 2026-10-02  │
│ identity_service_date_2 │ identity                  │ 2026-10-04  │ 2026-10-04  │
└─────────────────────────┴───────────────────────────┴─────────────┴─────────────┘
```

There is one row per manifest, so the bounds trace the three writes: the first insert spread three days across one manifest, the second insert added October 4, and the delete touched only October 2. The `partition_field_transform` is `identity` because we partitioned on the date column directly. A query with `WHERE service_date = DATE '2026-10-04'` can rule out the first and third manifests on these bounds alone, without reading a single manifest entry.

## Layer 4: Data Files and Delete Files

At the bottom of the tree are Parquet files. The data files are regular Parquet that any reader can open. The delete file works differently. It is a *position delete* file, and it lists rows to ignore by file and row position:

```sql
SELECT regexp_replace(file_path, '.*/data/', '') AS data_file, pos
FROM read_parquet(
    '/data/lake/demo/services/data/*/*-deletes.parquet',
    hive_partitioning = false
)
ORDER BY pos
LIMIT 5;
```

```text
┌──────────────────────────────────────────────────────────────────────┬───────┐
│                              data_file                               │  pos  │
│                               varchar                                │ int64 │
├──────────────────────────────────────────────────────────────────────┼───────┤
│ service_date=2026-10-02/01a12bb2-ad7f-7690-bda8-690b622b119a.parquet │     1 │
│ service_date=2026-10-02/01a12bb2-ad7f-7690-bda8-690b622b119a.parquet │     4 │
│ service_date=2026-10-02/01a12bb2-ad7f-7690-bda8-690b622b119a.parquet │     7 │
│ service_date=2026-10-02/01a12bb2-ad7f-7690-bda8-690b622b119a.parquet │    10 │
│ service_date=2026-10-02/01a12bb2-ad7f-7690-bda8-690b622b119a.parquet │    13 │
└──────────────────────────────────────────────────────────────────────┴───────┘
```

This is how the extension implements `DELETE` and `UPDATE`: it leaves the data file alone and records the positions of the deleted rows, a strategy called [merge-on-read]({% link docs/current/core_extensions/iceberg/writing_to_iceberg.md %}#limitations-for-update-and-delete).

Every reader then has to combine the two files to get the correct rows. Writes are cheap, and reads pay a small cost, which grows with the number of delete files. We set `hive_partitioning = false` because the `service_date=...` directory would otherwise be added as an extra column.

For tables with `format-version` 3, the same information is stored as a compact binary deletion vector in a [Puffin](https://iceberg.apache.org/puffin-spec/) file instead of a Parquet file.

## Why Look at This at All?

Most of the time, you do not need to. `FROM lake.demo.services` returns the right 11,000 rows, and the extension handles the tree. It becomes useful when something does not behave as you expect:

* **A query reads more files than you expected.** Compare the partition values and column bounds in the manifests with your filter.
* **A table gets slower over time.** Count the manifests and delete files. Many small commits and many deletes both add files that every query has to process.
* **Row counts look off.** The snapshot summaries show how many rows each commit added and deleted.
* **Another engine wrote the table.** The manifests show what it wrote, including properties that DuckDB does not use.

Since every layer is a file in a format DuckDB already reads, you can answer these questions with the same tool you use to query the data.

## Further Reading

* [Writes in DuckDB-Iceberg]({% post_url 2025-11-28-iceberg-writes-in-duckdb %})
* [Iceberg in the Browser]({% post_url 2025-12-16-iceberg-in-the-browser %})
* [New DuckDB-Iceberg Features in v1.5.3]({% post_url 2026-05-29-new-iceberg-features %})
