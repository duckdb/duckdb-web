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

_(Last updated: April 2026)_

The DuckDB project is governed by the [non-profit DuckDB Foundation]({% link foundation/index.html %}).
The Foundation and [DuckDB Labs](https://duckdblabs.com) are not funded by external investors (e.g., venture capital).
Instead, the Foundation is funded by contributions from its [members]({% link foundation/index.html %}#supporters),
while DuckDB Labs' revenue is based on [commercial support and feature prioritization services](https://duckdblabs.com/#support).

This list was compiled by the DuckDB maintainers and is based on the long-term strategic vision for the DuckDB project and general interactions with users in the open-source community (GitHub Issues and Discussions, social media, etc.).
For details on how to request features in DuckDB, please refer to the FAQ item [“I would like feature X to be implemented in DuckDB”]({% link faq.md %}#i-would-like-feature-x-to-be-implemented-in-duckdb-how-do-i-proceed).

## Planned Features

This section lists the features that the DuckDB team plans to work on **in the coming year**.

* Migration and documentation to [C client API]({% link docs/current/clients/c/overview.md %}) and [C extension API](https://github.com/duckdb/extension-template-c)
* Rust support for extensions
* Continuous improvements to [lakehouse formats]({% link docs/current/lakehouse_formats.md %}):
  [Iceberg]({% link docs/current/core_extensions/iceberg/overview.md %}),
  [Delta]({% link docs/current/core_extensions/delta.md %}),
  [Lance]({% link docs/current/core_extensions/lance.md %})
  and
  [DuckLake](https://ducklake.select/)
* [`MATCH_RECOGNIZE`](https://github.com/duckdb/duckdb/discussions/3994) for pattern matching
* [Support for async I/O](https://github.com/duckdb/duckdb/discussions/3560)
* [Parallel Python UDFs](https://github.com/duckdb/duckdb/issues/14817)
* Using the new [PEG parser]({% post_url 2024-11-22-runtime-extensible-parsers %}) by default
* C++17 support
* macOS installer
* Windows installer

Please note that there are **no guarantees** that a particular feature will be released within the next year. Everything on this page is subject to change without notice.

## Planned Deprecations

We are [gradually phasing out]({% link docs/current/sql/functions/lambda.md %}) the lambda syntax (`x -> x + 1`) in favor of the Pythonic `lambda x : x + 1`. [DuckDB v1.5]({% post_url 2026-03-09-announcing-duckdb-150 %}) throws a warning when using the deprecated syntax and DuckDB v2.0 will throw an error (unless configured explicitly to allow the old syntax).

## Future Work / Looking for Funding

There are several features and optimizations that we plan to implement at some point in the future.
If you would like to expedite the development of these items, please [get in touch with DuckDB Labs](https://duckdblabs.com/contact/).

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
* Guaranteeing [FIPS](https://en.wikipedia.org/wiki/FIPS_140-2)-compliance for the [database encryption]({% link docs/current/sql/statements/attach.md %}#database-encryption)
* Performance and out-of-core optimization on Windows
