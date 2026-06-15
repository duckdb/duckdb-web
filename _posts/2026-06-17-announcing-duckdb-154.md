---
layout: post
title: "Announcing DuckDB 1.5.4 Variegata"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/duckdb-release-1-5-4.svg"
image: "/images/blog/thumbs/duckdb-release-1-5-4.jpg"
excerpt: "Today we are releasing DuckDB 1.5.4 (Variegata) with bugfixes and performance improvements."
tags: ["release"]
---

> Today we are releasing two DuckDB versions:
> v1.4.5 LTS (Andium) and 
> v1.5.4 (Variegata).
> **This blog post is about the latest non-LTS version, v1.5.4 (Variegata).**

In this blog post, we highlight a few important fixes in DuckDB v1.5.4, the fifth patch release in [DuckDB's 1.5 (Variegata) line]({% post_url 2025-09-16-announcing-duckdb-140 %}).
The release ships bugfixes, performance improvements and security patches. You can find the complete [release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.5.4).

To install the new version, please visit the [installation page]({% link install/index.html %}).

VVV TODO everything below VVV


## Fixes

This version ships a number of performance improvements and bugfixes.

* [`#20233` Function chaining not allowed in QUALIFY #20233](https://github.com/duckdb/duckdb/issues/20233)

### Correctness

* [`#20008` Unexpected Result when Using Utility Function ALIAS #20008](https://github.com/duckdb/duckdb/issues/20008)
* [`#20410` ANTI JOIN produces wrong results with materialized CTEs](https://github.com/duckdb/duckdb/issues/20410)
* [`#20156` Streaming window unions produce incorrect results](https://github.com/duckdb/duckdb/issues/20156)
* [`#20413` ASOF joins with `predicate` fail with different errors for FULL, RIGHT, SEMI, and ANTI join types](https://github.com/duckdb/duckdb/issues/20413)
* [`#20090` mode() produces corrupted UTF-8 strings in parallel execution](https://github.com/duckdb/duckdb/issues/20090)

### Crashes and Internal Errors

* [`#20468` Segfault in Hive partitioning with NULL values](https://github.com/duckdb/duckdb-python/issues/127)
* [`#20086` Incorrect results when using positional joins and indexes](https://github.com/duckdb/duckdb/issues/20086)
* [`#20415` C API data creation causes segfault](https://github.com/duckdb/duckdb/issues/20415)

### Performance

* [`#20252` Optimize prepared statement parameter lookups](https://github.com/duckdb/duckdb/pull/20252)
* [`#20284` dbgen: use TaskExecutor framework to respect the `threads` setting](https://github.com/duckdb/duckdb/pull/20284)

### Miscellaneous

* [`#20233` Function chaining not allowed in QUALIFY #20233](https://github.com/duckdb/duckdb/issues/20233)
* [`#20339` Use UTF-16 console output in Windows shell](https://github.com/duckdb/duckdb/pull/20339)

## Conclusion
