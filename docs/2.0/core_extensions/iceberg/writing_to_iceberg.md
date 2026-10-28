---
layout: docu
redirect_from:
- /docs/preview/core_extensions/iceberg/writing
- /docs/current/core_extensions/iceberg/writing
- /docs/current/core_extensions/iceberg/writing_to_iceberg
- /docs/lts/core_extensions/iceberg/writing_to_iceberg
- /docs/preview/core_extensions/iceberg/writing_to_iceberg
title: Writing to Iceberg
---

The DuckDB `iceberg` extension supports writing to Iceberg tables when an [Iceberg catalog]({% link docs/2.0/core_extensions/iceberg/catalogs.md %}) is attached.
Writing to a table read directly from storage with [`iceberg_scan`]({% link docs/2.0/core_extensions/iceberg/iceberg_functions.md %}#iceberg_scan) is not supported: the catalog is required to commit the new table metadata.

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

## Creating Schemas and Tables

Iceberg namespaces are exposed as schemas, which can be created and dropped with [`CREATE SCHEMA`]({% link docs/2.0/sql/statements/create_schema.md %}) and [`DROP SCHEMA`]({% link docs/2.0/sql/statements/drop.md %}):

```sql
CREATE SCHEMA iceberg_catalog.sales;
USE iceberg_catalog.sales;
```

Tables are created with the standard [`CREATE TABLE`]({% link docs/2.0/sql/statements/create_table.md %}) syntax. [Iceberg table properties](https://iceberg.apache.org/spec/#table-metadata-fields) can be supplied with the `WITH` clause:

```sql
CREATE TABLE test_create_table (a INTEGER)
WITH (
    'format-version' = '2', -- format version will be elevated to format-version when creating a table
    'location' = 's3://path/to/data', -- location will be elevated to location when creating a table
    'property1' = 'value1',
    'property2' = 'value2'
);
```

Tables can also be created from the result of a query:

```sql
CREATE TABLE iceberg_catalog.sales.events_copy AS
    FROM iceberg_catalog.sales.events;
```

Table properties can also be inspected and modified after creation, see [Table Properties Functions]({% link docs/2.0/core_extensions/iceberg/iceberg_functions.md %}#table-properties-functions).

## `UPDATE` and `DELETE`

The [`UPDATE`]({% link docs/2.0/sql/statements/update.md %}) and [`DELETE`]({% link docs/2.0/sql/statements/delete.md %}) statements are supported on both partitioned and unpartitioned tables:

```sql
UPDATE iceberg_catalog.sales.events
SET event_name = 'view'
WHERE id = 1;

DELETE FROM iceberg_catalog.sales.events
WHERE event_time < TIMESTAMP '2026-01-01';
```

They use merge-on-read semantics and write positional deletes, see [Limitations for `UPDATE` and `DELETE`](#limitations-for-update-and-delete).

## `MERGE INTO`

The [`MERGE INTO`]({% link docs/2.0/sql/statements/merge_into.md %}) statement is the recommended way to express upserts against Iceberg tables, which do not have a primary key. You can apply a change set in a single statement, deciding per row whether to insert, update, or delete:

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

The [`ALTER TABLE`]({% link docs/2.0/sql/statements/alter_table.md %}) statement is supported against Iceberg tables, covering the most common schema-evolution operations:

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

-- Change the type of a column
ALTER TABLE iceberg_catalog.default.renamed_table
    ALTER COLUMN col1 TYPE BIGINT;

-- Set and drop the default value of a column
ALTER TABLE iceberg_catalog.default.renamed_table
    ALTER COLUMN col1 SET DEFAULT 0;
ALTER TABLE iceberg_catalog.default.renamed_table
    ALTER COLUMN col1 DROP DEFAULT;

-- Set the format-version
ALTER TABLE iceberg_catalog.default.renamed_table
    SET ('format-version' = 3);
```

Each `ALTER TABLE` statement updates the `current-schema-id` of the Iceberg table, and the changes become visible to other Iceberg-aware engines the next time they query the `LoadTableInformation` endpoint. Iceberg schema evolution is metadata-only, so no data files are rewritten.

## Partitioning

Tables can be partitioned with the `PARTITIONED BY` clause using the [Iceberg partition transforms](https://iceberg.apache.org/spec/#partition-transforms):

| Transform | Description |
| --- | --- |
| `⟨column⟩`{:.language-sql .highlight} | Identity: partition by the column value directly. |
| `year(⟨column⟩)`{:.language-sql .highlight}, `month(⟨column⟩)`{:.language-sql .highlight}, `day(⟨column⟩)`{:.language-sql .highlight}, `hour(⟨column⟩)`{:.language-sql .highlight} | Partition by a date or timestamp component. |
| `bucket(⟨n⟩, ⟨column⟩)`{:.language-sql .highlight} | Hash the column's value into `n` buckets. This is useful for stable partitioning on a high-cardinality column. |
| `truncate(⟨w⟩, ⟨column⟩)`{:.language-sql .highlight} | Group rows by the first `w` characters (or by the column's value rounded down to a multiple of `w` for numeric columns). This is useful for prefix-based partitioning. |

```sql
CREATE TABLE iceberg_catalog.default.events (
    event_id BIGINT,
    user_id BIGINT,
    country VARCHAR,
    event_time TIMESTAMP
)
PARTITIONED BY (day(event_time), bucket(16, user_id), truncate(2, country));
```

The partition spec of an existing table can be changed with `ALTER TABLE ... SET PARTITIONED BY`:

```sql
ALTER TABLE iceberg_catalog.default.events
    SET PARTITIONED BY (month(event_time));
```

The `bucket` and `truncate` transforms are also available as the [`iceberg_bucket` and `iceberg_truncate` functions]({% link docs/2.0/core_extensions/iceberg/iceberg_functions.md %}#partition-transform-functions).

> The `write.target-file-size-bytes` and `write.parquet.row-group-size-bytes` table properties are honored for both partitioned and unpartitioned tables. Files are rotated at row-group boundaries, so if the row-group size exceeds the target file size, DuckDB caps the row-group size to the target file size.

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

> Warning The `GEOGRAPHY` type is not yet supported in DuckDB-Iceberg.

## Limitations for `UPDATE` and `DELETE`

The `UPDATE` and `DELETE` operations have the following limitations:

* DuckDB-Iceberg only writes **positional deletes** (encoded as binary deletion vectors for v3 tables). Copy-on-write functionality is not yet supported.
* DuckDB-Iceberg only supports **merge-on-read semantics**. If a table has `write.update.mode` or `write.delete.mode` properties set to something other than `merge-on-read`, the operation fails.

## Unsupported Operations

The following are not yet supported by the DuckDB `iceberg` extension:

* The `GEOGRAPHY` data type
* Copy-on-write semantics for `UPDATE`, `DELETE`, and `MERGE INTO`

## See Also

For continuously replicating data from PostgreSQL, MySQL, or MongoDB into Iceberg via change data capture (CDC), see [Olake Go](https://olake.io/olake-go/) — an open-source tool that writes to Iceberg REST Catalogs, including the catalogs listed on the [Catalogs]({% link docs/2.0/core_extensions/iceberg/catalogs.md %}) page.
