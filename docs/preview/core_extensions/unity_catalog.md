---
github_repository: https://github.com/duckdb/unity_catalog
layout: docu
title: Unity Catalog Extension
---

The `unity_catalog` extension adds support for the [`Unity Catalog`](https://www.unitycatalog.io/) atop the
[`Delta Lake`](https://delta.io/) format and [DuckDB Delta extension]({% link docs/preview/core_extensions/delta.md %}).

The `delta` extension adds support for the [Delta Lake open-source storage format](https://delta.io/). It is built using the [Delta Kernel](https://github.com/delta-incubator/delta-kernel-rs). The extension offers **read support** for Delta tables, both local and remote.

For implementation details, see the [announcement blog post]({% post_url 2024-06-10-delta %}).

> Warning Both the `unity_catalog` and `delta` extensions are currently experimental and [only supported on given platforms](#supported-duckdb-versions-and-platforms).

## Installing and Loading

To install and load, run:

```sql
INSTALL unity_catalog;
LOAD unity_catalog;
```

## Usage

Given that you already have a Unity Catalog setup with either Databricks or Unity Catalog OSS, you will need to
configure your secret token, endpoint, and region; then attach to your catalog. For example an AWS configuration
would look like this:

```sql
CREATE SECRET uc (
    TYPE unity_catalog,
    TOKEN '⟨token⟩',
    ENDPOINT '⟨endpoint⟩',
    AWS_REGION '⟨region⟩'
);
ATTACH 'test_catalog' AS test_catalog (TYPE unity_catalog, DEFAULT_SCHEMA 'main');
```

Where `token` comes from your Databricks or OSS Unity Catalog deployment, and `endpoint` is your Unity Catalog REST API endpoint.

For more details on these deployments see [Databricks Unity Catalog Docs](https://docs.databricks.com/aws/en/data-governance/unity-catalog) and [OSS Unity Catalog Docs](https://docs.unitycatalog.io/).

To confirm correct attachment, try something like:

```sql
SHOW ALL TABLES;
SELECT * FROM test_catalog.test_schema.test_table LIMIT 10;
```

## Features

This extension is still experimental and work-in-progress; it supports:

- Listing available tables (`SHOW ALL TABLES;`)
- Interacting with tables using standard SQL (`SELECT * FROM <catalog>.<schema>.<table>;`)
- Time travel (`SELECT * FROM .. AT (VERSION => ..);`)
- Inserts (`INSERT INTO .. VALUES (..);`)

It does not currently support:

- `DELETE` or `UPDATE`
- Creation or manipulation of `TABLE`s `VIEW`s or `SCHEMA`s

## Supported DuckDB Versions and Platforms

The `unity_catalog` (and `delta`) extension currently supports the following platforms:

- Linux AMD64 (x86_64 and ARM64): `linux_amd64` and `linux_arm64`
- macOS Intel and Apple Silicon: `osx_amd64` and `osx_arm64`
- Windows AMD64: `windows_amd64`

Support for the [other DuckDB platforms]({% link docs/preview/extensions/extension_distribution.md %}#platforms) is work-in-progress.
