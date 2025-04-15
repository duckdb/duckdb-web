---
layout: docu
title: Limits
---

This page contains DuckDB's built-in limit values.

| Limit | Default value | Configuration option | Comment |
|---|---|---|---|
| Array size | 100000 | - | |
| BLOB size | 4 GB | - | |
| Expression depth | 1000 | [`max_expression_depth`]({% link docs/preview/configuration/overview.md %}) | |
| Memory allocation for a vector | 128 GB | - | |
| Memory use | 80% of RAM | [`memory_limit`]({% link docs/preview/configuration/pragmas.md %}#memory-limit) | Note: This limit only applies to the buffer manager. |
| String size | 4 GB | - | |
| Temporary directory size | unlimited | [`max_temp_directory_size`]({% link docs/preview/configuration/overview.md %}) | |