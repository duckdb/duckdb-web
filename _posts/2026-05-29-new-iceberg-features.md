---
layout: post
title:  "New DuckDB-Iceberg features in v1.5.3"
author: "Tom Ebergen, Thijs Bruineman"
thumb: "/images/blog/thumbs/iceberg-writes.svg"
image: "/images/blog/thumbs/iceberg-writes.png"
excerpt: "DuckDB-Iceberg now has a number of new features supporting Iceberg Tables and Iceberg Rest Catalogs."
tags: ["deep dive"]
---

Despite the work needed to develop the features needed for DuckLake v1.0 and Quack, the DuckLabs team is still hard at work on the [DuckDB-Iceberg extension]({% link docs/current/core_extensions/iceberg/overview.md %}).
In this blog post, we will demo some of the features that are available in [DuckDB v1.5.3]({% post_url 2026-05-20-announcing-duckdb-153 %}). Many of these features were ear marked for a future release in our last [Iceberg blog post]({% post_url 2025-11-28-iceberg-writes-in-duckdb %}) 


## Getting Started

To experiment with the new DuckDB-Iceberg features, you will need to connect to your favorite Iceberg REST Catalog. There are many ways to connect to an Iceberg REST Catalog: please have a look at the [Connecting to REST Catalogs]({% link docs/current/core_extensions/iceberg/iceberg_rest_catalogs.md %}) for connecting to catalogs like [Apache Polaris](https://polaris.apache.org/) or [Lakekeeper](https://lakekeeper.io/) and the [Connecting to S3 Tables]({% link docs/current/core_extensions/iceberg/amazon_s3_tables.md %}) page if you would like to connect to [Amazon S3 Tables](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables.html).

```sql
ATTACH '⟨warehouse_name⟩' AS my_datalake (
    TYPE iceberg,
    ⟨other options⟩
);
```


## `MERGE INTO` Support

DuckDB's [`MERGE INTO`]({% link docs/current/sql/statements/merge_into.md %}) statement is the recommended way to express upserts when the target table does not have a primary key. With v1.5.3, `MERGE INTO` is now fully supported against Iceberg tables. You can apply a change set to an Iceberg table in a single statement, deciding per row whether to insert, update or delete.

```sql
CREATE TABLE my_datalake.default.people (
    id INTEGER,
    name VARCHAR,
    salary FLOAT
);
INSERT INTO my_datalake.default.people
    VALUES (1, 'John', 92_000.0), (2, 'Anna', 100_000.0);

MERGE INTO my_datalake.default.people AS target
    USING (
        SELECT
            unnest([1, 3]) AS id,
            unnest(['John', 'Sarah']) AS name,
            unnest([105_000.0, 95_000.0]) AS salary
    ) AS upserts
    ON (upserts.id = target.id)
    WHEN MATCHED THEN UPDATE
    WHEN NOT MATCHED THEN INSERT;

SELECT *
FROM my_datalake.default.people
ORDER BY id;
```

```text
┌───────┬─────────┬──────────┐
│  id   │  name   │  salary  │
│ int32 │ varchar │  float   │
├───────┼─────────┼──────────┤
│     1 │ John    │ 105000.0 │
│     2 │ Anna    │ 100000.0 │
│     3 │ Sarah   │  95000.0 │
└───────┴─────────┴──────────┘
```

You can also combine matched and not-matched branches with `WHEN MATCHED THEN DELETE` to express a delete set in the same statement. As with `UPDATE` and `DELETE`, `MERGE INTO` uses merge-on-read semantics and writes positional deletes to the Iceberg table.

## `TRUNCATE` and `BUCKET` Support

The Iceberg specification defines several [partition transforms](https://iceberg.apache.org/spec/#partition-transforms) that determine how data files are laid out on disk. In v1.5.3, DuckDB-Iceberg supports creating, inserting into, and updating tables that use the `bucket` and `truncate` partition transforms.

`bucket(N, col)` hashes the column's value into `N` buckets, which is useful when you want stable partitioning on a high-cardinality column. `truncate(W, col)` groups rows by the first `W` characters (or by the column's value rounded down to a multiple of `W` for numeric columns), which is useful for prefix-based partitioning.

```sql
CREATE TABLE my_datalake.default.events (
    event_id BIGINT,
    user_id BIGINT,
    country VARCHAR,
    payload VARCHAR
)
PARTITIONED BY (bucket(16, user_id), truncate(2, country));

INSERT INTO my_datalake.default.events
    VALUES
        (1, 1001, 'United States', 'click'),
        (2, 1002, 'United Kingdom', 'view'),
        (3, 1003, 'Germany', 'click'),
        (4, 1004, 'Netherlands', 'view');
```

You can inspect the resulting data files to verify the partitioning:

```sql
SELECT file_path, record_count
FROM iceberg_metadata(my_datalake.default.events)
WHERE content = 'EXISTING';
```

Updates and deletes against bucket- and truncate-partitioned tables are also supported, using positional deletes under merge-on-read semantics.

## Iceberg Schema Properties

Iceberg catalogs allow arbitrary key-value [properties](https://iceberg.apache.org/spec/#namespaces) to be attached at the schema (namespace) level. These properties are typically used to record ownership, descriptions, default storage locations, or any other metadata that applies to every table in a schema.

* `iceberg_schema_properties`
* `set_iceberg_schema_properties`
* `remove_iceberg_schema_properties`

You can use them as follows:

```sql
-- to set schema properties
CALL set_iceberg_schema_properties(my_datalake.default, {
    'owner': 'analytics-team',
    'description': 'Default analytics schema'
});
-- to read schema properties
SELECT * FROM iceberg_schema_properties(my_datalake.default);
```

```text
┌─────────────┬──────────────────────────┐
│     key     │          value           │
│   varchar   │         varchar          │
├─────────────┼──────────────────────────┤
│ owner       │ analytics-team           │
│ description │ Default analytics schema │
└─────────────┴──────────────────────────┘
```

```sql
-- to remove schema properties
CALL remove_iceberg_schema_properties(
    my_datalake.default,
    ['description']
);
```

Schema properties are written through the Iceberg REST Catalog, so any other Iceberg-aware engine attached to the same catalog will see the updates immediately. The returned value is the number of remaining schema properties.

## `ALTER TABLE` Support

In v1.4.2, schema evolution of Iceberg tables was a documented limitation. In v1.5.3, the `ALTER TABLE` statement is now supported against Iceberg tables, covering the most common schema-evolution operations.

```sql
-- Create the table
Create table my_datalake.default.simple_table from values 
    (1, 'Andy'), 
    (2, 'Bob'),
    (3, 'Claire'),
    (4, 'Mr. Duck') t(col1, col2);

-- Rename the table
ALTER TABLE my_datalake.default.simple_table
    RENAME TO renamed_table;

-- Add a column
ALTER TABLE my_datalake.default.renamed_table
    ADD COLUMN col3 DOUBLE;

-- Rename a column
ALTER TABLE my_datalake.default.renamed_table
    RENAME COLUMN col2 TO name;

-- Drop a column
ALTER TABLE my_datalake.default.renamed_table
    DROP COLUMN col3;

-- Set the format-version
ALTER TABLE my_datalake.default.renamed_table
    SET ('format-versionn'=3);
```

Each `ALTER TABLE` statement will updatet the `current-schema-id` of the Iceberg table. The changes are visible to other Iceberg-aware engines the next time they query the LoadTableInformation endpoint. Iceberg schema evolution is metadata-only, so no data files are rewritten.

```sql
SELECT *
FROM my_datalake.default.renamed_table
ORDER BY col1;
```

```text
┌───────┬──────────┐
│ col1  │   name   │
│ int32 │ varchar  │
├───────┼──────────┤
│     1 │ Andy     │
│     2 │ Bob      │
│     3 │ Claire   │
│     4 │ Mr. Duck │
└───────┴──────────┘
```

## V3 Support

The [Iceberg v3 specification](https://iceberg.apache.org/spec/#version-3) introduces several new features that DuckDB-Iceberg now supports for both reads and writes:

* `VARIANT` and `TIMESTAMP_NS` data types
* Schema-level [default values](https://iceberg.apache.org/spec/#default-values) for columns
* Binary deletion vectors
* Row lineage tracking

The biggest change in practice is binary deletion vectors. In v2 tables, DuckDB-Iceberg writes positional deletes as Parquet files; in v3 tables, the same information is encoded as a much more compact binary deletion vector ([Puffin file](https://iceberg.apache.org/puffin-spec/)). DuckDB picks the right format automatically based on the table's `format-version`.

You can create a v3 table by setting the `format-version` table property at creation time:

```sql
CREATE TABLE my_datalake.default.v3_table 
WITH ('format-version'=3) 
AS FROM VALUES
 (1, {'kind': 'click', 'x': 10}::VARIANT, TIMESTAMP_NS '2026-05-20 12:00:00.123456789'),
 (2, {'kind': 'view'}::VARIANT, TIMESTAMP_NS '2026-05-20 12:00:00.987654321') 
 t(id, payload, event_time);

-- Deletes against a v3 table are written as binary deletion vectors
DELETE FROM my_datalake.default.v3_table
WHERE id = 1;

SELECT * FROM my_datalake.default.v3_table;
```

```text
┌───────┬──────────────────┬───────────────────────────────┐
│  id   │     payload      │          event_time           │
│ int32 │     variant      │         timestamp_ns          │
├───────┼──────────────────┼───────────────────────────────┤
│     2 │ {"kind": "view"} │ 2026-05-20 12:00:00.987654321 │
└───────┴──────────────────┴───────────────────────────────┘
```

Looking at the metadata for the table confirms that the delete was written as a deletion vector rather than as a positional-delete Parquet file:

```sql
SELECT manifest_content, content, file_format
FROM iceberg_metadata(my_datalake.default.v3_table);
```

```text
┌──────────────────┬──────────────────┬─────────────┐
│ manifest_content │     content      │ file_format │
│     varchar      │     varchar      │   varchar   │
├──────────────────┼──────────────────┼─────────────┤
│ DATA             │ EXISTING         │ parquet     │
│ DELETE           │ POSITION_DELETES │ puffin      │
└──────────────────┴──────────────────┴─────────────┘
```

> Note: the Geography type and Unknown type are not yet supported in DuckDB-Iceberg, we are planning to add those in DuckDB v2.0.0


## Conclusion and Future Work

With these features, DuckDB-Iceberg has closed many of the gaps called out in the [previous blog post]({% post_url 2025-11-28-iceberg-writes-in-duckdb %}): partitioned writes, schema evolution, `MERGE INTO`, and many Iceberg v3 features are now available. There is still more to come, and as always, if you would like to see a specific feature prioritized, please reach out to us in the [DuckDB-Iceberg GitHub repository](https://github.com/duckdb/duckdb-iceberg) or [get in touch](https://ducklabs.com/contact/) with our engineers.



