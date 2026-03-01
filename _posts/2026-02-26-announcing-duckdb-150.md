---
layout: post
title: "Announcing DuckDB 1.5.0"
author: "The DuckDB team"
thumb: "/images/blog/thumbs/duckdb-release-1-5-0.svg"
image: "/images/blog/thumbs/duckdb-release-1-5-0.png"
excerpt: "Today we are releasing DuckDB 1.5.0. ..."
tags: ["release"]
---

### Dynamic Prompts in the CLI

DuckDB v1.5.0 introduces dynamic prompts for the CLI. By default, these show the database and schema that you are currently connected to:

```batch
duckdb
```

```sql
«memory» D ATTACH 'my_database.duckdb';
«memory» D USE my_database;
«my_database» D CREATE SCHEMA my_schema;
«my_database» D USE my_schema;
«my_database.my_schema» D ...
```

The prompt also works when attaching to data lakes:

```sql
«memory» D ATTACH 'https://blobs.duckdb.org/datalake/tpch-sf1.ducklake'
             AS tpch_sf1;
«memory» D USE tpch_sf1;
«tpch_sf1» D ...
```

These prompts can be configured using bracket codes to have a maximum length, run a custom query, use different colors, etc.
See details in the [pull request](https://github.com/duckdb/duckdb/pull/19579).
