---
layout: docu
title: Limits
---

This page contains DuckDB's built-in limit values.
To check the value of a setting on your system, use the `current_setting` function.

## Limit Values

| Limit | Default value | Configuration option | Comment |
|---|---|---|---|
| Array size | 100000 | - | |
| BLOB size | 4 GB | - | |
| Expression depth | 1000 | [`max_expression_depth`]({% link docs/preview/configuration/overview.md %}) | |
| Memory allocation for a vector | 128 GB | - | |
| Memory use | 80% of RAM | [`memory_limit`]({% link docs/preview/configuration/pragmas.md %}#memory-limit) | Note: This limit only applies to the buffer manager. |
| String size | 4 GB | - | |
| Temporary directory size | unlimited | [`max_temp_directory_size`]({% link docs/preview/configuration/overview.md %}) | |

## Size of Database Files

DuckDB doesn't have a practical limit for the size of a single DuckDB database file.
We have database files using 15 TB+ of disk space and they work fine.
However, connecting to such a huge database may take a few seconds, and [checkpointing]({% link docs/preview/sql/statements/checkpoint.md %}) can be slower.
