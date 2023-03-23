---
layout: docu
title: Postgres Scanner
selected: Documentation/Postgres Scanner
---

The `postgres` extension allows DuckDB to directly read data from a running Postgres instance. The data can be queried directly from the underlying Postgres tables, or read into DuckDB tables.

## Loading the Extension

In order to use the Postgres extension it must first be installed and loaded. This can be done using the following commands:

```sql
INSTALL postgres;
LOAD postgres;
```

## Usage

To make a Postgres database accessible to DuckDB, use the `POSTGRES_ATTACH` command:

```sql
-- load all data from "public" schema of the postgres instance running on localhost into the schema "main"  
CALL POSTGRES_ATTACH('');
-- attach the database with the given schema, loading tables from the source schema "public" into the target schema "abc"
CALL postgres_attach('dbname=postgres user=postgres host=127.0.0.1', source_schema='public', sink_schema='abc');
```

`POSTGRES_ATTACH` takes a single required string parameter, which is the [`libpq` connection string](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING). For example you can pass `'dbname=postgresscanner'` to select a different database name. In the simplest case, the parameter is just `''`. There are three additional named parameters:

* `source_schema` the name of a non-standard schema name in Postgres to get tables from. Default is `public`.
* `sink_schema` the schema name in DuckDB to create views. Default is `main`.
* `overwrite` whether we should overwrite existing views in the target schema, default is `false`.
* `filter_pushdown` whether filter predicates that DuckDB derives from the query should be forwarded to Postgres, defaults to `false`.


The tables in the database are registered as views in DuckDB, you can list them as follows:

```sql
PRAGMA show_tables;
```

Then you can query those views normally using SQL.

## Querying individual tables
If you prefer to not attach all tables, but just query a single table, that is possible using the `POSTGRES_SCAN` function, e.g.

```sql
SELECT * FROM POSTGRES_SCAN('', 'public', 'mytable');
```

`POSTGRES_SCAN` takes three string parameters, the `libpq` connection string (see above), a Postgres schema name and a table name. The schema name is often `public`.

To use `filter_pushdown` use the `POSTGRES_SCAN_PUSHDOWN` function.

## Extra Information
See [the repo](https://github.com/duckdblabs/postgresscanner) for the source code of the extension, or the [official announcement](/2022/09/30/postgres-scanner) for implementation details and background.
