---
layout: post
title: "Announcing DuckDB 1.5.4 Variegata"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/duckdb-release-1-5-4.svg"
image: "/images/blog/thumbs/duckdb-release-1-5-4.jpg"
excerpt: "Today we are releasing DuckDB 1.5.4 (Variegata) with bugfixes and performance improvements."
tags: ["release"]
---

> We are simultaneously releasing two DuckDB versions:
> v1.4.5 LTS (Andium) and 
> v1.5.4 (Variegata).
> **This blog post is about the latest non-LTS version, v1.5.4 (Variegata).**
> For the LTS version, read the [v1.4.5 (Andium) announcement]({% post_url 2026-06-17-announcing-duckdb-145 %}).

In this blog post, we highlight a few important fixes in DuckDB v1.5.4, the fifth patch release in [DuckDB's 1.5 (Variegata) line]({% post_url 2025-09-16-announcing-duckdb-140 %}).
The release ships bugfixes, performance improvements and security patches. You can find the full [release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.5.4).

To install the new version, please visit the [installation page]({% link install/index.html %}).

## Fixes

This version ships a number of performance improvements and bugfixes.

## Correctness

* [#23031](https://github.com/duckdb/duckdb/pull/23031) – Fix VARIANT cast reading wrong rows under a filter
* [#23014](https://github.com/duckdb/duckdb/pull/23014) – MERGE INTO: only consider target table when binding `WHEN NOT MATCHED` and source table when binding `WHEN NOT MATCHED BY TARGET`
* [#22825](https://github.com/duckdb/duckdb/pull/22825) – Fix case-insensitive column match in INSERT ... SELECT ON CONFLICT
* [#22911](https://github.com/duckdb/duckdb/pull/22911) – Use non-deleted row count in `RowGroupReorderer`
* [#23194](https://github.com/duckdb/duckdb/pull/23194) – Fix variant shredding analysis logic discrepancy with shredded writing
* [#23234](https://github.com/duckdb/duckdb/pull/23234) – Fix problem with re-use of cached transform data for differently shredded files
* [#22844](https://github.com/duckdb/duckdb/pull/22844) – Window Self-Join Limits: don't apply the self-join optimisation more than once

## Crashes and Internal Errors

* [#21854](https://github.com/duckdb/duckdb/pull/21854) – Fix double free and memory leak in Arrow GeoArrow CRS serialization
* [#22836](https://github.com/duckdb/duckdb/pull/22836) – Fix progress bar output and crash when piping SQL
* [#23174](https://github.com/duckdb/duckdb/pull/23174) – Fix crash when storage path is not set
* [#23232](https://github.com/duckdb/duckdb/pull/23232) – Fix gzip compression write overflow
* [#23156](https://github.com/duckdb/duckdb/pull/23156) – Avoid trying to bind an expression that doesn't exist in `UNPIVOT`
* [#23189](https://github.com/duckdb/duckdb/pull/23189) – Guard against null row group reorder stats

## Generic Bugfixes

* [#22855](https://github.com/duckdb/duckdb/pull/22855) – Fix json_keys with wildcard paths
* [#23144](https://github.com/duckdb/duckdb/pull/23144) – Fix json argument order affecting result
* [#23116](https://github.com/duckdb/duckdb/pull/23116) – Reject NULL json key
* [#23137](https://github.com/duckdb/duckdb/pull/23137) – Fix `ignore_errors` silently accepting invalid JSON
* [#22882](https://github.com/duckdb/duckdb/pull/22882) – Fix geometry stats checkpointing when no changes are detected
* [#22815](https://github.com/duckdb/duckdb/pull/22815) – Render MAP values as valid SQL in `Value::ToSQLString()`
* [#23254](https://github.com/duckdb/duckdb/pull/23254) – Fix NULL propagation for date parts of infinite dates
* [#23190](https://github.com/duckdb/duckdb/pull/23190) – Fix selection vector use in Arrow extension callbacks

## Performance

* [#23253](https://github.com/duckdb/duckdb/pull/23253) – Trim the system heap in the allocator flush path on jemalloc builds
* [#23140](https://github.com/duckdb/duckdb/pull/23140) – Fix native geometry Parquet stats pruning and add `OPERATOR_ROW_GROUPS_SCANNED` to Parquet reader

## Miscellaneous

* [#23246](https://github.com/duckdb/duckdb/pull/23246) – Add explicit `-dark-mode` and `-light-mode` options to the CLI, and improve terminal background color detection
* [#23100](https://github.com/duckdb/duckdb/pull/23100) – Add hardening to many DuckDB/Parquet decompression and deserializing paths
* [#22690](https://github.com/duckdb/duckdb/pull/22690) – Add `vacuum_rebuild_indexes` as an (experimental) ATTACH option

## Conclusion

This post was a short summary of the changes in v1.5.4. As usual, you can find the [full release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.5.4).
We would like to thank our contributors for providing detailed issue reports and patches.
Stay tuned for [future DuckDB releasese]({% link release_calendar.md %}), including v2.0.0 in the fall!
