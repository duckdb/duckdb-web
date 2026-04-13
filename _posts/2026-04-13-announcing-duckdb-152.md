---
layout: post
title: "Announcing DuckDB 1.5.2"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/duckdb-release-1-5-2.svg"
image: "/images/blog/thumbs/duckdb-release-1-5-2.png"
excerpt: "We are releasing DuckDB version v1.5.2, a patch release with bugfixes and performance improvements, and support for the DuckLake v1.0 lakehouse format."
tags: ["release"]
---

In this blog post, we highlight a few important fixes in DuckDB v1.5.2, the second patch release in [DuckDB's v1.5 line]({% post_url 2026-03-09-announcing-duckdb-150 %}).
You can find the complete [release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.5.2).

To install the new version, please visit the [installation page]({% link install/index.html %}).

## Data Lake and Lakehouse Formats

### DuckLake

We are proud to release a stable, production-ready lakehouse specification and its reference implementation in DuckDB. We will publish a detailed post on the DuckLake blog in the coming hours, but until then, here's a quick summary: DuckLake v1.0 ships dozens of bugfixes and guarantees backward-compatibility.

### Iceberg

The [Iceberg extension]({% link docs/current/core_extensions/iceberg/overview.md %}) ships a number of new features. It now supports the following:

* `GEOMETRY` type
* `ALTER TABLE` statement
* Updates and deletes from [partitioned tables](https://iceberg.apache.org/docs/latest/partitioning/)
* Truncate and bucket partitions

Last week, DuckDB Labs engineer Tom Ebergen gave a talk at the [Iceberg Summit](https://www.icebergsummit.org/) titled [“Building DuckDB-Iceberg: Exploring the Iceberg Ecosystem”]({% link _library/building-duckdb-iceberg-exploring-the-iceberg-ecosystem.md %}), where he shared his experiences with Iceberg.

## Preliminary Jepsen Test Results

To make DuckDB as robust as possible, we started a collaboration with [Jepsen](https://jepsen.io/). The preliminary test suite is available at [https://github.com/duckdb/duckdb-jepsen](https://github.com/duckdb/duckdb-jepsen).

The test suite has uncovered a bug that was triggered by `INSERT INTO` statements that perform conflict resolution on a primary key, and already [shipped a fix](https://github.com/duckdb/duckdb/pull/21489) in this release.

## Benchmarks

We benchmarked DuckDB using the Linux v7 kernel on an [r8gd.8xlarge](https://instances.vantage.sh/aws/ec2/r8gd.8xlarge?currency=USD) instance with 32 vCPUs, 256 GiB RAM, and an NVMe SSD.
We first ran the scale factor 300 test on Ubuntu 24.04 LTS, then upgraded to Ubuntu 26.04 beta.
We noticed that the composite TPC-H score shows a **~10% improvement**, jumping from 778,041 to 854,676 when measured with TPC-H's QphH@Score metric.

## Coming Up

This quarter, we have quite a few exciting events lined up.

### DuckCon #7

On June 24, we'll host our next user conference, [DuckCon #7]({% link _events/2026/06/24/duckcon7.md %}), in Amsterdam's beautiful [Royal Tropical Institute](https://www.kit.nl/about-us/). If you have been building cool things with DuckDB, consider submitting a talk until April 22. Registrations are also open – and free!

### AI Council Talk

On May 12, DuckDB co-creator Hannes Mühleisen will give a talk at AI Council 2026 titled [“Super-Secret Next Big Thing for DuckDB”]({% link _library/super-secret-next-big-thing-for-duckdb.md %}). Well, at this point, we cannot tell you more than he will present the super-secret next big thing for DuckDB. But, if you cannot make it, don't worry: we'll publish the presentation afterwards.

### Ubuntu Summit Talk

We already talked about performance on Ubuntu. In late May, Gábor Szárnyas of DuckDB Labs will give a talk titled “DuckDB: Not Quack Science” at the [Ubuntu Summit in London]({% link _library/duckdb-not-quack-science.md %}).

### New DuckDB Releases

We plan to release a patch version of the DuckDB v1.4 LTS line, v1.4.5. We will also release DuckDB v1.5.3 in the coming months.

## Conclusion

This post is a short summary of the changes in v1.5.2. As usual, you can find the [full release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.5.2).
