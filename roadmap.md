---
layout: default
title: Development Roadmap
body_class: roadmap blog_typography post
redirect_from:
- /docs/lts/dev/roadmap
- /docs/current/dev/roadmap
max_page_width: small
toc: false
---

<div class="wrap pagetitle">
  <h1>Development Roadmap</h1>
</div>

_(Last updated: Oct 2026)_

This list was compiled by the DuckDB maintainers and is based on the long-term strategic vision for the DuckDB project and general interactions with users in the open-source community (GitHub Issues and Discussions, social media, etc.).
For details on how to request features in DuckDB, please refer to the FAQ item [“I would like feature X to be implemented in DuckDB”]({% link faq.md %}#i-would-like-feature-x-to-be-implemented-in-duckdb-how-do-i-proceed).

## Planned Features

This section lists the features that the DuckDB team plans to work on **in the coming year**.

* Stabilizing the [C API v2]({% link docs/2.0/clients/c/overview.md %}) and the [C extension API](https://github.com/duckdb/extension-template-c)
* Rust support for extensions
* Continuous improvements to [lakehouse formats]({% link docs/2.0/lakehouse_formats.md %}):
  [Iceberg]({% link docs/2.0/core_extensions/iceberg/overview.md %}),
  [Delta]({% link docs/2.0/core_extensions/delta.md %}),
  [Lance]({% link docs/2.0/core_extensions/lance.md %})
  and
  [DuckLake](https://ducklake.select/)
* [`MATCH_RECOGNIZE`](https://github.com/duckdb/duckdb/discussions/3994) for pattern matching
* [Parallel Python UDFs](https://github.com/duckdb/duckdb/issues/14817)
* macOS installer
* Windows installer

Please note that there are **no guarantees** that a particular feature will be released within the next year. Everything on this page is subject to change without notice.

## Delivered in DuckDB v2.0

The following features from the previous version of the roadmap were released in [DuckDB v2.0.0]({% post_url 2026-10-21-announcing-duckdb-200 %}):

* Using the new [PEG parser]({% post_url 2026-08-20-duckdb-20-peg-parser %}) by default
* Shipping the polished version of the [Quack protocol]({% link quack/index.html %})
* [Support for async I/O]({% post_url 2026-07-31-asynchronous-io %})
* C++17 support

## Planned Deprecations

We are [gradually phasing out]({% link docs/2.0/sql/functions/lambda.md %}) the lambda syntax (`x -> x + 1`) in favor of the Pythonic `lambda x : x + 1`. [DuckDB v1.5]({% post_url 2026-03-09-announcing-duckdb-150 %}) throws a warning when using the deprecated syntax and [DuckDB v2.0]({% post_url 2026-10-21-announcing-duckdb-200 %}#lambda-syntax) throws an error (unless configured explicitly to allow the old syntax). DuckDB v2.1 will remove the old syntax completely.

We are gradually phasing out macOS x86_64 (`osx_amd64`) from the list of [supported platforms]({% link docs/2.0/operations_manual/installing_duckdb/requirements.md %}#supported-platforms). In DuckDB v2.0, DuckDB and core extensions are still built and supported for this platform, but community extensions are no longer built for it. DuckDB v2.1 will stop supporting `osx_amd64`.

## Future Work

There are several features and optimizations that we plan to implement at some point in the future.

* Go support for extensions
* Time series optimizations
* Partition-aware optimizations
* Sorting-aware optimizations
* Better filter cardinality estimation using automatically maintained table samples
* [`ALTER TABLE` support for adding foreign keys](https://github.com/duckdb/duckdb/issues/57)
* Improvements of query profiling (especially for concurrently running queries)
* [Materialized views](https://github.com/duckdb/duckdb/discussions/3638)
* [Support for PL/SQL stored procedures](https://github.com/duckdb/duckdb/discussions/8104) (see Denis Hirn's [DuckPL talk]({% link _library/2026-01-30-duckpl-a-procedural-language-in-duckdb.md %}))
* [XML read support](https://github.com/duckdb/duckdb/discussions/9547)
* Guaranteeing [FIPS](https://en.wikipedia.org/wiki/FIPS_140-2)-compliance for the [database encryption]({% link docs/2.0/sql/statements/attach.md %}#database-encryption)
* Performance and out-of-core optimization on Windows
