---
layout: post
title: "Announcing DuckDB 1.4.3 LTS"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/duckdb-release-1-4-3-lts.svg"
image: "/images/blog/thumbs/duckdb-release-1-4-3-lts.png"
excerpt: "Today we are releasing DuckDB 1.4.3."
tags: ["release"]
---

In this blog post, we highlight a few important fixes in DuckDB v1.4.3, the third patch release in [DuckDB's 1.4 LTS line]({% post_url 2025-09-16-announcing-duckdb-140 %}).
You can find the complete [release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.4.3).

To install the new version, please visit the [installation page]({% link install/index.html %}).

## Windows ARM64

### Python Wheel Distribution for Windows ARM64

We now distribute Python wheels for Windows ARM64. This means that you take e.g. a Copilot+ laptop and run:

```bash
pip install duckdb
```

v1.4.4 is expected to also ship [extensions for Windows ARM64](https://github.com/duckdb/duckdb/pull/20004).

## Fixes

This version ships a few fixes:

* [`#19754` Rare segfault occurring in the encryption key cache](https://github.com/duckdb/duckdb/issues/19754)
* [`#19884` Copying to Parquet with a prepared statement did not work](https://github.com/duckdb/duckdb/issues/19884)
* [`#19469` Potential error in constraint violation message when checking foreign key constraints](https://github.com/duckdb/duckdb/issues/19469)
* [`#18997` Macro binding had slow performance for unbalanced trees](https://github.com/duckdb/duckdb/issues/18997)
* [`#19916` The default timezone of DuckDB Wasm in a browser had an offset inverted from what it should be](https://github.com/duckdb/duckdb/issues/19916)
* [`#19313` Wrong result in cornercase: a `HAVING` clause without a `GROUP BY` returned an incorrect result](https://github.com/duckdb/duckdb/issues/19313)
* [`#19924` The optimizer incorrectly removed the `ORDER BY` from aggregates](https://github.com/duckdb/duckdb/issues/19924)
* [`#19517` `JOIN` with a `LIKE` pattern resulted in columns being incorrectly included](https://github.com/duckdb/duckdb/issues/19517)
* [`#18782` Incorrect “rows affected” reported by ART index](https://github.com/duckdb/duckdb/issues/18782)
* [`#19575` Invalid Unicode error with `LIKE` expressions](https://github.com/duckdb/duckdb/issues/19575)

This was a short summary but there have been XX commits by over YY contributors since we v1.4.2. As usual, the full release notes can be [found on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.4.4). We would like to thank our contributors for providing detailed issue reports and patches!
