---
layout: post
title: "Announcing DuckDB 1.4.2 LTS"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/duckdb-release-1-4-2-lts.svg"
image: "/images/blog/thumbs/duckdb-release-1-4-2-lts.png"
excerpt: "Today we are releasing DuckDB 1.4.2."
tags: ["release"]
---

In this blog post, we highlight a few important fixes and convenience improvements in DuckDB v1.4.2, the second bugfix release in [DuckDB's 1.4 LTS line]({% post_url 2025-09-16-announcing-duckdb-140 %}).
You can find the complete [release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.4.2).

To install the new version, please visit the [installation page]({% link install/index.html %}).

## Windows Improvements

We are introducing beta support for Windows arm64. You can now install extensions on Windows arm64:

```sql
PRAGMA platform;
```

```text
┌───────────────┐
│   platform    │
│    varchar    │
├───────────────┤
│ windows_arm64 │
└───────────────┘
```

```sql
INSTALL spatial;
LOAD spatial;
SELECT ST_Area(ST_GeomFromText('POLYGON((0 0, 4 0, 4 3, 0 3, 0 0))')) AS area;
```

```text
┌────────┐
│  area  │
│ double │
├────────┤
│  12.0  │
└────────┘
```

## Iceberg Improvements

DuckDB v1.4.2 ships a number of improvements for the [`iceberg` extension]({% link docs/stable/core_extensions/iceberg/overview.md %}): insert, update, and delete statements are all supported now:

```sql
CREATE TABLE iceberg_catalog.default.simple_table
    (col1 INTEGER, col2 VARCHAR);

INSERT INTO iceberg_catalog.default.simple_table
    VALUES (1, 'hello'), (2, 'world'), (3, 'duckdb is great');

DELETE FROM iceberg_catalog.default.simple_table
WHERE col1 = 2;

UPDATE iceberg_catalog.default.simple_table
SET col1 = col1 + 5
WHERE col1 = 1;
```

We will publish a separate blog post on these improvements shortly. Stay tuned!

## Fixes for Crashes

We fixed several crashes and internal errors:

* [`duckdb#19238` MERGE into Iceberg table with TIMESTAMPTZ columns crashes](https://github.com/duckdb/duckdb/issues/19238)
* [`duckdb#19355` Unknown expression type invalidates database](https://github.com/duckdb/duckdb/issues/19355)
* [`duckdb#19357` Expected unified vector format of type VARCHAR, but found type INT32](https://github.com/duckdb/duckdb/issues/19357)
* [`duckdb#19455` Merge into failed: logical operator type mismatch](https://github.com/duckdb/duckdb/issues/19455)
* [`duckdb#19498` Window function. Crash with duckdb_pdqsort::pdqsort_detail::pdqsort_loop](https://github.com/duckdb/duckdb/issues/19498)
* [`duckdb#19700` RLE Select bug](https://github.com/duckdb/duckdb/issues/19700)

We also fixed several issues found by our [fuzzer](https://github.com/duckdb/duckdb-fuzzer/):

* [`duckdb-fuzzer#3389`](https://github.com/duckdb/duckdb-fuzzer/issues/3389)
* [`duckdb-fuzzer#4208`](https://github.com/duckdb/duckdb-fuzzer/issues/4208)
* [`duckdb-fuzzer#4296`](https://github.com/duckdb/duckdb-fuzzer/issues/4296)