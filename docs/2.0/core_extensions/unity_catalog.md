---
github_repository: https://github.com/duckdb/unity_catalog
layout: docu
redirect_from:
- /docs/extensions/unity_catalog
- /docs/stable/extensions/unity_catalog
- /docs/stable/core_extensions/unity_catalog
- /docs/current/core_extensions/unity_catalog
- /docs/lts/core_extensions/unity_catalog
- /docs/preview/core_extensions/unity_catalog
title: Unity Catalog Extension
---

The `unity_catalog` extension attaches a [Unity Catalog](https://www.unitycatalog.io/) catalog, on Databricks or Unity Catalog OSS, as a DuckDB database. You can list, read, insert into, and create its [Delta Lake](https://delta.io/) tables. It uses the [`delta` extension]({% link docs/2.0/core_extensions/delta.md %}) to access the tables.

For implementation details, see the [“Delta Grows Up: Writes, Unity Catalog and Time Travel” blog post]({% post_url 2026-05-07-delta-uc-updates %}).

> Note Both extensions are available on [a subset of platforms](#supported-platforms).

## Installing and Loading

The `unity_catalog` extension will be transparently [autoloaded]({% link docs/2.0/extensions/overview.md %}#autoloading-extensions) on first use from the official extension repository. It loads the `delta` extension itself.
If you would like to install and load it manually, run:

```sql
INSTALL AND LOAD unity_catalog;
```

## Usage

To connect to Unity Catalog on Databricks or Unity Catalog OSS, create a secret with your token, endpoint, and region, then attach a catalog:

```sql
CREATE SECRET (
    TYPE unity_catalog,
    TOKEN '⟨token⟩',
    ENDPOINT '⟨endpoint⟩',
    AWS_REGION '⟨region⟩'
);
ATTACH '⟨catalog_name⟩' AS my_catalog (TYPE unity_catalog, DEFAULT_SCHEMA 'main');
```

* `ENDPOINT` is the Unity Catalog REST API endpoint. For Databricks, it is your [Workspace URL](https://docs.databricks.com/aws/en/workspace/workspace-details#workspace-instance-names-urls-and-ids), typically `https://⟨instance⟩.cloud.databricks.com/`{:.language-sql .highlight}.
* `TOKEN` is a credential. For Databricks, it can be a [personal access token](https://docs.databricks.com/aws/en/dev-tools/auth/pat) with `unity-catalog` scope; see [Access Control in Unity Catalog](https://docs.databricks.com/aws/en/data-governance/unity-catalog/access-control/) for the other options. For Unity Catalog OSS, see the [OSS Unity Catalog documentation](https://docs.unitycatalog.io/).
* `AWS_REGION` is the region of the storage that holds the tables. It is required.

To read and write the table files, DuckDB also needs a [secret]({% link docs/2.0/configuration/secrets_manager.md %}) for that storage, e.g., an [S3 secret]({% link docs/2.0/core_extensions/httpfs/s3api.md %}) or an [Azure secret]({% link docs/2.0/core_extensions/azure.md %}#authentication-with-secret).

> Note Only Databricks reports a default namespace. When you attach a Unity Catalog OSS catalog, always set `DEFAULT_SCHEMA`: without it, queries against the catalog fail, even with fully qualified table names.

### Attach Options

When attaching a Unity Catalog catalog, you can pass the following options to [`ATTACH`]({% link docs/2.0/sql/statements/attach.md %}):

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `SECRET` | `VARCHAR` | unnamed secret | Name of the `unity_catalog` secret to use. Without it, the unnamed `unity_catalog` secret is used. |
| `DEFAULT_SCHEMA` | `VARCHAR` | detected | Schema that unqualified table names resolve to. Without it, DuckDB asks the server for the workspace's default namespace. |
| `READ_ONLY` | `BOOLEAN` | `false` | Attach the catalog in read-only mode. |
| `USE_IRC_SCAN_PLAN` | `BOOLEAN` | `false` | Plan scans on the server (Databricks only); see [Server-Side Scan Planning](#server-side-scan-planning). |

### Reading

Tables are named `⟨catalog⟩.⟨schema⟩.⟨table⟩`{:.language-sql .highlight}; names without a schema resolve to `DEFAULT_SCHEMA`:

```sql
SHOW ALL TABLES;
SELECT * FROM my_catalog.my_schema.my_table LIMIT 10;
```

### Time Travel

> New Time travel by timestamp was introduced in DuckDB 2.0.

To read a table as of a version or a point in time, use the `AT` clause:

```sql
SELECT * FROM my_catalog.my_schema.my_table AT (VERSION => 5);
SELECT * FROM my_catalog.my_schema.my_table AT (TIMESTAMP => TIMESTAMPTZ '2026-10-01 12:00:00+00');
```

A timestamp reads the latest version committed at or before that time. A timestamp before the table's first commit or later than the current time fails with an error.

### Writing

To append rows, use `INSERT INTO`:

```sql
INSERT INTO my_catalog.my_schema.my_table VALUES (1, 'hello');
INSERT INTO my_catalog.my_schema.my_table SELECT * FROM other_table;
```

### Data Types

Unity Catalog column types map to DuckDB types as follows. Since v1.5.6, DuckDB reads them from the table's Delta log.

* `timestamp` maps to `TIMESTAMP WITH TIME ZONE` and, since v1.5.6, `timestamp_ntz` to `TIMESTAMP`.
* Since v1.5.6, a column of a type that DuckDB cannot read is listed with the type `UNKNOWN`, e.g., in `DESCRIBE`. Reading the table fails with an error that names the column.

#### VARIANT Columns

> New Support for `VARIANT` columns was introduced in DuckDB 2.0.

Unity Catalog's `variant` maps to `VARIANT`. `VARIANT` columns can be read whether their files are shredded or not. Inserts write shredded variants if the table sets `delta.enableVariantShredding`. An `INSERT` into a table with a `VARIANT` inside a struct, list, or map fails with an error.

### Creating Tables

> New This feature was introduced in DuckDB 2.0.

`CREATE TABLE` in a Unity Catalog schema writes the first version of a new Delta table and registers the table with Unity Catalog.

Without a location, the table is a managed table: Unity Catalog chooses where it is stored, and the table uses [catalog-managed commits](#catalog-managed-commits):

```sql
CREATE TABLE my_catalog.my_schema.my_table (id INTEGER, name VARCHAR);
```

With the `location` option, the table is an external table at that location. The location can be any expression that evaluates to an absolute path or a URI:

```sql
CREATE TABLE my_catalog.my_schema.my_external_table (id INTEGER, name VARCHAR)
WITH (location = 's3://⟨my_bucket⟩/⟨path⟩');
```

Both managed and external tables can be partitioned:

```sql
CREATE TABLE my_catalog.my_schema.my_partitioned_table (id INTEGER, part VARCHAR)
PARTITIONED BY (part);
```

`CREATE TABLE IF NOT EXISTS` does nothing if Unity Catalog already has a table with this name.

For the forms and options that `CREATE TABLE` does not support, see [Limitations](#limitations).

> Warning Unity Catalog registers the table while `CREATE TABLE` runs, so a `ROLLBACK` of the surrounding transaction does not remove the table.

### Checkpointing

Since v1.5.1, `unity_catalog_checkpoint_table` compacts the Delta log of a table into a checkpoint file, which speeds up reads of tables with long logs. Pass the table name as a string, either fully qualified or relative to the catalog and schema set with `USE`:

```sql
CALL unity_catalog_checkpoint_table('my_catalog.my_schema.my_table');
```

The `CHECKPOINT` statement does not apply to Unity Catalog tables and fails with an error.

### Server-Side Scan Planning

> New This feature was introduced in DuckDB 2.0.

Databricks can plan scans on the server, through the Iceberg REST Catalog (IRC) API of Unity Catalog. The API uses catalog-wide statistics, which can improve filtering and reduce the number of files that a query scans. Unity Catalog OSS does not offer this API.

With `USE_IRC_SCAN_PLAN true`, DuckDB sends each scan's filters to the server and reads only the files that it returns, with their delete files. DuckDB still applies the filters itself:

```sql
ATTACH '⟨catalog_name⟩' AS my_catalog (
    TYPE unity_catalog,
    DEFAULT_SCHEMA 'main',
    USE_IRC_SCAN_PLAN true
);
```

* If the server cannot plan a scan, e.g., because it does not offer the API or refuses the table, DuckDB reads the table through its Delta log instead, and does not try scan planning again on this attached catalog for 15 minutes.
* Time travel queries (`AT (...)`) always read through the Delta log.
* Positional delete files and deletion vectors are applied. A table with equality delete files fails with an error; to read it, attach the catalog without `USE_IRC_SCAN_PLAN`.

### Catalog-Managed Commits

Managed tables in Databricks and in Unity Catalog OSS may use catalog-managed commits (Catalog-Coordinated Commits / CCv2), where Unity Catalog coordinates commits rather than writers committing directly to the Delta log. Since v1.5.2 (v1.5.5 for Unity Catalog OSS), DuckDB uses this protocol when the attached table requires it. `INSERT` statements are identical in syntax, but they commit through the catalog-managed write protocol, so Unity Catalog coordinates concurrent writers. For details, see the [“Delta Grows Up: Writes, Unity Catalog and Time Travel” blog post]({% post_url 2026-05-07-delta-uc-updates %}#catalog-managed-tables).

A managed table that DuckDB [creates](#creating-tables) uses catalog-managed commits. Tables created by other clients, e.g., Spark or the Unity Catalog CLI, are read and written the same way.

## Features

This extension supports:

* Listing available tables: `SHOW ALL TABLES;`{:.language-sql .highlight}
* Interacting with tables using standard SQL: `SELECT * FROM ⟨catalog⟩.⟨schema⟩.⟨table⟩;`{:.language-sql .highlight}
* [Time travel](#time-travel): `SELECT * FROM ... AT (VERSION => ...);`{:.language-sql .highlight} and `SELECT * FROM ... AT (TIMESTAMP => ...);`{:.language-sql .highlight}
* Inserts: `INSERT INTO ... VALUES (...);`{:.language-sql .highlight}
* Creating managed and external tables: `CREATE TABLE ... (...);`{:.language-sql .highlight}
* [Checkpointing](#checkpointing) individual tables (since v1.5.1): `CALL unity_catalog_checkpoint_table('my_catalog.my_schema.my_table');`{:.language-sql .highlight}

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
    * `SORTED BY`
    * `WITH` options other than `location`: unlike with the [`delta` extension]({% link docs/2.0/core_extensions/delta.md %}#table-properties), Delta table properties cannot be set

## Supported Platforms

The `unity_catalog` and `delta` extensions support the following platforms:

* Linux (x86_64 and ARM64): `linux_amd64` and `linux_arm64`
* macOS Intel and Apple Silicon: `osx_amd64` and `osx_arm64`
* Windows AMD64: `windows_amd64`

Support for the [other DuckDB platforms]({% link docs/2.0/extensions/extension_distribution.md %}#platforms) is work-in-progress.
