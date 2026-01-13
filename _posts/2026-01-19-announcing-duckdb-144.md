---
layout: post
title: "Announcing DuckDB 1.4.4 LTS"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/duckdb-release-1-4-4-lts.svg"
image: "/images/blog/thumbs/duckdb-release-1-4-4-lts.png"
excerpt: "Today we are releasing DuckDB 1.4.4. ..."
tags: ["release"]
---

In this blog post, we highlight a few important fixes in DuckDB v1.4.4, the fourth patch release in [DuckDB's 1.4 LTS line]({% post_url 2025-09-16-announcing-duckdb-140 %}).
You can find the complete [release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.4.4).

To install the new version, please visit the [installation page]({% link install/index.html %}).

## Fixes

This version ships a number of performance improvements and bugfixes.

### Correctness

* [`#18782` Incorrect “rows affected” was reported by ART index](https://github.com/duckdb/duckdb/issues/18782)
...

### Crashes and Internal Errors

* [`#19469` Potential error occurred in constraint violation message when checking foreign key constraints](https://github.com/duckdb/duckdb/issues/19469)
...

### Performance

* [`#18997` Macro binding had slow performance for unbalanced trees](https://github.com/duckdb/duckdb/issues/18997)
...

### Miscellaneous

* [`#19575` Invalid Unicode error with `LIKE` expressions](https://github.com/duckdb/duckdb/issues/19575)
...

## Conclusion

This post was a short summary of the changes in v1.4.4. As usual, you can find the [full release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.4.4).
We would like to thank our contributors for providing detailed issue reports and patches.
In the coming month, we'll release DuckDB v1.5.0.
We'll also keep v1.4 LTS updated until mid-September. We'll announce v1.4.5 in the [release calendar]({% link release_calendar.md %}) in the coming months.
