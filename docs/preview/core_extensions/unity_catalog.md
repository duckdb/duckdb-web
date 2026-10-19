---
github_repository: https://github.com/duckdb/unity_catalog
layout: docu
title: Unity Catalog Extension
---

The `unity_catalog` extension adds support for the [`Unity Catalog`](https://www.unitycatalog.io/) atop the
[`Delta Lake`](https://delta.io/) format and [DuckDB Delta extension]({% link docs/preview/core_extensions/delta.md %}).

The [`delta` extension]({% link docs/preview/core_extensions/delta.md %}) adds support for the [Delta Lake open-source storage format](https://delta.io/). It is built using the [Delta Kernel](https://github.com/delta-incubator/delta-kernel-rs). The extension reads and writes Delta tables, both local and remote.

For implementation details, see the [announcement blog post]({% post_url 2024-06-10-delta %}).

> Note Both extensions are [only supported on given platforms](#supported-duckdb-versions-and-platforms).

## Installing and Loading

To install and load, run:

```sql
INSTALL unity_catalog;
LOAD unity_catalog;
```

## Usage

Given that you already have a Unity Catalog setup with either Databricks or Unity Catalog OSS, configure a secret with your token, endpoint, and region, then attach to your catalog:

```sql
CREATE SECRET (
    TYPE unity_catalog,
    TOKEN '⟨token⟩',
    ENDPOINT '⟨endpoint⟩',
    AWS_REGION '⟨region⟩'
);
ATTACH 'my_catalog' AS my_catalog (TYPE unity_catalog, DEFAULT_SCHEMA 'main');
```

Where `ENDPOINT` is your Unity Catalog REST API endpoint and `TOKEN` is a suitable credential. For Databricks, `ENDPOINT` is your [Workspace URL](https://docs.databricks.com/aws/en/workspace/workspace-details#workspace-instance-names-urls-and-ids) (typically `https://⟨instance⟩.cloud.databricks.com/`) and `TOKEN` can be e.g., a [personal access token](https://docs.databricks.com/aws/en/dev-tools/auth/pat) with `unity-catalog` scope — see [Access Control in Unity Catalog](https://docs.databricks.com/aws/en/data-governance/unity-catalog/access-control/) for the full range of options. For OSS Unity Catalog, see the [OSS Unity Catalog documentation](https://docs.unitycatalog.io/).

### Attach Options

When attaching a Unity Catalog catalog, you can pass the following options to `ATTACH`:

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `SECRET` | `VARCHAR` | unnamed secret | Name of the `unity_catalog` secret to use. Without it, the unnamed `unity_catalog` secret is used. |
| `DEFAULT_SCHEMA` | `VARCHAR` | detected | Schema that unqualified table names resolve to. Without it, DuckDB asks the server for the workspace's default namespace. |
| `READ_ONLY` | `BOOLEAN` | `false` | Attach the catalog in read-only mode. |
| `USE_IRC_SCAN_PLAN` | `BOOLEAN` | `false` | Plan scans on the server; see [Server-Side Scan Planning](#server-side-scan-planning). |

> Note Only Databricks reports a default namespace. When you attach a Unity Catalog OSS catalog, always set `DEFAULT_SCHEMA`: without it, queries against the catalog fail, even with fully qualified table names.

### Reading

```sql
SHOW ALL TABLES;
SELECT * FROM my_catalog.my_schema.my_table LIMIT 10;
```

### Time Travel

To read a table as of a version or a point in time, use the `AT` clause:

```sql
SELECT * FROM my_catalog.my_schema.my_table AT (VERSION => 5);
SELECT * FROM my_catalog.my_schema.my_table AT (TIMESTAMP => TIMESTAMPTZ '2026-10-01 12:00:00+00');
```

> New Time travel by timestamp is introduced in DuckDB 2.0.

A timestamp reads the latest version committed at or before that time. A timestamp before the table's first commit or later than the current time fails with an error.

### Writing

Standard inserts are supported:

```sql
INSERT INTO my_catalog.my_schema.my_table VALUES (1, 'hello');
INSERT INTO my_catalog.my_schema.my_table SELECT * FROM other_table;
```

### Data Types

Since v1.5.6, DuckDB reads a table's schema from its Delta log and handles Unity Catalog's column types as follows:

* `timestamp` maps to `TIMESTAMP WITH TIME ZONE` and `timestamp_ntz` to `TIMESTAMP`.
* A column of a type that DuckDB cannot read is listed with the type `UNKNOWN`, e.g., in `DESCRIBE`. Reading the table fails with an error that names the column.

#### Variant Columns

> New Support for `VARIANT` columns is introduced in DuckDB 2.0.

Unity Catalog's `variant` maps to `VARIANT`. `VARIANT` columns can be read, shredded or not. Inserts write shredded variants if the table sets `delta.enableVariantShredding`. Inserts into a table with a `VARIANT` nested in a `STRUCT` or a list fail with an error.

### Creating Tables

> New This feature is introduced in DuckDB 2.0.

`CREATE TABLE` in a Unity Catalog schema writes the first version of a new Delta table and registers the table with Unity Catalog.

Without a location, the table is a managed table: Unity Catalog chooses where it is stored, and the table uses [catalog-managed commits](#catalog-managed-commits):

```sql
CREATE TABLE my_catalog.my_schema.my_table (id INTEGER, name VARCHAR);
```

With the `location` option, the table is an external table at that location. The location can be any expression that evaluates to an absolute path or a URI:

```sql
CREATE TABLE my_catalog.my_schema.my_external_table (id INTEGER, name VARCHAR)
WITH (location = 's3://my-bucket/my_external_table');
```

Both managed and external tables can be partitioned:

```sql
CREATE TABLE my_catalog.my_schema.my_partitioned_table (id INTEGER, part VARCHAR)
PARTITIONED BY (part);
```

`CREATE TABLE IF NOT EXISTS` does nothing if Unity Catalog already has a table with this name.

For the forms and options that `CREATE TABLE` does not support, see [Limitations](#limitations).

> Warning Unity Catalog registers the table while `CREATE TABLE` runs, so a `ROLLBACK` of the surrounding transaction does not remove the table.

### Server-Side Scan Planning

> New This feature is introduced in DuckDB 2.0.

With `USE_IRC_SCAN_PLAN true`, DuckDB asks Unity Catalog to plan each scan through its Iceberg REST Catalog API. DuckDB sends the query's filters, the server prunes the list of files to read and returns it with the table's delete files, and DuckDB reads these files and applies the filters again itself:

```sql
ATTACH 'my_catalog' AS my_catalog (
    TYPE unity_catalog,
    DEFAULT_SCHEMA 'main',
    USE_IRC_SCAN_PLAN true
);
```

* If the server cannot plan a scan, e.g., because it does not offer the API or refuses the table, DuckDB reads the table through its Delta log instead, and does not try scan planning again on this attached catalog for 15 minutes.
* Time travel queries (`AT (...)`) always read through the Delta log.
* Positional delete files and deletion vectors are applied. A table with equality delete files cannot be read with scan planning.

### Catalog-Managed Commits

Managed tables in Databricks and in Unity Catalog OSS may use catalog-managed commits (Catalog-Coordinated Commits / CCv2), where Unity Catalog coordinates commits rather than writers committing directly to the Delta log. Since v1.5.2 (v1.5.5 for Unity Catalog OSS), DuckDB transparently uses this protocol when the attached table requires it — the insert syntax is identical:

```sql
INSERT INTO my_catalog.my_schema.my_catalog_managed_table VALUES (1, 'hello');
```

A managed table that DuckDB [creates](#creating-tables) uses catalog-managed commits. Tables created by other clients, e.g., Spark or the Unity Catalog CLI, are read and written the same way.

## Features

This extension supports:

* Listing available tables: `SHOW ALL TABLES;`{:.language-sql .highlight}
* Interacting with tables using standard SQL: `SELECT * FROM ⟨catalog⟩.⟨schema⟩.⟨table⟩;`{:.language-sql .highlight}
* [Time travel](#time-travel): `SELECT * FROM ... AT (VERSION => ...);`{:.language-sql .highlight} and `SELECT * FROM ... AT (TIMESTAMP => ...);`{:.language-sql .highlight}
* Inserts: `INSERT INTO ... VALUES (...);`{:.language-sql .highlight}
* Creating managed and external tables: `CREATE TABLE ... (...);`{:.language-sql .highlight}
* Checkpointing individual tables (since v1.5.1): `CALL unity_catalog_checkpoint_table('my_catalog.my_schema.my_table');`{:.language-sql .highlight}

## Limitations

* `DELETE` and `UPDATE` are not supported.
* `DROP TABLE` and `ALTER TABLE` are not supported, nor is creating or changing views or schemas.
* Inserts into a table with column `DEFAULT` values or generated columns fail with an error, as DuckDB cannot compute these columns yet.
* Reading a table with an `INTERVAL` column fails with an error, as Delta intervals and DuckDB's `INTERVAL` differ in meaning.
* The following `CREATE TABLE` forms and options are not supported and fail with an error:
    * `CREATE OR REPLACE TABLE` and `CREATE TABLE ... AS SELECT`
    * constraints, including `NOT NULL` and `PRIMARY KEY`
    * column `DEFAULT` values and generated columns
    * columns of a type that Delta cannot store, e.g., `TIME`
    * `SORTED BY`, and `WITH` options other than `location`, including Delta table properties

## Supported DuckDB Versions and Platforms

The `unity_catalog` (and `delta`) extension currently supports the following platforms:

* Linux AMD64 (x86_64 and ARM64): `linux_amd64` and `linux_arm64`
* macOS Intel and Apple Silicon: `osx_amd64` and `osx_arm64`
* Windows AMD64: `windows_amd64`

Support for the [other DuckDB platforms]({% link docs/preview/extensions/extension_distribution.md %}#platforms) is work-in-progress.
