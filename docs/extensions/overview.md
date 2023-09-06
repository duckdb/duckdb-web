---
layout: docu
title: Extensions
---
DuckDB has a number of extensions available for use. Not all of them are included by default in every distribution, but DuckDB has a mechanism that allows for remote installation.

## Remote Installation

If a given extensions is not available with your distribution, you can do the following to make it available.

```sql
INSTALL 'fts';
LOAD 'fts';
```

If you are using the Python API client, you can install and load them with the `load_extension(name: str)` and `install_extension(name: str)` methods.

## Unsigned Extensions

All verified extensions are signed, if you wish to load your own extensions or extensions from untrusted third-parties you'll need to enable the `allow_unsigned_extensions` flag.  
To load unsigned extensions using the CLI, you'll need to pass the `-unsigned` flag to it on startup.

## Listing Extensions

You can check the list of core and installed extensions with the following query:
```sql
SELECT * FROM duckdb_extensions();
```

## All Available Extensions

| Extension name | Description | Aliases |
|---|-----|--|
| autocomplete                                                                                                                        | Adds supports for autocomplete in the shell                          |                 |
| arrow [<span class="git">GitHub</span>](https://github.com/duckdblabs/arrow)                                                | A zero-copy data integration between Apache Arrow and DuckDB         |                 |
| [excel](excel)                                                                                                                      | Adds support for Excel-like format strings                           |                 |
| [fts](full_text_search)                                                                                                             | Adds support for Full-Text Search Indexes                            |                 |
| [httpfs](httpfs)                                                                                                                    | Adds support for reading and writing files over a HTTP(S) connection | http, https, s3 |
| [iceberg](iceberg) [<span class="git">GitHub</span>](https://github.com/duckdblabs/duckdb_iceberg)                          | Adds support for the Apache Iceberg format                           |                 |
| icu                                                                                                                                 | Adds support for time zones and collations using the ICU library     |                 |
| inet                                                                                                                                | Adds support for IP-related data types and functions                 |                 |
| jemalloc                                                                                                                            | Overwrites system allocator with JEMalloc                            |                 |
| [json](json)                                                                                                                        | Adds support for JSON operations                                     |                 |
| parquet                                                                                                                             | Adds support for reading and writing parquet files                   |                 |
| [postgres_scanner](postgres_scanner) [<span class="git">GitHub</span>](https://github.com/duckdblabs/postgres_scanner)      | Adds support for reading from a PostgreSQL database                  | postgres        |
| [spatial](spatial) [<span class="git">GitHub</span>](https://github.com/duckdblabs/duckdb_spatial)                          | Adds support for geospatial data processing                          |                 |
| [sqlite_scanner](sqlite_scanner) [<span class="git">GitHub</span>](https://github.com/duckdblabs/sqlite_scanner)            | Adds support for reading SQLite database files                       | sqlite, sqlite3 |
| [substrait](substrait) [<span class="git">GitHub</span>](https://github.com/duckdblabs/substrait)                           | Support substrait query plans in DuckDB                              |                 |
| tpcds                                                                                                                               | Adds TPC-DS data generation and query support                        |                 |
| tpch                                                                                                                                | Adds TPC-H data generation and query support                         |                 |
| visualizer                                                                                                                          |                                                                      |                 |

## Downloading Extensions Directly from S3

Downloading an extension directly could be helpful when building a lambda or container that uses DuckDB.
DuckDB extensions are stored in public S3 buckets, but the directory structure of those buckets is not searchable. 
As a result, a direct URL to the file must be used. 
To directly download an extension file, use the following format:  

```text
https://extensions.duckdb.org/v{release_version_number}/{platform_name}/{extension_name}.duckdb_extension.gz
```

For example:

```text
https://extensions.duckdb.org/v{{ site.currentduckdbversion }}/windows_amd64/json.duckdb_extension.gz
```

The list of supported platforms may increase over time, but the current list of platforms includes:
* linux_amd64_gcc4
* linux_amd64
* linux_arm64
* osx_amd64
* osx_arm64
* windows_amd64
* windows_amd64_rtools

See above for a list of extension names and how to pull the latest list of extensions.


## Loading an Extension from Local Storage

Extensions are stored in gzip format, so they must be unzipped prior to use. 
There are many methods to decompress gzip. Here is a Python example:

```python
import gzip
import shutil

with gzip.open('httpfs.duckdb_extension.gz','rb') as f_in:
   with open('httpfs.duckdb_extension', 'wb') as f_out:
     shutil.copyfileobj(f_in, f_out)
```

After unzipping, the install and load commands can be used with the path to the .duckdb_extension file. 
For example, if the file was unzipped into the same directory as where DuckDB is being executed:
```sql
INSTALL 'httpfs.duckdb_extension';
LOAD 'httpfs.duckdb_extension';
```

## Extension Template

A template for creating extensions is available in the [`extension-template` repository](https://github.com/duckdb/extension-template/). Note that this project is work-in-progress.

## Pages in This Section

<!--
any extensions that have their own pages will automatically be added to a table of contents that is rendered directly below this list.
-->
