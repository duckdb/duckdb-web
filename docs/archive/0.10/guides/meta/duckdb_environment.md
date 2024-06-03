---
layout: docu
title: DuckDB Environment
---

DuckDB provides a number of functions and `PRAGMA` options to retrieve information on the running DuckDB instance and its environment.

## Version

The `version()` function returns the version number of DuckDB.

```sql
SELECT version();
```

| version() |
|-----------|
| v0.10.2   |

Using a `PRAGMA`:

```sql
PRAGMA version;
```

| library_version | source_id  |
|-----------------|------------|
| v0.10.2         | 1601d94f94 |

## Platform

The platform information consists of the operating system, system architecture, and, optionally, the compiler.
The platform is used when [installing extensions](../../extensions/working_with_extensions#platforms).
To retrieve the platform, use the following `PRAGMA`:

```sql
PRAGMA platform;
```

On macOS, running on Apple Silicon architecture, the result is:

| platform  |
|-----------|
| osx_arm64 |

On Windows, running on an AMD64 architecture, the platform is `windows_amd64`.
On CentOS 7, running on the AMD64 architecture, the platform is `linux_amd64_gcc4`.
On Ubuntu 22.04, running on the ARM64 architecture, the platform is `linux_arm64`.

## Extensions

To get a list of DuckDB extension and their status (e.g., `loaded`, `installed`), use the [`duckdb_extensions()` function](../../extensions/overview#listing-extensions):

```sql
SELECT *
FROM duckdb_extensions();
```

## Meta Table Functions

DuckDB has the following built-in table functions to obtain metadata about available catalog objects:

* [`duckdb_columns()`](../../sql/duckdb_table_functions#duckdb_columns): columns
* [`duckdb_constraints()`](../../sql/duckdb_table_functions#duckdb_constraints): constraints
* [`duckdb_databases()`](../../sql/duckdb_table_functions#duckdb_databases): lists the databases that are accessible from within the current DuckDB process
* [`duckdb_dependencies()`](../../sql/duckdb_table_functions#duckdb_dependencies): dependencies between objects
* [`duckdb_extensions()`](../../sql/duckdb_table_functions#duckdb_extensions): extensions
* [`duckdb_functions()`](../../sql/duckdb_table_functions#duckdb_functions): functions
* [`duckdb_indexes()`](../../sql/duckdb_table_functions#duckdb_indexes): secondary indexes
* [`duckdb_keywords()`](../../sql/duckdb_table_functions#duckdb_keywords): DuckDB's keywords and reserved words
* [`duckdb_optimizers()`](../../sql/duckdb_table_functions#duckdb_optimizers): the available optimization rules in the DuckDB instance
* [`duckdb_schemas()`](../../sql/duckdb_table_functions#duckdb_schemas): schemas
* [`duckdb_sequences()`](../../sql/duckdb_table_functions#duckdb_sequences): sequences
* [`duckdb_settings()`](../../sql/duckdb_table_functions#duckdb_settings): settings
* [`duckdb_tables()`](../../sql/duckdb_table_functions#duckdb_tables): base tables
* [`duckdb_types()`](../../sql/duckdb_table_functions#duckdb_types): data types
* [`duckdb_views()`](../../sql/duckdb_table_functions#duckdb_views): views
* [`duckdb_temporary_files()`](../../sql/duckdb_table_functions#duckdb_temporary_files): the temporary files DuckDB has written to disk, to offload data from memory