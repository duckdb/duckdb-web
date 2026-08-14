---
github_repository: https://github.com/duckdb/unity_catalog
layout: docu
redirect_from:
- /docs/extensions/unity_catalog
- /docs/stable/extensions/unity_catalog
- /docs/preview/core_extensions/unity_catalog
- /docs/stable/core_extensions/unity_catalog
title: Unity Catalog Extension
---

The `unity_catalog` extension adds support for the [`Unity Catalog`](https://www.unitycatalog.io/) atop the
[`Delta Lake`](https://delta.io/) format and [DuckDB Delta extension]({% link docs/current/core_extensions/delta.md %}).

The [`delta` extension]({% link docs/current/core_extensions/delta.md %}) adds support for the [Delta Lake open-source storage format](https://delta.io/). It is built using the [Delta Kernel](https://github.com/delta-incubator/delta-kernel-rs). The extension offers **read support** for Delta tables, both local and remote.

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

### Reading

```sql
SHOW ALL TABLES;
SELECT * FROM my_catalog.my_schema.my_table LIMIT 10;
```

### Writing

Standard inserts are supported:

```sql
INSERT INTO my_catalog.my_schema.my_table VALUES (1, 'hello');
INSERT INTO my_catalog.my_schema.my_table SELECT * FROM other_table;
```

### Catalog-Managed Commits

Databricks Unity Catalog tables may use catalog-managed commits (Catalog-Coordinated Commits / CCv2), where commit coordination is handled by Databricks rather than written directly to the Delta log. DuckDB transparently uses this protocol when the attached table requires it — the insert syntax is identical:

```sql
INSERT INTO my_catalog.my_schema.my_catalog_managed_table VALUES (1, 'hello');
```

> Note DuckDB does not yet support `CREATE TABLE` DDL, so CMC-enabled tables must be created via Spark or the UC CLI (setting the `delta.feature.catalogManaged` table property). Once a table is CMC-enabled, DuckDB reads and writes it transparently.

## Features

This extension supports:

- Listing available tables: `SHOW ALL TABLES;`{:.language-sql .highlight}
- Interacting with tables using standard SQL: `SELECT * FROM ⟨catalog⟩.⟨schema⟩.⟨table⟩;`{:.language-sql .highlight}
- Time travel: `SELECT * FROM ... AT (VERSION => ...);`{:.language-sql .highlight}
- Inserts: `INSERT INTO ... VALUES (...);`{:.language-sql .highlight}
- Checkpointing individual tables: `CALL unity_catalog_checkpoint_table('my_catalog.my_schema.my_table');`{:.language-sql .highlight}

It does not currently support:

- `DELETE`{:.language-sql .highlight} or `UPDATE`{:.language-sql .highlight}
- Creation or manipulation of tables, views or schemas

## Supported DuckDB Versions and Platforms

The `unity_catalog` (and `delta`) extension currently supports the following platforms:

- Linux AMD64 (x86_64 and ARM64): `linux_amd64` and `linux_arm64`
- macOS Intel and Apple Silicon: `osx_amd64` and `osx_arm64`
- Windows AMD64: `windows_amd64`

Support for the [other DuckDB platforms]({% link docs/current/extensions/extension_distribution.md %}#platforms) is work-in-progress.
