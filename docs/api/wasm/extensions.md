---
layout: docu
title: Extensions
selected: Client APIs
---

Default [extensions](../../extensions/overview) enabled in DuckDB-Wasm are Parquet and FTS. HTTPFS is a specific re-implementation that comes bundled by default. 

JSON and Excel are build-time opt-in. To add more extensions, you will have to build DuckDB-Wasm by yourself.

Dynamic extension loading is currently experimental, participate in the [tracking issue](https://github.com/duckdb/duckdb-wasm/issues/1202) or try it on the experimental deployment at: https://shellwip.duckdb.org.