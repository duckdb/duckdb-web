---
layout: docu
title: Writing to Iceberg
---

The DuckDB `iceberg` extension supports writing to Iceberg tables when an [Iceberg catalog]({% link docs/current/core_extensions/iceberg/catalogs.md %}) is attached.
Writing to a table read directly from storage with [`iceberg_scan`]({% link docs/current/core_extensions/iceberg/iceberg_functions.md %}#iceberg_scan) is not supported: the catalog is required to commit the new table metadata.

## Supported Operations

The `iceberg` extension supports the following operations when used with a REST Catalog attached:

* `CREATE/DROP SCHEMA`
* `CREATE/DROP TABLE`
* `INSERT INTO`
* `UPDATE`
* `DELETE`
* `MERGE INTO`
* `ALTER TABLE`
* `SELECT`

Since these operations are supported, the following will also work:

```sql
COPY FROM DATABASE duckdb_db TO iceberg_datalake;
-- Or
COPY FROM DATABASE iceberg_datalake TO duckdb_db;
```

This functionality enables deep copies between Iceberg and DuckDB storage.

## Creating Tables

Tables are created with the standard [`CREATE TABLE`]({% link docs/current/sql/statements/create_table.md %}) syntax. [Iceberg table properties](https://iceberg.apache.org/spec/#table-metadata-fields) can be supplied with the `WITH` clause:

```sql
CREATE TABLE test_create_table (a INTEGER)
WITH (
    'format-version' = '2', -- format version will be elevated to format-version when creating a table
    'location' = 's3://path/to/data', -- location will be elevated to location when creating a table
    'property1' = 'value1',
    'property2' = 'value2'
);
```

Table properties can also be inspected and modified after creation, see [Table Properties Functions]({% link docs/current/core_extensions/iceberg/iceberg_functions.md %}#table-properties-functions).

## `MERGE INTO`

The [`MERGE INTO`]({% link docs/current/sql/statements/merge_into.md %}) statement is the recommended way to express upserts against Iceberg tables, which do not have a primary key. You can apply a change set in a single statement, deciding per row whether to insert, update, or delete:

```sql
MERGE INTO iceberg_catalog.default.people AS target
    USING (
        FROM (VALUES
            (1, 'John', 105_000.0),
            (3, 'Sarah', 95_000.0)
        ) t(id, name, salary)
    ) AS upserts
    ON (upserts.id = target.id)
    WHEN MATCHED THEN UPDATE
    WHEN NOT MATCHED THEN INSERT;
```

You can also use `WHEN MATCHED THEN DELETE` to express a delete set in the same statement. As with `UPDATE` and `DELETE`, `MERGE INTO` uses merge-on-read semantics and writes positional deletes to the Iceberg table.

## `ALTER TABLE` and Schema Evolution

The [`ALTER TABLE`]({% link docs/current/sql/statements/alter_table.md %}) statement is supported against Iceberg tables, covering the most common schema-evolution operations:

```sql
-- Rename the table
ALTER TABLE iceberg_catalog.default.simple_table
    RENAME TO renamed_table;

-- Add a column
ALTER TABLE iceberg_catalog.default.renamed_table
    ADD COLUMN col3 DOUBLE;

-- Rename a column
ALTER TABLE iceberg_catalog.default.renamed_table
    RENAME COLUMN col2 TO name;

-- Drop a column
ALTER TABLE iceberg_catalog.default.renamed_table
    DROP COLUMN col3;

-- Set the format-version
ALTER TABLE iceberg_catalog.default.renamed_table
    SET ('format-version' = 3);
```

Each `ALTER TABLE` statement updates the `current-schema-id` of the Iceberg table, and the changes become visible to other Iceberg-aware engines the next time they query the `LoadTableInformation` endpoint. Iceberg schema evolution is metadata-only, so no data files are rewritten.

## Partition Transforms

In addition to identity partitioning, DuckDB-Iceberg supports creating, inserting into, and updating tables that use the `bucket` and `truncate` [partition transforms](https://iceberg.apache.org/spec/#partition-transforms).

The `bucket(N, col)` transform hashes the column's value into `N` buckets, which is useful for stable partitioning on a high-cardinality column. `truncate(W, col)` groups rows by the first `W` characters (or by the column's value rounded down to a multiple of `W` for numeric columns), which is useful for prefix-based partitioning.

```sql
CREATE TABLE iceberg_catalog.default.events (
    event_id BIGINT,
    user_id BIGINT,
    country VARCHAR,
    payload VARCHAR
)
PARTITIONED BY (bucket(16, user_id), truncate(2, country));
```

Updates and deletes against `bucket`- and `truncate`-partitioned tables are also supported, using positional deletes under merge-on-read semantics.

## Iceberg V3 Support

DuckDB-Iceberg supports the following [Iceberg v3 specification](https://iceberg.apache.org/spec/#version-3) features for both reads and writes:

* `VARIANT` and `TIMESTAMP_NS` data types
* Schema-level [default values](https://iceberg.apache.org/spec/#default-values) for columns
* Binary deletion vectors
* Row lineage tracking

The biggest change in practice is binary deletion vectors. In v2 tables, DuckDB-Iceberg writes positional deletes as Parquet files; in v3 tables, the same information is encoded as a much more compact binary deletion vector ([Puffin file](https://iceberg.apache.org/puffin-spec/)). DuckDB picks the right format automatically based on the table's `format-version`. You can create a v3 table by setting the `format-version` table property at creation time:

```sql
CREATE TABLE iceberg_catalog.default.v3_table
WITH ('format-version' = 3) AS
    FROM (VALUES
        (1, {'kind': 'click', 'x': 10}::VARIANT, TIMESTAMP_NS '2026-05-20 12:00:00.123456789'),
        (2, {'kind': 'view'}::VARIANT, TIMESTAMP_NS '2026-05-20 12:00:00.987654321')
    ) t(id, payload, event_time);
```

> Warning The `GEOGRAPHY` and `UNKNOWN` types are not yet supported in DuckDB-Iceberg; they are planned for DuckDB v2.0.0.

## Limitations for `UPDATE` and `DELETE`

The `UPDATE` and `DELETE` operations have the following limitations:

* They only work on tables that are **not sorted**. Attempting these operations on sorted tables.
* DuckDB-Iceberg only writes **positional deletes** (encoded as binary deletion vectors for v3 tables). Copy-on-write functionality is not yet supported.
* DuckDB-Iceberg only supports **merge-on-read semantics**. If a table has `write.update.mode` or `write.delete.mode` properties set to something other than `merge-on-read`, the operation fails.

## Unsupported Operations

The following are not yet supported by the DuckDB `iceberg` extension:

* The `GEOGRAPHY` and `UNKNOWN` data types (planned for DuckDB v2.0.0)
* Copy-on-write semantics for `UPDATE`, `DELETE`, and `MERGE INTO`
