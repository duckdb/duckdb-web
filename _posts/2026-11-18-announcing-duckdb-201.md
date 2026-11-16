---
layout: post
title: "Announcing DuckDB 2.0.1 LTS"
authors:
  - The DuckDB team
thumb: "/images/blog/thumbs/duckdb-release-2-0-1.svg"
image: "/images/blog/thumbs/duckdb-release-2-0-1.png"
excerpt: "Today we are releasing DuckDB 2.0.1, the first patch release of our 2.0 LTS line. Along with bugfixes, performance improvements, and security patches, we are shipping Sirius as a new core extension."
tag: release
---

> New Guillermo Sanchez and Pedro Holanda from DuckLabs were recently guests on The New Stack Podcast. Guillermo talked about Quack, DuckDB's client-server protocol, in the episode [“DuckDB Has an Answer to ‘Bloated’ Database Messages”]({% link _library/2026-11-14-duckdb-has-an-answer-to-bloated-database-messages.md %}), while Pedro talked about the DuckLake 1.1 release in [“DuckLake 1.1 Solves the Absurd Complexity of Data Lakes at AI Scale”]({% link _library/2026-11-14-ducklake-11-solves-the-absurd-complexity-of-data-lakes-at-ai-scale.md %}). Check them out!

In this blog post, we highlight a few important fixes in DuckDB 2.0.1, the first patch release in [DuckDB's 2.0 LTS (Cyanoptera) line]({% post_url 2026-10-21-announcing-duckdb-200 %}).
The release ships bugfixes, performance improvements, and security patches. You can find the full [release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v2.0.1).

To install the new version, please visit the [installation page]({% link docs/2.0/installation.html %}).

## Important Fixes

### Silent Data Loss on Affected Linux Kernels

Some Linux kernel versions have a bug ([CVE-2026-97945](https://app.opencve.io/cve/CVE-2026-97945)) that can cause memory freed lazily with `MADV_FREE` to be silently zeroed after it has been reused.
DuckDB 2.0.1 avoids this issue: its bundled allocator no longer frees memory this way ([`#28267`](https://github.com/duckdb/duckdb/pull/28267)).
If you cannot upgrade right away, you can work around the issue by setting the `DUCKDB_JE_MALLOC_CONF` environment variable to `muzzy_decay_ms:0`.

### Reading Databases Written by DuckDB 1.x

DuckDB 2.0.0 could miss rows with `NULL` values when filtering tables in database files written by DuckDB 1.x ([`#28355`](https://github.com/duckdb/duckdb/pull/28355)).
DuckDB 2.0.1 fixes this, along with several issues affecting views, macros, and other objects stored by 1.x versions.

### Security Fixes

We fixed a remote path traversal issue that occurred when external access was disabled.
DuckDB now also refuses to run `CREATE SECRET` statements if `enable_external_access` is set to `false`.
Additionally, this release pulls in a fix for the Brotli decoder (CVE-2026-111497).

> Warning Two changes in this release may require action on your side.
>
> In DuckDB 2.0.0, `UPDATE ... FROM` and `MERGE` statements updated a target row only once if it matched multiple source rows. However, this change caused a significant performance regression, so DuckDB 2.0.1 reverts to the 1.x behavior, where the target row is updated once per match ([`#28701`](https://github.com/duckdb/duckdb/pull/28701)). We plan to ship a proper fix in DuckDB 2.1. In the meantime, we recommend making sure that each target row matches at most one source row.
>
> Secret scopes that end at a host or bucket name now require an exact match or a `/` boundary ([`#28684`](https://github.com/duckdb/duckdb/pull/28684)). For example, the scope `s3://bucket-` no longer matches `s3://bucket-1/`. If a URL contains an explicit port, the scope also needs to include the port.

## New Core Extension: Sirius

DuckDB 2.0.1 adds [Sirius]({% link docs/2.0/core_extensions/sirius.md %}), a GPU-native SQL engine that runs DuckDB queries on NVIDIA GPUs, as a core extension ([`#28022`](https://github.com/duckdb/duckdb/pull/28022)).
Sirius is available on Linux (x86-64 and arm64) and requires an NVIDIA GPU with a CUDA 12 or 13 driver.

To use Sirius, first install and load the extension. Then, you can check its status as follows:

```sql
INSTALL sirius;
LOAD sirius;
FROM sirius_status();
```

When you load Sirius for the first time, it detects your CUDA version and downloads the matching backend, which is about 1 GB.
If a query uses features that Sirius does not support yet, DuckDB falls back to its CPU engine to run it.

## Registering Extension Repositories by Host

DuckDB 2.0.0 introduced [custom extension repositories]({% link docs/2.0/extensions/extension_repositories.md %}), which serve extensions signed with the publisher's own keys.
In DuckDB 2.0.1, you can register such a repository by naming the publisher's host ([`#28719`](https://github.com/duckdb/duckdb/pull/28719)):

```sql
CREATE EXTENSION REPOSITORY extensions.example.org;
INSTALL AND LOAD my_ext FROM extensions.example.org;
```

DuckDB reads the repository's URL from `https://extensions.example.org/.well-known/duckdb-extension-repo.json` over verified HTTPS, then fetches the repository's signing keys and pins them.
The statement returns the SHA-256 fingerprint of each pinned key, so you can compare them against a value published through another channel.
If you would like to publish your own repository, see the new [“Publishing an Extension Repository” page]({% link docs/2.0/extensions/publishing_extension_repositories.md %}).

Unlike adding a repository by its prefix, adding one by its host does not require an opt-in.
To support this, the `allow_extension_repositories` setting has new values: `hosts` (the new default) allows adding repositories by host, `allowed` also allows adding them by prefix, `hosts_only` only adds and trusts repositories resolved from their host, and `forbidden` disables custom repositories.
The previous default value, `undecided`, is no longer accepted.
If only extensions signed by the DuckDB team should be loaded in your environment, set `allow_extension_repositories` to `forbidden`.
For details, see the [“Securing Extensions” page]({% link docs/2.0/operations_manual/securing_duckdb/securing_extensions.md %}#custom-extension-repositories).

## Other Fixes

Here are some other important fixes from the DuckDB 2.0.1 release, organized by category:

### Correctness

* [`#27514`](https://github.com/duckdb/duckdb/pull/27514) – Fix `IS NULL` pruning of Parquet pages with constant string statistics
* [`#27923`](https://github.com/duckdb/duckdb/pull/27923) – Fix `hour`, `minute`, and `second` rounding `TIMESTAMP_NS` values up into the next second
* [`#27779`](https://github.com/duckdb/duckdb/pull/27779) – Fix `LIMIT` being dropped above a join with an aggregate over an empty table
* [`#28698`](https://github.com/duckdb/duckdb/pull/28698) – Fix wrong results when a lateral join reads from a CTE
* [`#28210`](https://github.com/duckdb/duckdb/pull/28210) – Fix random functions returning the same values in processes cloned with `fork()`

### Storage and Transactions

* [`#27764`](https://github.com/duckdb/duckdb/pull/27764) – Keep the rows of bulk inserts invisible to other transactions until commit
* [`#26814`](https://github.com/duckdb/duckdb/pull/26814) – Fix lost index entries when an automatic checkpoint runs after WAL replay
* [`#28190`](https://github.com/duckdb/duckdb/pull/28190) – Fix rows getting lost after a restart that follows a reverted commit

### Crashes and Internal Errors

* [`#28293`](https://github.com/duckdb/duckdb/pull/28293) – Fix crash in `list_select` and `list_where` on empty lists
* [`#27596`](https://github.com/duckdb/duckdb/pull/27596) – Fix window operators hanging when they hit the memory limit
* [`#27936`](https://github.com/duckdb/duckdb/pull/27936) – Fix deadlocks in materialized CTEs

### Performance

* [`#28646`](https://github.com/duckdb/duckdb/pull/28646) – Fix aggregates such as `quantile_cont` and `arg_max` running out of memory on large group-bys
* [`#27760`](https://github.com/duckdb/duckdb/pull/27760) – Push filters on views below subqueries, which can make queries orders of magnitude faster
* [`#27326`](https://github.com/duckdb/duckdb/pull/27326) – Use the [Parquet page index](https://parquet.apache.org/docs/file-format/pageindex/) to skip pages, e.g., in files written by Spark
* [`#28193`](https://github.com/duckdb/duckdb/pull/28193) – Improve join ordering for range joins

### Miscellaneous

* [`#27685`](https://github.com/duckdb/duckdb/pull/27685) – Add the `RETURN_COLUMN_TYPES` option to [`COPY ... TO`]({% link docs/2.0/sql/statements/copy.md %}#copy--to)
* [`#27969`](https://github.com/duckdb/duckdb/pull/27969) – Add the `parquet_can_have_nan` setting for Parquet files whose statistics do not account for `NaN` values
* [`#28011`](https://github.com/duckdb/duckdb/pull/28011) – Ship the Windows CLI as ZIP archives for WinGet

## Extensions and Clients

Several extensions and clients also received a number of patches:

* The [`azure` extension]({% link docs/2.0/core_extensions/azure.md %}) no longer deletes live data files stored at `abfss://⟨container⟩@⟨account⟩` paths when running `CHECKPOINT` on DuckLake ([`duckdb-azure#211`](https://github.com/duckdb/duckdb-azure/pull/211)).
* The [`iceberg` extension]({% link docs/2.0/core_extensions/iceberg/overview.md %}) ships many correctness and performance fixes. For example, TLS now stays enabled when using vended path-style S3 credentials ([`duckdb-iceberg#1527`](https://github.com/duckdb/duckdb-iceberg/pull/1527)). Note that `iceberg_rewrite_data_files` now returns Spark's output column names ([`duckdb-iceberg#1597`](https://github.com/duckdb/duckdb-iceberg/pull/1597)).
* In the [`postgres` extension]({% link docs/2.0/core_extensions/postgres/overview.md %}), queries that only touch a single attached PostgreSQL database are now executed entirely in PostgreSQL. If you would like to disable this, run `SET pg_enable_remote_pushdown = false` before attaching the database ([`duckdb-postgres#643`](https://github.com/duckdb/duckdb-postgres/pull/643)).
* The [Python client]({% link docs/2.0/clients/python/overview.md %}) received fixes for several hangs and crashes at exit, including on Python 3.14 ([`duckdb-python#709`](https://github.com/duckdb/duckdb-python/pull/709), [`duckdb-python#719`](https://github.com/duckdb/duckdb-python/pull/719)). Fetching `TIMESTAMPTZ` values also no longer requires the `pytz` package ([`duckdb-python#710`](https://github.com/duckdb/duckdb-python/pull/710)).
* The [`spatial` extension]({% link docs/2.0/core_extensions/spatial/overview.md %}) is now available in DuckDB-Wasm, and the [`vortex` extension]({% link docs/2.0/core_extensions/vortex.md %}) is now available on Windows.

## End of Life for DuckDB 1.4 LTS

Community support for DuckDB 1.4 LTS (Andium) ended on November 17, 2026.
If you are still using it, we recommend upgrading to DuckDB 2.0 LTS, which is supported until at least October 2027.
For details, see the [release calendar]({% link release_calendar.md %}#lts-releases).

## Conclusion

This post was a short summary of the changes in v2.0.1. As usual, you can find the [full release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v2.0.1).
We would like to thank our contributors for providing detailed issue reports and patches.

We are also grateful to the following people, whose reports helped us make DuckDB more robust when reading malformed or corrupted data:

* [@TristanInSec](https://github.com/TristanInSec) for reporting out-of-bounds reads and a string-length buffer sizing overflow in `DICT_FSST` decompression, and for reporting missing validation of Arrow string offsets.
* [@zerovulnlabs](https://github.com/zerovulnlabs) for reporting missing page-size validation when reading uncompressed Parquet V2 pages.

Stay tuned for [future DuckDB releases]({% link release_calendar.md %}), including v2.1.0 in the first half of 2027!
