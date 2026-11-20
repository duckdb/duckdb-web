---
layout: post
title: "Announcing DuckDB 2.0.1 LTS"
authors:
  - The DuckDB team
thumb: "/images/blog/thumbs/duckdb-release-2-0-1.svg"
image: "/images/blog/thumbs/duckdb-release-2-0-1.png"
excerpt: "Today we are releasing DuckDB 2.0.1, the first patch release of our 2.0 LTS line. This release ships bugfixes, performance improvements, and security patches. In addition, a capability is added to define custom extension repositories with only their hostname."
tag: release
---

Today we're releasing DuckDB 2.0.1, the first patch release in the [2.0 LTS (Cyanoptera) line]({% post_url 2026-10-21-announcing-duckdb-200 %}). This planned release arrives one month after 2.0.0 and contains bugfixes, performance improvements, and security patches. In addition, it provides a more convenient way of registering custom extension repositories.

You can obtain a copy from the [installation page]({% link docs/2.0/installation.html %}). For a detailed overview of the changes, see the [release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v2.0.1). Read on for some highlights.

## Changes That May Require Action

A few fixes in this release change existing behavior. In each case, the previous behavior was incorrect or a security risk, so we chose to fix it in 2.0.1 rather than wait for the next major release. If you rely on any of the behaviors below, review them before upgrading.

### Stricter `SECRET` Scope Matching

A `SECRET` scoped to a host or bucket could also match other hosts or buckets with the same prefix, so it could be sent somewhere it wasn't meant for ([`#28684`](https://github.com/duckdb/duckdb/pull/28684)). A URL now matches such a scope only if it is identical to the scope or continues with a `/`. For example, the scope `s3://bucket-` no longer matches `s3://bucket-1/`.

**Action:** check your host- and bucket-scoped `SECRET`s and make sure each scope uses the full host or bucket name. If a URL has an explicit port, the scope must include it too.

### `UPDATE ... FROM` and `MERGE` Again Apply Every Match

In DuckDB 2.0.0, if several source rows matched the same target row, `MERGE` raised an error and `UPDATE ... FROM` updated the target row once, using one of the matches. Enforcing this behavior serialized large updates, causing a significant performance regression.

DuckDB 2.0.1 restores the 1.x behavior for both statements ([`#28701`](https://github.com/duckdb/duckdb/pull/28701)): the target row is updated once per match, so the final value can be non-deterministic, and the row is counted and returned (with `RETURNING`) once per match.

**Action:** review your `UPDATE ... FROM` and `MERGE` statements. To keep updates deterministic, make sure each target row is matched by at most one source row, or that all matching source rows have identical values for the updated columns.

We expect a fix that keeps both correctness and performance in DuckDB 2.1.

## Improvement: Registering Extension Repositories by Host

DuckDB 2.0.0 introduced [custom extension repositories]({% link docs/2.0/extensions/installing_extensions.md %}#extension-repositories), which host extensions signed with the publisher's own keys.
In DuckDB 2.0.1, you can register such a repository by naming the publisher's host ([`#28719`](https://github.com/duckdb/duckdb/pull/28719)).
For example, you can register `duckdb.org` as a repository:

```sql
CREATE EXTENSION REPOSITORY duckdb.org;
```

Then, core extensions are reachable through it:

```sql
INSTALL AND LOAD spatial FROM duckdb.org;
```

Under the hood, the host acts as an extra redirect.
DuckDB first reads `https://duckdb.org/.well-known/duckdb-extension-repo.json` over verified HTTPS.
This file contains no keys or extensions: it only states where the host's repository lives, in this case, `https://extensions.duckdb.org`.
DuckDB then follows this pointer, reads the repository's own `.well-known/duckdb-extension-repo.json` file, and pins the signing keys listed there.
Only the owner of a host can publish files under its `.well-known` path, so serving this file is proof of control over the host, and no central registry is involved.
The redirect also decouples the repository's name from its location: the name can be your organization's domain, while the extensions are served from a CDN, an S3 bucket, or GitHub Pages.
The `CREATE EXTENSION REPOSITORY` statement returns the SHA-256 fingerprint of each pinned key, so you can compare them against values published through another channel.

The power of this feature lies in the fact that your organization can do the same: publish a `.well-known/duckdb-extension-repo.json` file on your own domain, and your users can install your extensions with the same succinct syntax:

```sql
INSTALL AND LOAD ⟨extension⟩ FROM ⟨your_domain⟩;
```

To get started, see the new [“Publishing an Extension Repository” page]({% link docs/2.0/extensions/publishing_extension_repositories.md %}).

Unlike adding a repository by its prefix, adding one by its host does not require an opt-in.
To support this, the `allow_extension_repositories` setting has new values: `hosts` (the new default) allows adding repositories by host, `allowed` also allows adding them by prefix, `hosts_only` only adds and trusts repositories resolved from their host, and `forbidden` disables custom repositories.
The previous default value, `undecided`, is no longer accepted.
If only extensions signed by the DuckDB team should be loaded in your environment, set `allow_extension_repositories` to `forbidden`.
For details, see the [“Securing Extensions” page]({% link docs/2.0/operations_manual/securing_duckdb/securing_extensions.md %}#custom-extension-repositories).

## Important Fixes

### Silent Data Loss on Affected Linux Kernels

Some Linux kernel versions have a bug ([CVE-2026-97945](https://app.opencve.io/cve/CVE-2026-97945)) that can cause memory freed lazily with `MADV_FREE` to be silently zeroed after it has been reused.
DuckDB 2.0.1 avoids this issue: its bundled allocator no longer frees memory this way ([`#28267`](https://github.com/duckdb/duckdb/pull/28267)).
The patch works by setting the bundled jemalloc's `muzzy_decay_ms` to `0`. If you cannot upgrade right away, you should set the `DUCKDB_JE_MALLOC_CONF` environment variable to `muzzy_decay_ms:0`, which achieves the same effect.

### Reading Databases Written by DuckDB 1.x

DuckDB 2.0.0 could miss rows with `NULL` values when filtering tables in database files written by DuckDB 1.x ([`#28355`](https://github.com/duckdb/duckdb/pull/28355)).
DuckDB 2.0.1 fixes this, along with several issues affecting views, macros, and other objects stored by 1.x versions.

### Security Fixes

Configuring `enable_external_access=false` should prevent access to external state but would still allow `CREATE SECRET`, which can result in accessing external state. This is now fixed ([`28637`](https://github.com/duckdb/duckdb/pull/28637)) by refusing `CREATE SECRET` with a `Permission Error` and an error message indicating `Creating secrets is disabled when enable_external_access is false`.

We also fixed a remote path traversal issue ([`#28684`](https://github.com/duckdb/duckdb/pull/28684)) that occurred when DuckDB was configured with `enable_external_access=false`.

Additionally, this release pulls in a fix ([`#27791`](https://github.com/duckdb/duckdb/pull/27791)) for the Brotli decoder ([CVE-2026-111497](https://app.opencve.io/cve/CVE-2026-111497)).

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

* [`#28646`](https://github.com/duckdb/duckdb/pull/28646) – Fix aggregates such as `quantile_cont` and `arg_max` running out of memory on large `GROUP BY` queries
* [`#27760`](https://github.com/duckdb/duckdb/pull/27760) – Push down filters to `VIEW`s used in subqueries, which can make queries orders of magnitude faster
* [`#27326`](https://github.com/duckdb/duckdb/pull/27326) – Use the [Parquet page index](https://parquet.apache.org/docs/file-format/pageindex/) to skip pages, e.g., in files written by Spark
* [`#28193`](https://github.com/duckdb/duckdb/pull/28193) – Improve join ordering for range joins

### Miscellaneous

* [`#27685`](https://github.com/duckdb/duckdb/pull/27685) – Add the `RETURN_COLUMN_TYPES` option to [`COPY ... TO`]({% link docs/2.0/sql/statements/copy.md %}#copy--to)
* [`#27969`](https://github.com/duckdb/duckdb/pull/27969) – Add the `parquet_can_have_nan` setting for Parquet files whose statistics do not account for `NaN` values
* [`#28011`](https://github.com/duckdb/duckdb/pull/28011) – Ship the Windows CLI as ZIP archives for WinGet

## Extensions and Clients

As is customary for DuckDB releases, while DuckDB 2.0.1 itself is a patch release, extensions and clients ship new features along with their fixes. Here are some highlights:

* The [`azure` extension]({% link docs/2.0/core_extensions/azure.md %}) no longer deletes live data files stored at `abfss://⟨container⟩@⟨account⟩` paths when running `CHECKPOINT` on DuckLake ([`duckdb-azure#211`](https://github.com/duckdb/duckdb-azure/pull/211)).
* The experimental [`glue` extension]({% link docs/2.0/core_extensions/glue.md %}) attaches an AWS Glue Data Catalog as a DuckDB database, so you can read and write its Hive tables stored as Parquet, CSV, JSON, or Avro files on S3.
* The [`iceberg` extension]({% link docs/2.0/core_extensions/iceberg/overview.md %}) ships many correctness and performance fixes. For example, TLS now stays enabled when using vended path-style S3 credentials ([`duckdb-iceberg#1527`](https://github.com/duckdb/duckdb-iceberg/pull/1527)). Note that `iceberg_rewrite_data_files` now returns Spark's output column names ([`duckdb-iceberg#1597`](https://github.com/duckdb/duckdb-iceberg/pull/1597)).
* [`pg_duckdb`](https://github.com/duckdb/pg_duckdb), the PostgreSQL extension that embeds DuckDB, now publishes binaries for all supported PostgreSQL versions on its [GitHub releases page](https://github.com/duckdb/pg_duckdb/releases). It also ships a number of bugfixes and improves compatibility with other popular PostgreSQL extensions such as Citus and pgvector.
* In the [`postgres` extension]({% link docs/2.0/core_extensions/postgres/overview.md %}), queries that only touch a single attached PostgreSQL database are now executed entirely in PostgreSQL. If you would like to disable this, run `SET pg_enable_remote_pushdown = false` before attaching the database ([`duckdb-postgres#643`](https://github.com/duckdb/duckdb-postgres/pull/643)).
* The [Python client]({% link docs/2.0/clients/python/overview.md %}) received fixes for several hangs and crashes at exit, including on Python 3.14 ([`duckdb-python#709`](https://github.com/duckdb/duckdb-python/pull/709), [`duckdb-python#719`](https://github.com/duckdb/duckdb-python/pull/719)). Fetching `TIMESTAMPTZ` values no longer requires the `pytz` package ([`duckdb-python#710`](https://github.com/duckdb/duckdb-python/pull/710)).
* The [`aws`]({% link docs/2.0/core_extensions/aws.md %}) and [`glue`]({% link docs/2.0/core_extensions/glue.md %}) extensions are now available in DuckDB-Wasm, and the [`vortex` extension]({% link docs/2.0/core_extensions/vortex.md %}) is now available on Windows.
* The `wasm_mvp` platform was discontinued. Core extensions are no longer built for this platform. The remaning Wasm platforms are `wasm_eh` for slim deployments and `wasm_threads` for enabling threads and SIMD operations.

## End of Life for DuckDB 1.4 LTS

Community support for DuckDB 1.4 LTS (Andium) ended on November 17, 2026.
If you are still using it, we recommend upgrading to DuckDB 2.0 LTS, which is supported until at least October 2027.
For details, see the [release calendar]({% link release_calendar.md %}#lts-releases).

## Conclusion

This post was a short summary of the changes in v2.0.1. As usual, you can find the [full release notes on GitHub](https://github.com/duckdb/duckdb/releases/tag/v2.0.1).
We would like to thank our contributors for providing detailed issue reports and patches.

We are also grateful to the following people whose reports helped us make DuckDB and its extensions more robust and secure:

* [@TristanInSec](https://github.com/TristanInSec) for reporting out-of-bounds reads and a string-length buffer sizing overflow in `DICT_FSST` decompression, and for reporting missing validation of Arrow string offsets.
* [@zerovulnlabs](https://github.com/zerovulnlabs) for reporting missing page-size validation when reading uncompressed Parquet V2 pages.
* zz lin for reporting a problem in the MySQL extension.

Stay tuned for [future DuckDB releases]({% link release_calendar.md %}), including v2.1.0 in the first half of 2027!
