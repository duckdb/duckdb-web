---
layout: post
title: "Gems of DuckDB 1.2"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/gems-of-duckdb-1-2.svg"
image: "/images/blog/thumbs/gems-of-duckdb-1-2.png"
excerpt: "We highlight a few exciting features that were introduced in DuckDB 1.2."
tags: ["releases"]
---

We published the DuckDB 1.2.1 bugfix release yesterday. As usual, please consult the [release notes](https://github.com/duckdb/duckdb/releases/tag/v1.2.1) for the full list of changes and the [installation page](({% link  docs/installation/index.html %})) for instructions on installing or upgrading. In this post, we'll highlight a few features that were recently added to DuckDB and improvements that have been made in its ecosystem.

## New Clients Page

DuckDB clients are distributed through several centralized repositories, such as [CRAN](https://cran.r-project.org/web/packages/duckdb/index.html) for R and [Maven](https://mvnrepository.com/artifact/org.duckdb/duckdb_jdbc) for Java. To help users keep track of the rollout of a new DuckDB release, we reworked our [clients page]({% link docs/stable/clients/overview.md %}) to show the latest version for each client. The page also clarifies the support tiers that apply to clients.

## Simpler Installation

In line with DuckDB's “low friction” principle, we made sure that you can install the [DuckDB command line client]({% link docs/stable/clients/cli/overview.md %}) more easily.

### Installation Script on Linux and macOS

DuckDB can now be installed on UNIX-like systems with an installation script:

```bash
curl https://install.duckdb.org | sh
```

The script determines your operating system and architecture, and downloads the latest available DuckDB binary.
Running the script does not require root (sudo) privileges, and it only uses the `curl` and `zcat` tools, which are widely available.

> You can inspect the shell script by visiting [`install.duckdb.org`](https://install.duckdb.org) in your browser.

### Signed Binaries on Windows

Starting with v1.2.1, we ship digitally signed binaries for the DuckDB Windows command line client. This means that you can run DuckDB in environments where signed binaries are a requirement.

## Unsung DuckDB 1.2 Features

Further to the [“What's New in 1.2.0” section of the announcement blog post]({% post_url 2025-02-05-announcing-duckdb-120 %}#whats-new-in-120), we collected five new features that were introduced in v1.2.0:

### `OR` / `IN` Filter Pushdown

Starting with version 1.2.0, DuckDB [supports `OR` and `IN` expressions for filter pushdown](https://github.com/duckdb/duckdb/pull/14313).
This optimization comes especially handy when querying remote Parquet files or DuckDB databases.

### `-f` Command Line Flag

The DuckDB CLI client now [supports the `-f` flag](https://github.com/duckdb/duckdb/pull/15050) to execute SQL script files:

```bash
duckdb -f script.sql
```

This is equivalent to:

```bash
duckdb -c ".read scripts.sql"
```

This feature is documented in the [DuckDB tldr page](https://tldr.inbrowser.app/pages/common/duckdb). If you have [tldr](https://tldr.sh/) installed, you can get this page in the CLI via `tldr duckdb`.

### `allowed_directories` / `allowed_paths` Options

We continue adding support for [operating DuckDB in secure environments]({% link docs/stable/operations_manual/securing_duckdb/overview.md %}). The [`allowed_directories` and `allowed_paths` options](https://github.com/duckdb/duckdb/pull/14568) allow restricting DuckDB's access to certain directories or files (resp.).
These options allows fine-grained access control for the file system.
For example, you can set DuckDB to only use the `/tmp` directory.

```sql
SET allowed_directories = ['/tmp'];  
SET enable_external_access = false;  
FROM read_csv('test.csv');  
```

With the setting applied, DuckDB will refuse to read files in the current working directory:

```console
Permission Error:  
Cannot access file "test.csv" - file system operations are disabled by configuration  
```

### `sum(BOOLEAN)`

You can now directly [compute the sum of `BOOLEAN` expressions](https://github.com/duckdb/duckdb/pull/15042) without wrapping them into a `CASE` expression:

```sql
SELECT sum(l_extendedprice > 500) FROM lineitem;  
```

This is equivalent to:

```sql
SELECT sum(CASE WHEN l_extendedprice > 500 THEN 1 END) FROM lineitem;  
```

### Excel Extension

Prior to DuckDB 1.2, Excel files were only supported by the [`spatial` extension]({% link docs/stable/extensions/spatial/overview.md %}), which is a heavyweight extension with several dependencies.
Starting with 1.2, the [`excel` extension](({% link docs/stable/extensions/excel.md %})) – which was previously limited to computing a few formulas – can read and write Excel sheets. For example:

```sql
FROM read_xlsx('test.xlsx', header = true);  
```

> If you would like to work with _Google Sheets_ sheets, take a look at the [`gsheets` community extension]({% post_url 2025-02-26-google-sheets-community-extension %}).

## On the Interweb

There are several repositories and pieces of information on DuckDB on the internet.
We highlight two important ones:

### Awesome DuckDB

The ecosystem around DuckDB keeps growing: many projects are built both with DuckDB and within DuckDB. The community-driven [`awesome-duckdb` repository](https://github.com/davidgasquez/awesome-duckdb), maintained by [David Gasquez](https://github.com/davidgasquez), lists these and has recently surpassed 200 entries.

### DuckDB File Signature

DuckDB's file signature, `DUCK` (hex: `44 55 43 4B`), is now listed on [Wikipedia](https://en.wikipedia.org/wiki/List_of_file_signatures).
