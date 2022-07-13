---
layout: docu
title: Extensions
selected: Documentation/Extensions
---
DuckDB has a number of extensions available for use. Not all of them are included by default in every distribution, but DuckDB has a mechanism that allows for remote installation.

## Remote installation

If a given extensions is not available with your distribution, you can do the following to make it available.

```sql
INSTALL 'fts';
LOAD 'fts';
```

If you are using the Python API client, you can install and load them with the `load_extension(name: str)` and `install_extension(name: str)` methods.

## Listing extensions

You can check the list of core and installed extensions with the following query:
```sql
select * From duckdb_extensions();
```

| Extension name   | Description                                                          |
| ---------------- | -------------------------------------------------------------------- |
| fts              | Adds support for Full-Text Search Indexes                            |
| httpfs           | Adds support for reading and writing files over a HTTP(S) connection |
| icu              | Adds support for time zones and collations using the ICU library     |
| json             | Adds support for JSON operations                                     |
| parquet          | Adds support for reading and writing parquet files                   |
| postgres_scanner | Adds support for reading from a Postgres database                    |
| sqlite_scanner   | Adds support for reading SQLite database files                       |
| substrait        | Adds support for the Substrait integration                           |
| tpcds            | Adds TPC-DS data generation and query support                        |
| tpch             | Adds TPC-H data generation and query support                         |

## All available extensions

<!--
any extensions that have their own pages will automatically be added to a table of contents that is rendered directly below this list.
each extension should eventually have it's own page, and be removed from this list.
-->

 * excel
 * httpfs
 * icu
 * parquet
 * substrait
 * tpch
 * tpcds
 * visualizer
