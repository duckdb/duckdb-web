---
layout: default
title: DuckDB Preview (Alpha/Nightly) Installation
excerpt: DuckDB preview installation page
body_class: blog_typography nightly_install
max_page_width: medium
redirect_from:
  - /preview
  - /nightly
  - /nightlies
  - /install/nightly
  - /install/nightlies
---

<div class="wrap pagetitle pagetitle--small">
  <div class="pagetitle-heading" role="heading" aria-level="1">DuckDB Preview (Alpha/Nightly) Installation</div>
</div>

The preview (nightly) builds provide development versions of DuckDB. As such, they are constantly in flux and they are less suitable for production use than the stable releases of DuckDB. You should only use these releases if you are looking for [recent bugfixes](https://github.com/duckdb/duckdb/pulls?q=is%3Apr+is%3Amerged) or optimizations.

There are currently the following DuckDB versions under development:

* v1.4: the LTS release.
* v1.5: the current stable DuckDB release.
* v2.0: the next DuckDB version, in an early stage of the development.

Note that for most users, we recommend the [stable DuckDB releases]({% link install/index.html %}).

## Python

For Python, we distribute different nightly builds. Note that not all of them are available at all times and a few days can be skipped when nightly builds fail.

### Python v1.4-dev

```batch
pip install "duckdb<1.5.0" --pre --upgrade
```

### Python v1.5-dev

```batch
pip install "duckdb<1.6.0" --pre --upgrade
```

### Python v2.0-dev

See the [installation page]({% link install/index.html %}?environment=python&version=preview).

## Command Line Interface (CLI) Client

### v1.5-dev CLI

To download the v1.5-dev command line client, use the following links:

| Platform | Architecture       | v1.5-dev CLI client                                                                |
| -------- | ------------------ | ---------------------------------------------------------------------------------- |
| Linux    | `arm64`            | [zip](https://artifacts.duckdb.org/v1.5-variegata/duckdb-binaries-linux-arm64.zip) |
| Linux    | `x86_64`           | [zip](https://artifacts.duckdb.org/v1.5-variegata/duckdb-binaries-linux-amd64.zip) |
| macOS    | `arm64` / `x86_64` | [zip](https://artifacts.duckdb.org/v1.5-variegata/duckdb-binaries-osx.zip)         |
| Windows  | `arm64` / `x86_64` | [zip](https://artifacts.duckdb.org/v1.5-variegata/duckdb-binaries-windows.zip)     |

### v2.0-dev CLI

See the [installation page]({% link install/index.html %}?environment=cli&version=preview).

## Java

See the [installation page]({% link install/index.html %}?environment=java&version=preview).

## ODBC

See the [installation page]({% link install/index.html %}?environment=odbc&version=preview).

## C/C++ Libraries

### v1.5-dev C/C++ Libraries

To download the C/C++ libraries, use the following links:

| Platform | Architecture       | v1.5-dev C/C++ library                                                             |
| -------- | ------------------ | ---------------------------------------------------------------------------------- |
| Linux    | `arm64`            | [zip](https://artifacts.duckdb.org/v1.5-variegata/duckdb-binaries-linux-arm64.zip) |
| Linux    | `x86_64`           | [zip](https://artifacts.duckdb.org/v1.5-variegata/duckdb-binaries-linux-amd64.zip) |
| macOS    | `arm64` / `x86_64` | [zip](https://artifacts.duckdb.org/v1.5-variegata/duckdb-binaries-osx.zip)         |
| Windows  | `arm64` / `x86_64` | [zip](https://artifacts.duckdb.org/v1.5-variegata/duckdb-binaries-windows.zip)     |


### v2.0-dev C/C++ Libraries

See the [installation page]({% link install/index.html %}?environment=c&version=preview).

## Node.js (Neo)

For the DuckDB Node Neo driver, the nightly release is currently not available.
