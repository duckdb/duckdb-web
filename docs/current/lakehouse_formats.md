---
layout: docu
redirect_from:
- /docs/lakehouse_formats
- /docs/preview/lakehouse_formats
- /docs/stable/./lakehouse_formats
title: Lakehouse Formats
---

Lakehouse formats, often referred to as open table formats, are specifications for storing data in object storage while maintaining some guarantees such as ACID transactions or keeping snapshot history. Over time, multiple lakehouse formats have emerged, each one with its own unique approach to managing its metadata (a.k.a. catalog). In this page, we will go over the support that DuckDB offers for some of these formats as well as some workarounds that you can use to still use DuckDB and get close to full interoperability with these formats.

## DuckDB Lakehouse Support Matrix

DuckDB supports Iceberg, Delta, Lance and DuckLake as first-class citizens. The following matrix represents what DuckDB natively supports out of the box through core extensions.

|                              | DuckLake                                                              | Iceberg                                                                 | Delta                                                      | Lance                                                      |
| ---------------------------- | :-------------------------------------------------------------------- | :---------------------------------------------------------------------- | :--------------------------------------------------------- | :--------------------------------------------------------- |
| Extension                    | [`ducklake`](https://ducklake.select/docs/stable/duckdb/introduction) | [`iceberg`]({% link docs/lts/core_extensions/iceberg/overview.md %}) | [`delta`]({% link docs/lts/core_extensions/delta.md %}) | [`lance`]({% link docs/lts/core_extensions/lance.md %}) |
| Read                         | ✅                                                                    | ✅                                                                      | ✅                                                         | ✅                                                         |
| Write                        | ✅                                                                    | ✅                                                                      | ✅                                                         | ✅                                                         |
| Deletes                      | ✅                                                                    | ✅                                                                      | ❌                                                         | ✅                                                         |
| Updates                      | ✅                                                                    | ✅                                                                      | ❌                                                         | ✅                                                         |
| Upserting                    | ✅                                                                    | ❌                                                                      | ❌                                                         | ✅                                                         |
| Create table                 | ✅                                                                    | ✅                                                                      | ❌                                                         | ✅                                                         |
| Create table with partitions | ✅                                                                    | ❌                                                                      | ❌                                                         | ❌                                                         |
| Attaching to a catalog       | ✅                                                                    | ✅                                                                      | ✅ \*                                                      | ✅                                                         |
| Rename table                 | ✅                                                                    | ❌                                                                      | ❌                                                         | ❌                                                         |
| Rename columns               | ✅                                                                    | ❌                                                                      | ❌                                                         | ✅                                                         |
| Add/drop columns             | ✅                                                                    | ❌                                                                      | ❌                                                         | ✅                                                         |
| Alter column type            | ✅                                                                    | ❌                                                                      | ❌                                                         | ✅                                                         |
| Compaction and maintenance   | ✅                                                                    | ❌                                                                      | ❌                                                         | ✅                                                         |
| Encryption                   | ✅                                                                    | ❌                                                                      | ❌                                                         | ❌                                                         |
| Manage table properties      | ✅                                                                    | ❌                                                                      | ❌                                                         | ❌                                                         |
| Time travel                  | ✅                                                                    | ✅                                                                      | ✅                                                         | ❌                                                         |
| Query table changes          | ✅                                                                    | ❌                                                                      | ❌                                                         | ❌                                                         |

\* Through the [`unity_catalog`](https://github.com/duckdb/unity_catalog) extension.

DuckDB aims to build native extensions with minimal dependencies. The `iceberg` extension for example, has no dependencies on third-party Iceberg libraries, which means all data and metadata operations are implemented natively in the DuckDB extension. For the `delta` extension, we use the [`delta-kernel-rs` project](https://github.com/delta-io/delta-kernel-rs), which is meant to be a lightweight platform for engines to build delta integrations that are as close to native as possible.

> **Why do native implementations matter?** Native implementations allow DuckDB to do more performance optimizations such as complex filter pushdowns (with file-level and row-group level pruning) and improve memory management.
