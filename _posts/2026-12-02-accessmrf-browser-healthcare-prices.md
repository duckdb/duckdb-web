---
layout: post
title: "How AccessMRF Makes 10 TB of Healthcare Pricing Data Queryable in the Browser"
authors:
  - Felix Haba
  - Geertjan Wielenga
thumb: "/images/blog/thumbs/healthcare.svg"
image: "/images/blog/thumbs/healthcare.png"
excerpt: "AccessMRF transforms the US government's Transparency in Coverage dataset—scattered across 200 insurer websites in bulky JSON files—into a queryable, browser-accessible snapshot using DuckDB-Wasm and Frozen DuckLake. By shifting compute to the user's device, Felix Haba has eliminated server-side query costs and made healthcare pricing data usable to anyone, anywhere."
tag: using-duckdb
---

In the United States, federal regulation requires health insurers to publish machine-readable price data, but the result is thousands of large files scattered across different websites with no central repository. Each file is a compressed JSON archive, often gigabytes when unpacked, and not streamable—meaning anyone who wants to analyze them needs expensive server-side compute or must download and process massive datasets locally.

[AccessMRF](https://www.accessmrf.com) started as a metadata catalog that helped researchers and healthcare consultants find these files. Now, thanks to [DuckDB-Wasm]({% link docs/2.0/clients/wasm/overview.md %}) and [Frozen DuckLake](https://duckdb.org/2025/10/24/frozen-ducklake), it has evolved into something more powerful: a browser-based query engine over 10 TB of healthcare pricing data, with no server-side query costs.

## The Problem: Pricing Data That's Hard to Use

The US government's [Transparency in Coverage](https://www.cms.gov/newsroom/fact-sheets-transparency-coverage-final-rules-cms-9882-f) (TiC) initiative mandates that insurers publish negotiated price rates. In theory, this creates a public resource. In practice, the implementation creates barriers.

* **Decentralized:** Around 200 insurers publish data on their own websites in different locations, with no central repository.
* **Large and uncompressed:** Source files are 3 GB compressed and expand to 350 GB or more when uncompressed.
* **Non-streamable:** The JSON format cannot be streamed, so processing requires loading entire files into memory.
* **Gated by commercial tooling:** Most accessible analysis tools are licensed products, creating a paywall that excludes researchers, independent consultants, and smaller employers from the data.

Benefits consultants, healthcare economists, self-funded employers, and researchers have legitimate uses for this data—validating claims, assessing negotiated rates, publishing research—but the practical and economic barriers have made it inaccessible to most.

## The Solution: Frozen DuckLake in the Browser

AccessMRF now transforms the raw TiC data into a [Frozen DuckLake](https://duckdb.org/2025/10/24/frozen-ducklake), a read-only snapshot of the data served over HTTPS. Users query it directly in their browser using [DuckDB-Wasm]({% link docs/2.0/clients/wasm/overview.md %}), which means:

* **No marginal cost:** Query compute happens on the user's device, not on a central server. AccessMRF pays only fixed storage costs, not per-query fees.
* **Instant queries:** Users can slice and analyze 10 TB of pricing data in seconds.
* **No engineering pipeline required:** Experts with SQL knowledge can query the data without building a data engineering infrastructure.

The trade-off is data freshness. The Frozen DuckLake is rebuilt daily via a cron job, creating a lag between when new insurer data arrives and when it becomes queryable. But for most analysis use cases—validating claims, benchmarking rates, publishing research—daily snapshots are sufficient.

## How It Works: From JSON to Browser Query

The pipeline looks like this:

1. **Discover:** AccessMRF's metadata catalog indexes where each insurer publishes its TiC files.
2. **Convert:** Raw JSON files are transformed into [Parquet](https://parquet.apache.org/), organized for efficient querying on specific keys.
3. **Build:** A Frozen DuckLake catalog is assembled using the S3 API for fast file traversal. S3 is faster than HTTPS for packing ~150,000 Parquet files into the catalog.
4. **Publish:** The DuckLake catalog root path is repointed to HTTPS for public access. Because the catalog uses relative paths, this switch is seamless.
5. **Query:** [DuckDB-Wasm]({% link docs/2.0/clients/wasm/overview.md %}) runs in the browser, executing SQL against the published Frozen DuckLake without modifying it. Only the data needed to answer each query is fetched from storage.

This architecture eliminates the need for a managed analytical service like BigQuery, which would require a login, paywall, or usage-based billing that would be prohibitively expensive at public scale.

## Why This Matters

Making public datasets queryable without a paywall removes a barrier to insight. For healthcare specifically:

* **Researchers** can publish analysis of pricing patterns and trends without licensing commercial data platforms.
* **Benefits consultants** can validate claims and benchmark rates for their clients without expensive tools.
* **Self-funded employers** can analyze negotiated rates and assess their plan performance.
* **Healthcare innovators** can build tools and services on top of transparent, accessible data.

And underlying all of this is Felix's core motivation: price uncertainty deters people from seeking preventive care. By making pricing data accessible, it becomes possible for people to make informed healthcare decisions earlier, potentially reducing costs and improving outcomes.

## The Broader Vision

AccessMRF's long-term goal is to become a freely available public resource that improves data quality and enables new healthcare technologies. As more experts and innovators have access to the data, they can identify quality issues, spot patterns, and build services that were impossible when the data was gated behind commercial licensing.

The technology—DuckDB-Wasm and Frozen DuckLake—makes this possible. By shifting compute to the user's device, it eliminates the cost barrier that would otherwise require a business model incompatible with public access.

## Try It Yourself

You can explore AccessMRF's data at [accessmrf.com](https://www.accessmrf.com). If you're a healthcare consultant, researcher, or analyst, try running a query over the 10 TB dataset. The data is public; the barrier to access is no longer financial.

## Further Reading

* [AccessMRF](https://www.accessmrf.com)
* [Felix Haba's work on healthcare price transparency](https://www.felixhaba.com/writing/simplifying-healthcare-price-transparency-files-with-minhashing/)
* [Frozen DuckLakes for Multi-User, Serverless Data Access](https://duckdb.org/2025/10/24/frozen-ducklake)
* [DuckDB-Wasm documentation]({% link docs/2.0/clients/wasm/overview.md %})
* [Transparency in Coverage final rules](https://www.cms.gov/newsroom/fact-sheets-transparency-coverage-final-rules-cms-9882-f)
