---
layout: docu
title: Extensions
selected: Client APIs
---

Default [extensions](../../extensions/overview) currently enabled in DuckDB-Wasm are Parquet and FTS. HTTPFS is a specific re-implementation that comes bundled by default. 

JSON and Excel are build-time opt-in.

## Dynamic (= runtime) extension loading

Dynamic extension loading is currently experimental, participate in the [tracking issue](https://github.com/duckdb/duckdb-wasm/issues/1202) or try it on the experimental deployment at: https://shellwip.duckdb.org.

{% include iframe.html src="https://shellwip.duckdb.org" %}
