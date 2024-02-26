---
layout: docu
title: PostgreSQL Scanner Extension
redirect_from:
  - docs/archive/0.9.1/extensions/postgres_scanner
---

The `postgres` extension allows DuckDB to directly read data from a running PostgreSQL instance. The data can be queried directly from the underlying PostgreSQL tables, or read into DuckDB tables. See the [official announcement](/2022/09/30/postgres-scanner) for implementation details and background.

## Usage

To make a PostgreSQL database accessible to DuckDB, use the `postgres_attach` command:

```sql
-- load all data from "public" schema of the postgres instance running on localhost into the schema "main"  
CALL postgres_attach('');
-- attach the database with the given schema, loading tables from the source schema "public" into the target schema "abc"
CALL postgres_attach('dbname=postgres user=postgres host=127.0.0.1', source_schema='public', sink_schema='abc');
```

`postgres_attach` takes a single required string parameter, which is the [`libpq` connection string](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING). For example you can pass `'dbname=postgresscanner'` to select a different database name. In the simplest case, the parameter is just `''`. There are three additional named parameters:

* `source_schema` the name of a non-standard schema name in PostgreSQL to get tables from. Default: `public`.
* `sink_schema` the schema name in DuckDB to create views. Default: `main`.
* `overwrite` whether we should overwrite existing views in the target schema. Default: `false`.
* `filter_pushdown` whether filter predicates that DuckDB derives from the query should be forwarded to PostgreSQL. Default: `false`.


The tables in the database are registered as views in DuckDB, you can list them as follows:

```sql
PRAGMA show_tables;
```

Then you can query those views normally using SQL.

## Querying Individual Tables

If you prefer to not attach all tables, but just query a single table, that is possible using the `postgres_scan` function, e.g.:

```sql
SELECT * FROM postgres_scan('', 'public', 'mytable');
```

The `postgres_scan` function takes three string parameters, the `libpq` connection string (see above), a PostgreSQL schema name and a table name. The schema often used in PostgreSQL is `public`.

To use `filter_pushdown` use the `postgres_scan_pushdown` function.

## Loading the Extension

PostgreSQL extension will be, by default, autoloaded on first use. If you prefer to do so explicitly, it can always be done using the following commands:

```sql
INSTALL postgres;
LOAD postgres;
```

## GitHub Repository

[<span class="github">GitHub</span>](https://github.com/duckdb/postgres_scanner)