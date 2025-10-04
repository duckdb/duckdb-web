---
layout: default
title: Development Roadmap
body_class: roadmap blog_typography post
redirect_from:
- /docs/stable/dev/roadmap
- /docs/stable/dev/roadmap/
- /docs/preview/dev/roadmap
- /docs/preview/dev/roadmap/
max_page_width: small
toc: false
---

<div class="wrap pagetitle">
  <h1>Development Roadmap</h1>
</div>

## Overview

The DuckDB project is governed by the [non-profit DuckDB Foundation]({% link foundation/index.html %}).
The Foundation and [DuckDB Labs](https://duckdblabs.com) are not funded by external investors (e.g., venture capital).
Instead, the Foundation is funded by contributions from its [members]({% link foundation/index.html %}#supporters),
while DuckDB Labs' revenue is based on [commercial support and feature prioritization services](https://duckdblabs.com/#support).

## Planned Features (Last Updated: September 2025)

This section lists the features that the DuckDB team plans to work on **in the coming year**.

* Migration and documentation to [C client API]({% link docs/stable/clients/c/overview.md %}) and [C extension API](https://github.com/duckdb/extension-template-c)
* Generic ODBC catalog, similarly to the existing PostgreSQL / MySQL / SQLite integrations
* Go and Rust support for extensions
* Improvements to lakehouse formats
    * Improved support for the Iceberg format through the [`iceberg` extension]({% link docs/stable/core_extensions/iceberg/overview.md %}). This was partially implemented in [v1.4.0]({% post_url 2025-09-16-announcing-duckdb-140 %}), which can Iceberg tables.
    * Improved support for Delta Lake through the [`delta` extension]({% link docs/stable/core_extensions/delta.md %}).
    * In May 2025, we released [DuckLake](https://ducklake.select/), a new lakehouse format. We would like to emphasize that we are still committed to developing both the `iceberg` and `delta` extensions. We also strive to [provide interoperability]({% post_url 2025-09-17-ducklake-03 %}#interoperability-with-iceberg) between DuckLake and other lakehouse formats.
* [`MATCH RECOGNIZE`](https://github.com/duckdb/duckdb/discussions/3994) for pattern matching
* Distribution of musl libc binaries
* Distribution of Windows ARM64 extensions
* [`GEOMETRY` type](https://github.com/duckdb/duckdb/pull/19136)

This list was compiled by the DuckDB maintainers and is based on the long-term strategic vision for the DuckDB project and general interactions with users in the open-source community (GitHub Issues and Discussions, social media, etc.).
For details on how to request features in DuckDB, please refer to the FAQ item [“I would like feature X to be implemented in DuckDB”]({% link faq.md %}#i-would-like-feature-x-to-be-implemented-in-duckdb-how-do-i-proceed).

Please note that there are **no guarantees** that a particular feature will be released within the next year. Everything on this page is subject to change without notice.

## Future Work

There are several items that we plan to implement at some point in the future.
If you would like to expedite the development of these features, please [get in touch with DuckDB Labs](https://duckdblabs.com/contact/).

* Time series optimizations
* Partition-aware optimizations
* Sorting-aware optimizations
* Better filter cardinality estimation using automatically maintained table samples
* [Parallel Python UDFs](https://github.com/duckdb/duckdb/issues/14817)
* [`ALTER TABLE` support for adding foreign keys](https://github.com/duckdb/duckdb/discussions/4204)
* Improvements of query profiling (especially for concurrently running queries)
* [XML read support](https://github.com/duckdb/duckdb/discussions/9547)
* [Materialized views](https://github.com/duckdb/duckdb/discussions/3638)
* [Support for async I/O](https://github.com/duckdb/duckdb/discussions/3560)
* [Support for PL/SQL stored procedures](https://github.com/duckdb/duckdb/discussions/8104)
