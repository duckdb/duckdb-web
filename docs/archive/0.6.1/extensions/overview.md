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

## Unsigned extensions

All verified extensions are signed, if you wish to load your own extensions or extensions from untrusted third-parties you'll need to enable the `allow_unsigned_extensions` flag.  
To load unsigned extensions using the CLI, you'll need to pass the `-unsigned` flag to it on startup.

## Listing extensions

You can check the list of core and installed extensions with the following query:
```sql
select * from duckdb_extensions();
```

## All available extensions

|  Extension name   |                             Description                              |     Aliases     |
|-------------------|----------------------------------------------------------------------|-----------------|
| excel             |                                                                      |                 |
| fts               | Adds support for Full-Text Search Indexes                            |                 |
| httpfs            | Adds support for reading and writing files over a HTTP(S) connection | http, https, s3 |
| icu               | Adds support for time zones and collations using the ICU library     |                 |
| inet              | Adds support for IP-related data types and functions                 |                 |
| jemalloc          | Overwrites system allocator with JEMalloc                            |                 |
| json              | Adds support for JSON operations                                     |                 |
| parquet           | Adds support for reading and writing parquet files                   |                 |
| postgres_scanner  | Adds support for reading from a Postgres database                    | postgres        |
| sql_auto_complete |                                                                      |                 |
| sqlite_scanner    | Adds support for reading SQLite database files                       | sqlite, sqlite3 |
| substrait        | Adds support for the Substrait integration                           |
| tpcds             | Adds TPC-DS data generation and query support                        |                 |
| tpch              | Adds TPC-H data generation and query support                         |                 |
| visualizer        |                                                                      |                 |


## Pages in this Section

<!--
any extensions that have their own pages will automatically be added to a table of contents that is rendered directly below this list.
-->
