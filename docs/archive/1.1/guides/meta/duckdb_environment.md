---
layout: docu
title: DuckDB Environment
---

DuckDB provides a number of functions and `PRAGMA` options to retrieve information on the running DuckDB instance and its environment.

## Version

The `version()` function returns the version number of DuckDB.

```sql
SELECT version() AS version;
```

<div class="monospace_table"></div>

| version |
|-----------|
| v{{ site.currentduckdbversion }} |

Using a `PRAGMA`:

```sql
PRAGMA version;
```

<div class="monospace_table"></div>

| library_version | source_id  |
|-----------------|------------|
| v{{ site.currentduckdbversion }} | {{ site.currentduckdbhash }} |

## Platform

The platform information consists of the operating system, system architecture, and, optionally, the compiler.
The platform is used when [installing extensions]({% link docs/archive/1.1/extensions/working_with_extensions.md %}#platforms).
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

To get a list of DuckDB extension and their status (e.g., `loaded`, `installed`), use the [`duckdb_extensions()` function]({% link docs/archive/1.1/extensions/overview.md %}#listing-extensions):

```sql
SELECT *
FROM duckdb_extensions();
```

## Meta Table Functions

DuckDB has the following built-in table functions to obtain metadata about available catalog objects:

* [`duckdb_columns()`]({% link docs/archive/1.1/sql/meta/duckdb_table_functions.md %}#duckdb_columns): columns
* [`duckdb_constraints()`]({% link docs/archive/1.1/sql/meta/duckdb_table_functions.md %}#duckdb_constraints): constraints
* [`duckdb_databases()`]({% link docs/archive/1.1/sql/meta/duckdb_table_functions.md %}#duckdb_databases): lists the databases that are accessible from within the current DuckDB process
* [`duckdb_dependencies()`]({% link docs/archive/1.1/sql/meta/duckdb_table_functions.md %}#duckdb_dependencies): dependencies between objects
* [`duckdb_extensions()`]({% link docs/archive/1.1/sql/meta/duckdb_table_functions.md %}#duckdb_extensions): extensions
* [`duckdb_functions()`]({% link docs/archive/1.1/sql/meta/duckdb_table_functions.md %}#duckdb_functions): functions
* [`duckdb_indexes()`]({% link docs/archive/1.1/sql/meta/duckdb_table_functions.md %}#duckdb_indexes): secondary indexes
* [`duckdb_keywords()`]({% link docs/archive/1.1/sql/meta/duckdb_table_functions.md %}#duckdb_keywords): DuckDB's keywords and reserved words
* [`duckdb_optimizers()`]({% link docs/archive/1.1/sql/meta/duckdb_table_functions.md %}#duckdb_optimizers): the available optimization rules in the DuckDB instance
* [`duckdb_schemas()`]({% link docs/archive/1.1/sql/meta/duckdb_table_functions.md %}#duckdb_schemas): schemas
* [`duckdb_sequences()`]({% link docs/archive/1.1/sql/meta/duckdb_table_functions.md %}#duckdb_sequences): sequences
* [`duckdb_settings()`]({% link docs/archive/1.1/sql/meta/duckdb_table_functions.md %}#duckdb_settings): settings
* [`duckdb_tables()`]({% link docs/archive/1.1/sql/meta/duckdb_table_functions.md %}#duckdb_tables): base tables
* [`duckdb_temporary_files()`]({% link docs/archive/1.1/sql/meta/duckdb_table_functions.md %}#duckdb_temporary_files): the temporary files DuckDB has written to disk, to offload data from memory
* [`duckdb_types()`]({% link docs/archive/1.1/sql/meta/duckdb_table_functions.md %}#duckdb_types): data types
* [`duckdb_views()`]({% link docs/archive/1.1/sql/meta/duckdb_table_functions.md %}#duckdb_views): views