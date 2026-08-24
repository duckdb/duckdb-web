---
layout: post
title: "Announcing DuckDB 1.5.1"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/duckdb-release-1-5-1.svg"
image: "/images/blog/thumbs/duckdb-release-1-5-1.png"
excerpt: "We are releasing DuckDB version 1.5.1, a patch release with bugfixes, performance improvements and support for the Lance lakehouse format."
tags: ["release"]
---

In this blog post, we highlight a few important fixes in DuckDB v1.5.1, the first patch release in [DuckDB's v1.5 line]({% post_url 2026-03-09-announcing-duckdb-150 %}).
You can find the complete [release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.5.1).

To install the new version, please visit the [installation page]({% link install/index.html %}).

## Data Lake and Lakehouse Formats

### Lance Support

Thanks to the collaboration with LanceDB, DuckDB now supports reading and writing the [Lance lakehouse format](https://github.com/lance-format/lance/) through the [`lance` core extension]({% link docs/current/core_extensions/lance.md %}).

```sql
INSTALL lance;
LOAD lance;
```

You can write to Lance as follows:

```sql
COPY (
    SELECT 1::BIGINT AS id, 'a'::VARCHAR AS s
    UNION ALL
    SELECT 2::BIGINT AS id, 'b'::VARCHAR AS s
) TO 'example.lance' (FORMAT lance);
```

And read it like so:

```sql
SELECT count(*) FROM 'example.lance';
```

```text
┌──────────────┐
│ count_star() │
│    int64     │
├──────────────┤
│            2 │
└──────────────┘
```

> Lance support is also available for DuckDB v1.4.4 LTS and v1.5.0.

### Iceberg Support

We extended support for [Iceberg v3](https://iceberg.apache.org/spec/#version-3) tables, including:

* the [`VARIANT`](https://github.com/duckdb/duckdb-iceberg/pull/474) and [`TIMESTAMP_NS`](https://github.com/duckdb/duckdb-iceberg/pull/765) types
* [default values](https://iceberg.apache.org/spec/#default-values)
* [deletion vectors](https://github.com/duckdb/duckdb-iceberg/pull/728) (delete and update v3 tables)
* [inserting into a partitioned table](https://github.com/duckdb/duckdb-iceberg/pull/744)
* [creating a partitioned table](https://github.com/duckdb/duckdb-iceberg/pull/744)
* [Parquet Copy options support](https://github.com/duckdb/duckdb-iceberg/pull/765)

## Configuration Options

The [`httpfs` extension]({% link docs/current/core_extensions/httpfs/overview.md %}) has a [new setting](https://github.com/duckdb/duckdb-httpfs/pull/285):

```sql
SET force_download_threshold = 2_000_000;
```

This will force full file download on any file < 2 MB.
The default value is 0, but we may revisit the setting default in the next release.

## Fixes

### Globbing Performance

There have been reports by users (thanks!) that S3 globbing performance degraded in certain cases – this has now been [addressed](https://github.com/duckdb/duckdb-httpfs/pull/284).

### Non-Interactive Shell

On Linux and macOS, DuckDB's new CLI had an issue executing the input received through a [non-interactive shell](https://github.com/duckdb/duckdb/issues/21243).
In practice, this meant that scripts piped into DuckDB were not executed.
For v1.5.0, there was a [simple workaround available]({% link docs/current/guides/troubleshooting/command_line.md %}).
We fixed the issue in v1.5.1, so there is no need for a workaround.

### Indexes

This release ships [two](https://github.com/duckdb/duckdb/pull/21270) [fixes](https://github.com/duckdb/duckdb/pull/21427) for [ART indexes]({% link docs/current/sql/indexes.md %}).
If you are using indexes in your workload (directly or through key / unique constraints), we recommend updating to v1.5.1 as soon as possible.

## Landing Page Improvements

We are shipping a new section of the landing page that showcases all the technologies DuckDB can run on... or in! [Check it out!]({% link index.html %}#ecosystem)

## Conclusion

This post is a short summary of the changes in v1.5.1. As usual, you can find the [full release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.5.1).
