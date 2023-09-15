---
layout: docu
title: Extensions
---

The default [extensions](../../extensions/overview) currently enabled in DuckDB-Wasm are Parquet and FTS. The [`httpfs` extension](../../extensions/httpfs) is a specific re-implementation that comes bundled by default. 

JSON and Excel are build-time opt-in.

## Dynamic (= Runtime) Extension Loading

Dynamic extension loading is currently experimental, participate in the [tracking issue](https://github.com/duckdb/duckdb-wasm/issues/1202) or try it on the experimental deployment at: <https://shellwip.duckdb.org>.

<!-- markdownlint-disable-next-line -->
{% include iframe.html src="https://shellwip.duckdb.org" %}
