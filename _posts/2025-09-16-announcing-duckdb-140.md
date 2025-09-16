---
layout: post
title: "Announcing DuckDB 1.4.0"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/duckdb-release-1-4-0.svg"
image: "/images/blog/thumbs/duckdb-release-1-4-0.png"
excerpt: "We're releasing DuckDB version 1.4.0, codenamed “Andium”. This is an LTS release with 1 year of community support, which packs new features such as database encryption, the MERGE statement and Iceberg writes."
tags: ["release"]
---

We are proud to release DuckDB v1.4.0, named “Andium” after the _Andean teal_ (Anas andium), which lives in the Andean highlands of Colombia, Venezuela and Ecuador.

In this blog post, we cover the most important updates for this release around support, features and extensions. DuckDB is moving rather quickly, and we could cover only a small fraction of the changes in this release. For the complete release notes, see the [release page on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.4.0).

> To install the new version, please visit the new [installation page]({% link install/index.html %}). Note that it can take a few days to release some client libraries (e.g., Go, R, Java) due to the extra changes and review rounds required.

## Long Term Support (LTS) Edition

We are delighted to see that DuckDB is used regularly in production environments and realize that such deployments often come with a requirement for long-term maintenance.
In the past, we would automatically deprecate old DuckDB versions whenever the newer version was released. But we’re changing this today.

Starting with this release, every _other_ DuckDB version is going to be a Long Term Support (LTS) edition.
For LTS DuckDB versions, [community support](https://duckdblabs.com/community_support_policy/) will last a year after the release (for now).
[DuckDB Labs](https://duckdblabs.com/) is also starting to offer support for older LTS versions after their community support has expired.

<div align="center" style="margin:10px">
    <img
      src="/images/blog/lts-support.svg"
      alt="DuckDB Long-Term Support"
      width="700"
    />
</div>

<details markdown='1'>
<summary markdown='span'>
Click to see the end-of-life (EOL) dates for DuckDB releases.
</summary>
|    Version | Codename     | End of community support |
| ---------: | ------------ | ------------------------ |
|       0.\* |              | 2024-06-03               |
|     1.0.\* | Nivis        | 2024-09-09               |
|     1.1.\* | Eatoni       | 2025-02-05               |
|     1.2.\* | Histrionicus | 2025-05-21               |
|     1.3.\* | Ossivalis    | 2025-09-16               |
| 1.4.\* LTS | Andium       | 2026-09-16               |
<details>

## New Features

### Database Encryption

Being able to encrypt DuckDB database files has been a [long-standing feature request](https://github.com/duckdb/duckdb/discussions/4512). Starting with this release, DuckDB supports encryption of its files. Encryption keys are given using the `ENCRYPTION_KEY` parameter for to [`ATTACH`]({% link docs/stable/sql/statements/attach.md %}), like so:

```sql
ATTACH 'encrypted.db' AS enc (ENCRYPTION_KEY 'asdf');
```

DuckDB uses the industry-standard [AES encryption](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) with a key length of 256 bits using the recommended [GCM](https://en.wikipedia.org/wiki/Galois/Counter_Mode) mode by default.

The encryption covers the main database file, the write-ahead-log (WAL) file, and even temporary files. To encrypt data, DuckDB can use either the built-in `mbedtls` library or the OpenSSL library from the `httpfs` extension. Note that the OpenSSL versions are much faster due to hardware acceleration, so make sure to `LOAD httpfs` for good encryption performance.

Encryption support in DuckDB was implemented by [Lotte Felius (@ccfelius)](https://github.com/ccfelius).

### `MERGE` Statement

DuckDB now supports `MERGE INTO` as an alternative to `INSERT INTO ... ON CONFLICT`.
`MERGE INTO` does not require a primary key since it works on any custom merge condition. This is a very common statement in OLAP systems that do not support primary keys but still want to support upserting (i.e., `UPDATE` plus `INSERT`) functionality.

In this example we use a simple condition matching on a key and we call the `RETURNING` statement to get a summary of the updated and inserted rows.

```sql
CREATE TABLE Stock(item_id INTEGER, balance INTEGER);
INSERT INTO Stock VALUES (10, 2200), (20, 1900);

WITH new_stocks(item_id, volume) AS (VALUES (20, 2200), (30, 1900))
    MERGE INTO Stock
        USING new_stocks USING (item_id)
    WHEN MATCHED
        THEN UPDATE SET balance = balance + volume
    WHEN NOT MATCHED
        THEN INSERT VALUES (new_stocks.item_id, new_stocks.volume)
    RETURNING merge_action, *;
```

```text
┌──────────────┬─────────┬─────────┐
│ merge_action │ item_id │ balance │
│   varchar    │  int32  │  int32  │
├──────────────┼─────────┼─────────┤
│ UPDATE       │      20 │    4100 │
│ INSERT       │      30 │    1900 │
└──────────────┴─────────┴─────────┘
```

`MERGE INTO` also supports more complex conditions and DELETE statements.

```sql
WITH deletes(item_id, delete_threshold) AS (VALUES (10, 3000))
    MERGE INTO Stock
        USING deletes USING (item_id)
    WHEN MATCHED AND balance < delete_threshold
        THEN DELETE
    RETURNING merge_action, *;
```

```text
┌──────────────┬─────────┬─────────┐
│ merge_action │ item_id │ balance │
│   varchar    │  int32  │  int32  │
├──────────────┼─────────┼─────────┤
│ DELETE       │   10    │  2200   │
└──────────────┴─────────┴─────────┘
```



### Iceberg Writes

The [duckdb-iceberg]({% link docs/stable/core_extensions/iceberg/overview.md %}) extension now **supports writing to Iceberg**.

<details markdown='1'>
<summary markdown='span'>
Click to see the code snippet showing Iceberg writes.
</summary>
```sql
-- Having setup an Iceberg REST catalog using
-- https://github.com/duckdb/duckdb-iceberg/blob/main/scripts/start-rest-catalog.sh
INSTALL iceberg;
LOAD iceberg;
ATTACH '' AS iceberg_datalake (
        TYPE ICEBERG,
        CLIENT_ID 'admin',
        CLIENT_SECRET 'password',
        ENDPOINT 'http://127.0.0.1:8181'
    );
CREATE SECRET (
        TYPE S3,
        KEY_ID 'admin',
        SECRET 'password',
        ENDPOINT '127.0.0.1:9000',
        URL_STYLE 'path',
        USE_SSL 0
    );
USE iceberg_datalake.default;
ATTACH 'duckdb.db' AS duckdb_db;
CREATE TABLE duckdb_db.t AS SELECT range a FROM range(4);
CREATE TABLE t AS SELECT * FROM duckdb_db.t;
FROM iceberg_datalake.default.t;
```

```text
┌───────┐
│   a   │
│ int64 │
├───────┤
│     0 │
│     1 │
│     2 │
│     3 │
└───────┘
```
</details>

This means that copying data from DuckDB or DuckLake to Iceberg is now possible.

* **Copying from Iceberg to DuckDB/DuckLake** is also supported via the `COPY` statement:

  ```sql
  COPY FROM DATABASE iceberg_datalake TO duckdb_db;
  ```

* **Copying from DuckLake/DuckDB to Iceberg** needs manual creation of the schemas on the Iceberg side of things:

  ```sql
  CREATE SCHEMA iceberg_datalake.main;
  COPY FROM DATABASE duckdb_db TO iceberg_datalake;
  ```

### CLI Progress Bar ETA

Community member [Rusty Conover (@rustyconover)](https://github.com/rustyconover) [contributed](https://github.com/duckdb/duckdb/pull/18575) an ETA (estimated time of arrival) feature to the DuckDB command line client. Estimating the remaining time is a [difficult problem](https://xkcd.com/612/) as progress measurements can vary a lot due to noise. To alleviate this, the ETA feature first collects some initial performance data, then continues to refine its estimate using a [Kalman filter](https://en.wikipedia.org/wiki/Kalman_filter). Here's how it works in practice:

<video muted controls loop width="700" class="lightmode-img">
  <source src="https://blobs.duckdb.org/videos/cli-eta-light.mov" type="video/mp4">
</video>
<video muted controls loop width="700" class="darkmode-img">
  <source src="https://blobs.duckdb.org/videos/cli-eta-dark.mov" type="video/mp4">
</video>

### `FILL` Window Function

[Richard (@hawkfish)](https://github.com/hawkfish) built a new window function, `FILL`, that can be used to _interpolate_ missing values in ordered windows. Here is an example, you can see a missing value between 1 and 42, it's interpolated to 21 in the result.

```SQL
FROM (VALUES (1, 1), (2, NULL), (3, 42)) t(c1, c2) SELECT fill(c2) OVER (ORDER BY c1) f;
```

This will be the result:
| f |
|---:|
| 1 |
| 21 |
| 42 |

### Teradata Connector

DuckDB now has a [Teradata Connector](https://github.com/duckdb/duckdb-teradata).
A separate blog post will be coming.

## Performance and Optimizations

### Sorting Rework

[Laurens (@lnkuiper)](https://github.com/lnkuiper) [rewrote DuckDB’s sorting implementation](https://github.com/duckdb/duckdb/pull/17584#thread-scaling-performance) ([again](https://github.com/duckdb/duckdb/pull/1561)). This new implementation uses a k-way merge sort to reduce data movement. It is also adaptive to pre-sorted data and uses a new API that makes it possible to use this new sorting code elsewhere in DuckDB, for example in window functions. We are seeing much better thread scaling performance with this implementation. We will publish a separate blog post with more detailed performance measurements.

### Materializing Common Table Expressions

Common table expressions (CTEs) are now materialized by default (instead of inlining them). This both improves performance and resolves some correctness bugs that happened due to inlining.
This feature was [implemented](https://github.com/duckdb/duckdb/pull/17459) by [Denis Hirn (kryonix)](https://github.com/kryonix), who [contributed support for recursive CTEs](https://github.com/duckdb/duckdb/pull/404) back in 2020.

### Checkpointing In-Memory Tables

In-memory tables now support [checkpointing](https://github.com/duckdb/duckdb/pull/18348). This has two key benefits:

1. In-memory tables now support compression. This is disabled by default – you can turn it on using:

```sql
ATTACH ':memory:' AS memory_compressed (COMPRESS);
```

Checkpointing triggers vacuuming deleted rows, allowing space to be reclaimed after deletes/truncation.

## Distribution 

### MacOS Notarization

MacOS has a fairly advanced model to ensure system integrity built around cryptographic signatures along with so-called “[notarization](https://developer.apple.com/documentation/Security/notarizing-macos-software-before-distribution)” by Apple. We had been signing our binaries [for about two years already](https://github.com/duckdb/duckdb/pull/7484).
Starting from this release, the DuckDB command line utility (`duckdb`) and the dynamic library `libduckdb…dylib` are _released with this notarization_. This will reduce the amount of complaints when using web browsers to download our binaries. Unfortunately, macOS does not yet fully support notarization of command line utility, so the “open with double click” use case will still have to wait. The recommended path to install the CLI on macOS is still our install script: `curl https://install.duckdb.org | bash`

### Moved Python Integration to its Own Repository

We have been slowly moving language integrations (“clients”) into their own repositories from `duckdb/duckdb`. For this release, we moved the Python client to its [own repository](https://github.com/duckdb/duckdb-python), `duckdb/duckdb-python`. Please make sure to [file issues](https://github.com/duckdb/duckdb-python/issues/new) related to the Python client there.

## Final Thoughts

These were a few highlights – but there are many more features and improvements in this release. There have been over 3,500 commits by over 90 contributors since we released v1.3.2. The full release notes can be [found on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.4.0). We would like to thank our community for providing detailed issue reports and feedback. And our special thanks goes to external contributors, who directly landed features in this release!
