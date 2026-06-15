---
github_repository: https://github.com/duckdb/duckdb-iceberg
layout: docu
title: Writing to Iceberg
---

The `iceberg` extension supports writing to Iceberg tables that are managed by an [Iceberg REST Catalog]({% link docs/current/core_extensions/iceberg/iceberg_rest_catalogs.md %}). All write operations go through the attached catalog and are committed as new Iceberg snapshots.

> Writing requires an attached catalog. The path-based `iceberg_scan` interface described in the [overview]({% link docs/current/core_extensions/iceberg/overview.md %}) is read-only. To write, first [attach an Iceberg REST catalog]({% link docs/current/core_extensions/iceberg/iceberg_rest_catalogs.md %}).

The examples below assume a catalog has been attached as `my_catalog`.

## Creating Schemas and Tables

Iceberg namespaces are exposed as schemas. You can create and drop schemas and tables with standard SQL:

```sql
CREATE SCHEMA my_catalog.sales;
USE my_catalog.sales;

CREATE TABLE my_catalog.sales.events (
    id INTEGER,
    event_name VARCHAR,
    event_time TIMESTAMP
);

-- Create a table from a query
CREATE TABLE my_catalog.sales.events_copy AS
    FROM my_catalog.sales.events;

DROP TABLE my_catalog.sales.events_copy;
```

## Partitioning

Tables can be partitioned with the `PARTITIONED BY` clause using the [Iceberg partition transforms](https://iceberg.apache.org/spec/#partition-transforms):

| Transform | Description |
| --- | --- |
| `⟨column⟩`{:.language-sql .highlight} | Identity – partition by the column value directly. |
| `year(⟨column⟩)`{:.language-sql .highlight}, `month(⟨column⟩)`{:.language-sql .highlight}, `day(⟨column⟩)`{:.language-sql .highlight}, `hour(⟨column⟩)`{:.language-sql .highlight} | Partition by a date/timestamp component. |
| `bucket(⟨n⟩, ⟨column⟩)`{:.language-sql .highlight} | Hash the column into `n` buckets. |
| `truncate(⟨n⟩, ⟨column⟩)`{:.language-sql .highlight} | Truncate the column value to width `n`. |

```sql
CREATE TABLE my_catalog.sales.events (
    id INTEGER,
    event_name VARCHAR,
    event_time TIMESTAMP
)
PARTITIONED BY (day(event_time), bucket(16, id));
```

The partition spec can be changed on an existing table with `ALTER TABLE ... SET PARTITIONED BY`:

```sql
ALTER TABLE my_catalog.sales.events SET PARTITIONED BY (month(event_time));
```

> The `write.target-file-size-bytes` and `write.parquet.row-group-size-bytes` table properties are not honored for partitioned tables and raise an error. Set [`ignore_target_file_size_for_partitioned_tables`]({% link docs/current/core_extensions/iceberg/reference.md %}#settings) or `ignore_row_group_size_for_partitioned_tables` to `true` to ignore them instead.

## Table Properties

[Iceberg table properties](https://iceberg.apache.org/spec/#table-metadata-fields) can be set at creation time with a `WITH` clause. The `format-version` and `location` keys are recognized specially; any other key-value pairs are stored as table properties:

```sql
CREATE TABLE my_catalog.sales.events (a INTEGER)
WITH (
    'format-version' = '2',                 -- Iceberg format version (2 or 3)
    'location' = 's3://my-bucket/events',   -- base location for the table's data
    'my.custom.property' = 'value'
);
```

Existing properties can be inspected and modified with the property functions:

```sql
-- View properties
SELECT * FROM iceberg_table_properties(my_catalog.sales.events);

-- Set properties
CALL set_iceberg_table_properties(
    my_catalog.sales.events,
    MAP {'write.update.mode': 'merge-on-read', 'write.delete.mode': 'merge-on-read'}
);

-- Remove properties
CALL remove_iceberg_table_properties(my_catalog.sales.events, ['my.custom.property']);
```

See the [Functions and Settings Reference]({% link docs/current/core_extensions/iceberg/reference.md %}#table-and-schema-property-functions) for the equivalent schema (namespace) property functions.

## Inserting Data

```sql
INSERT INTO my_catalog.sales.events
VALUES (1, 'click', TIMESTAMP '2026-06-01 10:00:00');

-- Insert the result of a query
INSERT INTO my_catalog.sales.events
    SELECT * FROM source_table;

-- Match columns by name rather than position
INSERT INTO my_catalog.sales.events BY NAME
    SELECT event_time, id, event_name FROM source_table;
```

## Updating and Deleting

```sql
UPDATE my_catalog.sales.events SET event_name = 'view' WHERE id = 1;

DELETE FROM my_catalog.sales.events WHERE event_time < TIMESTAMP '2026-01-01';
```

`UPDATE` and `DELETE` are supported on both partitioned and unpartitioned tables. They use **merge-on-read** semantics and write **positional delete** files; see [Limitations](#limitations).

## Merging Data

`MERGE INTO` performs an upsert against a source relation. The join key is given with a second `USING` clause (see the [`MERGE INTO` statement]({% link docs/current/sql/statements/merge_into.md %})):

```sql
MERGE INTO my_catalog.sales.events AS target
USING new_events AS source USING (id)
WHEN MATCHED THEN UPDATE SET event_name = source.event_name
WHEN NOT MATCHED THEN INSERT VALUES (source.id, source.event_name, source.event_time);
```

## Evolving the Schema

The following `ALTER TABLE` operations are supported:

```sql
ALTER TABLE my_catalog.sales.events ADD COLUMN source VARCHAR DEFAULT 'web';
ALTER TABLE my_catalog.sales.events DROP COLUMN source;
ALTER TABLE my_catalog.sales.events RENAME COLUMN id TO event_id;
ALTER TABLE my_catalog.sales.events ALTER COLUMN event_id TYPE BIGINT;
ALTER TABLE my_catalog.sales.events RENAME TO event_log;
ALTER TABLE my_catalog.sales.events ALTER COLUMN event_id SET DEFAULT 0;
ALTER TABLE my_catalog.sales.events ALTER COLUMN event_id DROP DEFAULT;
```

## Copying Between DuckDB and Iceberg

Because the full DDL and DML set is supported, [`COPY FROM DATABASE`]({% link docs/current/sql/statements/copy.md %}#copy-from-database--to) can perform deep copies between Iceberg and DuckDB storage in either direction:

```sql
COPY FROM DATABASE duckdb_db TO my_catalog;
COPY FROM DATABASE my_catalog TO duckdb_db;
```

To copy an Iceberg catalog into [DuckLake]({% link docs/current/core_extensions/ducklake.md %}), see [Interoperability with DuckLake]({% link docs/current/core_extensions/iceberg/overview.md %}#interoperability-with-ducklake).

## Limitations

* `UPDATE` and `DELETE` write **positional deletes** only; copy-on-write is not supported.
* `UPDATE` and `DELETE` only support **merge-on-read** semantics. If a table sets `write.update.mode` or `write.delete.mode` to anything other than `merge-on-read`, the operation fails.
* The `write.target-file-size-bytes` and `write.parquet.row-group-size-bytes` table properties are not honored for partitioned tables (see [Partitioning](#partitioning)).
