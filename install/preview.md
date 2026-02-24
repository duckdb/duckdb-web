---
layout: default
title: DuckDB Preview (Nightly) Installation
excerpt: DuckDB preview installation page
body_class: blog_typography nightly_install
max_page_width: medium
toc: false
redirect_from:
  - /preview
  - /nightly
  - /nightlies
  - /install/nightly
  - /install/nightlies
---

<div class="wrap pagetitle pagetitle--small">
  <h1>DuckDB Preview (Nightly) Installation</h1>
</div>

The preview (nightly) builds provide the latest development version of DuckDB. As such, they are constantly in flux and they are less suitable for production use than the stable releases of DuckDB. You should only use these releases if you are looking for [recent bugfixes](https://github.com/duckdb/duckdb/pulls?q=is%3Apr+is%3Amerged) or optimizations.

There are currently the following DuckDB versions under development:

* v1.4 (LTS)
* v1.5 (to be released soon)
* v1.6 (pre-alpha)

## Command Line Interface (CLI), C and C++ clients

For the CLI, C and C++ clients, there are three preview builds available:

| Platform | Architecture       | v1.4-dev                                                                             | v1.5-dev                                                                                | v1.6-dev                                                                        |
| -------- | ------------------ | ------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| Linux    | `arm64`            | [Download](https://artifacts.duckdb.org/v1.4-andium/duckdb-binaries-linux-arm64.zip) | [Download](https://artifacts.duckdb.org/v1.5-variegata/duckdb-binaries-linux-arm64.zip) | [Download](https://artifacts.duckdb.org/latest/duckdb-binaries-linux-arm64.zip) |
| Linux    | `x86_64`           | [Download](https://artifacts.duckdb.org/v1.4-andium/duckdb-binaries-linux-amd64.zip) | [Download](https://artifacts.duckdb.org/v1.5-variegata/duckdb-binaries-linux-amd64.zip) | [Download](https://artifacts.duckdb.org/latest/duckdb-binaries-linux-amd64.zip) |
| macOS    | `arm64` / `x86_64` | [Download](https://artifacts.duckdb.org/v1.4-andium/duckdb-binaries-osx.zip)         | [Download](https://artifacts.duckdb.org/v1.5-variegata/duckdb-binaries-osx.zip)         | [Download](https://artifacts.duckdb.org/latest/duckdb-binaries-osx.zip)         |
| Windows  | `arm64` / `x86_64` | [Download](https://artifacts.duckdb.org/v1.4-andium/duckdb-binaries-windows.zip)     | [Download](https://artifacts.duckdb.org/v1.5-variegata/duckdb-binaries-windows.zip)     | [Download](https://artifacts.duckdb.org/latest/duckdb-binaries-windows.zip)     |

## Python

For Python, we distribute two nightly builds.

* To install the nightly build for the 1.4 LTS version of DuckDB, run:

  ```batch
  pip install "duckdb<1.5.0"
  ```

* To install the nightly build based on v1.5-dev, run:

  ```batch
  pip install duckdb --pre --upgrade
  ```

## Java

The following Maven snippet imports the SNAPSHOT version of the Java package:

```xml
<dependencies>
    <dependency>
        <groupId>org.duckdb</groupId>
        <artifactId>duckdb_jdbc</artifactId>
        <!-- replace the hash of the build here -->
        <version>1.5-627976eb-SNAPSHOT</version>
    </dependency>
</dependencies>

<repositories>
    <repository>
        <id>central-snapshots</id>
        <url>https://central.sonatype.com/repository/maven-snapshots/</url>
        <snapshots><enabled>true</enabled></snapshots>
    </repository>
</repositories>
```

## Node.js (Neo)

For the DuckDB Node Neo driver, the nightly release is currently not available.

## ODBC

For ODBC, the preview builds are based on the `main` branch of the [`duckdb/duckdb-odbc` repository](https://github.com/duckdb/duckdb-odbc/).

| Platform | Architecture       | Download                                                                         |
| -------- | ------------------ | -------------------------------------------------------------------------------- |
| Linux    | `arm64`            | [Download](https://artifacts.duckdb.org/duckdb-odbc/main/odbc-linux-arm64.zip)   |
| Linux    | `x86_64`           | [Download](https://artifacts.duckdb.org/duckdb-odbc/main/odbc-linux-amd64.zip)   |
| macOS    | `arm64` / `x86_64` | [Download](https://artifacts.duckdb.org/duckdb-odbc/main/odbc-osx-universal.zip) |
| Windows  | `arm64`            | [Download](https://artifacts.duckdb.org/duckdb-odbc/main/odbc-windows-arm64.zip) |
| Windows  | `x86_64`           | [Download](https://artifacts.duckdb.org/duckdb-odbc/main/odbc-windows-amd64.zip) |

## R

In R, run the following to install the latest DuckDB from source based on the `main` branch of the [`duckdb/duckdb-r` repository](https://github.com/duckdb/duckdb-r/).

```R
install.packages("pak")
pak::pak("duckdb/duckdb-r")
```
