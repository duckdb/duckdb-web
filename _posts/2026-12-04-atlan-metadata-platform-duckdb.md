---
layout: post
title: "How Atlan Moved Its Data Platform from Spark and StarRocks to DuckDB on S3"
authors:
  - Mustafa Hasan Khan
  - Geertjan Wielenga
  - Tim Cox
thumb: "/images/blog/thumbs/atlan.svg"
image: "/images/blog/thumbs/atlan.png"
excerpt: "Atlan, the context layer for AI, processes metadata for some of the world’s largest companies, on busy days billions of rows. It moved that work off Spark onto DuckDB running in-process on Parquet files and Iceberg tables in S3, then replaced StarRocks with a DuckDB service on ephemeral compute, cutting costs by about 40%. This is how, and why, Atlan’s data platform is now DuckDB and object storage."
tag: case-study
---

[Atlan](https://atlan.com/) now runs its entire data platform on DuckDB and object storage, handling both analytical and operational workloads. DuckDB runs in-process on Parquet files and Apache Iceberg tables in Amazon S3, a DuckDB service on ephemeral compute has replaced StarRocks at about 40% lower cost, and Atlan’s new AI registry is built on the same foundation. Several of Atlan’s patches are in [DuckDB 2.0]({% post_url 2026-10-21-announcing-duckdb-200 %}).

> Quote
>
> It almost seemed too good to be true: in-process, zero external dependencies, lightweight, and super fast.
>
> — Mustafa Hasan Khan, senior software engineer, Atlan
{: .quote-large}

## What Atlan Does

Atlan is the context layer for AI. It began as a data catalog and lineage tool that pulls metadata from every warehouse, database, and BI tool an organization runs, so data teams can see where a number came from, who owns it, and whether it can be trusted. That problem only grows with the organization, which is why Atlan’s customer base skews toward large enterprises, including Fortune 100 companies.

The same question now comes from AI agents. When an agent answers "what was our churn rate last quarter?", a 200 OK response from the API does not mean the answer is correct because the agent may not know which source it used. Atlan gives agents governed, verifiable context, so that an agent’s output can be traced and checked in the same way as a dashboard. Agents also read that context far more often than people do, and write back what they learn, which puts much more load on the platform underneath.

## Processing Metadata on Spark

Atlan ingests metadata about every data asset in the systems it connects to: technical metadata, usage data, and lineage. Until 2024 all of that processing ran on [Apache Spark](https://spark.apache.org/) with Delta Lake. One of the heaviest parts was building lineage, for which Atlan ingests query history from its customers’ warehouses, billions of rows of it, and works out which tables feed which reports.

Spark was not scaling with the workload. Costs grew with every customer, and the pipelines regularly failed with out-of-memory errors that engineers had to investigate. The workload was batch analytics over files in object storage, and running a distributed cluster for it added cost and operational work the team wanted to avoid.

## Moving to DuckDB

Atlan had been following DuckDB since the 0.2 releases. For a team that wanted to process files in S3 without running a cluster, it fit well: it runs inside the Python process the pipeline already uses, it has no external dependencies, and it reads Parquet from object storage directly. **"It almost seemed too good to be true,"** says Mustafa, a senior software engineer who has been at Atlan for four years and led the migration together with an architect.

The early builds crashed with segmentation faults, and the team filed a series of issues in 2024, some of which led to improvements in DuckDB’s Parquet reader. The approach still suited Atlan: start with a small component running inside the existing process, and add infrastructure only when a workload needs it.

## How the Pipelines Run Today

Atlan’s metadata pipelines now run DuckDB in-process, inside Python workers on Kubernetes pods and [Temporal](https://temporal.io/) workflows. Each worker reads the Parquet files it needs from S3, runs the lineage and processing queries locally, and writes results back to object storage. Atlan does not need to size a cluster or keep a coordinator running, and there is no second system to deploy on a customer’s infrastructure. That matters because many of its enterprise customers want both the platform and the data to stay in their own cloud account, and with DuckDB the data stays there in open formats, Parquet and Iceberg, that other engines can read as well.

Data volumes are the same as before. Across its customer base Atlan processes hundreds of millions of rows on a typical day and billions on the busiest days. According to Mustafa, the pipelines are faster than the Spark versions and cost far less to run.

## Replacing StarRocks and ClickHouse

After the Spark migration, DuckDB became Atlan’s default choice for any workload that reads or writes S3, and the company has since replaced other systems with it.

The most recent was [StarRocks](https://www.starrocks.io/). With DuckDB already running the pipelines, Atlan wanted a single engine for processing and serving, and an isolated instance per tenant rather than a shared cluster. In October it shut down its StarRocks clusters. It now runs an in-house service based on DuckDB on ephemeral compute that reads and writes object storage directly. Costs fell by about 40%.

Atlan is also replacing [ClickHouse](https://clickhouse.com/) for trace storage with a design that writes from DuckDB directly to object storage, because it is faster on Atlan’s workload and easier to deploy. The new AI registry, built on AWS, uses DuckDB to read and write S3, with [Apache Iceberg](https://iceberg.apache.org/) tables and an Iceberg REST catalog on top. Atlan can still be deployed on any cloud, but its data platform now consists of DuckDB and object storage, handling both analytical and operational workloads.

## Contributing to DuckDB 2.0

Atlan is already running the [DuckDB 2.0]({% post_url 2026-10-21-announcing-duckdb-200 %}) alpha internally and plans to ship its next data-platform release on it, having seen no regressions compared with the 1.x release it used before. 

Mustafa has had several pull requests merged for 2.0:

* aggregates whose state holds strings or lists now spill to disk instead of failing with an out-of-memory error ([#24499](https://github.com/duckdb/duckdb/pull/24499))
* an opt-in setting lets the external file cache write evicted blocks of remote files to the temporary directory, so that a later query reads them back from local disk rather than fetching them from S3 again ([#24062](https://github.com/duckdb/duckdb/pull/24062))
* JSON functions for in-place edits: `json_set`, `json_insert`, `json_replace`, `json_remove` ([#23786](https://github.com/duckdb/duckdb/pull/23786))
* JSON functions for merge-patch diffs, normalization, deep merging, and stripping nulls ([#21668](https://github.com/duckdb/duckdb/pull/21668), [#21531](https://github.com/duckdb/duckdb/pull/21531), [#21748](https://github.com/duckdb/duckdb/pull/21748)), covered in [Reconciling JSON in DuckDB, One Patch at a Time]({% post_url 2026-08-18-reconciling-json %})

For example, setting one field of a metadata document in place:

```sql
SELECT json_set('{"name": "orders", "owner": "finance"}', '$.certificate', '"VERIFIED"') AS updated;
```

```text
{"name":"orders","owner":"finance","certificate":"VERIFIED"}
```

And computing the patch that turns one version of a document into the next:

```sql
SELECT json_merge_patch_diff(
    '{"name": "orders", "owner": "finance", "tags": ["pii"]}',
    '{"name": "orders", "owner": "sales"}'
) AS patch;
```

```text
{"tags":null,"owner":"sales"}
```

The external file cache setting is off by default and is turned on with:

```sql
SET external_file_cache_spill = true;
```

Atlan’s next proposals concern its heaviest workload, Iceberg on S3: better manifest fetching and caching, fewer round trips to object storage, and improved filter pushdown in the Iceberg scanner.

Those improvements reach Atlan’s customers directly as well. Atlan’s [Lakehouse](https://docs.atlan.com/platform/lakehouse/connect-query-engines) exposes each customer’s metadata through an Iceberg REST catalog, and DuckDB is one of the engines they can query it with.

We would like to thank Mustafa for the conversation. If you are reading this, are using DuckDB, and would like to share your story, drop us a line at [geertjan@ducklabs.com](mailto:geertjan@ducklabs.com).

## About Atlan

[Atlan](https://atlan.com/) is the context layer for AI. It connects to the warehouses, databases, and BI tools an organization runs and turns their metadata, lineage, and business definitions into governed context that people and AI agents can both use.

