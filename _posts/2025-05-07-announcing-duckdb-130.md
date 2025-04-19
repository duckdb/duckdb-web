---
layout: post
title: "Announcing DuckDB 1.3.0"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/duckdb-release-1-3-0.svg"
image: "/images/blog/thumbs/duckdb-release-1-3-0.png"
excerpt: "The DuckDB team is happy to announce that today we're releasing DuckDB version 1.3.0, codenamed “CODENAME”."
tags: ["release"]
---

To install the new version, please visit the [installation guide]({% link docs/installation/index.html %}).
For the release notes, see the [release page](https://github.com/duckdb/duckdb/releases/tag/v1.3.0).

> Some packages (Go, R, Java) take a few extra days to release due to the extra changes and reviews required.

We are proud to release DuckDB 1.3.0. This release is codenamed “CODENAME” after ...

## What's New in 1.3.0


### Breaking Changes

[**The release is built using `manylinux_2_28`.**](https://github.com/duckdb/duckdb/pull/16956)
Now that all mainstream distributions use [glibc 2.28](https://lists.gnu.org/archive/html/info-gnu/2018-08/msg00000.html) or newer, we can retire the `_gcc4` special case for Linux binary distributions.

### New Extension Features

* encoding extension
* Iceberg (Amazon S3 Tables, etc.)

### New Feature 1

* [UUIDv7]({% link docs/preview/sql/data_types/numeric.md %}#uuidv7)
* initial value [list_reduce's lambda function]({% link docs/preview/sql/functions/lambda.md %})

### New Feature 2



## Final Thoughts

TODO: conclusions and acknowledgement

These were a few highlights – but there are many more features and improvements in this release.  There have been **over XX commits** by over YY contributors since we released 1.2.2.
The full release notes can be [found on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.3.0).

