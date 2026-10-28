---
layout: post
title: "Schema Evolution End-to-End: CDC Replication → Apache Iceberg → DuckDB"
authors:
  - Olake Go
excerpt: "Schema changes in source databases — added columns, widened types, dropped fields — propagate automatically through Iceberg to DuckDB when a CDC replication tool keeps the schema in sync. This post shows the complete path, from configuring replication to querying the evolved table in DuckDB."
tag: using-duckdb
---

Schema changes in operational databases — added columns, widened types, dropped fields — typically force manual pipeline updates. Apache Iceberg's metadata-only schema evolution removes that burden: a CDC tool propagates the change, and DuckDB reads the new schema on the next query with no manual step.

This post walks the complete path using [Olake Go](https://olake.io/olake-go/) — an [open-source EL platform](https://olake.io/docs/) for CDC and incremental replication to Apache Iceberg — with DuckDB querying the results through [Lakekeeper](https://lakekeeper.io), an open-source Iceberg REST Catalog.

> This example uses PostgreSQL. Olake Go supports the same replication workflow for MySQL, MongoDB, Oracle, MSSQL, DB2, Kafka, and S3 — only `source.json` changes.

## Pipeline Overview

```text
┌────────────────┐   WAL / binlog   ┌─────────────────┐   Parquet + metadata   ┌─────────────────┐
│  Source DB     │ ───────────────> │   Olake Go      │ ─────────────────────> │  S3 (Iceberg)   │
│  (PostgreSQL)  │                  │   CDC sync      │                         │  data files     │
└────────────────┘                  └─────────────────┘                         └────────┬────────┘
                                                                                          │ schema pointer
                                                                                 ┌────────▼────────┐
                                                                                 │  Lakekeeper     │
                                                                                 │  (catalog)      │
                                                                                 └────────┬────────┘
                                                                                          │ ATTACH
                                                                                 ┌────────▼────────┐
                                                                                 │  DuckDB         │
                                                                                 │  SQL queries    │
                                                                                 └─────────────────┘
```

When the source schema changes, Olake Go detects it on the next sync, commits the schema update to Iceberg, and DuckDB reflects the new schema on the following query.

## Prerequisites

* DuckDB with the [`iceberg`]({% link docs/2.0/core_extensions/iceberg/overview.md %}) extension
* [Docker](https://docs.docker.com/get-started/get-docker/)
* A running [Lakekeeper](https://lakekeeper.io) catalog and an S3-compatible object store
* PostgreSQL with logical replication enabled (`wal_level = logical`)

## Configure Olake Go

Clone the Olake repository:

```bash
git clone https://github.com/datazip-inc/olake
```

Olake Go reads from three files: `source.json` (source connection), `destination.json` (the Iceberg catalog), and `selected_streams.json` (which tables to replicate and how).

Create a config directory:

```bash
mkdir -p ~/olake-config
```

**`~/olake-config/source.json`** — PostgreSQL connection and CDC settings:

```json
{
  "host": "⟨db_host⟩",
  "port": 5432,
  "database": "⟨db_name⟩",
  "username": "⟨db_user⟩",
  "password": "⟨db_password⟩",
  "update_method": {
    "type": "CDC",
    "replication_slot": "olake_slot",
    "publication": "olake_pub",
    "initial_wait_time": 120
  }
}
```

Before running Olake Go, create the replication slot and publication in PostgreSQL:

```sql
SELECT pg_create_logical_replication_slot('olake_slot', 'pgoutput');
CREATE PUBLICATION olake_pub FOR ALL TABLES;
```

**`~/olake-config/destination.json`** — Lakekeeper as the Iceberg catalog, S3 as storage:

```json
{
  "type": "ICEBERG",
  "writer": {
    "catalog_type": "rest",
    "rest_catalog_url": "http://⟨lakekeeper_host⟩/catalog",
    "token": "⟨bearer_token⟩",
    "iceberg_s3_path": "⟨warehouse_name⟩",
    "aws_access_key": "⟨s3_access_key⟩",
    "aws_secret_key": "⟨s3_secret_key⟩",
    "aws_region": "⟨s3_region⟩",
    "arrow_writes": false
  }
}
```

## Discover Streams

Run `discover` to inspect the source and write `available_streams.json` to the config directory:

```bash
docker run --pull=always \
  -v ~/olake-config:/mnt/config \
  olakego/source-postgres:latest \
  discover \
  --config /mnt/config/source.json
```

Create `selected_streams.json` to configure the `orders` table. The top-level key is `selected_streams`; each namespace maps to an array of stream objects. Set `sync_new_columns` to `true` so Olake Go automatically picks up columns added to the source after the initial sync:

```json
{
  "selected_streams": {
    "public": [
      {
        "stream_name": "orders",
        "sync_mode": "cdc",
        "selected_columns": {
          "sync_new_columns": true
        }
      }
    ]
  }
}
```

## Start the Sync

Run `sync` to perform the initial full load and then continue in CDC mode:

```bash
docker run --pull=always \
  -v ~/olake-config:/mnt/config \
  olakego/source-postgres:latest \
  sync \
  --config /mnt/config/source.json \
  --selected-streams /mnt/config/selected_streams.json \
  --destination /mnt/config/destination.json \
  --state /mnt/config/state.json
```

Olake Go creates `state.json` after the first run. On subsequent runs, it reads that file to resume from the saved WAL position instead of performing a full reload.

## Attach the Catalog in DuckDB

```sql
INSTALL iceberg;
LOAD iceberg;

CREATE SECRET s3_secret (
    TYPE s3,
    KEY_ID '⟨s3_access_key⟩',
    SECRET '⟨s3_secret_key⟩',
    REGION '⟨s3_region⟩'
);

CREATE SECRET lakekeeper_secret (
    TYPE iceberg,
    TOKEN '⟨bearer_token⟩'
);

ATTACH '⟨warehouse_name⟩' AS lakekeeper_catalog (
    TYPE iceberg,
    URI 'http://⟨lakekeeper_host⟩/catalog',
    SECRET lakekeeper_secret
);
```

Tables are accessible with the three-part name `lakekeeper_catalog.public.orders`.

## Schema Change 1: Adding a Column

Add a `region` column to the source table:

```sql
ALTER TABLE orders ADD COLUMN region VARCHAR(50);
```

Rerun the sync command and then query from DuckDB. Olake Go adds the new field to the Iceberg schema with a new field ID:

```sql
SELECT order_id, region
FROM lakekeeper_catalog.public.orders
ORDER BY order_id
LIMIT 5;
```

Rows inserted before the `ALTER TABLE` return `NULL` for `region`. New rows carry the actual value. The existing Parquet files are never rewritten — Iceberg stores the schema change in a new `metadata.json`, not in the data files.

> Note `sync_new_columns: true` in `selected_streams.json` is required for Olake Go to pick up the new column automatically. Without it, add the column name to the stream's `selected_columns.columns` array in `selected_streams.json` manually before the next sync.

## Schema Change 2: Widening a Type

Promote `customer_id` from `INTEGER` to `BIGINT`:

```sql
ALTER TABLE orders ALTER COLUMN customer_id TYPE BIGINT;
```

Iceberg v2 supports these type widening promotions natively: `INT → BIGINT`, `FLOAT → DOUBLE`, and `DECIMAL` precision increases. Olake Go propagates the type change to the Iceberg schema on the next sync. Iceberg records the new type in a fresh `metadata.json` without rewriting existing data files. DuckDB reflects the new type on the next query:

```sql
DESCRIBE lakekeeper_catalog.public.orders;
```

The `customer_id` column now shows as `BIGINT`. Existing Parquet files that stored the column as 32-bit integers are still readable: DuckDB widens the values on read.

## Schema Change 3: Dropping a Column

Drop `amount` from the source table:

```sql
ALTER TABLE orders DROP COLUMN amount;
```

Olake Go updates the Iceberg schema so incoming rows no longer include the column. Iceberg does not remove the column from the existing data files — the physical files are immutable. The column disappears from the live schema but historical snapshots remain fully intact.

Use `iceberg_snapshots` to find the snapshot committed before the drop:

```sql
SELECT snapshot_id, committed_at
FROM iceberg_snapshots(lakekeeper_catalog.public.orders)
ORDER BY committed_at;
```

Then query a historical snapshot directly with `AT (VERSION => ...)`:

```sql
SELECT order_id, amount
FROM lakekeeper_catalog.public.orders
AT (VERSION => ⟨snapshot_id_before_drop⟩)
LIMIT 5;
```

The historical snapshot returns `amount` even though the live table no longer has it.

In each case, DuckDB resolves the schema from Lakekeeper on every query — when Olake Go commits a schema change, DuckDB picks it up automatically with no manual step.

## Further Reading

* [Iceberg Catalogs supported by DuckDB]({% link docs/2.0/core_extensions/iceberg/catalogs.md %})
* [Lakekeeper in DuckDB]({% link docs/2.0/core_extensions/iceberg/catalogs.md %}#lakekeeper)
* [Writing to Iceberg with DuckDB — schema evolution]({% link docs/2.0/core_extensions/iceberg/writing_to_iceberg.md %}#alter-table-and-schema-evolution)
* [What Is Inside an Iceberg Table?]({% post_url 2026-10-13-inside-iceberg-table %})
* [Olake Go documentation](https://olake.io/olake-go/)
* [Olake Go schema evolution](https://olake.io/docs/features/schema/)
* [Olake Go supported catalogs](https://olake.io/docs/understanding/compatibility-catalogs/)
