---
layout: post
title: "Schema Evolution End-to-End: CDC Replication → Apache Iceberg → DuckDB"
authors:
  - Olake Go
excerpt: "Schema changes in source databases — added columns, widened types, dropped fields — propagate automatically through Iceberg to DuckDB when a CDC replication tool keeps the schema in sync. This post shows the complete path, from configuring replication to querying the evolved table in DuckDB."
tag: using-duckdb
---

When an operational database evolves — a column is added, a type is widened, a field is removed — downstream analytics pipelines often need manual intervention: update the warehouse schema, backfill historical rows, fix queries. Apache Iceberg handles these changes through metadata-only schema evolution, which means no data files are rewritten. When a CDC replication tool propagates the schema change to Iceberg, DuckDB reads the new schema on the next query, with no session restart and no manual step.

This post walks the complete path: an operational database undergoes schema changes, [Olake Go](https://olake.io/olake-go/) replicates those changes into an Iceberg table on S3, and DuckDB queries the evolved table through an AWS Glue catalog.

> This example uses PostgreSQL as the source database. Olake Go supports the same CDC workflow for MySQL, MongoDB, Oracle, MSSQL, DB2, Kafka, and S3. Only the `source.json` changes; everything else in this post applies to any supported source.

## Prerequisites

* [DuckDB](https://duckdb.org/docs/installation/) with the [`iceberg`]({% link docs/2.0/core_extensions/iceberg/overview.md %}) and [`aws`]({% link docs/2.0/core_extensions/aws.md %}) extensions
* [Docker](https://docs.docker.com/get-docker/)
* An AWS account with an S3 bucket and Glue Data Catalog access
* PostgreSQL with logical replication enabled (`wal_level = logical`)

## Configure Olake Go

Olake Go reads from three config files: `source.json` (connection to the source database), `destination.json` (the Iceberg catalog and storage target), and `selected_streams.json` (which tables to replicate and how).

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

**`~/olake-config/destination.json`** — AWS Glue as the Iceberg catalog, S3 as storage:

```json
{
  "type": "ICEBERG",
  "writer": {
    "catalog_type": "glue",
    "catalog_name": "olake_iceberg",
    "iceberg_s3_path": "s3://⟨bucket_name⟩/",
    "aws_region": "⟨aws_region⟩",
    "aws_access_key": "⟨aws_access_key⟩",
    "aws_secret_key": "⟨aws_secret_key⟩",
    "arrow_writes": false
  }
}
```

## Discover Streams

Run `discover` to let Olake Go inspect the source and write `available_streams.json` and `selected_streams.json`:

```bash
docker run --pull=always \
  -v ~/olake-config:/mnt/config \
  olakego/source-postgres:latest \
  discover \
  --config /mnt/config/source.json
```

The output files appear in `~/olake-config`. Edit `selected_streams.json` to configure each table. To automatically pick up new columns when the source schema changes, set `sync_new_columns` to `true`:

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

## Start the Initial Sync

Run `sync` to perform the initial full load and then continue in CDC mode:

```bash
docker run --pull=always \
  -v ~/olake-config:/mnt/config \
  olakego/source-postgres:latest \
  sync \
  --config /mnt/config/source.json \
  --selected-streams /mnt/config/selected_streams.json \
  --available-streams /mnt/config/available_streams.json \
  --destination /mnt/config/destination.json \
  --state /mnt/config/state.json
```

Olake Go writes a `state.json` to the config directory. Pass `--state /mnt/config/state.json` on subsequent runs so the sync resumes from where it left off instead of doing a full refresh.

After the initial sync, the `orders` table is in Glue and its data files are on S3. DuckDB can now query it.

## Attach the Catalog in DuckDB

```sql
INSTALL iceberg;
INSTALL aws;
LOAD iceberg;
LOAD aws;

CREATE SECRET (
    TYPE s3,
    PROVIDER credential_chain,
    REGION '⟨aws_region⟩'
);

ATTACH '⟨account_id⟩' AS glue_catalog (
    TYPE iceberg,
    ENDPOINT_TYPE 'glue'
);
```

Query the table:

```sql
DESCRIBE glue_catalog.public.orders;
```

```text
┌─────────────┬─────────────┬─────────┐
│ column_name │ column_type │  null   │
├─────────────┼─────────────┼─────────┤
│ order_id    │   INTEGER   │   YES   │
│ customer_id │   INTEGER   │   YES   │
│ order_time  │  TIMESTAMP  │   YES   │
│ amount      │   DOUBLE    │   YES   │
└─────────────┴─────────────┴─────────┘
```

## Schema Change 1: Adding a Column

Add a `region` column in the source database:

```sql
ALTER TABLE orders ADD COLUMN region VARCHAR(50);
```

On the next sync run, Olake Go detects the new column and adds it to the Iceberg schema with a new field ID. Historical rows receive `NULL` for `region`; new rows carry the value. Rerun the sync command (with `--state`) and then query from DuckDB:

```sql
DESCRIBE glue_catalog.public.orders;
```

```text
┌─────────────┬─────────────┬─────────┐
│ column_name │ column_type │  null   │
├─────────────┼─────────────┼─────────┤
│ order_id    │   INTEGER   │   YES   │
│ customer_id │   INTEGER   │   YES   │
│ order_time  │  TIMESTAMP  │   YES   │
│ amount      │   DOUBLE    │   YES   │
│ region      │   VARCHAR   │   YES   │
└─────────────┴─────────────┴─────────┘
```

The column is there, and existing data files are untouched. Iceberg stores the schema as metadata; the Parquet files themselves do not change.

> Note `sync_new_columns: true` in `selected_streams.json` is what causes the new column to be picked up automatically. Without it, you must add the column to `selected_columns.columns` manually and re-run with `--discover-schema`.

## Schema Change 2: Widening a Type

Promote `customer_id` from `INTEGER` to `BIGINT` at the source:

```sql
ALTER TABLE orders ALTER COLUMN customer_id TYPE BIGINT;
```

Iceberg v2 supports type widening promotions natively: `INT → BIGINT`, `FLOAT → DOUBLE`, `DATE → TIMESTAMP`, and `DECIMAL` precision increases. Olake Go propagates the type change to the Iceberg schema. No data files are rewritten — the promotion is a metadata-only change. DuckDB reflects it on the next query:

```sql
DESCRIBE glue_catalog.public.orders;
```

```text
┌─────────────┬─────────────┬─────────┐
│ column_name │ column_type │  null   │
├─────────────┼─────────────┼─────────┤
│ order_id    │   INTEGER   │   YES   │
│ customer_id │    BIGINT   │   YES   │  ← widened
│ order_time  │  TIMESTAMP  │   YES   │
│ amount      │   DOUBLE    │   YES   │
│ region      │   VARCHAR   │   YES   │
└─────────────┴─────────────┴─────────┘
```

## Schema Change 3: Dropping a Column

Drop `amount` at the source:

```sql
ALTER TABLE orders DROP COLUMN amount;
```

When Olake Go detects the drop, it updates the Iceberg schema so new rows arrive without the column. Crucially, Iceberg does not remove the column from the existing data files. The column stays in the schema for historical snapshots. DuckDB's `AT (VERSION = ...)` syntax makes historical data queryable alongside the current schema:

```sql
-- Current snapshot: no amount column
DESCRIBE glue_catalog.public.orders;

-- Historical snapshot: amount column present
SELECT order_id, amount
FROM glue_catalog.public.orders
AT (VERSION = ⟨snapshot_id⟩)
LIMIT 5;
```

To find the snapshot ID before the drop:

```sql
SELECT snapshot_id, committed_at
FROM iceberg_snapshots(glue_catalog.public.orders)
ORDER BY committed_at;
```

## Why This Matters

DuckDB resolves the Iceberg table schema from the catalog's current metadata on every query. When Olake Go commits a schema change to the catalog, DuckDB picks it up immediately — no session restart, no manual `ALTER TABLE` in DuckDB, no pipeline pause. The Glue catalog is the single source of schema truth for both the replication tool and the query engine.

## Further Reading

* [Iceberg Catalogs supported by DuckDB]({% link docs/2.0/core_extensions/iceberg/catalogs.md %})
* [Writing to Iceberg with DuckDB — schema evolution]({% link docs/2.0/core_extensions/iceberg/writing_to_iceberg.md %}#alter-table-and-schema-evolution)
* [Olake Go CDC replication](https://olake.io/olake-go/)
* [Olake Go schema evolution documentation](https://olake.io/docs/features/schema/)
* [Olake Go supported catalogs](https://olake.io/docs/understanding/compatibility-catalogs/)
