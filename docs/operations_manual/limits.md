---
layout: docu
title: Limits
---

This pages contains DuckDB's built-in limit values.

| Limit | Default value | Configuration option |
|---|---|---|
| Array size | 100000 | - |
| BLOB size | 4 GB | - |
| Expression depth | 1000 | [`max_expression_depth`]({% link docs/configuration/overview.md %}) |
| Memory allocation | 128 GB | - |
| Memory use | 80% of RAM | [`memory_limit`]({% link docs/configuration/overview.md %}) |
| String size | 4 GB | - |
| Temporary directory size | unlimited | [`max_temp_directory_size`]({% link docs/configuration/overview.md %}) |
