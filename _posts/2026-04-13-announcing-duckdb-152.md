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

We are proud to release a stable, production-ready lakehouse specification and its reference implementation in DuckDB.

We published a [detailed blog post on the DuckLake site](https://ducklake.select/2026/04/13/ducklake-10/) but here's a quick summary: DuckLake v1.0 ships dozens of bugfixes and guarantees backward-compatibility. Additionally, it has a number of cool features: [data inlining](https://ducklake.select/2026/04/02/data-inlining-in-ducklake/), sorted tables, bucket partitioning, and deletion buffers as Iceberg-compatible Puffin files. More on this in the [announcement blog post](https://ducklake.select/2026/04/13/ducklake-10/).

### Iceberg

The [Iceberg extension]({% link docs/current/core_extensions/iceberg/overview.md %}) ships a number of new features. It now supports the following:

* `GEOMETRY` type
* `ALTER TABLE` statement
* Updates and deletes from [partitioned tables](https://iceberg.apache.org/docs/latest/partitioning/)
* Truncate and bucket partitions

Last week, DuckLabs engineer Tom Ebergen gave a talk at the [Iceberg Summit](https://www.icebergsummit.org/) titled [“Building DuckDB-Iceberg: Exploring the Iceberg Ecosystem”]({% link _library/2026-04-08-building-duckdb-iceberg-exploring-the-iceberg-ecosystem.md %}), where he shared his experiences with Iceberg.

## Preliminary Jepsen Test Results

To make DuckDB as robust as possible, we started a collaboration with [Jepsen](https://jepsen.io/). The preliminary test suite is available at [https://github.com/duckdb/duckdb-jepsen](https://github.com/duckdb/duckdb-jepsen).

The test suite has uncovered a bug that was triggered by `INSERT INTO` statements that perform conflict resolution on a primary key, and already [shipped a fix](https://github.com/duckdb/duckdb/pull/21489) in this release.

## New Online Shell

The online [WebAssembly]({% link docs/current/clients/wasm/overview.md %}) shell at [`shell.duckdb.org`](https://shell.duckdb.org/) received a complete overhaul.
A highlight of the new shell is the ability to store and list files using the `.files` dot command and its variants.

Using the file storage feature, you can turn your browser session into workbench: you can drag-and-drop files from your local file system to upload them, create new ones using DuckDB's [`COPY ... TO` statement]({% link docs/current/sql/statements/copy.md %}#copy--to) and download the results. For more information on this feature, use the `.help` command.

<!--
<img src="{% link images/blog/online-shell-example.png %}" alt="Example use of the new online shell at shell.duckdb.org" width="800" />
-->

The new shell comes with a few built-in datasets: you're welcome to try them out and experiment.
Your old links to `shell.duckdb.org` should still work but if you experience any problems, please submit an issue in the [`duckdb-web` repository](https://github.com/duckdb/duckdb-wasm).

## Benchmarks

We benchmarked DuckDB using the Linux v7 kernel on an [r8gd.8xlarge](https://instances.vantage.sh/aws/ec2/r8gd.8xlarge?currency=USD) instance with 32 vCPUs, 256 GiB RAM, and an NVMe SSD.
We first ran the scale factor 300 test on Ubuntu 24.04 LTS, then upgraded to Ubuntu 26.04 beta.
We noticed that the composite TPC-H score shows a **~10% improvement**, jumping from 778,041 to 854,676 when measured with TPC-H's QphH@Score metric.

## Coming Up

This quarter, we have quite a few exciting events lined up.

**DuckCon #7.** On June 24, we'll host our next user conference, [DuckCon #7]({% link _events/2026-06-24-duckcon7.html %}), in Amsterdam's beautiful [Royal Tropical Institute](https://www.kit.nl/about-us/).

**AI Council Talk.** On May 12, DuckDB co-creator Hannes Mühleisen will give a talk at AI Council 2026 titled [“Super-Secret Next Big Thing for DuckDB”]({% link _library/2026-05-12-super-secret-next-big-thing-for-duckdb.md %}). Well, at this point, we cannot tell you more than he will present the super-secret next big thing for DuckDB. But, if you cannot make it, don't worry: we'll publish the presentation afterwards.

**Ubuntu Summit Talk.** We already talked about performance on Ubuntu. In late May, Gábor Szárnyas of DuckLabs will give a talk titled [“DuckDB: Not Quack Science”]({% link _library/2026-05-27-duckdb-not-quack-science.md %}) at the [Ubuntu Summit](https://ubuntu.com/summit).

## Conclusion

This post is a short summary of the changes in v1.5.2. As usual, you can find the [full release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v1.5.2).
