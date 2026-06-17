---
layout: post
title: "Announcing DuckDB 1.4.5 LTS (Andium)"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/duckdb-release-1-4-5-lts.svg"
image: "/images/blog/thumbs/duckdb-release-1-4-5-lts.jpg"
excerpt: "Today we are releasing DuckDB 1.4.5 LTS with bugfixes and performance improvements."
tags: ["release"]
---

> We are simultaneously releasing two DuckDB versions:
> v1.4.5 LTS (Andium) and 
> v1.5.4 (Variegata).
> **This blog post is about the LTS version, v1.4.5 (Andium).**
> For the latest stable version, read the [v1.5.4 (Variegata) announcement]({% post_url 2026-06-17-announcing-duckdb-154 %}).

In this blog post, we highlight a few important fixes in DuckDB v1.4.5, the sixth patch release in [DuckDB's 1.4 LTS line]({% post_url 2025-09-16-announcing-duckdb-140 %}).
The release ships bugfixes, performance improvements and security patches. You can find the complete [release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.4.5).

To install the new version, please visit the [installation page]({% link install/index.html %}#version=lts).

## Fixes

### Generic Bugfixes

* [`#20760`](https://github.com/duckdb/duckdb/pull/20760) – Fix escape handling in `AddEscapes` function
* [`#21316`](https://github.com/duckdb/duckdb/pull/21316) – Fix unbounded row group growth for indexed tables on repeated load and insert cycles
* [`#21577`](https://github.com/duckdb/duckdb/pull/21577) – Fix for CSV reader buffer-boundary value read
* [`#20686`](https://github.com/duckdb/duckdb/pull/20686) – Secret Manager: Ensure secrets are created exactly once
* [`#23197`](https://github.com/duckdb/duckdb/pull/23197) – Backport out-of-bounds security fixes from [`#23100`](https://github.com/duckdb/duckdb/pull/23100)

### Correctness

* [`#21482`](https://github.com/duckdb/duckdb/pull/21482) – Correctly detect overflows when decoding integers from storage
* [`#21177`](https://github.com/duckdb/duckdb/pull/21177) – Backport support for the `* NOT SIMILAR TO 'pattern'` from [`#19232`](https://github.com/duckdb/duckdb/pull/19232)

### Crashes and Internal Errors

* [`#20804`](https://github.com/duckdb/duckdb/pull/20804) – Backport various race condition fixes from [`#20803`](https://github.com/duckdb/duckdb/pull/20803)

### Performance

* [`#21090`](https://github.com/duckdb/duckdb/pull/21090) – AsOf Simple Joins improvements
* [`#21178`](https://github.com/duckdb/duckdb/pull/21178) – Backport zstd improvements from [`#20943`](https://github.com/duckdb/duckdb/pull/20943)

### Miscellaneous

* [`#23130`](https://github.com/duckdb/duckdb/pull/23130) – Backport GetLocalFileSystem improvements from [`#21983`](https://github.com/duckdb/duckdb/pull/21983)
* [`#20727`](https://github.com/duckdb/duckdb/pull/20727) – Use FileSystem APIs in QueryProfiler::Write

## Conclusion

This post was a short summary of the changes in v1.4.5. As usual, you can find the [full release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.4.5).
We would like to thank our contributors for providing detailed issue reports and patches.
Stay tuned for [future DuckDB releasese]({% link release_calendar.md %}), including v2.0.0 in the fall!
