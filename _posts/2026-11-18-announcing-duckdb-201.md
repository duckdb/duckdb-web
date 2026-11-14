---
layout: post
title: "Announcing DuckDB 2.0.1 LTS"
authors:
  - The DuckDB team
thumb: "/images/blog/thumbs/duckdb-release-2-0-1.svg"
image: "/images/blog/thumbs/duckdb-release-2-0-1.png"
excerpt: "We are releasing DuckDB 2.0.1, the first patch release of the 2.0 LTS line, with bugfixes, performance improvements, security patches, and Sirius as a new core extension."
tag: release
---

In this blog post, we highlight a few important fixes in DuckDB 2.0.1, the first patch release in [DuckDB's 2.0 LTS (Cyanoptera) line]({% post_url 2026-10-21-announcing-duckdb-200 %}).
You can find the full [release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v2.0.1).

To install the new version, please visit the [installation page]({% link docs/2.0/installation.html %}).

## Important Fixes

**Silent data loss on affected Linux kernels.**
A Linux kernel bug ([CVE-2026-97945](https://app.opencve.io/cve/CVE-2026-97945)) can cause memory freed lazily with `MADV_FREE` to be silently zeroed after reuse.
DuckDB's bundled allocator no longer frees memory this way ([`#28267`](https://github.com/duckdb/duckdb/pull/28267)).
If you cannot upgrade yet, set the `DUCKDB_JE_MALLOC_CONF=muzzy_decay_ms:0` environment variable.

**Reading databases written by DuckDB 1.x.**
DuckDB 2.0.0 could miss `NULL` rows when filtering tables in database files written by DuckDB 1.x ([`#28355`](https://github.com/duckdb/duckdb/pull/28355)).
We also fixed several issues with views, macros, and other objects stored by 1.x versions.

**Security.**
This release fixes remote path traversal when external access is disabled, refuses `CREATE SECRET` when `enable_external_access` is `false`, and pulls in a Brotli decoder fix (CVE-2026-111497).

> Warning Two changes in this release may require action:
>
> * **`UPDATE ... FROM` and `MERGE`:** DuckDB 2.0.0 updated a target row only once if it matched multiple source rows, but this caused a significant performance regression. DuckDB 2.0.1 reverts to the 1.x behavior of updating the row once per match ([`#28701`](https://github.com/duckdb/duckdb/pull/28701)), and we plan a proper fix for DuckDB 2.1. We recommend making sure that each target row matches at most one source row.
> * **Secret scopes:** A scope ending at a host or bucket name now requires an exact match or a `/` boundary ([`#28684`](https://github.com/duckdb/duckdb/pull/28684)), so `s3://bucket-` no longer matches `s3://bucket-1/`. URLs with an explicit port also need the port in the scope.

## New Core Extension: Sirius

DuckDB 2.0.1 adds [Sirius]({% link docs/2.0/core_extensions/sirius.md %}), a GPU-native SQL engine that runs DuckDB queries on NVIDIA GPUs, as a core extension ([`#28022`](https://github.com/duckdb/duckdb/pull/28022)).
Sirius is available on Linux (x86-64 and arm64) and requires an NVIDIA GPU with a CUDA 12 or 13 driver:

```sql
INSTALL sirius;
LOAD sirius;
FROM sirius_status();
```

On first load, Sirius detects your CUDA version and downloads the matching backend, which is about 1 GB.
Queries using features that Sirius does not support yet fall back to DuckDB's CPU engine.

## Fixes

### Correctness

* [`#27514`](https://github.com/duckdb/duckdb/pull/27514) – Fix `IS NULL` pruning of Parquet pages with constant string statistics
* [`#27923`](https://github.com/duckdb/duckdb/pull/27923) – Fix `hour`, `minute`, and `second` on `TIMESTAMP_NS` rounding up into the next second
* [`#27779`](https://github.com/duckdb/duckdb/pull/27779) – Fix `LIMIT` dropped above a join with an aggregate over an empty table
* [`#28698`](https://github.com/duckdb/duckdb/pull/28698) – Fix wrong results when a lateral join reads a CTE
* [`#28210`](https://github.com/duckdb/duckdb/pull/28210) – Fix random functions returning the same values in processes cloned with `fork()`

### Storage and Transactions

* [`#27764`](https://github.com/duckdb/duckdb/pull/27764) – Keep the rows of bulk inserts invisible to other transactions until commit
* [`#26814`](https://github.com/duckdb/duckdb/pull/26814) – Fix lost index entries when an automatic checkpoint runs after WAL replay
* [`#28190`](https://github.com/duckdb/duckdb/pull/28190) – Fix rows lost after a restart following a reverted commit

### Crashes and Internal Errors

* [`#28293`](https://github.com/duckdb/duckdb/pull/28293) – Fix `list_select` and `list_where` crash on empty lists
* [`#27596`](https://github.com/duckdb/duckdb/pull/27596) – Fix window operators hanging when hitting the memory limit
* [`#27936`](https://github.com/duckdb/duckdb/pull/27936) – Fix deadlocks of materialized CTEs

### Performance

* [`#28646`](https://github.com/duckdb/duckdb/pull/28646) – Fix aggregates such as `quantile_cont` and `arg_max` running out of memory on large group-bys
* [`#27760`](https://github.com/duckdb/duckdb/pull/27760) – Push filters on views below subqueries, which can be orders of magnitude faster
* [`#27326`](https://github.com/duckdb/duckdb/pull/27326) – Use the [Parquet page index](https://parquet.apache.org/docs/file-format/pageindex/) to skip pages, e.g., in files written by Spark
* [`#28193`](https://github.com/duckdb/duckdb/pull/28193) – Improve join ordering for range joins

### Miscellaneous

* [`#27685`](https://github.com/duckdb/duckdb/pull/27685) – Add the `RETURN_COLUMN_TYPES` option to [`COPY ... TO`]({% link docs/2.0/sql/statements/copy.md %}#copy--to)
* [`#27969`](https://github.com/duckdb/duckdb/pull/27969) – Add the `parquet_can_have_nan` setting for Parquet files with `NaN` values missing from their statistics
* [`#28011`](https://github.com/duckdb/duckdb/pull/28011) – Ship the Windows CLI as ZIP archives for WinGet

## Extensions and Clients

* **Azure:** Fix `CHECKPOINT` on DuckLake deleting live data files stored at `abfss://⟨container⟩@⟨account⟩` paths ([`duckdb-azure#211`](https://github.com/duckdb/duckdb-azure/pull/211))
* **Iceberg:** Many correctness and performance fixes, including keeping TLS on with vended path-style S3 credentials ([`duckdb-iceberg#1527`](https://github.com/duckdb/duckdb-iceberg/pull/1527)). Note that `iceberg_rewrite_data_files` now returns Spark's output column names ([`duckdb-iceberg#1597`](https://github.com/duckdb/duckdb-iceberg/pull/1597)).
* **PostgreSQL:** Queries that only touch a single attached PostgreSQL database are now executed entirely in PostgreSQL. To disable this, run `SET pg_enable_remote_pushdown = false` before attaching ([`duckdb-postgres#643`](https://github.com/duckdb/duckdb-postgres/pull/643)).
* **Python:** Fix hangs and crashes at exit, including on Python 3.14 ([`duckdb-python#709`](https://github.com/duckdb/duckdb-python/pull/709), [`duckdb-python#719`](https://github.com/duckdb/duckdb-python/pull/719)), and drop the `pytz` requirement for fetching `TIMESTAMPTZ` values ([`duckdb-python#710`](https://github.com/duckdb/duckdb-python/pull/710))
* **Platforms:** The [`spatial` extension]({% link docs/2.0/core_extensions/spatial/overview.md %}) is now available in DuckDB-Wasm and the [`vortex` extension]({% link docs/2.0/core_extensions/vortex.md %}) on Windows

## DuckDB 1.4 Reached End of Life

Community support for DuckDB 1.4 LTS (Andium) ended on November 17, 2026.
If you are still using it, we recommend upgrading to DuckDB 2.0 LTS, which is supported until at least October 2027.
For details, see the [release calendar]({% link release_calendar.md %}#lts-releases).

## Conclusion

This post was a short summary of the changes in v2.0.1. As usual, you can find the [full release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v2.0.1).
We would like to thank our contributors for providing detailed issue reports and patches.

We are grateful to the following people, whose reports helped us make DuckDB more robust when reading malformed or corrupted data:

* [@TristanInSec](https://github.com/TristanInSec) for reporting out-of-bounds reads and a string-length buffer sizing overflow in `DICT_FSST` decompression, and for reporting missing validation of Arrow string offsets.
* [@zerovulnlabs](https://github.com/zerovulnlabs) for reporting missing page-size validation when reading uncompressed Parquet V2 pages.
