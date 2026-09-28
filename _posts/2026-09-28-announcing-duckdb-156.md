---
layout: post
title: "Announcing DuckDB 1.5.6"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/duckdb-release-1-5-6.svg"
image: "/images/blog/thumbs/duckdb-release-1-5-6.png"
excerpt: "Today we are releasing DuckDB 1.5.6 with bugfixes and performance improvements."
tags: ["release"]
---

In this blog post, we highlight a few important fixes in DuckDB v1.5.6, the seventh patch release in [DuckDB's 1.5 (Variegata) line]({% post_url 2026-03-09-announcing-duckdb-150 %}).
The release ships bugfixes, performance improvements and security patches. You can find the full [release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.5.6).

To install the new version, please visit the [installation page]({% link install/index.html %}).

Here are the most important fixes from the DuckDB v1.5.6 release, organized by category:

## Correctness

* [`#24240`](https://github.com/duckdb/duckdb/pull/24240) – Fix `LIMIT` pushdown through a volatile projection with an `OFFSET`
* [`#24239`](https://github.com/duckdb/duckdb/pull/24239) – Don't push filters on volatile groups through aggregates
* [`#24119`](https://github.com/duckdb/duckdb/pull/24119) – Fix `UNNEST` pushdown
* [`#24399`](https://github.com/duckdb/duckdb/pull/24399) – Preserve `NULL`s in Top-N window elimination when the `ORDER BY` expression has no column references
* [`#24551`](https://github.com/duckdb/duckdb/pull/24551) – Fix Top-N window elimination for nullable ordering expressions
* [`#25831`](https://github.com/duckdb/duckdb/pull/25831) – Fix wrong results from common subplan elimination with `UNION ALL` arms sharing a join subtree
* [`#25714`](https://github.com/duckdb/duckdb/pull/25714) – Fix silent truncation of very long integer literals into `HUGEINT`
* [`#25766`](https://github.com/duckdb/duckdb/pull/25766) – Fix `max` on Hive partition column after file pruning
* [`#24438`](https://github.com/duckdb/duckdb/pull/24438) – Fix ICU `strptime` leaking time zone state between rows
* [`#24845`](https://github.com/duckdb/duckdb/pull/24845) – Fix `GEOMETRY` row group pruning with `NULL`s and empty geometries
* [`#25728`](https://github.com/duckdb/duckdb/pull/25728) – Fix reading and writing `TIME_NS` values in Parquet
* [`#26027`](https://github.com/duckdb/duckdb/pull/26027) – Fix Parquet v2 value count mismatch for `NULL`s in a list that fills a page
* [`#26162`](https://github.com/duckdb/duckdb/pull/26162) – Fix Parquet `VARIANT` shredding for `REQUIRED` fields and element groups

### Crashes and Internal Errors

* [`#25103`](https://github.com/duckdb/duckdb/pull/25103) – Fix crash in Top-N with `LIMIT 0`
* [`#24427`](https://github.com/duckdb/duckdb/pull/24427) – Fix segfault in `url_decode` with `TRY()` on dictionary-encoded columns
* [`#24447`](https://github.com/duckdb/duckdb/pull/24447) – Fix failed checkpoint marker recovery
* [`#25490`](https://github.com/duckdb/duckdb/pull/25490) – Close the main WAL handle before renaming over it during WAL recovery

### Generic Bugfixes

* [`#24065`](https://github.com/duckdb/duckdb/pull/24065) – Automatically roll back failed implicitly-wrapped multi-statements on all paths
* [`#25693`](https://github.com/duckdb/duckdb/pull/25693) – Fix dead node counting in ART indexes
* [`#25573`](https://github.com/duckdb/duckdb/pull/25573) – Report the real storage version when opening a DuckDB v2.0+ database file
* [`#25808`](https://github.com/duckdb/duckdb/pull/25808) – Reject invalid UTF-8 produced by `printf`'s `%c` conversion

### Miscellaneous

* [`#26102`](https://github.com/duckdb/duckdb/pull/26102) – Add `enable_optimistic_write` setting
* [`#25283`](https://github.com/duckdb/duckdb/pull/25283) – Harden temporary file reads
* [`#24362`](https://github.com/duckdb/duckdb/pull/24362) – Unify C API symbol versioning for clients and extensions, stabilize all v1 APIs
* [`#25214`](https://github.com/duckdb/duckdb/pull/25214) – Always quote identifiers in error messages
* [`#24127`](https://github.com/duckdb/duckdb/pull/24127) – Remove the Julia client from the main repository in favor of [`duckdb/DuckDB.jl`](https://github.com/duckdb/DuckDB.jl)

## Conclusion

This post was a short summary of the changes in v1.5.6. As usual, you can find the [full release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.5.6).
We would like to thank our contributors for providing detailed issue reports and patches.
Stay tuned for [future DuckDB releases]({% link release_calendar.md %}), including v2.0.0 in October!
