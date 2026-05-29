---
layout: post
title: "New DuckDB-Iceberg Features in v1.5.3"
author: "Tom Ebergen, Thijs Bruineman"
thumb: "/images/blog/thumbs/iceberg-in-v153.svg"
image: "/images/blog/thumbs/iceberg-in-v153.jpg"
excerpt: "DuckDB-Iceberg now has a number of new features supporting Iceberg Tables and Iceberg REST Catalogs: `MERGE INTO`, `ALTER TABLE`, partition transforms, V3 support, and others!"
tags: ["extensions"]
---

Despite the work required to develop the features needed for DuckLake v1.0 and Quack, the DuckLabs team is still hard at work on the [DuckDB-Iceberg extension]({% link docs/current/core_extensions/iceberg/overview.md %}).
In this blog post, we will demonstrate some of the features that are available in [DuckDB v1.5.3]({% post_url 2026-05-20-announcing-duckdb-153 %}). Many of these features were earmarked for a future release in our last Iceberg-themed blog post [“Writes in DuckDB-Iceberg”]({% post_url 2025-11-28-iceberg-writes-in-duckdb %}) – you can think of this post as “Part 2” to that blog post.

## Getting Started

To experiment with the new DuckDB-Iceberg features, you will need to connect to your favorite Iceberg REST Catalog. There are many ways to do so: please have a look at the [Connecting to REST Catalogs page]({% link docs/current/core_extensions/iceberg/iceberg_rest_catalogs.md %}), which has instructions for catalogs such as [Apache Polaris](https://polaris.apache.org/) and [Lakekeeper](https://lakekeeper.io/). If you would like to connect to [Amazon S3 Tables](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables.html), please consult the [Connecting to S3 Tables page]({% link docs/current/core_extensions/iceberg/amazon_s3_tables.md %}). In any case, your `ATTACH` command will look something like this:

```sql
ATTACH '⟨warehouse_name⟩' AS my_datalake (
    TYPE iceberg,
    ⟨other options⟩
);
```

## `MERGE INTO` Support

DuckDB's [`MERGE INTO`]({% link docs/current/sql/statements/merge_into.md %}) statement is the recommended way to express upserts when the target table does not have a primary key – which is the case for all [lakehouse formats]({% link docs/current/lakehouse_formats.md %}).
With v1.5.3, `MERGE INTO` is now fully supported against Iceberg tables. You can apply a change set to an Iceberg table in a single statement, deciding per row whether to insert, update or delete.

Let's take this table for example:

```sql
CREATE TABLE my_datalake.default.people (
    id INTEGER,
    name VARCHAR,
    salary FLOAT
);
INSERT INTO my_datalake.default.people
    VALUES (1, 'John', 92_000.0), (2, 'Anna', 100_000.0);
```

```text
┌───────┬─────────┬──────────┐
│  id   │  name   │  salary  │
│ int32 │ varchar │  float   │
├───────┼─────────┼──────────┤
│     1 │ John    │  92000.0 │
│     2 │ Anna    │ 100000.0 │
└───────┴─────────┴──────────┘
```

Let's run an update on this table with two records, one increasing person 1's salary and another adding a new person with id 3.

```sql
MERGE INTO my_datalake.default.people AS target
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

When querying the result, we get the following:

```sql
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

You can also combine matched and unmatched branches with `WHEN MATCHED THEN DELETE` to express a delete set in the same statement. As with `UPDATE` and `DELETE`, `MERGE INTO` uses merge-on-read semantics and writes positional deletes to the Iceberg table.

## `ALTER TABLE` Support

In DuckDB v1.4's Iceberg extension, the lack of schema evolution of Iceberg tables was a [documented limitation]({% link docs/lts/core_extensions/iceberg/iceberg_rest_catalogs.md %}#unsupported-operations).
In v1.5.3, the `ALTER TABLE` statement is now supported against Iceberg tables, covering the most common schema-evolution operations.

```sql
-- Create the table
CREATE TABLE my_datalake.default.simple_table AS
    FROM (VALUES
        (1, 'Andy'),
        (2, 'Bob'),
        (3, 'Claire'),
        (4, 'Mr. Duck')) t(col1, col2);

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
    SET ('format-version' = 3);
```

If we query the table after the schema changes, we get the following:

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

In the background, each `ALTER TABLE` statement updates the `current-schema-id` of the Iceberg table. The changes are visible to other Iceberg-aware engines the next time they query the `LoadTableInformation` endpoint. Iceberg schema evolution is metadata-only, so no data files are rewritten.

## `truncate` and `bucket` Support

The Iceberg specification defines several [partition transforms](https://iceberg.apache.org/spec/#partition-transforms) that determine how data files are laid out on disk. In v1.5.3, DuckDB-Iceberg supports creating, inserting into, and updating tables that use the `bucket` and `truncate` partition transforms.

The `bucket(N, col)` transform hashes the column's value into `N` buckets, which is useful when you want stable partitioning on a high-cardinality column. `truncate(W, col)` groups rows by the first `W` characters (or by the column's value rounded down to a multiple of `W` for numeric columns), which is useful for prefix-based partitioning.

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
WITH ('format-version' = 3) AS
    FROM (VALUES
        (1, {'kind': 'click', 'x': 10}::VARIANT, TIMESTAMP_NS '2026-05-20 12:00:00.123456789'),
        (2, {'kind': 'view'}::VARIANT, TIMESTAMP_NS '2026-05-20 12:00:00.987654321')
    ) t(id, payload, event_time);

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

> Note: the Geography type and Unknown type are not yet supported in DuckDB-Iceberg; we are planning to add those in DuckDB v2.0.0.


## Conclusion and Future Work

With these features, DuckDB-Iceberg has closed many of the gaps called out in the [previous blog post]({% post_url 2025-11-28-iceberg-writes-in-duckdb %}): partitioned writes, schema evolution, `MERGE INTO`, and many Iceberg v3 features are now available. There is still more to come, and as always, if you would like to see a specific feature prioritized, please reach out to us in the [DuckDB-Iceberg GitHub repository](https://github.com/duckdb/duckdb-iceberg) or [get in touch](https://ducklabs.com/contact/) with our engineers.
