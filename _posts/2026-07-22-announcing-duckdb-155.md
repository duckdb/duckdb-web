---
layout: post
title: "Announcing DuckDB 1.5.5"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/duckdb-release-1-5-5.svg"
image: "/images/blog/thumbs/duckdb-release-1-5-5.jpg"
excerpt: "Today we are releasing DuckDB 1.5.5 with bugfixes and performance improvements."
tags: ["release"]
---

In this blog post, we highlight a few important fixes in DuckDB v1.5.5, the sixth patch release in [DuckDB's 1.5 (Variegata) line]({% post_url 2026-03-09-announcing-duckdb-150 %}).
The release ships bugfixes, performance improvements and security patches. You can find the full [release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.5.5).

To install the new version, please visit the [installation page]({% link install/index.html %}).

Here are the most important fixes from the DuckDB v1.5.5 release, organized by category:

## Correctness

* [`#23693`](https://github.com/duckdb/duckdb/pull/23693) – Fix swapped min/max for multi-row-group 128-bit `DECIMAL` in `RETURN_STATS`

### Crashes and Internal Errors

* [`#23517`](https://github.com/duckdb/duckdb/pull/23517) – Fix min/max aggregate stats when row groups are filtered, which caused a crash
* [`#23351`](https://github.com/duckdb/duckdb/pull/23351) – Fix deadlock in `TemporaryMemoryManager`
* [`#23566`](https://github.com/duckdb/duckdb/pull/23566) – Fix C API scalar bind subquery crash
* [`#23757`](https://github.com/duckdb/duckdb/pull/23757) – Fix segfault in external hash aggregate when radix bits grow after going external
* [`#23861`](https://github.com/duckdb/duckdb/pull/23861) – Fix concurrent `ALTER` and `INSERT` crash
* [`#23593`](https://github.com/duckdb/duckdb/pull/23593) – Fixed unsafe iteration when parent is `NULL` in string cast
* [`#23341`](https://github.com/duckdb/duckdb/pull/23341) – Add additional guards to `DICT_FSST` to prevent exception during compression with small block sizes

### Generic Bugfixes

* [`#23458`](https://github.com/duckdb/duckdb/pull/23458) – Fix false RLE corruption error
* [`#23534`](https://github.com/duckdb/duckdb/pull/23534) – Fix Arrow type extension bugs
* [`#23507`](https://github.com/duckdb/duckdb/pull/23507) – Fix `ALTER TABLE ADD COLUMN IF NOT EXISTS ... DEFAULT` regression
* [`#23714`](https://github.com/duckdb/duckdb/pull/23714) – Fix `DROP COLUMN` corrupting per-column metadata block bookkeeping
* [`#23808`](https://github.com/duckdb/duckdb/pull/23808) – Fix `ALTER` dependency preservation in DependencyManager
* [`#23790`](https://github.com/duckdb/duckdb/pull/23790) – `TryLookupEntry` now uses default schema as fallback
* [`#23354`](https://github.com/duckdb/duckdb/pull/23354) – Prevent `NULL MAP` keys in `MultiFileReader` due to missing default values
* [`#23803`](https://github.com/duckdb/duckdb/pull/23803) – Fix malformed JSON when rendering via duckbox
* [`#23879`](https://github.com/duckdb/duckdb/pull/23879) – Fix reset of `empty_range` in the `TIMESTAMP` `range()` table function
* [`#23479`](https://github.com/duckdb/duckdb/pull/23479) – Fix eviction node memory leak when using external files

### Performance

* [`#23483`](https://github.com/duckdb/duckdb/pull/23483) – Enable `ALP` and `ALP_RD` for storage version v1.5.0 and up with smaller block sizes

### Miscellaneous

* [`#21293`](https://github.com/duckdb/duckdb/pull/21293) – Add support for `duckdb://` URI scheme in ADBC
* [`#23230`](https://github.com/duckdb/duckdb/pull/23230) – Support the ADBC Statistics API
* [`#23316`](https://github.com/duckdb/duckdb/pull/23316) – Add request body length to HTTP logs
* [`#23327`](https://github.com/duckdb/duckdb/pull/23327) – Show transport errors in HTTP log
* [`#23752`](https://github.com/duckdb/duckdb/pull/23752) – Include extension header in libduckdb archives

## Conclusion

This post was a short summary of the changes in v1.5.5. As usual, you can find the [full release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.5.5).
We would like to thank our contributors for providing detailed issue reports and patches.
Stay tuned for [future DuckDB releases]({% link release_calendar.md %}), including v2.0.0 in the fall!
