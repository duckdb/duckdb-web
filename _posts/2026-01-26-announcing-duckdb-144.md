---
layout: post
title: "Announcing DuckDB 1.4.4 LTS"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/duckdb-release-1-4-4-lts.svg"
image: "/images/blog/thumbs/duckdb-release-1-4-4-lts.jpg"
excerpt: "Today we are releasing DuckDB 1.4.4 with bugfixes and performance improvements."
tags: ["release"]
---

In this blog post, we highlight a few important fixes in DuckDB v1.4.4, the fourth patch release in [DuckDB's 1.4 LTS line]({% post_url 2025-09-16-announcing-duckdb-140 %}).
The release ships bugfixes, performance improvements and security patches. You can find the complete [release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.4.4).

To install the new version, please visit the [installation page]({% link install/index.html %}).

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

This post was a short summary of the changes in v1.4.4. As usual, you can find the [full release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.4.4).
We would like to thank our contributors for providing detailed issue reports and patches.
In the coming month, we'll release DuckDB v1.5.0.
We'll also keep v1.4 LTS updated until mid-September. We'll announce the release date of v1.4.5 in the [release calendar]({% link release_calendar.md %}) in the coming months.

> Earlier today, we pushed an incorrect tag that was visible for a few minutes.
No binaries or extensions were available under this tag and we replaced it as soon as we noticed the issue.
Our apologies for the erroneous release.
